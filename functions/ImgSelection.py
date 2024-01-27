# El siguiente programa contiene las funciones para la lectura del documento de identificadores #
# y la seleccion de imagenes para el dataset ####################################################
# SECCION DE IMPORTE DE LIBRERIAS
import os
import pandas as pd

# La siguiente funcion realiza la lectura del archivo e identificacion de cada una de las imagenes #
def seleccionCaracteristicas(url_dir = ""):
    # Lectura de dataset como archivo #
    file_read: pd.DataFrame = pd.read_excel(url_dir, index_col = 0)

    
    salida_val_1 = file_read[file_read[file_read.columns[-1]] == 0]

    salida_val_2 = file_read[file_read[file_read.columns[-1]] == 1]

    salida_val_3 = file_read[file_read[file_read.columns[-1]] == 2]

    return salida_val_1

if __name__ == "__main__":
    print("hola")
    #seleccionCaracteristicas("../documents/identificadores.xlsx")