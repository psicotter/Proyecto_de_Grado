## El siguiente codigo alberga las funciones de lectura e identifiacion de imagenes como objetos ##
# SECCION DE IMPORTE DE LIBRERIAS UTILITARIAS DE PYTHON #
import os
import cv2
import numpy as np
## SECCION DE IMPORT DE LIBRERIAS PROPIAS #

# La clase imagen, alberga todas las caracteristicas de una imagen ingresada para el procesamiento #
# Tambien tiene los metodos necesarios del procesamiento de la misma ###############################
class lectorImagen:
    # Propiedades de la imagen #
    id_: str = "" #Inicial_tipo-anho_ancho_alto_numero-tipo_archivo
    nombre_img: str = ""
    ruta: str = ""
    width: int = 0
    heigth: int = 0
    score: float = 0.0
    codigo_ref: int = int
    tipo_archivo: str = ""
    img = None
    # Inicializacion de objeto, con atributos predefinidos #
    def __init__(
            self,
            ruta: str
        ):
        # designacion de valores de identificacion
        self.identificar_archivo(ruta)

        # Designa los valores de la imagen
        self.lectura_img()

        ## DEsignacion de if
        self.crear_identificacion()

    def identificar_archivo(self, ruta: str) -> None:
        if not os.path.isfile(ruta):
            raise ValueError("La ruta ingresada no corresponde a una ruta real.")
        
        # Asignacion de ruta
        self.ruta = ruta
        
        ## Designacion de las propiedades de la imagen seleccionada
        tmp_name: str = str(os.path.basename(ruta))

        # Asignacion de tipo y nombre
        self.nombre_img = tmp_name.split('.')[0]
        self.tipo_archivo = tmp_name.split('.')[1]
        
    def lectura_img(self) -> None:
        # Lectura de la imagen
        self.img = cv2.imread(self.ruta, 0)

        # Designacion de valores de tamaño
        temp_values = self.img.shape
        self.heigth = temp_values[0]
        self.width = temp_values[1]


    # Funciones utilitarias y de validacion
    # La siguiente funcion, visualiza de manera completa una imagen, en formato alterado por opencv.
    def show_img(self, imagen = None, nombre_ventana: str = "Imagen", val_objeto: bool = True) -> None:
        ## Validar si la imagen que se desea mostrar es la actual
        if val_objeto == True:
            imagen = self.img.copy()
        
        cv2.imshow(nombre_ventana, imagen)
        
        # Cerrar con una tecla 
        while True:
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
        
        # Close the openCV window
        cv2.destroyAllWindows()

    # La siguiente funcion busca extraer todas las caracteristicas de una imagen
    def auto_ajuste(self) -> None:
        # Es necesario validar si la imagen con la que se va a experimentar solo tiene 2 canales o si esta a color
        if len(self.img.shape) > 2:
            # Se almacena una copia  de la imagen real
            self.img = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        # Ajuste de tamanho inicial
        if self.width > 1000 and self.heigth > 808:
            self.func_resize()
        
        # Se almacena una copia de la imagen
        img_to_mod = self.img.copy()

        # Lectura de brillo
        brillo_img = int(img_to_mod.mean())

        ## Ajuste de tonalidades de brillo y extraccion de treshold
        if brillo_img < 240:
            # Ajuste de brillo
            img_to_mod = cv2.convertScaleAbs(img_to_mod, alpha=2, beta=50)
            # Primer procesamiento de treshhold
            img_to_mod = cv2.adaptiveThreshold(
                img_to_mod, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                cv2.THRESH_BINARY, 11, 2
            )
        # Modificacion a imagenes con brillo adecuado
        # else:
        #     _, img_to_mod = cv2.threshold(
        #         img_to_mod, 125, 255,
        #         cv2.THRESH_BINARY
        #     )

        self.img = img_to_mod
        # Segunda modificacion
        blur = cv2.GaussianBlur(img_to_mod,(5,5),0)
        _, th3 = cv2.threshold(blur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        self.img_mod = th3

    def extraccion_contornos(self):
        pos_maximas = []
        area_l = 0
        img_process = self.img_mod.copy()
        img_original = self.img.copy()
        # Modo 2 de modificacion
        blur = cv2.GaussianBlur(img_original,(5,5),0)
        _, thresh = cv2.threshold(blur,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

        ## Desarrollo de kernel para extraccion de objeto
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7,7))
        dilate = cv2.dilate(thresh, kernel, iterations=1)
        
        ## busqueda de contronos
        cnts = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if len(cnts) == 2 else cnts[1]
        image_number = 0
        for c in cnts:
            x, y, w, h = cv2.boundingRect(c)
            area_temp = w*h
            if area_temp > area_l:
                pos_maximas = [x, y, w, h]
            #cv2.rectangle(img_process, (x, y), (x + w, y + h), (36, 255, 12), 2)
            #ROI = img_process[y:y+h, x:x+w]
            #cv2.imwrite("ROI_{}.png".format(image_number), ROI)
            #image_number += 1
        self.img_mod = self.img_mod[
            pos_maximas[1]: pos_maximas[1] + pos_maximas[3],
            pos_maximas[0]: pos_maximas[0] + pos_maximas[2]
        ]
        self.func_resize(ancho = 262, alto = 212, val_re = False)
        #self.show_img(imagen = self.img_mod, val_objeto = False)

    # funcion para modificacion de tamaño de imagen
    def func_resize(self, ancho: int = 1000, alto: int = 808, val_re = True) -> None:
        if val_re:
            self.img = cv2.resize(self.img, (ancho, alto))
        else:
            self.img_mod = cv2.resize(self.img_mod, (ancho, alto))

    # Seccion de funciones de ficha de identificacion y manipulacion de archivos
    # Creacion de numero de identifiacion
    def crear_identificacion(self):
        # Valor de identificacion
        try:
            num_final = int(self.nombre_img)
        except Exception as e:
            num_final = 100001

        self.id_ = "{}-{}{}-{}".format(
            self.width,
            self.heigth,
            self.tipo_archivo[0].capitalize(),
            num_final
        )

    ## Guardar modificacion de imagen
    def guardar_md(self) -> None:
        try:
            cv2.imwrite(self.ruta, self.img_mod)
        except Exception as e:
            print(e)
    # Destrucctor de la clase que lee la imagen
    def __del__(self):
        pass
    
if __name__ == "__main__":
    print("Objeto imagenes")