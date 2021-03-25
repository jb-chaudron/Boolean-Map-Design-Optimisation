# Boolean-Map-Design-Optimisation

## Table of contents
* [General Informations](#general-info)
* [Theoretical Background](#theroy)
* [Aim and Design of the project](#aim)
* [Technologies](#technologies)


## General Information
This project originate from my Bachelor's Thesis, and was achieved in December 2019, at the university of Lyon II for the class "Outil de Conception d'expérience"
(Tools for Experimental Design) taught by Alexandre Bluet.

## Theoretical Background
Introduced by Huang & Pashler in 2007, the theory of Boolean map tried to explain how visual attention worked, and how could conscious perception happen.
In brief, it was proposed that disponible information from uncounscious perception were queried by two kind of operations.

* The Feature location procedure
* The location Feature procedure

It is thought that sensorial information would have some dimensions, containing informations about colors, shape, speed etc... .
The features can be thought as the information itself, as "Red" would be a feature of the dimension "Color".
So, from the two procedures, the first one aims to retrieve the Information located at some place.
For instance, a red square is placed at the top right spot of an image, by querying the features at this place, the cognitive systems would recieve the informations
"Red" and "Square".
Next, the Location feature procedure, aims to retrieve the location of every objects which have a specific feature.
For instance, one could search for every "Red" objects in a picture.

On top of that, one can build successive filters through Boolean operation such as Intersection and Union of Boolean Map.
Hence, one can query the location of all "Red" and "Square" objects, performing an Intersection of the two maps "Red" and "Square".
One could also query the union of these two maps.
According to the authors, one couldn't be aware of several different features in the same dimensions, e.g. one couldn't be
aware of both a "Red" and a "Green" object.
Even though one might think one perception is continous, the idea would be that, if an object changes it's features, as long as one hasn't refresh
it's query about the object, the known feature about this object doesn't change.


* Huang, L., & Pashler, H. (2007). A Boolean map theory of visual attention. Psychological review, 114(3), 599.

## Aim and Design of the project
This project aims to assess the idea that one has to refresh it's perception in order to access to information about the world.
For that, we've designed an experiment, in which one has to follow several objects, moving on a screen.
Their is one central target and several peripherical distractors.
The target will change it's color, and the subject has to report it in order to finish the study.
The distractor may on may not change their color, if this changes are reported, the subject obtain more point or gratification (Or whatever positiv depending on the ressources).

The idea is as follow :

* First, if one has to stay focus on the color of the target, the query should either focus on querying the position of objects with the same color as the target's
or on querying color of the object at the target location (i.e. the target itself).
* Second, whatever Boolean Union or Intersection is made, as the target color should be queried, the only information that should be refreshed would be about
the target's color. Then the changes in the distractors should include either a change form the target color to another one, either from any color to the target's one.

Thus we expect that the more reported changes in distractors should include a change from or to the target's color.

Another aspect of the experiment is the nature of the idea of "Same feature". Indeed, when does a color begin to be different to another, it feels like a small
difference in the wavelenght of a color, should not count as a clear change of color.
But then it's obvious that "Green" and "Red" are different colors.
We encode this as a normal distribution centered at the target colors, to account for the distance to this color, we use the HLS system.
The question is then, what is the standard deviation that encode the shape of this distribution, i.e. what color is similar to the mean.

In order to assess this last question, we use Hierarchical Bayes Modelling.
An Invese-Gamma distribution gives us the standard deviation of the normal distribution encoding the probability to detect any color, when the
subject has to stay focus on a target having a given color. 
For the sake of the experiment, the target could only start with one of four colors ("Red","Green","Blue","Yellow") which correspond to the four foundamental colors,
opposed on to the other given Hering's Chromatic circle.
Thus, as the experiment progress, the normal distribution update itself to fit the ability of the subject to detect any color given that he is looking at a "Red" target.
This also allows us to design specific color display strategy, in order to test specific hypothesis.

## Technologies
Project is created with:
* Python
* Psychopy

Peirce, J. W., Gray, J. R., Simpson, S., MacAskill, M. R., Höchenberger, R., Sogo, H., Kastman, E., Lindeløv, J. (2019). PsychoPy2: experiments in behavior made easy. Behavior Research Methods. 
	
