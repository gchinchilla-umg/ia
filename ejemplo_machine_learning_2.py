from sklearn.tree import DecisionTreeClassifier
import numpy as np

print("=== predictor de decision del semaforo metodo supervisado ===\n")

# Cada fila es: [cola_ns, cola_eo, fase_actual]
# fase_actual: 0 = NS en verde, 1 = EO en verde
X_train = np.array([
    [2, 8, 0],
    [3, 7, 0],
    [1, 6, 1],
    [8, 2, 1],
    [7, 3, 1],
    [6, 1, 0],
    [5, 5, 0],
    [4, 6, 0],
    [6, 4, 1],
    [9, 2, 0],
    [2, 9, 1],
    [3, 3, 0],
    [7, 7, 1],
    [10, 4, 0],
    [4, 10, 1],
])

# Etiqueta objetivo:
# 0 = Dar VERDE a NS
# 1 = Dar VERDE a EO
# Dato historico de decisiones de trafico
y_train = np.array([
    1, 1, 1,
    0, 0, 0,
    0, 1, 0,
    0, 1, 0,
    1, 0, 1,
])

modelo = DecisionTreeClassifier(max_depth=4, random_state=42)
modelo.fit(X_train, y_train)

print("Modelo entrenado con datos historicos de trafico.\n")
print("Ingresa el estado actual del cruce:")

cola_ns = int(input("Autos en cola Norte-Sur: "))
cola_eo = int(input("Autos en cola Este-Oeste: "))
fase_actual = int(input("Fase actual (0=NS verde, 1=EO verde): "))

datos_usuario = np.array([[cola_ns, cola_eo, fase_actual]])

prediccion = modelo.predict(datos_usuario)[0]
prob = modelo.predict_proba(datos_usuario)[0]

print("\n" + "=" * 58)
if prediccion == 0:
    print("decision sugerida: verde para norte-sur NS")
    print(f"Confianza: {prob[0] * 100:.1f}%")
else:
    print("decision sugerida: verde para este-oeste eo")
    print(f"Confianza: {prob[1] * 100:.1f}%")
print("=" * 58)

print("\nNota: este ejemplo es aprendizaje supervisado No RL")
