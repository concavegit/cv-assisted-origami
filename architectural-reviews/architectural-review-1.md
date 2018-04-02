# Background and context
We are trying to use `opencv` to project origami instructions onto a presented sheet of paper.
Our MVP is to have the user manually hit `next` for the program to proceed to the next step and assume only 2D structures.
The projection will only project when the model is parallel to the camera.
The stretch goal is to automatically detect when a step is completed and/or to keep track of 3D structures.
We will also implement detection when the shape is not parallel to the camera.

# Key questions
- How to detect which side of the 2D figure is displayed
- Is there a way to detect folds better?
- What is an elegant way to keep the state of the paper? Do we use vertices and lines?

# Agenda
- Give background info
- Discuss current ideas about question
- Ask key questions
- Ask for answers
- Ask for questions
