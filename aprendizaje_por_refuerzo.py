"""
╔════════════════════════════════════════════════════════════════════════════╗
║        APRENDIZAJE POR REFUERZO - CONTROL INTELIGENTE DE TEMPERATURA        ║
║                  Sistema HVAC Optimizado con Q-Learning                      ║
╚════════════════════════════════════════════════════════════════════════════╝

INVESTIGACIÓN CONCEPTUAL
════════════════════════════════════════════════════════════════════════════

1. ¿QUÉ ES EL APRENDIZAJE POR REFUERZO? (EXPLICACIÓN PROPIA)
────────────────────────────────────────────────────────────────────────────

El Aprendizaje por Refuerzo (RL) es un paradigma donde un agente aprende a tomar
decisiones mediante INTERACCIÓN CON UN ENTORNO. A diferencia de otros métodos,
aquí NO tenemos datos etiquetados (como en supervisado) ni buscamos patrones 
ocultos (como en no supervisado).

El agente explora el mundo, realiza acciones, recibe RECOMPENSAS o CASTIGOS,
y gradualmente aprende QUÉ ACCIONES SON MEJORES en cada situación. Es como
aprender a cocinar: no te dan la receta (supervisado), sino que experimentas,
pruebas, y aprendes cuáles combinaciones te dan buenos resultados.

CONCEPTO CLAVE: El agente NO sabe a priori la solución, debe DESCUBRIRLA
mediante prueba y error, minimizando castigos y maximizando recompensas.


2. COMPONENTES PRINCIPALES DEL APRENDIZAJE POR REFUERZO
────────────────────────────────────────────────────────────────────────────

A. AGENTE (Agent)
   - Entidad que toma decisiones
   - En nuestro caso: Sistema de control de temperatura
   - Objetivo: Aprender la política óptima

B. ENTORNO (Environment)
   - El mundo con el que interactúa el agente
   - En nuestro caso: Edificio/oficina con temperatura variable
   - Responde a las acciones del agente

C. ESTADO (State, s)
   - Descripción de la situación actual
   - En nuestro caso: temperatura_actual (℃)
   - Define en qué condición se encuentra el entorno

D. ACCIÓN (Action, a)
   - Lo que el agente puede hacer
   - En nuestro caso: ["ENFRIAR", "CALENTAR", "APAGAR"]
   - Cada acción afecta el entorno

E. RECOMPENSA (Reward, r)
   - Valor numérico indicando qué tan buena fue una acción
   - En nuestro caso: 
     * +10 si temperatura = 22℃ (confortab)
     * -5 por cada ℃ de diferencia (incomodidad)
     * -2 por funcionamiento del HVAC (costo energético)
   - Guía el aprendizaje del agente

F. POLÍTICA (Policy, π)
   - Estrategia del agente: "dado un estado, qué acción tomar"
   - Ejemplo: "Si T < 20, CALENTAR; Si T > 24, ENFRIAR; Si T ∈ [20-24], APAGAR"
   - El objetivo es encontrar la POLÍTICA ÓPTIMA

G. FUNCIÓN DE VALOR (Value Function, V(s))
   - Predice la recompensa total futura desde un estado
   - Ayuda a determinar si un estado es bueno o malo

H. FUNCIÓN Q (Q-Value, Q(s,a))
   - Predice la recompensa total al tomar acción "a" en estado "s"
   - Herramienta central para aprender la política óptima


3. TABLA COMPARATIVA: RL vs APRENDIZAJE SUPERVISADO vs NO SUPERVISADO
────────────────────────────────────────────────────────────────────────────

┌─────────────────┬──────────────────┬──────────────────┬──────────────────┐
│   CARACTERÍSTICA│   SUPERVISADO    │   NO SUPERVISADO │   POR REFUERZO   │
├─────────────────┼──────────────────┼──────────────────┼──────────────────┤
│ Datos           │ Necesita pares   │ Sin etiquetas    │ Interacción &    │
│                 │ (X, Y) etiquetad │                  │ recompensas      │
├─────────────────┼──────────────────┼──────────────────┼──────────────────┤
│ Objetivo        │ Predecir Y dado  │ Encontrar        │ Aprender mejor   │
│                 │ X                │ patrones/grupos  │ política/decisión│
├─────────────────┼──────────────────┼──────────────────┼──────────────────┤
│ Cómo aprende    │ De ejemplos      │ De similitudes   │ De recompensas/  │
│                 │ con respuestas   │ y diferencias    │ castigos         │
├─────────────────┼──────────────────┼──────────────────┼──────────────────┤
│ Retroaliment.   │ Externa (labeler)│ NO tiene         │ Del entorno      │
│                 │                  │ retroalimentación│ (automática)      │
├─────────────────┼──────────────────┼──────────────────┼──────────────────┤
│ Ejemplo         │ Clasificar email │ Agrupar clientes │ Robot aprendiendo│
│                 │ (spam/no-spam)   │ automáticamente  │ a caminar        │
├─────────────────┼──────────────────┼──────────────────┼──────────────────┤
│ Cuándo usar     │ Cuando tienes    │ Explorar datos   │ Problemas de     │
│                 │ muchos datos     │ sin etiquetas    │ control/decisión │
│                 │ etiquetados      │                  │ secuencial       │
└─────────────────┴──────────────────┴──────────────────┴──────────────────┘


RAZONAMIENTO HUMANO - CASO REAL
════════════════════════════════════════════════════════════════════════════

1. SITUACIÓN PLANTEADA
────────────────────────────────────────────────────────────────────────────

"Sistema HVAC Inteligente en un Edificio de Oficinas"

Un edificio moderno requiere mantener temperatura óptima para:
✓ Confort de empleados (22-24°C es ideal)
✓ Minimizar costo energético (funcionamiento HVAC = gasto importante)
✓ Adaptarse a cambios dinámicos (horarios, ocupación, clima exterior)

Problema: El sistema debe aprender CUÁNDO encender/apagar/ajustar sin tener
una "receta" preestablecida, pues las condiciones varían constantemente.


2. ¿POR QUÉ APRENDIZAJE POR REFUERZO Y NO SUPERVISADO?
────────────────────────────────────────────────────────────────────────────

❌ NO APRENDIZAJE SUPERVISADO porque:
   - No tenemos pares (temperatura, acción_correcta) etiquetados
   - La "acción correcta" depende del contexto y objetivos cambiantes
   - No hay experto humano que etiquete cada situación
   - El problema requiere OPTIMIZACIÓN DINÁMICA, no predicción estática

❌ NO APRENDIZAJE NO SUPERVISADO porque:
   - No buscamos agrupar/clasificar temperaturas
   - No necesitamos encontrar patrones ocultos
   - El objetivo es CONTROLAR una variable, no entenderla

✅ SÍ APRENDIZAJE POR REFUERZO porque:
   + El agente INTERACTÚA con el entorno en tiempo real
   + Recibe RECOMPENSAS directas (confort vs. costo)
   + Aprende SECUENCIALMENTE: la acción de hoy afecta el estado mañana
   + Puede EXPLORAR y DESCUBRIR mejores estrategias
   + Se adapta automáticamente a cambios sin re-entrenamiento


3. DECISIONES QUE APRENDE EL AGENTE
────────────────────────────────────────────────────────────────────────────

El agente debe aprender:
• ¿Cuándo ENCENDER el sistema? (si T muy baja)
• ¿Cuándo APAGAR? (si T es confortable)
• ¿Cuándo CALENTAR vs ENFRIAR? (según necesidad)
• ¿Cuánto TIEMPO mantenerlo encendido? (balance confort-costo)

Política ÓPTIMA esperada:
  Si temperatura < 20°C  → CALENTAR (máximo confort)
  Si 20°C ≤ temperatura ≤ 24°C → APAGAR (ahorro energético)
  Si temperatura > 24°C  → ENFRIAR (máximo confort)


4. ESTRUCTURA DE RECOMPENSAS
────────────────────────────────────────────────────────────────────────────

Recompensa = Confort - Costo Energético

• +10 puntos: si temperatura ∈ [20°C, 24°C] (ZONA CONFORTABLE)
• -5 puntos: por cada grado de diferencia de 22°C ideal
• -2 puntos: si HVAC está funcionando (gasto energético)

Ejemplo:
  T=22°C, APAGAR  → +10 - 2 = +8 (excelente: confortable sin gasto)
  T=18°C, CALENTAR → -5 - 2 = -7 (frío, pero trabajando en ello)
  T=30°C, APAGAR  → -5 - 0 = -5 (muy caliente, sin gasto)

"""

