---
title: Tech
permalink: /tech/
---

Behind the GUI, our architecture can be summed up by this diagram:

![](https://github.com/concavegit/cv-assisted-origami/blob/master/documents/class_diagram.png?raw=true)

Starting at the leaves of this tree, the `Instruction` class looks into a directory and finds all files with a name like `step01.png`.
It then creates a list of these images in `steps` and keeps track of the current step number in `currentstep`. A program that uses this class uses `nextStep` to get the next instruction image.

The `DetectPaper` and `OverlayInstruction` stages are not really classes rather than strategies used to solve the problems.
[The Simple and Effective](https://concavegit.github.io/cv-assisted-origami/tech/#the-simple-and-effective) and [The Simple and More Effective](https://concavegit.github.io/cv-assisted-origami/tech/#the-simple-and-more-effective) detect the paper differently as described in those sections.

# Projecting Instructions onto a Paper
In all cases the instructions are stored as images with solid black outlines and other notation for folds.

## MVP

## The Simple and Effective
The simple method lies in first scaling the instruction image and then moving it to the correct location on the camera input.
Since the paper is white and the background is black, turning all colors below some intensity into black and other colors white turns the image into a white shape representing the model and black everywhere else. Afterwards, the vertices are detected and the area of the shape is found using the [shoelace formula](https://en.wikipedia.org/wiki/Shoelace_formula).
The same area-finding procedure is used on the image of the instruction image.
By comparing the areas, the instruction image can be scaled to the size of the user's paper.
The placement of the image of the instruction is done by overlaying the centroids of the vertices of the scaled instruction image and the user's paper.

This method is simple and effective, though it requires the paper to be parallel to the camera as well as a specific rotation.

## The Simple and More Effective
