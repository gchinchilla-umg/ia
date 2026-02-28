import random
from collections import defaultdict

"""
APRENDIZAJE POR REFUERZO EN CONSOLA: SEMAFORO INTELIGENTE

Agente: controlador del semaforo
Entorno: cruce con dos vias (NS y EO)
Estado: nivel de cola en NS y EO + fase actual
Acciones: 0 = verde NS, 1 = verde EO
Recompensa: penaliza colas largas y cambios de fase innecesarios
"""


class SemaforoEntorno:
    def __init__(self, max_cola=30, capacidad_paso=2, semilla=42):
        self.max_cola = max_cola
        self.capacidad_paso = capacidad_paso
        self.rand = random.Random(semilla)
        self.reset()

    def reset(self):
        self.cola_ns = self.rand.randint(0, 5)
        self.cola_eo = self.rand.randint(0, 5)
        self.fase_actual = self.rand.choice([0, 1])
        return self._estado()

    def _bucket(self, cola):
        if cola <= 2:
            return 0
        if cola <= 5:
            return 1
        if cola <= 9:
            return 2
        if cola <= 14:
            return 3
        if cola <= 20:
            return 4
        return 5

    def _estado(self):
        return (self._bucket(self.cola_ns), self._bucket(self.cola_eo), self.fase_actual)

    def step(self, accion):
        llegan_ns = self.rand.randint(0, 3)
        llegan_eo = self.rand.randint(0, 3)

        self.cola_ns = min(self.max_cola, self.cola_ns + llegan_ns)
        self.cola_eo = min(self.max_cola, self.cola_eo + llegan_eo)

        cambio_fase = 1 if accion != self.fase_actual else 0

        if accion == 0:
            salen = min(self.capacidad_paso, self.cola_ns)
            self.cola_ns -= salen
        else:
            salen = min(self.capacidad_paso, self.cola_eo)
            self.cola_eo -= salen

        self.fase_actual = accion

        cola_total = self.cola_ns + self.cola_eo
        recompensa = -cola_total - (2 * cambio_fase)

        estado_siguiente = self._estado()
        info = {
            "cola_ns": self.cola_ns,
            "cola_eo": self.cola_eo,
            "cola_total": cola_total,
            "cambio_fase": cambio_fase,
        }
        return estado_siguiente, recompensa, info


class AgenteQLearning:
    def __init__(self, alpha=0.12, gamma=0.95, epsilon=0.35, epsilon_min=0.03, epsilon_decay=0.995):
        self.q = defaultdict(lambda: [0.0, 0.0])
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_min = epsilon_min
        self.epsilon_decay = epsilon_decay

    def elegir_accion(self, estado, explorar=True):
        if explorar and random.random() < self.epsilon:
            return random.choice([0, 1])
        q_ns, q_eo = self.q[estado]
        return 0 if q_ns >= q_eo else 1

    def aprender(self, estado, accion, recompensa, estado_siguiente):
        mejor_q_sig = max(self.q[estado_siguiente])
        q_actual = self.q[estado][accion]
        self.q[estado][accion] = q_actual + self.alpha * (
            recompensa + self.gamma * mejor_q_sig - q_actual
        )

    def decaer_exploracion(self):
        self.epsilon = max(self.epsilon_min, self.epsilon * self.epsilon_decay)


def entrenar(episodios=700, pasos_por_episodio=60):
    env = SemaforoEntorno()
    agente = AgenteQLearning()
    historial = []

    print("=" * 72)
    print("ENTRENAMIENTO Q-LEARNING: SEMAFORO INTELIGENTE")
    print("=" * 72)

    for ep in range(1, episodios + 1):
        estado = env.reset()
        recompensa_total = 0

        for _ in range(pasos_por_episodio):
            accion = agente.elegir_accion(estado, explorar=True)
            estado_sig, recompensa, _ = env.step(accion)
            agente.aprender(estado, accion, recompensa, estado_sig)
            recompensa_total += recompensa
            estado = estado_sig

        agente.decaer_exploracion()
        historial.append(recompensa_total)

        if ep % 100 == 0:
            prom = sum(historial[-100:]) / 100
            print(f"Episodio {ep:>3} | Promedio ultimos 100: {prom:>8.2f} | epsilon: {agente.epsilon:.3f}")

    return agente


def mostrar_politica(agente):
    print("\nPOLITICA APRENDIDA (resumen)")
    print("Estado = (bucket_cola_ns, bucket_cola_eo, fase_actual)")
    print("Accion 0: verde NS | Accion 1: verde EO")
    print("-" * 72)

    muestras = [
        (0, 5, 0),
        (5, 0, 1),
        (4, 4, 0),
        (1, 3, 0),
        (3, 1, 1),
    ]

    for estado in muestras:
        q_ns, q_eo = agente.q[estado]
        accion = 0 if q_ns >= q_eo else 1
        nombre = "VERDE NS" if accion == 0 else "VERDE EO"
        print(f"Estado {estado} -> {nombre:8s} | Q_NS={q_ns:8.2f} | Q_EO={q_eo:8.2f}")


def probar(agente, pasos=30):
    env = SemaforoEntorno(semilla=7)
    estado = env.reset()

    print("\nSIMULACION FINAL (sin exploracion)")
    print("-" * 72)
    print(f"{'Paso':>4} | {'Accion':>9} | {'NS':>3} | {'EO':>3} | {'Total':>5} | {'Recompensa':>10}")
    print("-" * 72)

    recompensa_total = 0
    cambios = 0

    for paso in range(1, pasos + 1):
        accion = agente.elegir_accion(estado, explorar=False)
        estado, recompensa, info = env.step(accion)

        nombre = "VERDE NS" if accion == 0 else "VERDE EO"
        recompensa_total += recompensa
        cambios += info["cambio_fase"]

        print(
            f"{paso:>4} | {nombre:>9} | {info['cola_ns']:>3} | {info['cola_eo']:>3} | "
            f"{info['cola_total']:>5} | {recompensa:>10.2f}"
        )

    print("-" * 72)
    print(f"Recompensa total: {recompensa_total:.2f}")
    print(f"Cambios de fase:  {cambios}")
    print(f"Cola final NS:    {env.cola_ns}")
    print(f"Cola final EO:    {env.cola_eo}")


if __name__ == "__main__":
    agente = entrenar(episodios=700, pasos_por_episodio=60)
    mostrar_politica(agente)
    probar(agente, pasos=30)
