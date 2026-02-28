"""
APRENDIZAJE POR REFUERZO: SEMAFORO INTELIGENTE (RL vs SUPERVISADO)

Este archivo CONVIERTE el enfoque supervisado (ejemplo_machine_learning_2.py)
a un enfoque por REFUERZO que cumple completamente con los requisitos de RL.

Componentes RL implementados:
- Agente: AgenteQLearning
- Entorno: SemaforoEntorno (simulación interactiva)
- Estado: (cola_ns, cola_eo, fase_actual)
- Acciones: 0=Verde NS, 1=Verde EO
- Recompensa: -cola_total - (2 * cambio_fase)
- Política: Tabla Q aprendida por Q-Learning
"""

import random
from collections import defaultdict

# ==============================================================================
# CLASE 1: ENTORNO DEL SEMAFORO (Simulación interactiva)
# ==============================================================================

class SemaforoEntorno:
    """
    Simula una intersección de tráfico con dos vías: Norte-Sur (NS) y Este-Oeste (EO).
    
    El agente interactúa con este entorno para aprender qué decisión tomar
    en cada estado (situación de tráfico).
    """
    
    def __init__(self, max_cola=30, capacidad_paso=2, semilla=42):
        """
        max_cola: número máximo de autos permitidos en una cola
        capacidad_paso: autos que pueden pasar por fase de verde (2 autos/5 segundos)
        semilla: para reproducibilidad de la simulación
        """
        self.max_cola = max_cola
        self.capacidad_paso = capacidad_paso
        self.rand = random.Random(semilla)
        self.reset()
    
    def reset(self):
        """Reinicia el entorno para un nuevo episodio"""
        self.cola_ns = self.rand.randint(0, 5)
        self.cola_eo = self.rand.randint(0, 5)
        self.fase_actual = self.rand.choice([0, 1])
        return self._estado()
    
    def _bucket(self, cola):
        """
        Discretiza la cola continua en 6 categorías (buckets).
        Esto reduce el espacio de estados para que sea manejable.
        
        Simulación real: colas 0-30
        Estados abstractos: 0-5 (representando rangos)
        """
        if cola <= 2:
            return 0   # Muy pocos autos
        if cola <= 5:
            return 1   # Pocos autos
        if cola <= 9:
            return 2   # Moderados
        if cola <= 14:
            return 3   # Muchos
        if cola <= 20:
            return 4   # Muchos autos
        return 5       # Máximo congestionamiento
    
    def _estado(self):
        """Retorna el estado actual como tupla (bucket_ns, bucket_eo, fase_actual)"""
        return (self._bucket(self.cola_ns), self._bucket(self.cola_eo), self.fase_actual)
    
    def step(self, accion):
        """
        Ejecuta una acción en el entorno y retorna:
        - estado_siguiente: nuevo estado
        - recompensa: evaluación numérica de la acción
        - info: información adicional para debugging
        
        FLUJO DEL PASO:
        1. Llegan nuevos autos aleatoriamente
        2. Se aplica la acción (verde NS o EO)
        3. Se descarga la cola correspondiente
        4. Se calcula recompensa por cola y cambio de fase
        """
        
        # 1. ARRIBO: Nuevos autos llegan aleatoriamente (0-3 por fase)
        llegan_ns = self.rand.randint(0, 3)
        llegan_eo = self.rand.randint(0, 3)
        
        self.cola_ns = min(self.max_cola, self.cola_ns + llegan_ns)
        self.cola_eo = min(self.max_cola, self.cola_eo + llegan_eo)
        
        # 2. CAMBIO DE FASE: ¿Se cambió el semáforo?
        cambio_fase = 1 if accion != self.fase_actual else 0
        
        # 3. DESCARGA: Los autos pasan según dónde está el verde
        if accion == 0:  # Verde NS
            salen = min(self.capacidad_paso, self.cola_ns)
            self.cola_ns -= salen
        else:  # Verde EO
            salen = min(self.capacidad_paso, self.cola_eo)
            self.cola_eo -= salen
        
        self.fase_actual = accion
        
        # 4. RECOMPENSA: Penaliza cola total y cambios innecesarios
        cola_total = self.cola_ns + self.cola_eo
        # Recompensa negativa (el agente aprende a MINIMIZAR esta cantidad)
        recompensa = -cola_total - (2 * cambio_fase)
        
        estado_siguiente = self._estado()
        info = {
            "cola_ns": self.cola_ns,
            "cola_eo": self.cola_eo,
            "cola_total": cola_total,
            "cambio_fase": cambio_fase,
        }
        return estado_siguiente, recompensa, info


