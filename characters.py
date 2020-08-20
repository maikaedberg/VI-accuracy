import json
import moviegraphs
from imdb import IMDb

json_dir = '/project/vi_json/'


def cast_list(movie_id):
    """given the imdb id of a movie,
    returns a dictionary where the keys are associcated to the 
    characters and the values are the actors that play them"""
    roles = dict()
    
    ia = IMDb()
    movie = ia.get_movie(movie_id[2:])
    
    for i in movie['cast']:
        actor = i["name"]
        character = i.currentRole
        if not isinstance(character, list):
            character = [character]
        for i in character:
            if "name" in i:
                roles[i["name"]] = actor
            
    return roles

def get_character_app_dict(name):
    """returns a dictionary where the key is the actor 
    name in the VideoIndexer dataset, and the value is the 
   intervals (in seconds) at which they appear"""
    
    with open(json_dir + name + '.json') as infile:
        data = json.load(infile)
    char_app = dict()
    for i in data["summarizedInsights"]["faces"]:
        char_app[i["name"]] = [(j['startSeconds'],j['endSeconds']) for j in i["appearances"]]
    return char_app


def chars_in_scenes(scenes, chars):
    """return a list of actors given a list of tuples of start and end 
    seconds of each scene, so characters[i] gives all the actors 
    that appear between s_e[i][0] and s_e[i][1], according to VI"""
    res  = []
    for (s, e) in scenes:
        characters = []
        for (c, apperances) in chars.items():
            for a in apperances: 
                # if the two tuples (s,e) and (a[0], a[1]) overlap
                if(a[1] >= s and a[0] <= e): 
                    characters.append(c) 
                    break
        res.append(characters)
    return res

def get_chars_vi(test_id):
    """returns a list such that list[i] gives
    the set of actors found in the i-th Mg scene"""
    scenes = moviegraphs.load_scenes(test_id, all_mg)
    chars = get_character_app_dict(test_id)
    c = chars_in_scenes(scenes, chars)
    actors = cast_list(test_id)
    
    for i in range(len(c)):
        unknown = []
        for j in range(len(c[i])):
            if c[i][j] in actors:
                c[i][j] = actors[c[i][j]]
            else:
                unknown.append(c[i][j])
                c[i][j] = 'Unknown'
            
    return [set(i) for i in c]

def char_precision(test_id, all_mg):
    """returns the precision of the face identification
    software comparing the VI results to the information 
    on the MG dataset"""
    scenes = moviegraphs.load_scenes(test_id, all_mg)
    chars = get_character_app_dict(test_id)
    chars_vi = chars_in_scenes(scenes, chars)
    
    actors = cast_list(test_id)
    MG = all_mg[test_id]
    res = []
    for i in MG.clip_graphs.values():
        res.append([actors[j] for j in i.get_nodes_of_type("entity") if j in actors])
    
    total, correct = 0, 0

    for i in range(len(chars_vi)):
        for j in range(len(chars_vi[i])):
            if 'Unknown' not in chars_vi[i][j]:
                if chars_vi[i][j] in res[i]:
                    correct += 1
                total += 1
    return (correct / total) if total != 0 else 0

