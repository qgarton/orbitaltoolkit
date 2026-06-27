### Used for testing calling other scripts in python from a python script
from scipy.optimize import fsolve


def test(somenum):
  def f(x): 
    return x**2 - 4
  xopt = fsolve(f, 1)
  print("\nWow Everything worked and stuff!!!\nEven x =", xopt[0], "\nType =", type(xopt[0]))
  return somenum+2


if __name__ == '__main__':
  print("This is not the main sript: Please call LambertsEq.py")





