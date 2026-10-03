# moore.py
# Máquina de Moore: recorre estados y emite microoperaciones.
# Recibe un objeto Instruccion, no vuelve a analizar el texto.

from instruccion import Instruccion

# Estados de Moore (cada uno con salida asociada)
M_PREPARAR_DIR = "Preparar dirección"
M_LEER_MEMORIA = "Leer memoria"
M_CARGAR_REG   = "Cargar registro"
M_SUMAR        = "Sumar"
M_ALMACENAR    = "Almacenar"
M_DETENER      = "Detener"
M_FIN          = "Fin"

# Rutas de estados por operación
RUTAS_MOORE = {
    "MOV": [M_PREPARAR_DIR, M_LEER_MEMORIA, M_CARGAR_REG, M_FIN],
    "ADD": [M_SUMAR, M_FIN],
    "STO": [M_PREPARAR_DIR, M_LEER_MEMORIA, M_ALMACENAR, M_FIN],
    "END": [M_DETENER, M_FIN],
}


class MaquinaMoore:
    def __init__(self, instruccion: Instruccion):
        self.instruccion = instruccion
        self.ruta = RUTAS_MOORE[instruccion.operacion]
        self.indice = 0

    # Salida asociada al estado actual
    def _salida_estado(self, estado: str):
        inst = self.instruccion

        if estado == M_PREPARAR_DIR:
            return f"MAR ← {inst.direccion}"

        if estado == M_LEER_MEMORIA:
            if inst.operacion == "MOV":
                return "MBR ← M[MAR]"
            else:  # STO
                return "MBR ← ACC"

        if estado == M_CARGAR_REG:
            return f"{inst.registros[0]} ← MBR"

        if estado == M_SUMAR:
            return "ACC ← AL + BL"

        if estado == M_ALMACENAR:
            return "M[MAR] ← MBR"

        if estado == M_DETENER:
            return "HALT ← 1"

        if estado == M_FIN:
            return None

        return None

    # siguientePaso()
    def siguiente_paso(self):
        """Emite la salida del estado actual y avanza."""
        if self.indice >= len(self.ruta):
            return None
        estado = self.ruta[self.indice]
        salida = self._salida_estado(estado)
        self.indice += 1
        return salida

    # generar_todas()
    def generar_todas(self) -> list[str]:
        """Recorre la ruta completa y retorna las microoperaciones."""
        micros = []
        while True:
            salida = self.siguiente_paso()
            if salida is None:
                break
            micros.append(salida)
        return micros