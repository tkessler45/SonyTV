__author__ = 'tkessler'

from SonyTV import SonyTV

def launchTV():
    TV = SonyTV()
    TV.controller2()

if __name__ == "__main__":
    launchTV()