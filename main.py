import sys
import time
from PyQt5 import QtWidgets, QtCore, QtGui


import instruction
import overlay_instruction2


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
        self.title = QtWidgets.QLabel(self)
        self.title.setText("Would you like instructions projected onto the paper or in the frame's corner?")
        self.title.resize(self.bWidth + 650,self.bHeight)
        self.title.move((self.width/2) - (self.bWidth/2) - 285,10)
        self.title.setFont(QtGui.QFont('SansSerif', 13))
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
        self.projectButton.clicked.connect(self.projectOptions)
        self.projectButton.resize(self.bWidth + self.wOffset, self.bHeight + self.hOffset)
        self.projectButton.move((self.width + self.wOffset)*(3/4) - self.bWidth/2 - 39, 125)

    def overlayOptions(self):
        # clear Window
        self.title.deleteLater()
        self.quitButton.deleteLater()
        self.overlayButton.deleteLater()
        self.projectButton.deleteLater()

        # title
        title = QtWidgets.QLabel(self)
        title.setText("Choose your piece!")
        title.resize(self.bWidth + 100,self.bHeight)
        title.move((self.width/2) - (self.bWidth/2) - 50,10)
        title.setFont(QtGui.QFont('SansSerif', 13))
        title.show()

        # Piece options
        foxButton = QtWidgets.QPushButton("Fox", self)
        foxButton.clicked.connect(self.runFox)
        foxButton.resize(self.bWidth + self.wOffset,
                         self.bHeight + self.hOffset)
        foxButton.move((self.width + self.wOffset) /
                       2 - self.bWidth / 2 - 39, 125)
        foxButton.show()

    def projectOptions(self):
        # clear Window
        self.quitButton.deleteLater()
        self.overlayButton.deleteLater()
        self.projectButton.deleteLater()
        self.title.deleteLater()

        # title
        title = QtWidgets.QLabel(self)
        title.setText("Choose your piece!")
        title.resize(self.bWidth + 100,self.bHeight)
        title.move((self.width/2) - (self.bWidth/2) - 50,10)
        title.setFont(QtGui.QFont('SansSerif', 13))
        title.show()

        # Piece options
        samButton = QtWidgets.QPushButton("Samurai", self)
        samButton.clicked.connect(self.runSam)
        samButton.resize(self.bWidth + self.wOffset, self.bHeight + self.hOffset)
        samButton.move((self.width + self.wOffset)/2 - self.bWidth/2 - 39, 125)
        samButton.show()

    def runSam(self):
        overlay_instruction2.run('CompGenInstructions')
        self.__init__()

    def runFox(self):
        instruction.run('OrigamiFox')
        self.__init__()

    def close_appllication(self):
        sys.exit()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    GUI = Window()
    sys.exit(app.exec_())
<<<<<<< HEAD
=======


run()
>>>>>>> 00154349f64795558b818a47bb708e9ac99afcc0
