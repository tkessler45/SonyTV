__author__ = 'tkessler'

from SonyTV import SonyTV

def launchTV():
    TV = SonyTV(ip="192.168.1.14") #mac=F0:BF:97:78:CA:0D
    TV.controller2(open('/Users/tkessler/favchannels.txt','r'))

if __name__ == "__main__":
    launchTV()