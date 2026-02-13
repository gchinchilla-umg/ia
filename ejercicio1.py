#-- IA simbolica --
def motor_inferencia(sintomas):
    # Regla 1: Si el equipo no enciende y no hay luz  --> Problema de energía
 if("no_enciende" in sintomas and "sin_luces" in sintomas):
        return "Falta de fuente de poder"
    # Regla 2: Si el equipo enciende y no hay pantalla  --> Error de pantalla
 elif("enciende" in sintomas and "sin_imagen" in sintomas):
     return "Posible error en el flex de pantalla"
 else:
     return "Diagnostico insuficiente"
#--Interfaz de usuario--
print("sistama simbolico de soporte")
print("Ingrese el sintoma separado por comas (ejemplo: no_enciende, sin_luces):")
entrada_usuario = input(">").lower().replace("", "").split(",")
resultado = motor_inferencia(entrada_usuario)
print(f"IA simbolica: {resultado}")