# ============================================================
# perceptron simple — decision de credito bancario
# ============================================================

# ---------------------------
# 1. parametros del modelo
# ---------------------------

w1 = 1.0   # peso para ingresos altos
w2 = 1.2   # peso para historial crediticio bueno
w3 = 0.8   # peso para empleo estable

umbral = 1.8  # umbral (θ) previamente definido


# ------------------------------------------------------------
# 2. funcion para leer entradas binarias (0 | 1) con validacion
# ------------------------------------------------------------

def leer_variable(nombre):
    """
    Solicita un valor 0 o 1.
    Repite hasta que el usuario ingrese un valor valido.
    """
    while True:
        valor = input(f"Ingrese {nombre} (0 | 1): ").strip()

        # validacion basica: solo permitir '0' | '1'
        if valor in ("0", "1"):
            return int(valor)

        print("Error: Solo se permite 0 | 1.")


# ---------------------------
# 3. programa principal
# ---------------------------

def main():
    print("\nsistema de aprobacion de credito (perceptron simple)")
    print("----------------------------------------------------")

    # 1. solicitar al usuario los valores de las variables de entrada
    x1 = leer_variable("ingresos altos")
    x2 = leer_variable("historial crediticio bueno")
    x3 = leer_variable("empleo estable")

    # 2 y 3. utilizar pesos/umbral definidos y calcular suma ponderada
    z = (w1 * x1) + (w2 * x2) + (w3 * x3)

    # 4. determinar la salida 
    if z >= umbral:
        y = 1
    else:
        y = 0

    # mostrar resultado
    print("\nresultado del perceptron")
    print("----------------------")
    print(f"z = w1*x1 + w2*x2 + w3*x3")
    print(f"z = ({w1}*{x1}) + ({w2}*{x2}) + ({w3}*{x3}) = {z:.2f}")
    print(f"umbral (θ) = {umbral}")

    # 5. mensaje claro indicando la decision
    print("\ndecision")
    print("--------")
    if y == 1:
        print("credito aprobado (y = 1)")
    else:
        print("credito rechazado (y = 0)")

if __name__ == "__main__":
    main()