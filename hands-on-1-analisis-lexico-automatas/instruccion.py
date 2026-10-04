# instruccion.py
# Representación alterna de una instrucción validada.

class Instruccion:
    """Objeto instrucción con operación, registros y dirección."""
    def __init__(self, operacion: str, registros: list, direccion):
        self.operacion = operacion
        self.registros = registros
        self.direccion = direccion

    def __repr__(self):
        return (
            f'{{ operacion: "{self.operacion}", '
            f'registros: {self.registros}, '
            f'direccion: {self.direccion} }}'
        )


def construir_instruccion(tokens: list[dict]) -> Instruccion:
    """Transforma los tokens validados en un objeto Instruccion."""
    operacion = None
    registros = []
    direccion = None

    for tok in tokens:
        if tok["tipo"] in ("MOV", "ADD", "STO", "END"):
            operacion = tok["lexema"]
        elif tok["tipo"] == "REGISTRO":
            registros.append(tok["lexema"])
        elif tok["tipo"] == "NUMERO":
            direccion = int(tok["lexema"])

    if operacion is None:
        raise ValueError("La instrucción no contiene una operación válida")

    return Instruccion(operacion, registros, direccion)