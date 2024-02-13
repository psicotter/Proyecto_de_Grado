"""Modulo que almacena las funciones generales de procesamiento de archivos, listado de archivos y lectura 
de dataframes importantes para agilizar procesos."""

# SECION DE IMPORTE DE LIBRERIAS #
from os import path, listdir, remove
import pandas as pd
from shutil import move

## Seccion de funciones ##
class descriptor_archivos:
    lista_imgs: list = []
    ruta_imgs: str = ""
    ruta_archivo: str = ""
    ruta_sub_dcl: str = ""
    ruta_sub_dem: str = ""
    ruta_sub_norm: str = ""
    dataFrame_values: pd.DataFrame = None
    def __init__(self, ruta_actual: str = "") -> None:
        # Primera ruta - ruta actual de ejecucion
        self.ruta_actual = ruta_actual
        # Incializaicon de rutas de procesamiento
        if not self.init_ruta_arc():
            OSError("La ruta de documentos no existe o no es correcta.")
        if not self.init_ruta_img():
            OSError("La ruta de imagenes no existe o no es correcta.")
        if not self.init_ruta_subs():
            OSError("La ruta de carpetas de clasificacion no existe o no es correcta.")
        ## Lista de imagenes
        self.listar_imagenes()
        self.dataFrame_values = pd.read_excel(
            modificar_rutas(self.ruta_archivo), index_col = None
        )

        ## Orgnaizacion automatica de archivos
        ## self.organizar_archivos()

    def init_ruta_img(self) -> bool:
        ruta_imgs = "/assets/imgs/all_imgs"
        ruta_temp = self.ruta_actual + ruta_imgs
        if path.isdir(ruta_temp):
            self.ruta_imgs = ruta_temp
            return True
        return False
    
    def init_ruta_subs(self) -> bool:
        ruta_subs = "/assets/sub_imgs"
        ruta_temp = self.ruta_actual + ruta_subs
        if path.isdir(ruta_temp):
            self.ruta_sub_dcl = ruta_temp + "/" + "dcl_imgs"
            self.ruta_sub_dem = ruta_temp + "/" + "demencia_imgs"
            self.ruta_sub_norm = ruta_temp + "/" + "normal_imgs"
            return True
        return False
    
    def init_ruta_arc(self) -> bool:
        ruta_docs = "/assets/documents"
        ruta_temp = self.ruta_actual + ruta_docs
        if path.isdir(ruta_temp):
            primer_archivo = [
                ruta_temp + '/' + file for file in listdir(ruta_temp)
            ]
            if len(primer_archivo) < 1:
                return False
            self.ruta_archivo = primer_archivo[0]
            return True
        return False

    def listar_imagenes(self) -> None:
        self.lista_imgs = [
            [
                path.splitext(path.basename(ruta))[0],
                self.ruta_imgs + '/' + ruta
            ]
            for ruta in listdir(self.ruta_imgs)
        ]

    def organizar_archivos(self) -> None:
        # Transformacion de datos
        df_procesamiento = self.dataFrame_values.copy()
        df_procesamiento[df_procesamiento.columns[0]] = df_procesamiento[df_procesamiento.columns[0]].astype(int)
        ## Nueva ruta
        nueva_ruta = ""

        for values in self.lista_imgs:
            value_n = int(values[0])
            df_resultado = df_procesamiento[df_procesamiento.Imagen_id == value_n]
            val_obtenido = df_resultado.DX.values
            if (len(val_obtenido) > 0):
                val_obtenido = val_obtenido[0]
                if val_obtenido == 0:
                    nueva_ruta = modificar_rutas(self.ruta_sub_norm) + "/" + str(value_n) + ".png"
                if val_obtenido == 1:
                    nueva_ruta = modificar_rutas(self.ruta_sub_dcl) + "/" + str(value_n) + ".png"
                if val_obtenido == 2:
                    nueva_ruta = modificar_rutas(self.ruta_sub_dem) + "/" + str(value_n) + ".png"
            
            if not mover_archivos(modificar_rutas(values[1]), nueva_ruta):
                print(f"No fue posible mover el archivo: {values[1]}")


def modificar_rutas(ruta_ingresada: str = "") -> str:
    return ruta_ingresada.replace('\\', '/')

def mover_archivos(ruta_vieja: str = "", ruta_nueva: str = "") -> bool:
    if path.exists(ruta_vieja):
        if path.exists(ruta_nueva):
            remove(ruta_nueva)
        # Mueve el arhivo en caso no existan mas archivos
        move(ruta_vieja, ruta_nueva)
        return True
    return False

## Seccion main ##
if __name__ == "__main__":
    print("Modulo de procesamiento de archivos")