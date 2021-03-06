# Proposal

## Big Idea

The main idea of the project is to give guidance in a simple and efficient way to help individuals to make origami models.
The minimum viable product is drawing lines on a folded piece of paper as well as a quick instruction in words displayed on screen for a simple 2D origami model.

The stretch goals are:
- Be able to model and project 3d shapes
- Learn what folds you are bad at doing
- Improve tracking (qr codes, etc)
- animate the fold

## Learning Goals

### Kevin:
- get better with CV.
- Combine math and programming.

### Mark:
- learn more about openCV and CV in general.
- Realtime data analysis

### Sid:
- Learn all the math required for the geometry

## Implementation Plan
We will use opencv.

- Have a file per class
- Have a folds class describing, for example, the fold animation and the location of the fold line.
- Have a class called FoldStateManager which keeps track of the sequence of folds and the state of the paper.
- Use matrices to represent the paper tranformations.

## Project Schedule
- Have a class diagram ready by 4/3
- Have the project done by 4/28
- Have the MVP 4/6
- Have code mostly done by 4/24

## Collaboration
- Weekly meetings from 1630 to dinner
- Consult Brad Minch on origami
- Initially pair-program until we are predictable.
- Integrate when ready

## Risk
Our stretch goals are quite difficult, and CV is dependent on normalized environment.

## Additional Course Content
- Project organization on a high level
