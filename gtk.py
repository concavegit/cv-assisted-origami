import gi
from gi.repository import Gtk
from overlay_instruction2 import overlayVideo


gi.require_version('Gtk', '3.0')


class MyWindow(Gtk.Window):
    def __init__(self, cap=cv2.VideoCapture(0)):
        super().__init__(title='Hello World')
        self.hbox = Gtk.ButtonBox.new(Gtk.Orientation.HORIZONTAL)
        self.des1 = Gtk.Button(label='Piece 1')
        self.des2 = Gtk.Button(label="Piece 2")
        self.des3 = Gtk.Button(label='Piece 3')

        self.hbox.add(self.des1)
        self.hbox.add(self.des2)
        self.hbox.add(self.des3)

        self.des1.connect('clicked', self.onBNext)
        self.des2.connect('clicked', self.onBPrev)
        self.des3.connect('clicked', self.onBPrev)
        self.add(self.hbox)
        self.connect('destroy', self.destroy)
        self.show_all()
        # cameraP = threading.Thread(self.cvWin())
        # cameraP.start()

    def onBNext(self, button):
        overlayVideo(cv2.VideoCapture(0))

    def onBPrev(self, button):
        print('prev')

    def destroy(self, data):
        Gtk.main_quit(data)


win = MyWindow()
Gtk.main()
