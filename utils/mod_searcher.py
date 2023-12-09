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
    # Para leer dataframe de interés
    with open(path_file, 'rb') as fp:
        n_list = pickle.load(fp)
        return n_list

def read2list(path_file):
    df_list = read_list(path_file)
#     display('Tipo de variable', type(aux), 'Lectura de variable auxiliar', aux)
    return df_list[0]['Id'].to_list()