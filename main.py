#######################################################################################
# Codigo de ejecucion de main del proyecto para la tesis de Camilo, en este documento #
# se ejecutaran las funciones desarrolladas para el cumplimiento de los objetivos #####
# planteados para el procesamiento, analisis y clasificacion de imagenes de estudio ###
# psicocognitivo ######################################################################
#######################################################################################

# SECCION DE IMPORTE DE LIBRERIAS #
# Librerias utilitarias #
from os import getcwd
from time import time
# librerias de diseño propio #
from functions.obj_img import lectorImagen
from functions.file_module import descriptor_archivos

## Seccion de variables Globales
CONT_IMG_PROCS = 0

if __name__ == "__main__":
    ## Vamos a evaluar el tiempo de procesamiento
    tiempo_inicio = time()
    # Primero validamos la existencia de archivos.
    desc_m = descriptor_archivos(getcwd())

    # Se realiza una validacion de que la lista de imagenes existentes sea mayor a 0
    while True:
        # Validacion de final de la lista de objetos, o lista de objetos a preprocesar vacios
        if CONT_IMG_PROCS >= len(desc_m.lista_imgs) or len(desc_m.lista_imgs) == 0:
            break
        
        # Se crea un objeto para la lectura de la imagen ...
        #######################################################################################################
        # El siguiente procesamiento realizara las modificaciones necesarias para las imagenes de muestra del #
        # # proyecto, de tal manera que se realice la identificacion de la figura, la extraccion del minimo #####
        # recueadro que contenga toda la figura, para lo que se cambiara el color (escala de grices), se juga #
        # ra con el contraste, brillo y detalles de tal manera que cada uno de los dibujos sea correctamente ##
        # identificado y extraiido para su posterior almacenamiento en el dataset #############################
        #######################################################################################################
        ## Inicio de procesamiento de imagenes
        img_leida = lectorImagen(
            ruta = desc_m.lista_imgs[CONT_IMG_PROCS][-1]
        )
        img_leida.auto_ajuste()
        img_leida.extraccion_contornos()
        img_leida.guardar_md()
        #img_leida.auto_ajuste()
        
        # Fin de procesamiento y destruccion de objeto
        del img_leida
        
        # Contador de rutas extraidas del descriptor de archivos
        CONT_IMG_PROCS += 1
    
    desc_m.organizar_archivos()
    tiempo_final = time() - tiempo_inicio
    print(f"El tiempo que demoro el proceso total fue: {tiempo_final} sg")

    