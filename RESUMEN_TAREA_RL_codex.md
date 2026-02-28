# Informe: Aprendizaje por Refuerzo (Semaforo Inteligente)

## Objetivo
Comprender el funcionamiento del aprendizaje por refuerzo y explicar su logica con razonamiento propio, tanto a nivel conceptual como practico.

## 1) Investigacion conceptual

### Que es el aprendizaje por refuerzo
El aprendizaje por refuerzo (RL) es un enfoque donde un agente aprende a decidir mediante prueba y error. El agente interactua con un entorno, ejecuta acciones y recibe recompensas o castigos. Con esa experiencia acumulada aprende una estrategia que maximiza beneficio a largo plazo.

A diferencia de otros metodos, no se parte de respuestas etiquetadas correctas para cada situacion. El aprendizaje surge de la interaccion.

### Componentes principales
- Agente: quien toma decisiones (controlador del semaforo).
- Entorno: sistema con el que interactua (interseccion de trafico).
- Estado: descripcion del momento actual (colas en NS y EO, y fase actual).
- Acciones: decisiones posibles (dar verde a NS o dar verde a EO).
- Recompensa: evaluacion numerica de la accion (menos espera = mejor).
- Politica: regla aprendida para elegir accion segun estado.
- Q(s,a): valor esperado de tomar accion a en estado s.

### Diferencia con supervisado y no supervisado
- Supervisado: aprende de datos etiquetados. Es bueno para predecir una etiqueta, no para decidir secuencias de control en tiempo real.
- No supervisado: descubre patrones o grupos en datos sin etiquetas. Sirve para describir, no para controlar.
- Refuerzo: aprende decisiones secuenciales optimizando recompensas. Es ideal para problemas de control dinamico.

## 2) Razonamiento humano

### Situacion real propuesta
Control adaptativo de un semaforo en una interseccion con dos vias principales: Norte-Sur (NS) y Este-Oeste (EO).

### Por que este problema se resuelve con RL
Este problema requiere decisiones continuas donde cada accion afecta el estado siguiente. Si doy verde a NS, baja esa cola pero EO puede crecer. Eso obliga a optimizar a lo largo del tiempo, no solo en un instante.

No es el mejor caso para supervisado porque no hay una etiqueta universal de "accion correcta" para cada estado; depende del trafico cambiante.

No es el mejor caso para no supervisado porque no se busca agrupar estados de trafico, sino elegir acciones para minimizar espera.

RL si es adecuado porque aprende una politica de control directamente desde recompensas del entorno.

### Decisiones que debe aprender el agente
- Mantener verde en NS cuando NS esta mas congestionada.
- Cambiar a verde en EO cuando EO acumula mas cola.
- Evitar cambios de fase innecesarios para no empeorar el flujo.

### Recompensas propuestas
- Penalizacion por cola total (si hay mucha cola, recompensa mas negativa).
- Penalizacion por cambiar de fase (evita cambios bruscos constantes).

Con esta funcion de recompensa el agente aprende equilibrio entre fluidez y estabilidad.

## 3) Ejemplo practico en Python (consola)

Archivo: `aprendizaje_por_refuerzo_codex.py`

### Logica paso a paso
1. Entorno del semaforo:
- Simula llegadas aleatorias de autos.
- Aplica la accion elegida (verde NS o verde EO).
- Descarga autos de la via con luz verde.
- Calcula recompensa segun cola y cambio de fase.

2. Agente Q-learning:
- Guarda tabla Q para estados y acciones.
- Usa epsilon-greedy para balancear exploracion y explotacion.
- Actualiza Q con la ecuacion de Q-learning en cada paso.

3. Entrenamiento:
- Ejecuta muchos episodios.
- Cada episodio suma recompensas y mejora la politica.
- Epsilon baja gradualmente para explorar menos al final.

4. Prueba final:
- Se desactiva exploracion.
- El agente usa solo lo aprendido y se imprime una simulacion en consola.

### Salida esperada
- En entrenamiento: mejora del promedio de recompensas (menos negativo).
- En prueba: decisiones mas coherentes, menor cola total y menos cambios innecesarios.

## 4) Explicacion del resultado

### Interpretacion
Si la recompensa promedio mejora y el sistema mantiene colas mas controladas, hay evidencia de aprendizaje.

### Que aprendio el agente
El agente aprende a priorizar la via mas cargada y a evitar cambios de fase sin beneficio. Ese comportamiento surge de la experiencia con recompensas, no de reglas fijas escritas a mano.

## Conclusiones
- RL es el enfoque correcto para control secuencial en trafico.
- El caso del semaforo demuestra conexion clara entre teoria (agente, entorno, recompensa, politica) y practica (entrenamiento y mejora observable).
- El resultado evidencia aprendizaje real: mejores decisiones en simulacion final.

codex
