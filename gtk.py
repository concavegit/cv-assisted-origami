import gi
from gi.repository import Gtk, GLib
import threading
# from overlay_instruction2 import overlayVideo
import cv2

gi.require_version('Gtk', '3.0')


class MyWindow(Gtk.Window):
    def __init__(self, cap=cv2.VideoCapture(0)):
        super().__init__(title='Hello World')
        self.hbox = Gtk.ButtonBox.new(Gtk.Orientation.HORIZONTAL)
        self.bNext = Gtk.Button(label='Next')
        self.bPrev = Gtk.Button(label="Prev")
        self.hbox.add(self.bPrev)
        self.hbox.add(self.bNext)
        self.bNext.connect('clicked', self.onBNext)
        self.bPrev.connect('clicked', self.onBPrev)
        self.add(self.hbox)
        self.timeout_id = GLib.timeout_add(1000, self.hi, None)
        self.cap = cap
        self.connect('destroy', self.destroy)
        winShow = threading.Thread(self.show_all())
        winShow.start()
        # cameraP = threading.Thread(self.cvWin())
        # cameraP.start()

    def onBNext(self, button):
        print('next')

    def onBPrev(self, button):
        print('prev')

    def hi(self, data):
        print('hi')
        return True

    def destroy(self, data):
        Gtk.main_quit(data)

    def cvWin(self):
        while True:
            print('ho')


def show():
    while True:
        print('ho')


win = MyWindow()
Gtk.main()
