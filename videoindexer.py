import json

json_dir = '/project/vi_json/' #change to your path
movie_id = 'tt0146882'

with open(json_dir + movie_id + '.json') as f:
    data = json.load(f)
    
def time_to_secs(t):
    l = t.split(':')
    return round(int(l[0])*3600 + int(l[1])*60 + float(l[2]),2)

def load_cuts(data):
    """returns a list of cuts"""
    cuts = []
    for i in data["videos"][0]["insights"]["shots"]:
       cuts.append(time_to_secs(i["instances"][0]["end"]))
    return cuts

def load_shot_type(data):
    """returns a dictionary where the keys start and ending timestamp of 
    each shot and the values are the shot type labels"""
    shot_type = dict()
    types = {'Wide', 'Medium', 'CloseUp', 'ExtremeCloseUp'}
    
    for i in data["videos"][0]["insights"]["shots"]:
        shot = i["instances"][0]["start"], i["instances"][0]["end"]
        scale = [l for l in i["tags"] if l in types] if "tags" in i else ['Wide']
        shot_type[shot] = scale
    
    return shot_type

def load_scenes(data):
    """returns a list of tuples of the start and ending timestamp of 
    each scene"""
    scenes = []
    for i in data["videos"][0]["insights"]["scenes"]:
        scenes.append((i["instances"][0]["start"], i["instances"][0]["end"]))
    return scenes
    
def load_faces(data):
    """returns a dictionary where the keys are the names and the 
    values are the list of timestamps apperared"""
    faces = dict()
    
    for i in data["summarizedInsights"]["faces"]:
        faces[i["name"]] = []
        for j in i["appearances"]:
            faces[i["name"]].append((j['startTime'],j['endTime']))
            
    return faces
