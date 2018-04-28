#!/usr/bin/env python
import sys
import time
from PyQt5 import QtWidgets, QtCore, QtGui
import pygame


import origami_lib.instructionCorner as instructionCorner
import origami_lib.overlayInstruction as overlayInstruction
import origami_lib.ARProjection as ARProjection

class Window(QtWidgets.QMainWindow):
    """This class will allow the user to navigate our codebase by creating a GUI"""

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

        pygame.mixer.init()
        pygame.mixer.music.load('music/Japan.mp3')
        pygame.mixer.music.play(-1)

    def home(self):
        """This method defines the home screen for the GUI. Here the user can choose an instruction type."""

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
        self.quitButton.move((self.width / 2) - (self.bWidth / 2) - 17, 350)

        # Chose instruction type
        self.wOffset = 20  # width and height offset for positnioing
        self.hOffset = 70  # the larger buttons

        self.overlayButton = QtWidgets.QPushButton("Corner of Frame", self)
        self.overlayButton.clicked.connect(self.overlayOptions)
        self.overlayButton.resize(self.bWidth + self.wOffset, self.bHeight + self.hOffset)
        self.overlayButton.move((self.width + self.wOffset) / 6 - self.bWidth / 2, 125)

        self.projectButton = QtWidgets.QPushButton("Project", self)
        self.projectButton.clicked.connect(self.projectOptions)
        self.projectButton.resize(self.bWidth + self.wOffset, self.bHeight + self.hOffset)
        self.projectButton.move((self.width + self.wOffset)*(1/2) - self.bWidth/2 - 39, 125)

        self.projectButton = QtWidgets.QPushButton("Augmented Reality", self)
        self.projectButton.clicked.connect(self.runAR)
        self.projectButton.resize(self.bWidth + self.wOffset, self.bHeight + self.hOffset)
        self.projectButton.move((self.width + self.wOffset)*(5/6) - self.bWidth/2 - 84, 125)

    def overlayOptions(self):
        """Choose origami piece for displaying instructions in the corner"""

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
        foxButton.resize(self.bWidth + self.wOffset, self.bHeight + self.hOffset)
        foxButton.move((self.width + self.wOffset) / 2 - self.bWidth / 2 - 39, 125)
        foxButton.show()

    def projectOptions(self):
        """Choose origami piece for projection onto paper on table"""

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
        """When called helps user fold a samarai hat with instrictions projected onto paper on the table"""

        overlayInstruction.run('origami_lib/CompGenInstructions')
        self.__init__()

    def runFox(self):
        """Helps user fold a fox with instructinos in the upper left of the frame"""

        instructionCorner.run('origami_lib/OrigamiFox')
        self.__init__()

    def runAR(self):
        """Projects an image onto a paper which doesn't need to be parellel to the camera"""

        ARProjection.run('sq.png')
        self.__int__()

    def close_appllication(self):
        sys.exit()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    GUI = Window()
    sys.exit(app.exec_())