# ==============================================================================
# CLASE 2: AGENTE Q-LEARNING (Aprende mediante prueba y error)
# ==============================================================================

class AgenteQLearning:
    """
    Implementa el algoritmo Q-Learning.
    
    Mantiene una tabla Q(estado, acción) que estima el valor de tomar
    cada acción en cada estado. Aprende actualizando estos valores
    según las recompensas observadas.
    """
    
    def __init__(self, alpha=0.15, gamma=0.95, epsilon=0.40, epsilon_min=0.05, epsilon_decay=0.99):
        """
        alpha: tasa de aprendizaje (0-1). Qué tan rápido aprende de nuevas experiencias
        gamma: factor de descuento (0-1). Importancia de recompensas futuras
        epsilon: tasa de exploración inicial. Probabilidad de acción aleatoria
        epsilon_min: mínimo de exploración (para evitar perder política buena)
        epsilon_decay: cómo baja epsilon después de cada episodio
        """
        # Tabla Q: {estado: [Q_valor_accion_0, Q_valor_accion_1]}
        # Inicialmente todos los valores son 0.0
        self.q = defaultdict(lambda: [0.0, 0.0])
        
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_min = epsilon_min
        self.epsilon_decay = epsilon_decay
    
    def elegir_accion(self, estado, explorar=True):
        """
        EPSILON-GREEDY: Balance exploración vs explotación
        
        - Con probabilidad epsilon: acción aleatoria (EXPLORAR)
        - Con probabilidad (1-epsilon): mejor acción según Q (EXPLOTAR)
        
        Esto es CLAVE en RL: si solo explotamos, nos atrapamos en soluciones locales.
        Si solo exploramos, no usamos lo aprendido.
        """
        if explorar and random.random() < self.epsilon:
            # Explorar: acción aleatoria
            return random.choice([0, 1])
        else:
            # Explotar: mejor acción según tabla Q
            q_ns, q_eo = self.q[estado]
            # Si Q_NS >= Q_EO, elige NS; sino, elige EO
            return 0 if q_ns >= q_eo else 1
    
    def aprender(self, estado, accion, recompensa, estado_siguiente):
        """
        ECUACIÓN DE Q-LEARNING (Bellman):
        
        Q(s, a) = Q(s, a) + α * [r + γ * max(Q(s', a')) - Q(s, a)]
        
        Donde:
        - Q(s, a): valor actual de la acción en el estado
        - r: recompensa observada
        - γ * max(Q(s', a')): valor estimado del estado siguiente
        - α: qué tan rápido actualiza
        
        Esta ecuación es el corazón del aprendizaje por refuerzo.
        """
        # Mejor valor esperado del estado siguiente
        mejor_q_sig = max(self.q[estado_siguiente])
        
        # Valor actual de Q
        q_actual = self.q[estado][accion]
        
        # ACTUALIZAR Q con la ecuación de Bellman
        self.q[estado][accion] = q_actual + self.alpha * (
            recompensa + self.gamma * mejor_q_sig - q_actual
        )
    
    def decaer_exploracion(self):
        """
        Reduce epsilon después de cada episodio.
        Esto hace que el agente explore menos conforme aprende más.
        """
        self.epsilon = max(self.epsilon_min, self.epsilon * self.epsilon_decay)


# ==============================================================================
# FUNCIÓN 1: ENTRENAR AL AGENTE
# ==============================================================================

