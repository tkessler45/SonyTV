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
import threading, os

class chanbox(Frame):
    def __init__(self, parent=None, list="", command=None, args=None, **Options):
        Frame.__init__(self, master=parent, **Options)
        self.pack(fill=BOTH, expand=YES)
        self.items = list
        self.args = args
        self.cmd = command
        self.list = Listbox(self)
        self.scroll = Scrollbar(self)
        self.buildWidget()

    def buildWidget(self):
        scroll = self.scroll
        list = self.list
        scroll.config(command=list.yview)
        list.config(yscrollcommand=scroll.set)
        list.pack(side=LEFT, expand=YES, fill=BOTH)
        scroll.pack(side=RIGHT, fill=Y)
        self.populate(list,self.items)
        list.bind('<Double-1>', self.bindcmd)
        list.bind('<Return>', self.bindcmd)

    def populate(self, list, items):
        list.delete(0,END)
        for item in items:
            list.insert(END, item)

    def bindcmd(self,event):
        threading.Thread(target=self.cmd, args=(self.args,)).start()
        #self.cmd(self.args)
        #self.cmd(self,self.args)

def chanlisthandler(obj, *Options):
    #print(obj.cbox.list.get(obj.cbox.list.curselection())[:-1])
    obj.channel(obj.cbox.list.get(obj.cbox.list.curselection())[:-1])
    obj.cbox.list.selection_clear(0,END)

