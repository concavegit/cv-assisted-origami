import sys
import time
from PyQt5 import QtWidgets, QtCore, QtGui


import instruction


class Window(QtWidgets.QMainWindow):

    def __init__(self):
        super(Window, self).__init__()
        self.width = 700
        self.height = 400
        self.bWidth = 100
        self.bHeight = 30

        self.setGeometry(50, 50, self.width, self.height)
        self.setWindowTitle("CV-Assisted Origami")
        self.home()
        self.show()

    def home(self):
        # title
        self.title = QtWidgets.QTextEdit(self)
        self.title.setReadOnly(True)
        self.title.setText("Hello")
        # Quit button
        self.quitButton = QtWidgets.QPushButton("Quit", self)
        self.quitButton.clicked.connect(self.close_appllication)
        self.quitButton.resize(self.bWidth, self.bHeight)
        self.quitButton.move((self.width / 2) - (self.bWidth / 2), 350)
        # Chose instruction type
        self.wOffset = 20  # width and height offset for positnioing
        self.hOffset = 70  # the larger buttons

        self.overlayButton = QtWidgets.QPushButton("Corner of Frame", self)
        self.overlayButton.clicked.connect(self.overlayOptions)
        self.overlayButton.resize(
            self.bWidth + self.wOffset, self.bHeight + self.hOffset)
        self.overlayButton.move(
            (self.width + self.wOffset) / 4 - self.bWidth / 2, 125)

        self.projectButton = QtWidgets.QPushButton("Project", self)
        # self.projectButton.clicked.connect()
        self.projectButton.resize(
            self.bWidth + self.wOffset, self.bHeight + self.hOffset)
        self.projectButton.move(
            (self.width + self.wOffset) * (3 / 4) - self.bWidth / 2 - 39, 125)

    def overlayOptions(self):
        # clear Window
        self.quitButton.deleteLater()
        self.overlayButton.deleteLater()
        self.projectButton.deleteLater()

        # Piece options
        foxButton = QtWidgets.QPushButton("Fox", self)
        foxButton.clicked.connect(self.runFox)
        foxButton.resize(self.bWidth + self.wOffset,
                         self.bHeight + self.hOffset)
        foxButton.move((self.width + self.wOffset) /
                       2 - self.bWidth / 2 - 39, 125)
        foxButton.show()

    def runFox(self):
        instruction.run('OrigamiFox')
        self.__init__()

    def close_appllication(self):
        sys.exit()


def run():
    app = QtWidgets.QApplication(sys.argv)
    GUI = Window()
    sys.exit(app.exec_())


run()