def entrenar(episodios=300, pasos_por_episodio=60):
    """
    FASE DE ENTRENAMIENTO (APRENDIZAJE POR REFUERZO)
    
    El agente interactúa con el entorno durante múltiples episodios,
    acumulando experiencia y mejorando su política.
    
    Esto es DIFERENTE a supervisado: no hay etiquetas predefinidas,
    el agente aprende de las recompensas del entorno.
    """
    env = SemaforoEntorno()
    agente = AgenteQLearning()
    historial = []
    
    print("=" * 80)
    print("ENTRENAMIENTO: APRENDIZAJE POR REFUERZO (Q-LEARNING)")
    print("=" * 80)
    print("El agente aprende a controlar el semáforo mediante prueba y error.\n")
    
    for ep in range(1, episodios + 1):
        # Nuevo episodio
        estado = env.reset()
        recompensa_total = 0
        
        # 60 pasos por episodio (5 minutos de simulación)
        for paso in range(pasos_por_episodio):
            # 1. Agente elige acción (con probabilidad epsilon de explorar)
            accion = agente.elegir_accion(estado, explorar=True)
            
            # 2. Entorno ejecuta la acción y retorna siguiente estado + recompensa
            estado_sig, recompensa, _ = env.step(accion)
            
            # 3. Agente APRENDE de la experiencia (actualiza tabla Q)
            agente.aprender(estado, accion, recompensa, estado_sig)
            
            # 4. Acumular recompensa del episodio
            recompensa_total += recompensa
            estado = estado_sig
        
        # Después de cada episodio, explorar menos
        agente.decaer_exploracion()
        historial.append(recompensa_total)
        
        # Mostrar progreso cada 50 episodios
        if ep % 50 == 0:
            prom = sum(historial[-50:]) / 50
            print(f"Episodio {ep:>3} | Recompensa promedio (últimos 50): {prom:>8.2f} | "
                  f"ε={agente.epsilon:.3f}")
    
    print("\n" + "=" * 80)
    print("ENTRENAMIENTO COMPLETADO")
    print("El agente ha aprendido una política mediante prueba y error.")
    print("=" * 80 + "\n")
    
    return agente


# ==============================================================================
# FUNCIÓN 2: MOSTRAR LA POLÍTICA APRENDIDA
# ==============================================================================

def mostrar_politica(agente):
    """
    Muestra ejemplos de la política que aprendió el agente.
    
    La política es el resultado del aprendizaje: qué acción tomar en cada estado.
    
    En supervisado: la "política" sería las etiquetas predefinidas (y_train).
    En RL: la política es lo que el agente APRENDIÓ de la interacción.
    """
    print("=" * 80)
    print("POLÍTICA APRENDIDA (Ejemplos de decisiones)")
    print("=" * 80)
    print("Estado = (cola_ns_bucket, cola_eo_bucket, fase_actual)")
    print("Acción 0 = Verde NS | Acción 1 = Verde EO\n")
    
    # Mostrar algunos ejemplos de la tabla Q aprendida
    ejemplos = [
        (0, 5, 0),  # Pocas autos en NS, muchos en EO, fase actual NS
        (5, 0, 1),  # Muchos autos en NS, pocos en EO, fase actual EO
        (4, 4, 0),  # Muchos en ambos, fase NS
        (1, 3, 0),  # Pocos en NS, moderados en EO
        (3, 1, 1),  # Moderados en NS, pocos en EO, fase EO
    ]
    
    for estado in ejemplos:
        q_ns, q_eo = agente.q[estado]
        accion = 0 if q_ns >= q_eo else 1
        nombre = "VERDE NS" if accion == 0 else "VERDE EO"
        print(f"Estado {estado} → {nombre:>8} | Q(NS)={q_ns:>7.2f} | Q(EO)={q_eo:>7.2f}")
    
    print("\n" + "=" * 80 + "\n")


# ==============================================================================
# FUNCIÓN 3: PROBAR LA POLÍTICA APRENDIDA
# ==============================================================================

