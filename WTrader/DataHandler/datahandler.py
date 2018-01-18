import pickle
from pathlib import Path

def save_obj(obj, name ):
    with open( 'WTrader/Data/'+name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name ):
    with open( 'WTrader/Data/'+name + '.pkl', 'rb') as f:
        return pickle.load(f)

def obj_exist(name):
    my_file = Path("WTrader/Data/"+name+'.pkl')
    return my_file.is_file()