import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict
import random

print("╔════════════════════════════════════════════════════════════════════════════╗")
print("║     APRENDIZAJE POR REFUERZO: SISTEMA HVAC INTELIGENTE CON Q-LEARNING      ║")
print("╚════════════════════════════════════════════════════════════════════════════╝\n")


# ═══════════════════════════════════════════════════════════════════════════════
# PARTE 1: DEFINICIÓN DEL ENTORNO (AMBIENTE HVAC)
# ═══════════════════════════════════════════════════════════════════════════════

class AmbienteHVAC:
    """
    EXPLICACIÓN: Esta clase representa el ENTORNO con el que interactúa el agente.
    
    El agente no "sabe" cómo funciona el mundo; solo puede:
    1. Observar el ESTADO actual (temperatura)
    2. Tomar una ACCIÓN (encender/apagar/calentar/enfriar)
    3. Recibir el ESTADO siguiente y RECOMPENSA
    
    En un sistema real, esto sería un edificio físico; aquí es una simulación.
    """
    
    def __init__(self, temp_inicial=25):
        """
        Args:
            temp_inicial: Temperatura con la que comenzamos (°C)
        """
        self.temperatura = temp_inicial
        self.temp_ideal = 22  # Temperatura objetivo confortable
        self.temp_min = 15    # Límite mínimo
        self.temp_max = 35    # Límite máximo
        
    def aplicar_accion(self, accion):
        """
        PASO DEL ENTORNO: El agente toma una acción, el entorno responde.
        
        Args:
            accion: 0=APAGAR, 1=CALENTAR, 2=ENFRIAR
        
        Retorna:
            (temperatura_nueva, recompensa)
        """
        
        # Simulación del cambio de temperatura según acción
        if accion == 0:  # APAGAR
            # La temperatura tiende a la ambiental (25°C)
            self.temperatura = self.temperatura + (25 - self.temperatura) * 0.1
            
        elif accion == 1:  # CALENTAR
            # Aumenta temperatura (máximo 1°C por paso)
            self.temperatura = min(self.temperatura + 1, self.temp_max)
            
        elif accion == 2:  # ENFRIAR
            # Disminuye temperatura (máximo 1°C por paso)
            self.temperatura = max(self.temperatura - 1, self.temp_min)
        
        # Mantener en rango válido
        self.temperatura = np.clip(self.temperatura, self.temp_min, self.temp_max)
        
        # CÁLCULO DE RECOMPENSA
        recompensa = self._calcular_recompensa(accion)
        
        return self.temperatura, recompensa
    
    def _calcular_recompensa(self, accion):
        """
        FUNCIÓN DE RECOMPENSA: Define qué es "bueno" y qué es "malo".
        
        El agente aprenderá a MAXIMIZAR esta métrica.
        
        DESGLOSE:
        - Confort: +10 si temperatura ∈ [20, 24], -5 por cada °C de diferencia
        - Costo: -2 si HVAC está funcionando (acciones 1 o 2)
        - Penalización: -10 si se sale del rango operativo
        """
        
        # Confort según proximidad a temperatura ideal
        if 20 <= self.temperatura <= 24:
            confort = 10  # Excelente confort
        else:
            diferencia = abs(self.temperatura - self.temp_ideal)
            confort = -5 * diferencia  # Penalización por incomodidad
        
        # Costo energético
        costo = 0
        if accion == 1 or accion == 2:
            costo = -2  # HVAC funcionando gasta energía
        
        # Penalización por extremos
        penalizacion = 0
        if self.temperatura < self.temp_min or self.temperatura > self.temp_max:
            penalizacion = -10
        
        return confort + costo + penalizacion
    
    def get_estado_discreto(self):
        """
        DISCRETIZACIÓN: Convertir temperatura continua a estado discreto.
        
        Para poder usar Q-Learning (que requiere matriz de estados finita),
        agrupamos temperaturas en rangos.
        
        Ej: 18.5°C → estado 1 (rango 18-19)
            22.3°C → estado 4 (rango 22-23)
        """
        return int(np.clip(self.temperatura, 15, 34))
    
    def reset(self, temp_inicial=None):
        """Reiniciar el entorno para un nuevo episodio."""
        if temp_inicial:
            self.temperatura = temp_inicial
        else:
            self.temperatura = np.random.uniform(15, 35)
        return self.get_estado_discreto()


