#######################################################################################
# Codigo de ejecucion de main del proyecto para la tesis de Camilo, en este documento #
# se ejecutaran las funciones desarrolladas para el cumplimiento de los objetivos #####
# planteados para el procesamiento, analisis y clasificacion de imagenes de estudio ###
# psicocognitivo ######################################################################
#######################################################################################

# SECCION DE IMPORTE DE LIBRERIAS #
# Librerias utilitarias #
# librerias de diseño propio #
from functions.obj_img import Imgen

if __name__ == "__main__":
    #objeto_1 = Imgen(r"C:\Users\edavi\OneDrive\Escritorio\Py_completo\proyecto_camilo\assets\imgs\original_img\Figura_rey_hd_amp.png")
    objeto_1 = Imgen(r"C:\Users\edavi\OneDrive\Escritorio\Py_completo\proyecto_camilo\assets\imgs\all_imgs\97.png")
    print(objeto_1.id_)