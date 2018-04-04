# Background and Context
We are trying to use `opencv` to project origami instructions onto a presented sheet of paper in the form of lines. We are currently thinking that lines of different types of folds will be color coded. Our MVP is to have the user manually hit `next` for the program to proceed to the next step and assume only 2D structures. The projection will only project when the model is parallel to the camera. So, before the user fold the paper they will hold it parellel to the camera, and the program will draw a line onto the camera which will shown the user where to fold. Then the user will fold, and the process will repeat until the piece is done. The stretch goal is to automatically detect when a step is completed and/or to keep track of 3D structures. We will also implement detection when the shape is not parallel to the camera.

# Key Questions
* How to detect which side of the 2D figure is displayed
  * Origami folding requires flipping the piece sometimes. As an MVP we could assume the person flips it, but it would be cool to detect flipping of the paper.
  * As of now, we are thinking of coloring the paper or somehow detecting the transformation
* Is there a way to detect folds better?
  * We are thinking that the perimeter shape of the paper changes with each fold. Can we calculate what this should be each time?
* What is an elegant way to keep the state of the paper which would concern the natural properties and structure of paper while keeping relevant information?
  * Points of the perimeter?

# Agenda
* Make it clear that we would like feedback after the presention orally if time; in google form otherwise 
* Give background info (see Background and context
* Discuss current ideas about question
* Ask key questions
* Ask for questions about the aspects of our project we presented/answers to our key questions
