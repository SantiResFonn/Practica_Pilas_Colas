
import threading
import time

class Mensaje:
    def __init__(self,contenido: str):
        self.contenido: str = contenido.lower()
        self.prioridad_mensaje: int = self._asignar_prioridad_mensajes()
    def _asignar_prioridad_mensajes(self):
        prioridad = 0
        palabras_clave = {
            "emergencia": 10,
            "urgente": 8,
            "fallo critico": 9,
            "problema": 5,
            "consulta": 2,
            "duda": 1
        }
        
        for palabra, valor in palabras_clave.items():
          prioridad += self.contenido.count(palabra) * valor 
        
        return prioridad
    def __repr__(self):
        return str(self.contenido)

    def __gt__(self, otro: "Mensaje"):
        return self.prioridad_mensaje > otro.prioridad_mensaje  

    def __lt__(self, otro: "Mensaje"):
        return self.prioridad_mensaje < otro.prioridad_mensaje


class EmptyQueue(Exception):
    ...
class PriorityQueue:
    def __init__(self, priority):
        self.queue: list[Mensaje] = []
        self.__priority: str = priority

    def enqueue(self, element: int):
        self.queue.append(element)
        if(self.__priority == "min"):
            self.queue.sort()
        else:
            self.queue.sort(reverse = True)

    def dequeue(self):
        if(len(self.queue) == 0):
            raise EmptyQueue("Cola vacía...")
        return self.queue.pop(0)

    def first(self):
        if(len(self.queue) == 0):
            raise EmptyQueue("Cola vacía...")
        return self.queue[0]

    def __repr__(self):
        return str(self.queue)

class EmptyStack(Exception):
    ...


class Stack:
    def __init__(self):
        self.stack: list[int] = []

    def push(self,data:int):
        self.stack.append(data)
    def pop(self) -> int:
        if len(self.stack) == 0:
            raise EmptyStack("Pila vacia")
        return self.stack.pop()
    def peek(self) -> int:
        if len(self.stack) == 0:
            raise EmptyStack("Pila vacia")
        return self.stack[-1]
    def __repr__(self):
        return str(self.stack)
    def __len__(self):
        return len(self.stack)




class Agente:
    contador = 0
    def __init__(self, id: str,nivel_experiencia: str, solicitudes_acabadas: Stack = Stack()):
        #Clases por atributo
        self.id: str = id
        self.nivel_experiencia: str = nivel_experiencia.lower()
        self.solicitudes_acabadas: Stack = solicitudes_acabadas
        #Clases por instancia
        Agente.contador +=1
        self.nombre_agente = f"Agente-{self.contador}"
        self.estado: str = "disponible"
        self.tiempo_respuesta: float = 0
        self.factor_nivel = self.asignar_factor_nivel()
        self.lock = threading.Lock()
    def asignar_factor_nivel(self):
        if self.nivel_experiencia == "basico":
            self.factor_nivel = 1
        elif self.nivel_experiencia == "intermedio":
            self.factor_nivel = 0.75
        elif self.nivel_experiencia == "experto":
            self.factor_nivel = 0.5
        else:
            self.factor_nivel = 1
        return self.factor_nivel
    def asignar_tiempo_respuesta(self, mensaje: Mensaje):
        tiempo_asignado = (len(mensaje.contenido)/10) + (mensaje.prioridad_mensaje/2)
        self.tiempo_respuesta = tiempo_asignado*self.factor_nivel
        return self.tiempo_respuesta
    def cambiar_estado(self):
        if self.estado == "disponible":
            self.estado = "ocupado"
        else:
            self.estado = "disponible"
    def acabar_solicitud(self,mensaje: Mensaje):
        self.solicitudes_acabadas.push(mensaje)
        self.cambiar_estado()
    def empezar_atencion(self,mensaje: Mensaje):
        with self.lock:
            self.cambiar_estado()
            self.asignar_tiempo_respuesta(mensaje)
            print("\n📞🤝━━━━━━━━━━━━━━━━📞🤝")
            print("     LLAMADA EN PROGRESO     ")
            print(f"    🗣️ El agente está {self.nombre_agente} respondiendo el siguiente mensaje: {mensaje.contenido} ")
            print("📞🤝━━━━━━━━━━━━━━━━📞🤝")
            time.sleep(self.tiempo_respuesta)
            self.acabar_solicitud(mensaje)
            print("\n📴🔚━━━━━━━━━━━━━━━━📴🔚")
            print("     MENSAJE ATENDIDO     ")
            print("   ✅ Gracias por su tiempo")
            print(f"    {self.nombre_agente} esperando el siguiente mensaje.....")
            print("📴🔚━━━━━━━━━━━━━━━━📴🔚")

    def __gt__(self, otro: "Agente"):
        return self.factor_nivel > otro.factor_nivel
    def __lt__(self, otro: "Agente"):
        return self.factor_nivel < otro.factor_nivel

    def __getstate__(self):
        state = self.__dict__.copy()
        del state['lock'] 
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)
        self.lock = threading.Lock()





