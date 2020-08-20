import json
import videoindexer
import moviegraphs
import numpy as np

vid_dir = '/porject/mg_videoinfo/video_boundaries/'
json_dir = '/project/vi_json/'


def recall_precision_shots(movie_id):
    """returns the recall and precision of the shot detection software,
    comparing the MG dataset to the results found on VI"""
    
    scenes = moviegraphs.load_scenes(movie_id, all_mg)
    # s is the starting second of the movie (after the opneing credits)
    # e is the ending second of the movie (before the ending credits)
    s, e = scenes[0][0], scenes[-1][1]
    with open(json_dir + movie_id + '.json') as f:
        data = json.load(f)
        
    MG = [i for i in moviegraphs.load_cuts(vid_dir, movie_id) if s < i < e]
    VI = [i for i in videoindexer.load_cuts(data) if s  < i < e]
    
    count= 0
    for i in range(len(MG)):
        if i == 0: prev = 0
        for j in range(prev, len(VI)):
            if VI[j] - 1 <= MG[i] <= VI[j] + 1:
                prev = j + 1
                count += 1
    return (round(count / len(VI), 3), round(count / len(MG), 3))


            
