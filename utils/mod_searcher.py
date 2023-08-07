import pickle

# Funciones para escribir lista de búsqueda y poder leerla
# write list to binary file
def write_list(a_list,path_file):
    # store list in binary file so 'wb' mode
    with open(path_file, 'wb') as fp:
        pickle.dump(a_list, fp)
        print('Done writing list into a binary file')

# Read list to memory
def read_list(path_file):
    # for reading also binary mode is important
    with open(path_file, 'rb') as fp:
        n_list = pickle.load(fp)
        return n_list