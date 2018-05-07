---
title: Tech
permalink: /tech/
---

## The Challenge

To assist people with folding origami, we first identified two major challenges inherent to the process: interpretation of instructions, and execution of folds. Individuals who aspire to fold up their own origami creations however, probably wish to execute the folds involved of their own volition, and so we determined the most useful challenge in the space worth addressing dealt directly with the clarification of the fold explanations involved in any particular instruction set. Below is an example of a complicated and hard to interpret set of instructions.

![](https://github.com/concavegit/cv-assisted-origami/blob/gh-pages/PaperPics/Complicated.jpg?raw=true)

To accomplish this, we designed a mode of assistance that visualizes instructions on or near the paper in the same frame, such that the current state of the paper prior to any given fold instruction can be validated/compared to the instruction set with significantly more ease. The following content provides both a high-level architecture overview and detailed explanations for exactly how we did this.

## Overview

Behind the GUI, our architecture can be summed up by this diagram:

![](https://github.com/concavegit/cv-assisted-origami/blob/master/documents/class_diagram.png?raw=true)

Starting at the leaves of this tree, the `Instruction` class looks into a directory and finds all files with a name like `step01.png`.
It then creates a list of these images in `steps` and keeps track of the current step number in `currentstep`. A program that uses this class uses `nextStep` to get the next instruction image.

The `DetectPaper` and `OverlayInstruction` stages are not really classes rather than strategies used to solve the problems.
[The Simple and Effective](https://concavegit.github.io/cv-assisted-origami/tech/#the-simple-and-effective) and [The Simple and More Effective](https://concavegit.github.io/cv-assisted-origami/tech/#the-simple-and-more-effective) detect the paper differently as described in those sections.

# Projecting Instructions onto a Paper
In all cases the instructions are stored as images with solid black outlines and other notation for folds.

## MVP
This is an MVP because there is no projection of the paper, simply an image of the instructions in the upper right-hand corner of the display. Not only was it a first step in getting a product out, it also offers voice output for reading out loud instructions.

## The Simple and Effective
The simple method lies in first scaling the instruction image and then moving it to the correct location on the camera input.
Since the paper is white and the background is black, turning all colors below some intensity into black and other colors white turns the image into a white shape representing the model and black everywhere else. Afterwards, the vertices are detected and the area of the shape is found using the [shoelace formula](https://en.wikipedia.org/wiki/Shoelace_formula).
The same area-finding procedure is used on the image of the instruction image.
By comparing the areas, the instruction image can be scaled to the size of the user's paper.
The placement of the image of the instruction is done by overlaying the centroids of the vertices of the scaled instruction image and the user's paper.

The final result is this:

![](https://github.com/concavegit/cv-assisted-origami/blob/gh-pages/PaperPics/testresult.png?raw=true)

This method is simple and effective, though it requires the paper to be parallel to the camera as well as a specific rotation.

## The Simple and More Effective

The advanced method builds on top of prior methodologies by providing an augmented reality experience, and actually projecting the instructions onto the paper as it is folded. While this task is incredibly difficult to perform without depth sensing for 3D structure (for minute folds), it turns out it is not all too difficult to pull off for larger folds, which can be represented more accurately by the shape of the perimeter of the folding paper. Still, the ideal instruction needs to be transformed before it can be overlaid onto the webcam input. To do this, several steps were taken.

### Image thresholding

A similar, mean-based thresholding process was used for this method to the prior methods. A binary image was produced as output for contour detection.

### Countour detection

All the countours that can be extracted from the thresholded image are extracted and sorted into an array by area.

### Contour filtering

A set of rules was devised to determine whether a contour was "bad" or not. While the process used to determine these rules was extensive and highly based on trial and error, it remains an effective and necessary step for the detection of the paper.

### Countour approximation

For all the remaining "good" contours, a polygon approximation algorithm is executed. Highly irregular shapes produce shapes with a high edge count, and can be detected by using a proportionally small amount of the perimeter for approximation.

### Countour-Instruction verification

The number of sides of the instruction at a given state is used as a final filter for any remaining contours. The remaining contour, if any, represents a polygonal approximation of the paper.

### Homography estimation

At this point, the contour that is detected can be compared against the detected contour from the instructions to estimate a homography matrix. Essentially, this operation involves solving for some transformation matrix given both sets of points.

$$
s \begin{bmatrix} x'\\y'\\1\end{bmatrix}
= H \begin{bmatrix}x\\y\\1\end{bmatrix}
= \begin{bmatrix}h_{11} & h_{12} & h_{13} \\ h_{21} & h_{22} & h_{23}\\ h_{31} & h_{32} & h_{33} \end{bmatrix}
\begin{bmatrix}x\\y\\1\end{bmatrix}
$$


### Instruction overlay

We apply the estimated homography matrix as a transformation to the instruction image, and render it on a black canvas. This image is used as a mask over the webcam input, and the transformed instruction is overlaid on top of the camera feed.
