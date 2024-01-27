## El siguiente codigo alberga las funciones de lectura e identifiacion de imagenes como objetos ##
# SECCION DE IMPORTE DE LIBRERIAS #
import os
import cv2

# La clase imagen, alberga todas las caracteristicas de una imagen ingresada para el procesamiento #
# Tambien tiene los metodos necesarios del procesamiento de la misma ###############################
class Imgen:
    # Propiedades de la imagen #
    id_: str = "" #Inicial_tipo-anho_ancho_alto_numero-tipo_archivo
    nombre_img: str = ""
    ruta: str = ""
    tipo: str = ""
    width: int = 0
    heigth: int = 0
    score: float = 0.0
    codigo_ref: int = int
    tipo_archivo: str = ""
    # Inicializacion de objeto, con atributos predefinidos #
    def __init__(
            self,
            ruta: str,
            tipo: str = "r"
        ):
        # designacion de valores de identificacion
        self.identificar_archivo(ruta)

        # Propiedades de la imagen
        self.img = None
        self.tipo = tipo

        # Designa los valores de la imagen
        self.lectura_img()

        ## DEsignacion de if
        self.crear_identificacion()

    def identificar_archivo(self, ruta: str):
        if not os.path.isfile(ruta):
            raise ValueError("La ruta ingresada no corresponde a una ruta real.")
        
        # Asignacion de ruta
        self.ruta = ruta
        
        ## Designacion de las propiedades de la imagen seleccionada
        tmp_name: str = str(os.path.basename(ruta))

        # Asignacion de tipo y nombre
        self.nombre_img = tmp_name.split('.')[0]
        self.tipo_archivo = tmp_name.split('.')[1]
        
    def lectura_img(self):
        # Lectura de la imagen
        self.img = cv2.imread(self.ruta, 0)

        # Designacion de valores de tamaño
        temp_values = self.img.shape
        self.heigth = temp_values[0]
        self.width = temp_values[1]


    # Seccion de funciones de interaccion con imagenes
    def show_img(self, imagen = None, nombre_ventana: str = "Imagen"):
        ## Validar si la imagen que se desea mostrar es la actual
        if imagen == None:
            imagen = self.img.copy()
        
        cv2.imshow(nombre_ventana, imagen)
        
        # Cerrar con una tecla 
        while True:
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
        
        # Close the openCV window
        cv2.destroyAllWindows()
    
    # Creacion de numero de identifiacion
    def crear_identificacion(self):
        # Valor de identificacion
        try:
            num_final = int(self.nombre_img)
        except Exception as e:
            num_final = 100001

        self.id_ = "{}-{}{}-{}{}".format(
            self.tipo.capitalize(),
            self.width,
            self.heigth,
            self.tipo_archivo[0].capitalize(),
            num_final
        )
    
if __name__ == "__main__":
    print("Objeto imagenes")