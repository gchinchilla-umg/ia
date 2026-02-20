from sklearn.tree import DecisionTreeClassifier
import numpy as np

print("=== PREDICTOR DE ADMISIÓN UNIVERSITARIA ===\n")

# Datos de entrenamiento (ejemplos históricos)
# [promedio, horas_estudio_semanal, actividades_extracurriculares]
X_train = np.array([
    [85, 10, 2],
    [90, 15, 3],
    [70, 5, 1],
    [95, 20, 4],
    [60, 3, 0],
    [88, 12, 2],
    [75, 8, 1],
    [92, 18, 3],
    [65, 4, 1],
    [98, 22, 5]
])

# Etiquetas: 1 = Admitido, 0 = No admitido
y_train = np.array([1, 1, 0, 1, 0, 1, 0, 1, 0, 1])

# Entrenar el modelo
modelo = DecisionTreeClassifier(random_state=42)
modelo.fit(X_train, y_train)

print("Modelo entrenado con datos históricos.\n")

# Solicitar datos al usuario
print("Ingresa los datos del estudiante:")
promedio = float(input("Promedio general (0-100): "))
horas = float(input("Horas de estudio por semana: "))
actividades = int(input("Número de actividades extracurriculares: "))

# Preparar datos para predicción
datos_usuario = np.array([[promedio, horas, actividades]])

# Hacer predicción
prediccion = modelo.predict(datos_usuario)[0]
probabilidad = modelo.predict_proba(datos_usuario)[0]

# Mostrar resultado
print("\n" + "="*50)
if prediccion == 1:
    print("RESULTADO: El estudiante será ADMITIDO")
    print(f"Confianza: {probabilidad[1]*100:.1f}%")
else:
    print(" RESULTADO: El estudiante NO será admitido")
    print(f"Confianza: {probabilidad[0]*100:.1f}%")
print("="*50)