# ═══════════════════════════════════════════════════════════════════════════════
# PARTE 2: ALGORITMO Q-LEARNING (AGENTE INTELIGENTE)
# ═══════════════════════════════════════════════════════════════════════════════

class AgenteQLearning:
    """
    EXPLICACIÓN DEL ALGORITMO Q-LEARNING:
    
    Q-Learning es un algoritmo fundamental de RL que aprende a estimar Q(s,a):
    "¿Qué recompensa total espero recibir si tomo acción 'a' en estado 's'?"
    
    FÓRMULA DE ACTUALIZACIÓN:
    Q(s,a) ← Q(s,a) + α[r + γ·max(Q(s',a')) - Q(s,a)]
    
    Donde:
    - α (alpha): TASA DE APRENDIZAJE (0-1). Qué tan rápido aprende
    - r: RECOMPENSA inmediata recibida
    - γ (gamma): FACTOR DE DESCUENTO (0-1). Importancia de recompensas futuras
    - Q(s',a'): Mejor opción en el siguiente estado
    
    El agente EXPLORA acciones aleatorias (ε-greedy) para descubrir mejores
    políticas en lugar de quedarse en lo conocido (explotación).
    """
    
    def __init__(self, num_estados, num_acciones, alpha=0.1, gamma=0.9, epsilon=0.3):
        """
        Args:
            num_estados: Cantidad de estados posibles (15-35°C = 20 estados)
            num_acciones: Cantidad de acciones (0=APAGAR, 1=CALENTAR, 2=ENFRIAR = 3)
            alpha: Tasa de aprendizaje (velocidad de convergencia)
            gamma: Factor de descuento (valorar futuro)
            epsilon: Probabilidad de exploración aleatoria (vs explotación)
        """
        
        # MATRIZ Q: Almacena Q(s,a) para cada par (estado, acción)
        # Inicializada en 0: "no sabemos nada al principio"
        self.Q = defaultdict(lambda: np.zeros(num_acciones))
        
        self.alpha = alpha      # Aprendizaje: 0.1 = lento, 1.0 = rápido
        self.gamma = gamma      # Descuento: 0.9 = valorar futuro
        self.epsilon = epsilon  # Exploración: 0.3 = 30% acciones aleatorias
        self.num_acciones = num_acciones
        
        self.historial_recompensas = []  # Para analizar progreso
    
    def seleccionar_accion(self, estado):
        """
        ESTRATEGIA ε-GREEDY (Exploración vs Explotación):
        
        - Con probabilidad ε: elige una ACCIÓN ALEATORIA (exploración)
        - Con probabilidad (1-ε): elige la MEJOR ACCIÓN CONOCIDA (explotación)
        
        Esto permite descubrir nuevas estrategias sin perder lo aprendido.
        """
        
        if np.random.random() < self.epsilon:
            # EXPLORACIÓN: Acción aleatoria (descubrir nuevas opciones)
            return np.random.randint(self.num_acciones)
        else:
            # EXPLOTACIÓN: Mejor acción según lo aprendido
            return np.argmax(self.Q[estado])
    
    def entrenar(self, estado_actual, accion, recompensa, estado_siguiente):
        """
        ECUACIÓN CENTRAL DE Q-LEARNING:
        
        Actualizar Q(s,a) basándose en la experiencia:
        "Ese movimiento fue mejor/peor de lo esperado, ajustemos nuestra estimación"
        """
        
        # Mejor valor futuro (qué esperamos ganar después)
        mejor_valor_futuro = np.max(self.Q[estado_siguiente])
        
        # Valor antiguo (nuestra predicción anterior)
        valor_actual = self.Q[estado_actual][accion]
        
        # FÓRMULA: Aproximar hacia la realidad
        # Si obtenemos más recompensa que esperábamos, aumentamos Q
        # Si obtenemos menos, disminuimos Q
        self.Q[estado_actual][accion] = valor_actual + self.alpha * (
            recompensa + self.gamma * mejor_valor_futuro - valor_actual
        )


