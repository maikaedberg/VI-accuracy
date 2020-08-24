# The Accuracy of VideoIndexer

Code for analysing the accuracy of [VideoIndexer (VI)](http://videoindexer.ai) by comparing the results to that produced by the 
[MovieGraphs (MG)](http://moviegraphs.cs.toronto.edu/) dataset on two fronts:
1. shot boundary detection
2. character identification

### Requirements ###
`MovieGraphs` dataset, which you can download after filling this [google form](http://docs.google.com/forms/d/e/1FAIpQLScytuCn4kRBKFPPei0t01Sfadpu8Qh5i9fFvfODWAAJGyEs7g/viewform).

### Usage ###
After downloading the directory, first create a file titled `movie_list.txt`, where each line is the IMDb id and the title of the movie you are studying, separated by a tab.
Under a folder, where json_dir is the directory, store all the .json files created after analysing the movie through Microsoft VideoIndexer.

To get the precision and recall of the shot boundary detection software, run `shot_detection.py`. 
This creates a file `shot_boundaries.xlsx` where the first column are the IMdb ids, the second column are the precisions, and the third column are the recalls.
Now, to get the precision of the facial identification software, run `characters.py`. This creates the file `facial_identification_precision.xlsx` which gives
the precision of all the identified actors in VI. 
