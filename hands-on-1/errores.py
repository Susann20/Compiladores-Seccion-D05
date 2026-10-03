# errores.py
# Excepciones personalizadas del programa.
# Se ejecuta en:
# afd.py: para lanzar errores cuando la instrucción es inválida.
# main.py: para capturar esos errores y mostrar un mensaje al usuario.

class InstruccionInvalidaError(Exception):
    """
    Se lanza cuando el AFD rechaza la instrucción.
    Lleva un mensaje descriptivo para imprimir al usuario.
    """
    pass