def probar(agente, pasos=40):
    """
    FASE DE PRUEBA
    
    El agente ejecuta su política aprendida (sin exploración) para demostrar
    cómo controla el semáforo en tiempo real.
    
    En supervisado: predice una sola vez con datos del usuario.
    En RL: simula múltiples pasos para evaluar la calidad de la política.
    """
    env = SemaforoEntorno(semilla=7)
    estado = env.reset()
    
    print("=" * 100)
    print("SIMULACIÓN FINAL: El agente usa su política aprendida (SIN exploración aleatoria)")
    print("=" * 100)
    print(f"{'Paso':>4} | {'Acción':>10} | {'Cola NS':>8} | {'Cola EO':>8} | "
          f"{'Cola Total':>11} | {'Recompensa':>11}")
    print("-" * 100)
    
    recompensa_total = 0
    cambios_fase = 0
    
    for paso in range(1, pasos + 1):
        # Agente elige MEJOR acción (sin exploración)
        accion = agente.elegir_accion(estado, explorar=False)
        estado, recompensa, info = env.step(accion)
        
        nombre = "VERDE NS" if accion == 0 else "VERDE EO"
        recompensa_total += recompensa
        cambios_fase += info["cambio_fase"]
        
        print(f"{paso:>4} | {nombre:>10} | {info['cola_ns']:>8} | {info['cola_eo']:>8} | "
              f"{info['cola_total']:>11} | {recompensa:>11.2f}")
    
    print("-" * 100)
    print(f"Recompensa total:     {recompensa_total:>8.2f}")
    print(f"Cambios de fase:      {cambios_fase:>8}")
    print(f"Cola final NS:        {env.cola_ns:>8}")
    print(f"Cola final EO:        {env.cola_eo:>8}")
    print("=" * 100 + "\n")


# ==============================================================================
# FUNCIÓN 4: COMPARACIÓN CON SUPERVISADO
# ==============================================================================

def mostrar_diferencias():
    """Muestra las diferencias conceptuales entre este enfoque y el supervisado"""
    print("=" * 80)
    print("COMPARACIÓN: SUPERVISADO vs REFUERZO")
    print("=" * 80)
    print(f"{'Aspecto':<25} | {'Supervisado (ML2)':<30} | {'Refuerzo (ML3)':<30}")
    print("-" * 80)
    print(f"{'Datos':<25} | {'Historiales + etiquetas':<30} | {'Interacción con entorno':<30}")
    print(f"{'Algoritmo':<25} | {'Árbol de Decisión':<30} | {'Q-Learning':<30}")
    print(f"{'Aprendizaje':<25} | {'Una sola pasada':<30} | {'Múltiples episodios':<30}")
    print(f"{'Recompensa':<25} | {'No existe':<30} | {'Dinámica del entorno':<30}")
    print(f"{'Política':<25} | {'Predefinida en datos':<30} | {'Aprendida por RL':<30}")
    print(f"{'Decisión final':<25} | {'Predicción estática':<30} | {'Política optimizada':<30}")
    print("=" * 80 + "\n")


# ==============================================================================
# MAIN: EJECUTAR ENTRENAMIENTO Y PRUEBA
# ==============================================================================

if __name__ == "__main__":
    print("\n")
    print("╔" + "=" * 78 + "╗")
    print("║" + " SEMÁFORO INTELIGENTE: APRENDIZAJE POR REFUERZO ".center(78) + "║")
    print("║" + " (Conversión de Supervisado a RL - ejemplo_machine_learning_3.py ".center(78) + "║")
    print("╚" + "=" * 78 + "╝")
    print("\n")
    
    # 1. Mostrar diferencias
    mostrar_diferencias()
    
    # 2. ENTRENAR al agente
    agente = entrenar(episodios=300, pasos_por_episodio=60)
    
    # 3. Mostrar política aprendida
    mostrar_politica(agente)
    
    # 4. Ejecutar simulación final
    probar(agente, pasos=40)
    
    print("✅ CONCLUSIÓN:")
    print("   - El agente APRENDIÓ a controlar el semáforo mediante prueba y error")
    print("   - No usamos etiquetas predefinidas como en supervisado")
    print("   - La política surge de la INTERACCIÓN con el entorno")
    print("   - Esto es APRENDIZAJE POR REFUERZO (RL)")
    print("\n")
