import pickle
import pandas

# Funciones para escribir lista de búsqueda y poder leerla
# write list to binary file
def write_list(a_list,path_file):
    # store list in binary file so 'wb' mode
    with open(path_file, 'wb') as fp:
        pickle.dump(a_list, fp)
        print('Done writing list into a binary file')
        
# Write searched product ids in pickle
def write_df_search(df,output_path):
    # store list in binary file so 'wb' mode
    with open(output_path, 'wb') as fp:
        pickle.dump(df, fp)
        print('Done writing dataframe into a binary file')

# Read list to memory
def read_df_search(path_file):
    # Para leer dataframe de interés
    with open(path_file, 'rb') as fp:
        return pickle.load(fp)

# Read list to memory
def read_list(path_file):
    # Para leer dataframe de interés
    with open(path_file, 'rb') as fp:
        n_list = pickle.load(fp)
        return n_list

def read2list(path_file):
    # Función especial para tomas listas de dataframes con distintas búsquedas y devolución de la columna a lista de la primera búsqueda
    df_list = read_list(path_file)
    return df_list[0]['Id'].to_list()