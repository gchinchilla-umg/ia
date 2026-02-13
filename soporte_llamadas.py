#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Sistema de IA Simbolica para Soporte de Llamadas Telefonicas
Guillermo Chinchilla
0900 04 4218
"""

def verificar_condiciones_llamada(problemas_telefono):
    """
    Motor de inferencia soporte llamadas telefonicas.
    
    Args:
        problemas_telefono (list): Lista de síntomas reportados
        
    Returns:
        str: Diagnostico del problema y posible solucion
    """
    # Reglas combinadas primera linea
    
    # Combinacion 1: Sin senal y modo avion activado
    if "sin_senal" in problemas_telefono and "modo_avion" in problemas_telefono:
        return "Modo avion activado. Desactive el modo avion para recuperar la senal y poder realizar llamadas."
    
    # Combinacion 2: Sin senal y zona rural
    elif "sin_senal" in problemas_telefono and "zona_rural" in problemas_telefono:
        return "Problema de cobertura en zona rural. Intente moverse a un area con mejor senal."
    
    # Combinacion 3: Sin senal y batería baja
    elif "sin_senal" in problemas_telefono and "bateria_baja" in problemas_telefono:
        return "Senal debil y batería baja. La búsqueda continua de senal consume mas batería. Cargue el dispositivo para mejorar la recepcion."
    
    # Combinacion 4: Sin SIM y dispositivo nuevo
    elif "sin_sim" in problemas_telefono and "sim_nueva" in problemas_telefono:
        return "SIM nueva no activada. Contacte a su proveedor para activar la SIM."
    
    # Combinacion 5: Problemas de audio y volumen bajo
    elif ("sin_audio" in problemas_telefono or "no_escucha" in problemas_telefono or "no_habla" in problemas_telefono) and "volumen_bajo" in problemas_telefono:
        return "Volumen bajo o silenciado. Suba el volumen del dispositivo y verifique que no este en modo silencio."
    
    # Combinacion 6: Número invalido y llamada internacional
    elif "numero_invalido" in problemas_telefono and "llamada_internacional" in problemas_telefono:
        return "Formato de número internacional incorrecto. Asegúrese de incluir el codigo de país con el formato adecuado (ej: +502 para Guatemala)."
    
    # Combinacion 7: Senal debil y batería baja
    elif "senal_debil" in problemas_telefono and "bateria_baja" in problemas_telefono:
        return "Senal debil y batería baja. La búsqueda continua de senal consume mas batería. Cargue el dispositivo y busque mejor cobertura."
    
    # Combinacion 8: Problemas de red y saldo bajo
    elif ("red_inestable" in problemas_telefono or "red_congestionada" in problemas_telefono) and "saldo_bajo" in problemas_telefono:
        return "Red inestable y saldo bajo. La reconexion continua puede consumir saldo adicional. Espere a tener mejor senal antes de intentar llamar."
    
    # Combinacion 9: Sin senal y en edificio
    elif "sin_senal" in problemas_telefono and "en_edificio" in problemas_telefono:
        return "Senal bloqueada por estructura del edificio. Acerquese a una ventana o salga al exterior para mejorar la recepcion."
    
    # Combinacion 10: Llamada bloqueada y número desconocido
    elif "llamada_bloqueada" in problemas_telefono and "numero_desconocido" in problemas_telefono:
        return "Llamada bloqueada a número desconocido. Verifique la configuracion de bloqueo de llamadas desconocidas en su dispositivo."
    
    # Reglas simples (se aplican si no hay combinaciones)
    
    # Regla 1: Sin senal → Problema de cobertura
    elif "sin_senal" in problemas_telefono:
        return "Problema de cobertura. Verifique que no este en un area con senal limitada (sotanos, edificios, etc.)."
    
    # Regla 2: Sin SIM → SIM no instalada o mal colocada
    elif "sin_sim" in problemas_telefono:
        return "SIM no detectada. Verifique que la tarjeta SIM este correctamente instalada."
    
    # Regla 3: Sin saldo → Necesidad de recarga
    elif "sin_saldo" in problemas_telefono:
        return "Saldo insuficiente. Realice una recarga para poder realizar llamadas."
    
    # Regla 4: Modo avion activado
    elif "modo_avion" in problemas_telefono:
        return "Modo avion activado. Desactive el modo avion para realizar llamadas."
    
    # Regla 5: Batería crítica
    elif "bateria_baja" in problemas_telefono:
        return "Batería crítica. Conecte el dispositivo a un cargador para realizar llamadas."
    
    # Regla 6: Problemas de audio
    elif "sin_audio" in problemas_telefono or "no_escucha" in problemas_telefono or "no_habla" in problemas_telefono:
        return "Problema con el microfono o altavoz. Verifique que no esten bloqueados y que el volumen este activado."
    
    # Regla 7: Número marcado invalido
    elif "numero_invalido" in problemas_telefono:
        return "El numero marcado no es valido. Verifique el formato e intente nuevamente."
    
    # Regla 8: Restricciones de llamadas
    elif "llamada_bloqueada" in problemas_telefono:
        return "Llamada bloqueada. Verifique la configuracion de restriccion de llamadas en su dispositivo."
    
    # Regla 9: Problemas de red
    elif "red_2g" in problemas_telefono:
        return "Conectado a red 2G con limitaciones. Intente cambiar a 3G/4G en la configuracion de red."
    
    # Regla 10: Interferencia de senal
    elif "senal_intermitente" in problemas_telefono:
        return "Senal intermitente. Alejese de fuentes de interferencia como electrodomesticos o estructuras metalicas."
    
    # Si no se identifica ningún problema específico
    else:
        return "Diagnostico insuficiente. Por favor proporcione mas detalles sobre el problema."


def mostrar_opciones_problemas():
    """
    Muestra las opciones de problemas disponibles para que el usuario seleccione.
    """
    print("\nOpciones de problemas disponibles:")
    print("1. sin_senal - No hay senal de red")
    print("2. zona_rural - Ubicado en zona rural")
    print("3. sin_sim - No se detecta la tarjeta SIM")
    print("4. sim_nueva - Tarjeta SIM recien adquirida")
    print("5. sin_saldo - Sin saldo disponible")
    print("6. modo_avion - Modo avion activado")
    print("7. bateria_baja - Nivel de batería crítico")
    print("8. sin_audio - No hay audio en llamadas")
    print("9. no_escucha - No se escucha a la otra persona")
    print("10. no_habla - La otra persona no me escucha")
    print("11. numero_invalido - Número marcado invalido")
    print("12. llamada_bloqueada - Llamada rechazada por el sistema")
    print("13. red_2g - Conectado solo a red 2G")
    print("14. senal_intermitente - Senal que aparece y desaparece")
    print("15. senal_debil - Senal de baja intensidad")
    print("16. red_inestable - Red con problemas de estabilidad")
    print("17. red_congestionada - Red con muchos usuarios")
    print("18. saldo_bajo - Saldo casi agotado")
    print("19. volumen_bajo - Volumen del dispositivo bajo o silenciado")
    print("20. llamada_internacional - Intentando llamar a número internacional")
    print("21. en_edificio - Dentro de un edificio o estructura")
    print("22. numero_desconocido - Llamando a un número desconocido")
    print("\nIngrese los números correspondientes separados por comas (ejemplo: 1,5,7)")


def procesar_entrada_usuario(entrada):
    """
    Procesa la entrada del usuario y la convierte en una lista de problemas.
    
    Args:
        entrada (str): Entrada del usuario con números separados por comas
        
    Returns:
        list: Lista de problemas correspondientes a los números ingresados
    """
    opciones_problemas = {
        "1": "sin_senal",
        "2": "zona_rural",
        "3": "sin_sim",
        "4": "sim_nueva",
        "5": "sin_saldo",
        "6": "modo_avion",
        "7": "bateria_baja",
        "8": "sin_audio",
        "9": "no_escucha",
        "10": "no_habla",
        "11": "numero_invalido",
        "12": "llamada_bloqueada",
        "13": "red_2g",
        "14": "senal_intermitente",
        "15": "senal_debil",
        "16": "red_inestable",
        "17": "red_congestionada",
        "18": "saldo_bajo",
        "19": "volumen_bajo",
        "20": "llamada_internacional",
        "21": "en_edificio",
        "22": "numero_desconocido"
    }
    
    numeros_seleccionados = [num.strip() for num in entrada.split(",")]
    problemas_seleccionados = []
    
    for numero in numeros_seleccionados:
        if numero in opciones_problemas:
            problemas_seleccionados.append(opciones_problemas[numero])
    
    return problemas_seleccionados


def main():
    """
    Funcion principal que ejecuta el sistema de soporte para llamadas telefonicas.
    """
    print("=================================")
    print("Sistema de ia simbolica para soporte de llamadas telefonicas")
    print("=================================")
    print("\nEste sistema le ayudara a diagnosticar problemas al realizar llamadas telefonicas.")
    
    while True:
        mostrar_opciones_problemas()
        print("\nSeleccione los problemas que esta experimentando:")
        entrada_usuario = input("> ")
        
        if entrada_usuario.lower() in ["salir", "exit", "q", "quit"]:
            print("\n¡Gracias por utilizar nuestro sistema de soporte!")
            break
        
        problemas_telefono = procesar_entrada_usuario(entrada_usuario)
        
        if not problemas_telefono:
            print("\nNo se ha seleccionado ningun problema valido. Por favor intente nuevamente.")
            continue
        
        print("\nProblemas seleccionados:", ", ".join(problemas_telefono))
        diagnostico = verificar_condiciones_llamada(problemas_telefono)
        
        print("\n" + "=================================")
        print("diagnostico:")
        print(diagnostico)
        print("=================================")
        
        print("\n¿Desea realizar otro diagnostico? (s/n)")
        continuar = input("> ")
        if continuar.lower() not in ["s", "si", "sí", "y", "yes"]:
            print("\n¡Gracias por utilizar nuestro sistema de soporte!")
            break


if __name__ == "__main__":
    main()