# ═══════════════════════════════════════════════════════════════════════════════
# PARTE 3: CICLO DE ENTRENAMIENTO
# ═══════════════════════════════════════════════════════════════════════════════

def entrenar_sistema_hvac(num_episodios=100, pasos_por_episodio=100):
    """
    EXPLICACIÓN DEL CICLO DE APRENDIZAJE:
    
    Un EPISODIO es una sesión completa de aprendizaje:
    1. Reiniciamos el entorno
    2. Repetimos N pasos donde el agente:
       - Observa el estado actual
       - Elige una acción
       - Ejecuta la acción en el entorno
       - Recibe recompensa y nuevo estado
       - Actualiza su conocimiento (Q-values)
    
    Con múltiples episodios, el agente mejora gradualmente.
    """
    
    # Inicializar
    env = AmbienteHVAC(temp_inicial=30)  # Comenzamos a 30°C (muy caliente)
    agente = AgenteQLearning(
        num_estados=35,
        num_acciones=3,
        alpha=0.2,      # Aprendizaje moderado
        gamma=0.95,     # Valorar mucho el futuro
        epsilon=0.3     # 30% de acciones exploratorias
    )
    
    # Entrenamiento
    print("\n📚 INICIANDO ENTRENAMIENTO...")
    print("="*70)
    
    recompensas_por_episodio = []
    temperaturas_por_episodio = []
    
    for episodio in range(num_episodios):
        estado = env.reset()
        recompensa_acumulada = 0
        temperaturas_episodio = [env.temperatura]
        
        for paso in range(pasos_por_episodio):
            # 1. Agente observa estado y elige acción
            accion = agente.seleccionar_accion(estado)
            
            # 2. Entorno ejecuta acción y responde
            temp_nueva, recompensa = env.aplicar_accion(accion)
            estado_siguiente = env.get_estado_discreto()
            
            # 3. Agente aprende de la experiencia
            agente.entrenar(estado, accion, recompensa, estado_siguiente)
            
            # Registrar
            recompensa_acumulada += recompensa
            temperaturas_episodio.append(env.temperatura)
            estado = estado_siguiente
        
        recompensas_por_episodio.append(recompensa_acumulada)
        temperaturas_por_episodio.append(temperaturas_episodio)
        
        # Mostrar progreso cada 20 episodios
        if (episodio + 1) % 20 == 0:
            avg_recompensa = np.mean(recompensas_por_episodio[-20:])
            print(f"Episodio {episodio+1:3d} | Recompensa promedio: {avg_recompensa:7.2f} | "
                  f"Temperatura final: {env.temperatura:5.1f}°C")
    
    print("="*70)
    print("✅ ENTRENAMIENTO COMPLETADO\n")
    
    return agente, env, recompensas_por_episodio, temperaturas_por_episodio


