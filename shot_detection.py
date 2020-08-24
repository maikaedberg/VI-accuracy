import json
import videoindexer
import moviegraphs
import xlsxwriter

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
    VI = [i for i in videoindexer.load_cuts(data) if s < i < e]
    
    count = 0
    for i in range(len(MG)):
        if i == 0: prev = 0
        for j in range(prev, len(VI)):
            if VI[j] - 1 <= MG[i] <= VI[j] + 1:
                prev = j + 1
                count += 1
    return (round(count / len(VI), 3), round(count / len(MG), 3))

workbook = xlsxwriter.Workbook('shot_boundaries.xlsx')
worksheet = workbook.add_worksheet()

worksheet.write(0, 0, 'IMDb id')
worksheet.write(0, 1, 'precision')
worksheet.write(0, 2, 'recall')

row = 1
with open('movie_list.txt', 'r') as f:
    for l in f:
        movie_id = l.split('\t')[0]
        p, r = recall_precision_shots(movie_id)
        worksheet.write(row, 0, movie_id)
        worksheet.write(row, 1, '{}%'.format(round(p*100, 1))
        worksheet.write(row, 2, '{}%'.format(round(r*100, 1))
        row += 1
        
workbook.close()
