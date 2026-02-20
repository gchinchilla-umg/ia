from sklearn.cluster import KMeans
import numpy as np

print("=== AGRUPADOR AUTOMÁTICO DE ESTUDIANTES ===\n")
print("El sistema agrupa estudiantes en 3 perfiles según sus hábitos.\n")

# Datos de entrenamiento (estudiantes previos)
# [horas_estudio, horas_videojuegos, horas_deporte]
estudiantes_previos = np.array([
    [8, 1, 2],
    [7, 2, 3],
    [2, 8, 1],
    [3, 7, 2],
    [5, 4, 5],
    [6, 3, 6],
    [1, 9, 1],
    [9, 1, 1],
    [4, 5, 4],
    [8, 2, 2]
])

# Entrenar el modelo (sin etiquetas - encuentra grupos automáticamente)
modelo = KMeans(n_clusters=3, random_state=42)
modelo.fit(estudiantes_previos)

print("Modelo entrenado con datos de estudiantes anteriores.\n")
print("="*50)

# Solicitar datos al usuario
print("\nIngresa tus hábitos semanales:")
horas_estudio = float(input("Horas de estudio por semana: "))
horas_videojuegos = float(input("Horas jugando videojuegos: "))
horas_deporte = float(input("Horas haciendo deporte: "))

# Preparar datos
datos_usuario = np.array([[horas_estudio, horas_videojuegos, horas_deporte]])

# Predecir grupo
grupo = modelo.predict(datos_usuario)[0]

# Calcular perfiles de cada grupo
perfiles = {
    0: " ACADÉMICO - Enfocado en estudios",
    1: " GAMER - Prefiere entretenimiento digital",
    2: " BALANCEADO - Equilibra todas las actividades"
}

# Mostrar centros de grupos
print("\n" + "="*50)
print("PERFILES DETECTADOS POR EL MODELO:")
print("="*50)
for i, centro in enumerate(modelo.cluster_centers_):
    print(f"\nGrupo {i}:")
    print(f"  - Estudio: {centro[0]:.1f}h")
    print(f"  - Videojuegos: {centro[1]:.1f}h")
    print(f"  - Deporte: {centro[2]:.1f}h")

# Resultado final
print("\n" + "="*50)
print(f"TU PERFIL: GRUPO {grupo}")
print(f"Descripción: {perfiles.get(grupo, 'Perfil mixto')}")
print("="*50)

# Distancia a cada centro
distancias = modelo.transform(datos_usuario)[0]
print(f"\nSimilitud con cada grupo:")
for i, dist in enumerate(distancias):
    similitud = max(0, 100 - dist * 10)
    print(f"  Grupo {i}: {similitud:.1f}%")