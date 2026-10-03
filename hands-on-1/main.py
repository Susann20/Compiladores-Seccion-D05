# main.py
# Punto de entrada. AFD → Instrucción → Moore.

from afd import AFD
from instruccion import construir_instruccion
from moore import MaquinaMoore
from errores import InstruccionInvalidaError

def main():
    entrada = input("Ingrese una instrucción: ").strip()

    # 1. Validación con AFD
    print("\nVALIDACIÓN MEDIANTE AFD")
    afd = AFD()
    try:
        tokens = afd.validar(entrada)
    except InstruccionInvalidaError as e:
        print(f"Instrucción inválida: {e}")
        print("No se construye el objeto instrucción.")
        print("No se generan microoperaciones.")
        return

    print("Instrucción válida.")

    # 2. Tokens reconocidos
    print("\nTOKENS RECONOCIDOS")
    for t in tokens:
        print(f'{t["tipo"]} ("{t["lexema"]}")')

    # 3. Objeto instrucción
    instruccion = construir_instruccion(tokens)

    # 4. Componentes identificados
    print("\nCOMPONENTES IDENTIFICADOS")
    print(f"Mnemónico: {instruccion.operacion}")
    if instruccion.registros:
        if instruccion.operacion == "MOV":
            print(f"Registro destino: {instruccion.registros[0]}")
        elif instruccion.operacion == "ADD":
            print(f"Registros: {', '.join(instruccion.registros)}")
    if instruccion.direccion is not None:
        print(f"Dirección de memoria: {instruccion.direccion}")
        print("Direccionamiento: directo")

    # 5. Objeto instrucción impreso
    print("\nOBJETO INSTRUCCIÓN")
    print(instruccion)

    # 6. Microoperaciones con Moore
    print("\nMICROOPERACIONES GENERADAS POR MOORE")
    moore = MaquinaMoore(instruccion)
    for i, micro in enumerate(moore.generar_todas(), 1):
        print(f"{i}. {micro}")
    print("Generación terminada.")


if __name__ == "__main__":
    main()