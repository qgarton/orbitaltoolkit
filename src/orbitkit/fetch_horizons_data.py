"""
### fetch_horizons_data.py
# Created 7/16/2026
# Author: Claude AI (Coauthor: Quaid Garton)
# Last updated: 7/16/2026

Batch-downloads fresh JPL Horizons vector ephemeris data for the Sun and all
planets (+ Moon, Pluto) over a given date range, saving each body to its own
text file in the same format your parse_horizons_vectors() already expects.

Usage:
    python3 fetch_horizons_data.py
    python3 fetch_horizons_data.py --start 2026-01-01 --stop 2027-01-01 --step 1d
    python3 fetch_horizons_data.py --outdir docs/examples/solar_system_states
"""

import argparse
import time
from pathlib import Path

import requests

BASE_URL = "https://ssd.jpl.nasa.gov/api/horizons.api"

# JPL Horizons body ID codes.
# 10 = Sun, x99 = planet centers, 301 = Moon, 399 = Earth, 999 = Pluto (barycenter of system: 9)
BODIES = {
    "Sun": "10",
    "Mercury": "199",
    "Venus": "299",
    "Earth": "399",
    "Moon": "301",
    "Mars": "499",
    "Jupiter": "599",
    "Saturn": "699",
    "Uranus": "799",
    "Neptune": "899",
    "Pluto": "999",
}

CENTER = "500@0"  # Solar System Barycenter -- matches your existing files' frame


def fetch_vectors(command, start, stop, step, center=CENTER, timeout=30, max_retries=3):
    """Query the Horizons API for one body and return the raw ephemeris text."""
    params = {
        "format": "text",
        "COMMAND": f"'{command}'",
        "OBJ_DATA": "NO",
        "MAKE_EPHEM": "YES",
        "EPHEM_TYPE": "VECTORS",
        "CENTER": f"'{center}'",
        "START_TIME": f"'{start}'",
        "STOP_TIME": f"'{stop}'",
        "STEP_SIZE": f"'{step}'",
    }

    headers = {"User-Agent": "orbitkit-fetch-script/1.0 (contact: none)"}

    last_err = None
    for attempt in range(1, max_retries + 1):
        try:
            resp = requests.get(BASE_URL, params=params, headers=headers, timeout=timeout)
            resp.raise_for_status()

            text = resp.text
            if not text.strip():
                raise ValueError(
                    f"Empty response body (status {resp.status_code}). "
                    f"URL was: {resp.url}"
                )

            # format=text returns the raw Horizons ephemeris directly (not JSON-wrapped).
            # A real vectors result contains these markers; if they're missing, Horizons
            # likely returned an error/status message instead of ephemeris data.
            if "$$SOE" not in text or "$$EOE" not in text:
                raise ValueError(
                    f"Response doesn't look like valid ephemeris data. "
                    f"First 300 chars: {text[:300]!r}"
                )

            return text
        except (requests.RequestException, ValueError) as err:
            last_err = err
            print(f"    attempt {attempt}/{max_retries} failed: {err}")
            time.sleep(2 * attempt)  # simple backoff

    raise RuntimeError(f"Failed to fetch data for command={command!r} after {max_retries} attempts") from last_err


def fetch_body_physical_params(command, timeout=30):
    """
    Fetch Horizons' OBJ_DATA header for a body and try to parse its mass (kg)
    and mean radius (km) out of the GEOPHYSICAL PROPERTIES block.

    Returns (mass_kg, radius_km, raw_text). Either value may be None if it
    couldn't be parsed -- this is common for comets/asteroids, since Horizons
    rarely has a reliable mass for small bodies. raw_text is returned too, so
    you can eyeball the header yourself if the regex comes up empty.
    """
    params = {
        "format": "text",
        "COMMAND": f"'{command}'",
        "OBJ_DATA": "YES",
        "MAKE_EPHEM": "NO",  # header only -- skip generating any ephemeris rows
    }
    headers = {"User-Agent": "orbitkit-fetch-script/1.0 (contact: none)"}

    resp = requests.get(BASE_URL, params=params, headers=headers, timeout=timeout)
    resp.raise_for_status()
    text = resp.text

    # Mass is reported as e.g. "Mass x 10^24 (kg)= 5.97219+-0.0006" -- exponent
    # varies a lot by body size (10^21 for small moons, 10^27 for Jupiter, etc).
    mass_kg = None
    mass_match = re.search(r"[Mm]ass.*?x\s*10\^(\d+)\s*\(?kg\)?\s*=\s*([\d.]+)", text)
    if mass_match:
        exponent = int(mass_match.group(1))
        mantissa = float(mass_match.group(2))
        mass_kg = mantissa * 10 ** exponent

    # Radius: prefer "Vol. Mean Radius (km)", fall back to other common labels.
    radius_km = None
    radius_match = re.search(
        r"(?:Vol\.\s*Mean\s*Radius|Mean\s*[Rr]adius|Radius)\s*(?:\(km\)|,\s*km)?\s*=\s*([\d.]+)",
        text,
    )
    if radius_match:
        radius_km = float(radius_match.group(1))

    return mass_kg, radius_km, text


def print_physical_params(names=None):
    """Fetch and print mass/radius for the given body names (default: all of BODIES)."""
    names = names or list(BODIES.keys())
    for name in names:
        code = BODIES[name]
        print(f"{name} (id={code})...")
        try:
            mass_kg, radius_km, _ = fetch_body_physical_params(code)
        except requests.RequestException as err:
            print(f"  FAILED: {err}")
            continue

        mass_str = f"{mass_kg:.6e} kg" if mass_kg is not None else "not found"
        radius_str = f"{radius_km:.2f} km" if radius_km is not None else "not found"
        print(f"  mass   = {mass_str}")
        print(f"  radius = {radius_str}")



    outdir = Path(outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    print(f"Fetching Horizons vectors: {start} to {stop}, step={step}")
    print(f"Saving to: {outdir.resolve()}\n")

    failures = []
    for name, code in BODIES.items():
        print(f"Fetching {name} (id={code})...")
        try:
            text = fetch_vectors(code, start, stop, step)
        except RuntimeError as err:
            print(f"  FAILED: {err}")
            failures.append(name)
            continue

        out_path = outdir / f"{name}{suffix}"
        out_path.write_text(text, encoding="utf-8")
        print(f"  saved -> {out_path}")

        time.sleep(sleep_between)  # be polite to the public API

    print()
    if failures:
        print(f"Done with errors. Failed bodies: {failures}")
    else:
        print("Done. All bodies downloaded successfully.")


def parse_args():
    p = argparse.ArgumentParser(description="Download fresh JPL Horizons vector ephemeris data.")
    p.add_argument("--start", default="2026-01-01", help="Start date (YYYY-MM-DD). Default: 2026-01-01")
    p.add_argument("--stop", default="2027-01-01", help="Stop date (YYYY-MM-DD). Default: 2027-01-01")
    p.add_argument("--step", default="1d", help="Step size, e.g. '1d', '6h'. Default: 1d")
    p.add_argument(
        "--outdir",
        default="docs/examples/solar_system_states",
        help="Output directory for the ephemeris files. Default: docs/examples/solar_system_states",
    )
    p.add_argument(
        "--suffix",
        default="_ephem.txt",
        help="Filename suffix appended to each body name. Default: _ephem.txt",
    )
    return p.parse_args()


if __name__ == "__main__":
    print("fetch_horizons_data.py -- script version: 2026-07-16-v3\n")
    args = parse_args()
    batch_download(
        start=args.start,
        stop=args.stop,
        step=args.step,
        outdir=args.outdir,
        suffix=args.suffix,
    )
