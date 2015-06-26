__author__ = 'tkessler'

"""
Create SonyTV class with methods:
    channel -- convert number string to iterator and loop to pass values
    cmd -- accept and execute cmd keyword. If none, output possibilities...
    input -- change to designated input, or list possibilities...
    nav - accept continuous input for arrows...
        enter to select, esc to go back, H for home, q to exit
"""

import requests, time, socket, struct
from tkinter import *
from tkinter.simpledialog import askfloat

class SonyTV():
    def __init__(self, ip="192.168.1.7", mac="F0:BF:97:78:CA:0D"):
        self.ip = ip
        self.mac = mac
        self.cmds = {'Analog': 'AAAAAgAAAHcAAAANAw==',
            'Analog2': 'AAAAAQAAAAEAAAA4Aw==',
            'Analog?': 'AAAAAgAAAJcAAAAuAw==',
            '*AD': 'AAAAAgAAABoAAAA7Aw==',
            'PowerOff': 'AAAAAQAAAAEAAAAvAw==',
            'Audio': 'AAAAAQAAAAEAAAAXAw==',
            'Blue': 'AAAAAgAAAJcAAAAkAw==',
            'ChannelDown': 'AAAAAQAAAAEAAAARAw==',
            'ChannelUp': 'AAAAAQAAAAEAAAAQAw==',
            'Confirm': 'AAAAAQAAAAEAAABlAw==',
            'Display': 'AAAAAQAAAAEAAAA6Aw==',
            'Down': 'AAAAAQAAAAEAAAB1Aw==',
            'EPG': 'AAAAAgAAAKQAAABbAw==',
            'Exit': 'AAAAAQAAAAEAAABjAw==',
            'Forward': 'AAAAAgAAAJcAAAAcAw==',
            'Green': 'AAAAAgAAAJcAAAAmAw==',
            'Home': 'AAAAAQAAAAEAAABgAw==',
            'Input': 'AAAAAQAAAAEAAAAlAw==',
            'Left': 'AAAAAQAAAAEAAAA0Aw==',
            'Mute': 'AAAAAQAAAAEAAAAUAw==',
            'Next': 'AAAAAgAAAJcAAAA9Aw==',
            'Num0': 'AAAAAQAAAAEAAAAJAw==',
            'Num1': 'AAAAAQAAAAEAAAAAAw==',
            'Num2': 'AAAAAQAAAAEAAAABAw==',
            'Num3': 'AAAAAQAAAAEAAAACAw==',
            'Num4': 'AAAAAQAAAAEAAAADAw==',
            'Num5': 'AAAAAQAAAAEAAAAEAw==',
            'Num6': 'AAAAAQAAAAEAAAAFAw==',
            'Num7': 'AAAAAQAAAAEAAAAGAw==',
            'Num8': 'AAAAAQAAAAEAAAAHAw==',
            'Num9': 'AAAAAQAAAAEAAAAIAw==',
            'Options': 'AAAAAgAAAJcAAAA2Aw==',
            'PAP': 'AAAAAgAAAKQAAAB3Aw==',
            'Pause': 'AAAAAgAAAJcAAAAZAw==',
            'Play': 'AAAAAgAAAJcAAAAaAw==',
            'Prev': 'AAAAAgAAAJcAAAA8Aw==',
            'Red': 'AAAAAgAAAJcAAAAlAw==',
            'Return': 'AAAAAgAAAJcAAAAjAw==',
            'Rewind': 'AAAAAgAAAJcAAAAbAw==',
            'Right': 'AAAAAQAAAAEAAAAzAw==',
            'Stop': 'AAAAAgAAAJcAAAAYAw==',
            'SubTitle': 'AAAAAgAAAJcAAAAoAw==',
            'SyncMenu': 'AAAAAgAAABoAAABYAw==',
            'Up': 'AAAAAQAAAAEAAAB0Aw==',
            'VolumeDown': 'AAAAAQAAAAEAAAATAw==',
            'VolumeUp': 'AAAAAQAAAAEAAAASAw==',
            'Wide': 'AAAAAgAAAKQAAAA9Aw==',
            'Yellow': 'AAAAAgAAAJcAAAAnAw==',
            'HDMI1': 'AAAAAgAAABoAAABaAw==',
            'HDMI2': 'AAAAAgAAABoAAABbAw==',
            'HDMI3': 'AAAAAgAAABoAAABcAw==',
            'HDMI4': 'AAAAAgAAABoAAABdAw==', #break...
            'Replay': 'AAAAAgAAAJcAAAB5Aw==',
            'Advance': 'AAAAAgAAAJcAAAB4Aw==',
            'TopMenu': 'AAAAAgAAABoAAABgAw==',
            'PopUpMenu': 'AAAAAgAAABoAAABhAw==',
            'Eject': 'AAAAAgAAAJcAAABIAw==',
            'Rec': 'AAAAAgAAAJcAAAAgAw==',
            'ClosedCaption': 'AAAAAgAAAKQAAAAQAw==',
            'Teletext': 'AAAAAQAAAAEAAAA/Aw==',
            'GGuide': 'AAAAAQAAAAEAAAAOAw==',
            'DOT': 'AAAAAgAAAJcAAAAdAw==',
            'Digital': 'AAAAAgAAAJcAAAAyAw==',
            'BS': 'AAAAAgAAAJcAAAAsAw==',
            'CS': 'AAAAAgAAAJcAAAArAw==',
            'BSCS': 'AAAAAgAAAJcAAAAQAw==',
            'Ddata': 'AAAAAgAAAJcAAAAVAw==',
            'InternetWidgets': 'AAAAAgAAABoAAAB6Aw==',
            'InternetVideo': 'AAAAAgAAABoAAAB5Aw==',
            'SceneSelect': 'AAAAAgAAABoAAAB4Aw==',
            'Mode3D': 'AAAAAgAAAHcAAABNAw==',
            'iManual': 'AAAAAgAAABoAAAB7Aw==',
            'Jump': 'AAAAAQAAAAEAAAA7Aw==',
            'MyEPG': 'AAAAAgAAAHcAAABrAw==',
            'ProgramDescription': 'AAAAAgAAAJcAAAAWAw==',
            'WriteChapter': 'AAAAAgAAAHcAAABsAw==',
            'TrackID': 'AAAAAgAAABoAAAB+Aw==',
            'TenKey': 'AAAAAgAAAJcAAAAMAw==',
            'AppliCast': 'AAAAAgAAABoAAABvAw==',
            'acTVila': 'AAAAAgAAABoAAAByAw==',
            'DeleteVideo': 'AAAAAgAAAHcAAAAfAw==',
            'EasyStartUp': 'AAAAAgAAAHcAAABqAw==',
            'OneTouchTimeRec': 'AAAAAgAAABoAAABkAw==',
            'OneTouchView': 'AAAAAgAAABoAAABlAw==',
            'OneTouchRec': 'AAAAAgAAABoAAABiAw==',
            'OneTouchRecStop': 'AAAAAgAAABoAAABjAw==',
            'PicOff': 'AAAAAQAAAAEAAAA+Aw'}

    def controller(self):
        win = Tk()
        win.title('SonyTV')
        chanlist = ['66','125.1','130.1', '125.3','125.4','87.2','87.5','102.5','103.1','103.2','103.3','105.1']
        Button(win, text="Input", command=(lambda: self.command("Input"))).pack()
        Button(win, text="Volume Up", command=(lambda: self.command("VolumeUp"))).pack()
        Button(win, text="Volume Down", command=(lambda: self.command("VolumeDown"))).pack()
        Button(win, text="Mute", command=(lambda: self.command("Mute"))).pack()
        Button(win, text="Channel Up", command=(lambda: self.command("ChannelUp"))).pack()
        Button(win, text="Channel Down", command=(lambda: self.command("ChannelDown"))).pack()
        #Button(win, text="Enter Channel", command=(lambda: self.channel(str(askfloat("Channel", "Enter:"))))).pack()
        list = Listbox(win,listvariable=chanlist)
        list.pack()
        for item in chanlist:
            list.insert(END, item)
        Button(win, text="Go To...", command=(lambda: self.channel(chanlist[list.curselection()[0]]))).pack()
        chan = Entry(win, text="Entry")
        chan.pack()
        Button(win, text="Go", command=(lambda: self.channel(chan.get()))).pack()
        Button(win, text="Jump", command=(lambda: self.command("Jump"))).pack()
        Button(win, text="Quit", command=win.quit).pack()
        win.mainloop()

    # def set_button(event=None, buttons=struct_o_buttons):
    #     listbox = event.widget # where we clicked the mouse
    #     # what has been selected (what index was closest to the mouse)
    #     index = listbox.nearest(event.y)
    #     # I'll leave this to you to figure out how you might want to keep
    #     # track of the relationship between the listbox item and the buttons
    #     button = get_button_from(listbox, index, buttons)
    #     if button.cget('state') == NORMAL:
    #         button.config(state=DISABLED)
    #     else:
    #         button.config(state=NORMAL)

    def wakeup(self, ip, mac):
        add_oct = mac.split(':')
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        # hwa = '\x00\x21\x6A\xC7\x1A\x42'
        hwa = struct.pack('BBBBBB', int(add_oct[0],16),
            int(add_oct[1],16),
            int(add_oct[2],16),
            int(add_oct[3],16),
            int(add_oct[4],16),
            int(add_oct[5],16))
        s.sendto(b'\xff'*6 + hwa*16, (ip, 80))
        s.close()

    #def data(cmd):
    #    return '<?xml version="1.0" encoding="utf-8"?><s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/"><s:Body><u:X_SendIRCC xmlns:u="urn:schemas-sony-com:service:IRCC:1"><IRCCCode>'+cmd+'</IRCCCode></u:X_SendIRCC></s:Body></s:Envelope>'

    def command(self, cmdname):
        url = 'http://'+self.ip+'/IRCC'
        cmd = self.cmds[cmdname]
        data ='<?xml version="1.0" encoding="utf-8"?><s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/"><s:Body><u:X_SendIRCC xmlns:u="urn:schemas-sony-com:service:IRCC:1"><IRCCCode>'+cmd+'</IRCCCode></u:X_SendIRCC></s:Body></s:Envelope>'
        requests.post(url, data=data)

    def channel(self, numstr):
        numpad = ['Num0','Num1','Num2','Num3','Num4','Num5','Num6','Num7','Num8','Num9']
        for n in numstr:
            if n=='.':
                self.command('DOT')
            else:
                self.command(numpad[int(n)])
            time.sleep(0.1)
        self.command('Confirm')