class SonyTV(Frame):
    def __init__(self, ip="", mac="", parent=None, **Options):
        Frame.__init__(self, master=parent, **Options)
        self.pack()
        self.ip = ip
        self.mac = mac
        self.response = 1
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
        self.chanvar = ""

    def checkconnection(self, ip, widget):
        while True:
            self.response = os.system("ping -c 1 -W 10 " + ip + " > /dev/null 2> /dev/null")
            if self.response==0:
                widget.config(text="connected", bg='green')
            else:
                widget.config(text="no connection", bg='red')
            time.sleep(1)

    def controller(self):
        win = Tk()
        win.config(bg='#999999')
        win.title('SonyTV')
        chanlist = ['66','125.1','130.1', '125.3','125.4','87.2','87.5','102.5','103.1','103.2','103.3','105.1']
        inpt = Button(win, text="Input", command=(lambda: self.command("Input")))
        inpt.config(highlightbackground='#999999', image="")
        inpt.pack()
        volu=Button(win, text="Volume Up", command=(lambda: self.command("VolumeUp")))
        volu.config(highlightbackground='#999999')
        volu.pack()
        vold=Button(win, text="Volume Down", command=(lambda: self.command("VolumeDown")))
        vold.config(highlightbackground='#999999')
        vold.pack()
        mutb=Button(win, text="Mute", command=(lambda: self.command("Mute")))
        mutb.config(highlightbackground='#999999')
        mutb.pack()
        chup=Button(win, text="Channel Up", command=(lambda: self.command("ChannelUp")))
        chup.config(highlightbackground='#999999')
        chup.pack()
        chdn=Button(win, text="Channel Down", command=(lambda: self.command("ChannelDown")))
        chdn.config(highlightbackground='#999999')
        chdn.pack()
        #Button(win, text="Enter Channel", command=(lambda: self.channel(str(askfloat("Channel", "Enter:"))))).pack()
        list = Listbox(win,listvariable=chanlist)
        list.pack()
        for item in chanlist:
            list.insert(END, item)
        goto=Button(win, text="Go To...", command=(lambda: self.channel(chanlist[list.curselection()[0]])))
        goto.config(highlightbackground='#999999')
        goto.pack()
        chan = Entry(win, text="Entry")
        chan.config(highlightbackground='#999999')
        chan.pack()
        nugo=Button(win, text="Go", command=(lambda: self.channel(chan.get())))
        nugo.config(highlightbackground='#999999')
        nugo.pack()
        jump=Button(win, text="Jump", command=(lambda: self.command("Jump")))
        jump.config(highlightbackground='#999999')
        jump.pack()
        qbut=Button(win, text="Quit", command=win.quit)
        qbut.config(highlightbackground='#999999')
        qbut.pack()
        win.wm_attributes("-topmost", 1)
        win.mainloop()

    def controller2(self,favlist=""):
        def updatelabel(label):
            status.config(text=label)
            time.sleep(1)
            status.config(text="")
        def VolumeUp():
            threading.Thread(target=updatelabel, args=('Volume Up',)).start()
            self.command('VolumeUp')
        def VolumeDown():
            threading.Thread(target=updatelabel, args=('Volume Down',)).start()
            self.command('VolumeDown')
        def ChannelUp():
            threading.Thread(target=updatelabel, args=('Channel Up',)).start()
            self.command('ChannelUp')
        def ChannelDown():
            threading.Thread(target=updatelabel, args=('Channel Down',)).start()
            self.command('ChannelDown')
        def Input():
            threading.Thread(target=updatelabel, args=('Input',)).start()
            self.command('Input')
        def Mute():
            threading.Thread(target=updatelabel, args=('Mute',)).start()
            self.command('Mute')
        def Confirm(event):
            threading.Thread(target=updatelabel, args=('Enter',)).start()
            self.command('Confirm')
        def Up(event):
            threading.Thread(target=updatelabel, args=('Up',)).start()
            self.command('Up')
        def Down(event):
            threading.Thread(target=updatelabel, args=('Down',)).start()
            self.command('Down')
        def Left(event):
            threading.Thread(target=updatelabel, args=('Left',)).start()
            self.command('Left')
        def Right(event):
            threading.Thread(target=updatelabel, args=('Right',)).start()
            self.command('Right')
        def Escape(event):
            threading.Thread(target=updatelabel, args=('Exit',)).start()
            win.focus()
            self.command('Exit')
        def Keypress(event): #or <Keypress-]> below, for example...
            if event.char == "=": VolumeUp()
            if event.char == "-": VolumeDown()
            if event.char == "+": ChannelUp()
            if event.char == "_": ChannelDown()
            if event.char == "]": ChannelUp()
            if event.char == "[": ChannelDown()
            if event.char == "i": Input()
            if event.char == "m": Mute()
            if event.char == "0": self.command('Num0')
            if event.char == "1": self.command('Num1')
            if event.char == "2": self.command('Num2')
            if event.char == "3": self.command('Num3')
            if event.char == "4": self.command('Num4')
            if event.char == "5": self.command('Num5')
            if event.char == "6": self.command('Num6')
            if event.char == "7": self.command('Num7')
            if event.char == "8": self.command('Num8')
            if event.char == "9": self.command('Num9')
            if event.char == ".": self.command('DOT')

        win = Tk()
        win.wm_attributes("-topmost", 1)
        win.config(bg='#999999')
        address = Label(win, text=self.ip, bg="#999999")
        address.pack()
        stats = Label(win, text="")
        stats.pack()
        statsthread = threading.Thread(target=self.checkconnection, args=(self.ip, stats))
        statsthread.setDaemon(True)
        statsthread.start()
        Label(win, text="+: Volume Up\n-: Volume Down\n]: Channel Up\n[:Channel Down", bg="#999999").pack()
        status = Label(win)
        status.config(text="")
        status.config(bg='#999999')
        status.config(width=20, height=1)
        status.pack(fill=X)
        win.bind('<Up>', Up)
        win.bind('<Down>', Down)
        win.bind('<Left>', Left)
        win.bind('<Right>', Right)
        win.bind('<KeyPress>', Keypress)
        win.bind('<Shift-KeyPress>', Keypress)
        win.bind('<Return>', Confirm)
        win.bind('<Escape>', Escape)
        win.bind('<Button-1>', self.setfocus)
        # chanbox = Entry(win, text="Channel:", textvariable=self.chanvar)
        # chanbox.bind('<Return>', self.interchan)
        # chanbox.pack()
        self.cbox = chanbox(win,favlist,command=chanlisthandler, args=self)
        self.cbox.list.bind('<Escape>', Escape)
        btn = Button(win, text="Quit", command=self.quit)
        btn.config(highlightbackground='#999999')
        btn.pack()
        status.focus()
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
        if self.response==0:
            url = 'http://'+self.ip+'/IRCC'
            cmd = self.cmds[cmdname]
            data ='<?xml version="1.0" encoding="utf-8"?><s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/"><s:Body><u:X_SendIRCC xmlns:u="urn:schemas-sony-com:service:IRCC:1"><IRCCCode>'+cmd+'</IRCCCode></u:X_SendIRCC></s:Body></s:Envelope>'
            try:
                requests.post(url, data=data)
            except:
                print('Error')

    def channel(self, numstr):
        numpad = ['Num0','Num1','Num2','Num3','Num4','Num5','Num6','Num7','Num8','Num9']
        for n in numstr:
            if n=='.':
                self.command('DOT')
            else:
                self.command(numpad[int(n)])
            time.sleep(0.2)
        self.command('Confirm')

    def interchan(self, event):
        print(self.chanvar)
        self.channel(self.chanvar)
    def setfocus(self, event):
        self.master.focus_set()
        #self.focus_set()