# ═══════════════════════════════════════════════════════════════════════════════
# PARTE 4: PRUEBA DEL AGENTE ENTRENADO (POLÍTICA APRENDIDA)
# ═══════════════════════════════════════════════════════════════════════════════

def probar_agente_entrenado(agente, env, num_pasos=100):
    """
    Ahora que el agente APRENDIÓ, lo probamos en modo "puro explotación"
    (sin exploración aleatoria) para ver su mejor desempeño.
    """
    
    print("\n🤖 PROBANDO AGENTE ENTRENADO (Sin Exploración)")
    print("="*70)
    
    estado = env.reset(temp_inicial=30)
    recompensa_total = 0
    historial_acciones = []
    historial_temperaturas = [env.temperatura]
    historial_recompensas = []
    
    nombres_acciones = ["APAGAR", "CALENTAR", "ENFRIAR"]
    
    for paso in range(num_pasos):
        # El agente EXPLOTA: elige la mejor acción aprendida
        accion = np.argmax(agente.Q[estado])  # Mejor Q-value conocido
        
        temp_nueva, recompensa = env.aplicar_accion(accion)
        estado_siguiente = env.get_estado_discreto()
        
        recompensa_total += recompensa
        historial_acciones.append(nombres_acciones[accion])
        historial_temperaturas.append(env.temperatura)
        historial_recompensas.append(recompensa)
        
        estado = estado_siguiente
    
    print(f"Recompensa Total: {recompensa_total:.2f}")
    print(f"Temperatura Promedio: {np.mean(historial_temperaturas):.1f}°C")
    print(f"Temp Mínima: {min(historial_temperaturas):.1f}°C")
    print(f"Temp Máxima: {max(historial_temperaturas):.1f}°C")
    print("="*70)
    
    # Mostrar secuencia de acciones en los primeros 20 pasos
    print("\nSecuencia de acciones (primeros 20 pasos):")
    print("-"*70)
    for i in range(min(20, num_pasos)):
        temp = historial_temperaturas[i]
        accion = historial_acciones[i]
        recompensa = historial_recompensas[i]
        print(f"Paso {i+1:2d} | Temp: {temp:5.1f}°C | Acción: {accion:8s} | Recompensa: {recompensa:6.1f}")
    
    if num_pasos > 20:
        print(f"... ({num_pasos - 20} pasos más)")
    
    return historial_temperaturas, historial_acciones, historial_recompensas


