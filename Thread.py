import threading
import Logic
import time
import pickle


class SistemaAtencion:

    def __init__(self):
        self.cargar_datos()
    
    def cargar_datos(self):
        with open("mensajes.pkl", "rb") as file:
            self.mensajes = pickle.load(file)
        with open("agentes.pkl", "rb") as file:
            self.agentes = pickle.load(file)
    
    def agregar_mensaje(self, mensaje: str):
        mensaje_nuevo = Logic.Mensaje(mensaje)
        self.mensajes.enqueue(mensaje_nuevo)
        with open("mensajes.pkl", "wb") as file:
            pickle.dump(self.mensajes, file)

    def agregar_agente(self, id: str, nivel_de_experiencia: str):
        agente_nuevo = Logic.Agente(id, nivel_de_experiencia)
        self.agentes.enqueue(agente_nuevo)
        with open("agentes.pkl", "wb") as file:
            pickle.dump(self.agentes, file)

    def empezar_trabajo(self):
        while len(self.mensajes.queue) != 0:
            for agente in self.agentes.queue:
                if agente.estado == "disponible" and len(self.mensajes.queue) != 0:
                    mensaje = self.mensajes.dequeue()
                    threading.Thread(target=agente.empezar_atencion, args=(mensaje,)).start()
                    time.sleep(1)

    def hilo(self):
        print("📞📲━━━━━━━━━━━━━━━📞📲")
        print("      BIENVENIDO AL     ")
        print("    📞 GESTOR DE MENSAJES 📞")
        print("📞📲━━━━━━━━━━━━━━━📞📲")
        print("\n☎️ Esperando Mensajes...")
        iniciar_hilo = threading.Thread(target=self.empezar_trabajo)
        iniciar_hilo.start()
        iniciar_hilo.join()

