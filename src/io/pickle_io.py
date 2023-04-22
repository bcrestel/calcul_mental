import pickle

def read_from_pickle(file_name):
    with open(file_name, 'rb') as f:
        return pickle.load(f)


def write_to_pickle(object, file_name):
    with open(file_name, "wb") as f:
        pickle.dump(object, f)