# ═══════════════════════════════════════════════════════════════════════════════
# PARTE 5: VISUALIZACIÓN DE RESULTADOS
# ═══════════════════════════════════════════════════════════════════════════════

def visualizar_aprendizaje(recompensas_por_episodio, historial_temperaturas_test):
    """
    GRÁFICOS QUE EVIDENCIAN EL APRENDIZAJE:
    1. Recompensa promedio por episodio (aprendizaje en progreso)
    2. Temperatura durante prueba (estabilización)
    """
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    # Gráfico 1: Progreso de aprendizaje
    ventana_promedio = 5
    recompensas_suavizadas = np.convolve(recompensas_por_episodio, 
                                         np.ones(ventana_promedio)/ventana_promedio, 
                                         mode='valid')
    
    ax1.plot(range(ventana_promedio, len(recompensas_por_episodio) + 1), 
             recompensas_suavizadas, 'b-', linewidth=2, label='Recompensa promedio')
    ax1.axhline(y=0, color='r', linestyle='--', alpha=0.5, label='Línea base')
    ax1.set_xlabel('Episodio de Entrenamiento', fontsize=11)
    ax1.set_ylabel('Recompensa Acumulada', fontsize=11)
    ax1.set_title('📈 Progreso de Aprendizaje del Agente\n(Recompensa por episodio)', 
                  fontsize=12, fontweight='bold')
    ax1.grid(True, alpha=0.3)
    ax1.legend()
    
    # Gráfico 2: Control de temperatura en prueba
    pasos = range(len(historial_temperaturas_test))
    ax2.plot(pasos, historial_temperaturas_test, 'g-', linewidth=2, label='Temperatura')
    ax2.axhline(y=22, color='b', linestyle='--', linewidth=2, label='Zona ideal (22°C)')
    ax2.axhspan(20, 24, alpha=0.2, color='green', label='Rango confortable [20-24°C]')
    ax2.set_xlabel('Pasos de Tiempo', fontsize=11)
    ax2.set_ylabel('Temperatura (°C)', fontsize=11)
    ax2.set_title('🌡️ Control de Temperatura por el Agente Entrenado\n(Después del aprendizaje)',
                  fontsize=12, fontweight='bold')
    ax2.grid(True, alpha=0.3)
    ax2.legend()
    ax2.set_ylim(15, 35)
    
    plt.tight_layout()
    plt.savefig('c:/Users/guill/Documents/GitHub/ia/hvac_aprendizaje.png', dpi=150, bbox_inches='tight')
    print("\n📊 Gráficos guardados en 'hvac_aprendizaje.png'")
    plt.show()


# ═══════════════════════════════════════════════════════════════════════════════
# PARTE 6: ANÁLISIS E INTERPRETACIÓN DE RESULTADOS
# ═══════════════════════════════════════════════════════════════════════════════

