

# Computer-Vision-Assisted Origami
[Project Website](https://concavegit.github.io/cv-assisted-origami/)

[![Build Status](https://travis-ci.org/concavegit/cv-assisted-origami.svg?branch=master)](https://travis-ci.org/concavegit/cv-assisted-origami)
[![license](https://img.shields.io/github/license/mashape/apistatus.svg)](https://github.com/concavegit/cv-assisted-origami/blob/master/LICENSE)

![demo](https://github.com/concavegit/cv-assisted-origami/blob/gh-pages/PaperPics/testresult.png?raw=true)

This program utilizes the capibilities of the OpenCV library to help the user fold a piece of origami. There are three main
ways that the user can choose to engage with the program. The first is for the instructions to be displayed in the upper left
hand corner of the frame of the webcam's footage. The second is for the instructions to be projected onto the paper (as long
as it is parellel to the table). The last (which is still a bit experimental) is for the instructions to be projected onto the paper regardless of its orientation to the camera. Each of these modes requires the user to push a key for the next step
to be projected/displayed.

## Authors
The authors of this program are Kawin Nikomborirak, Mark Goldwater, and Sidd Garimella. You can read more about them on
the project website

## Dependencies:
To obtain the following dependencies, simply run `pip install -r REQUIREMENTS.txt`
  * OpenCV 3
  * Numpy 1.14.2
  * PyQt5
  * pygame
  * pyttsx3

## Quick start:

To run this software, execute main.py by typing `./main.py` in the cv-assisted-origami directory, and you should
be presented with the following GUI

## Usage:
Before running the program, it is necessary to set up an external webcam so that it faces downward at a table. This is where
all the folding will take place.

Modes:

1. Unassisted: Minimum Viability

    To begin, execute the fold instructions as they are displayed on-screen. Confirm fold completion and repeat until the final instruction is reached.

2. Assisted

    To begin receiving valid webcam input, find a surface that contrasts highly with the paper being folded, and position the webcam above it. Starting from the first instruction, continue folding the paper as instructions appear on-screen.

3. Augmented: Stretch

    Follow the instructions described in (2), but fold across the line that is projected over the paper on-screen. Continue folding over new lines as they appear on the paper until lines are no longer visible.

## Implementation Details:


## Contribution guidelines:

This repository can be easily forked and contributed to on Github. To suggest new changes, please submit a [pull request](https://github.com/concavegit/cv-assisted-origami/pulls).

## Questions/Concerns:

To report any bugs/issues, open a new [issue](https://github.com/concavegit/cv-assisted-origami/issues) under the repository.
