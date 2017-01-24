import pickle
from os import path


def get_path():
    """ Returns path to file 'companies.pickle'
    """
    here = path.dirname(__file__)
    return path.join(here, 'companies.pickle')


def save_with_pickle(data):
    """ Saves list of companies to 'companies.pickle' file
    """
    dbpath = get_path()
    with open(dbpath, 'wb') as dbfile:
        pickle.dump(data, dbfile)


def load_with_pickle():
    """ Loads list of companies from 'companies.pickle' file
    """
    dbpath = get_path()
    with open(dbpath, 'rb') as dbfile:
        data = pickle.load(dbfile)
    return data