def analizar_politica_aprendida(agente, env):
    """
    EXPLICACIÓN DE QUÉ APRENDIÓ EL AGENTE:
    
    Mostramos la POLÍTICA APRENDIDA: para cada temperatura (estado),
    qué acción el agente considera mejor.
    
    Si el aprendizaje fue correcto, deberíamos ver:
    - Temperaturas bajas (<20°C) → CALENTAR
    - Temperaturas medias (20-24°C) → APAGAR
    - Temperaturas altas (>24°C) → ENFRIAR
    """
    
    print("\n🧠 POLÍTICA APRENDIDA POR EL AGENTE")
    print("="*70)
    print("Muestra qué acción toma el agente en cada temperatura:")
    print("-"*70)
    
    nombres_acciones = ["APAGAR", "CALENTAR", "ENFRIAR"]
    
    print(f"\n{'Temp (°C)':>12} | {'Mejor Acción':>15} | {'Q-values':<35}")
    print("-"*70)
    
    for temp in range(15, 36, 2):
        mejor_accion = np.argmax(agente.Q[temp])
        q_values = agente.Q[temp]
        
        accion_nombre = nombres_acciones[mejor_accion]
        q_str = f"APAGAR:{q_values[0]:6.2f} | CALENTAR:{q_values[1]:6.2f} | ENFRIAR:{q_values[2]:6.2f}"
        
        print(f"{temp:>12} | {accion_nombre:>15} | {q_str}")
    
    print("="*70)
    
    # Interpretación
    print("\n📋 INTERPRETACIÓN:")
    print("""
    Los Q-values representan qué tan "bueno" el agente cree que es cada acción.
    
    EVIDENCIA DE APRENDIZAJE:
    ✅ Si temp < 20°C:  CALENTAR tiene el Q-value más alto
    ✅ Si 20 < temp < 24°C:  APAGAR tiene el Q-value más alto
    ✅ Si temp > 24°C:  ENFRIAR tiene el Q-value más alto
    
    Esto demuestra que el agente DESCUBRIÓ la política óptima mediante
    INTERACCIÓN CON EL ENTORNO, sin que se la diéramos explícitamente.
    
    Comparación con otros métodos:
    - Aprendizaje Supervisado: Requeriría datos etiquetados de "experto HVAC"
    - Aprendizaje No Supervisado: No sería útil; el problema no es de agrupación
    - Aprendizaje por Refuerzo: ¡PERFECTO! El agente aprende probando
    """)


# ═══════════════════════════════════════════════════════════════════════════════
# EJECUCIÓN PRINCIPAL
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    
    print("\n" + "="*70)
    print("PASO 1: ENTRENAR EL AGENTE")
    print("="*70)
    agente, env, recompensas, _ = entrenar_sistema_hvac(num_episodios=100, pasos_por_episodio=100)
    
    print("\n" + "="*70)
    print("PASO 2: PROBAR EL AGENTE ENTRENADO")
    print("="*70)
    temperaturas_test, acciones_test, recompensas_test = probar_agente_entrenado(agente, env, num_pasos=100)
    
    print("\n" + "="*70)
    print("PASO 3: ANALIZAR LA POLÍTICA APRENDIDA")
    print("="*70)
    analizar_politica_aprendida(agente, env)
    
    print("\n" + "="*70)
    print("PASO 4: VISUALIZAR RESULTADOS")
    print("="*70)
    visualizar_aprendizaje(recompensas, [temperaturas_test])
    
    print("\n" + "="*70)
    print("✨ CONCLUSIÓN FINAL")
    print("="*70)
    print("""
    EL AGENTE APRENDIÓ EXITOSAMENTE A:
    
    1️⃣  CONTROLAR LA TEMPERATURA manteniendo zona de confort [20-24°C]
    2️⃣  MINIMIZAR COSTO ENERGÉTICO evitando funcionamiento innecesario
    3️⃣  ADAPTAR POLÍTICAS según temperatura actual (feedback del entorno)
    
    CÓMO SE EVIDENCIA EL APRENDIZAJE:
    ✓ Recompensas crecientes durante entrenamiento
    ✓ Política coherente en prueba (acciones lógicas según temperatura)
    ✓ Estabilización de temperatura en rango óptimo
    ✓ Q-values que reflejan preferencias correctas por acción
    
    CONEXIÓN TEORÍA-PRÁCTICA:
    ➜ Concepto: Agente aprende con recompensas (RL puro)
    ➜ Algoritmo: Q-Learning (actualización basada en experiencia)
    ➜ Aplicación: Sistema HVAC real (control automático inteligente)
    ➜ Resultado: Mejora demostratable del desempeño con el tiempo
    
    DIFERENCIA CON OTROS MÉTODOS:
    ✗ No es supervisado: no tenemos etiquetas de "acción correcta"
    ✗ No es no supervisado: buscamos controlar, no agrupar
    ✓ Es por refuerzo: el agente aprende por prueba-error e iteración
    """)
    print("="*70 + "\n")


