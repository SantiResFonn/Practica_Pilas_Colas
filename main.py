from Thread import SistemaAtencion
import random

if __name__ == "__main__":
    sistema =  SistemaAtencion()

    palabras_clave = {
        "emergencia": 10,
        "urgente": 8,
        "fallo critico": 9,
        "problema": 5,
        "consulta": 2,
        "duda": 1
    }

    palabras_lista = list(palabras_clave.keys())

    for i in range(40):
        mensaje = " ".join(random.choices(palabras_lista, k=10))  
        sistema.agregar_mensaje(mensaje)
    
    sistema.hilo()