![](https://github.com/concavegit/cv-assisted-origami/blob/gh-pages/PaperPics/testresult.png?raw=true)

By overlaying instructions realtime onto your sheet of paper, we make following origami instructions more straightforward and clear.

# Quickstart
We assume you have [git](https://git-scm.com/) and [python](https://www.python.org/) installed.
1. Run `git clone https://github.com/concavegit/cv-assisted-origami.git` in the command line.
2. Run `cd cv-assisted-origami` in your command line.
3. Run `pip install -r REQUIREMENTS.txt`.
4. Run `./main.py` to run the program.

# Process
Our group began with two interests: machine learning and computer vision.
However, as the intersection between the two is either already done or the subject of PhD research, we began to ask what we enjoyed: origami.


From that point, we wanted to make instructions easier to follow using computer vision. Traditional origami books are often difficult to interpret/understand, so we wanted our program to make
doing origami easier and more accessible especially to the beginner. We spent around a week fleshing out this idea, after which we learned a few things from our peers.
One thing we learned was that we were getting hung up on some way to describe the state of an origami model to use in our program, when really all we needed was a picture of an outline of the desired outcome and a few lines to indicate folds.

We spent another week creating our minimum viable product (MVP) and once again turned to our peers for advice.
We were then reminded that much of origami is comparing the current step to the next step, and so as a future development we can put a picture of the next instruction in a corner for comparison. These were good ideas, and may implement them in the future.
