# afd.py
# Validación léxica y sintáctica de la instrucción.
# Implementa un AFD con estados y transiciones explícitos.

from errores import InstruccionInvalidaError

# Estados del AFD
Q0_INICIO     = "q0_inicio"
Q1_MOV        = "q1_mov"
Q2_ADD        = "q2_add"
Q3_STO        = "q3_sto"
Q4_END        = "q4_end"
Q5_REG_MOV    = "q5_reg_mov"
Q6_COMA       = "q6_coma"
Q7_NUMERO     = "q7_numero"
Q8_REG_ADD    = "q8_reg_add"
Q9_ACEPTACION = "q9_aceptacion"
Q_ERROR       = "q_error"

# Tabla de transiciones: (estado_actual, tipo_token) -> siguiente
TRANSICIONES = {
    # Desde inicio según mnemónico
    (Q0_INICIO, "MOV"): Q1_MOV,
    (Q0_INICIO, "ADD"): Q2_ADD,
    (Q0_INICIO, "STO"): Q3_STO,
    (Q0_INICIO, "END"): Q4_END,

    # MOV R, d
    (Q1_MOV, "REGISTRO"): Q5_REG_MOV,
    (Q5_REG_MOV, "COMA"): Q6_COMA,
    (Q6_COMA, "NUMERO"): Q7_NUMERO,
    (Q7_NUMERO, "FIN"): Q9_ACEPTACION,

    # ADD AL, BL
    (Q2_ADD, "REGISTRO"): Q8_REG_ADD,
    (Q8_REG_ADD, "COMA"): Q6_COMA,
    (Q6_COMA, "REGISTRO"): Q8_REG_ADD,
    (Q8_REG_ADD, "FIN"): Q9_ACEPTACION,

    # STO d
    (Q3_STO, "NUMERO"): Q7_NUMERO,
    (Q7_NUMERO, "FIN"): Q9_ACEPTACION,

    # END
    (Q4_END, "FIN"): Q9_ACEPTACION,
}

ESTADOS_ACEPTACION = {Q9_ACEPTACION}

# Clase AFD
class AFD:
    def __init__(self):
        self.estado_actual = Q0_INICIO
        self.tokens = []
        self.operacion_actual = None   

    # Tokenización
    def _tokenizar(self, entrada: str) -> list[dict]:
        """Convierte el texto en una lista de tokens."""
        tokens = []
        i = 0
        n = len(entrada)

        while i < n:
            c = entrada[i]

            if c.isspace():
                i += 1
                continue

            if c == ',':
                tokens.append({"tipo": "COMA", "lexema": ","})
                i += 1
                continue

            if c.isdigit():
                j = i
                while j < n and entrada[j].isdigit():
                    j += 1
                tokens.append({"tipo": "NUMERO", "lexema": entrada[i:j]})
                i = j
                continue

            if c.isalpha():
                j = i
                while j < n and entrada[j].isalnum():
                    j += 1
                lexema = entrada[i:j]

                if lexema in ("MOV", "ADD", "STO", "END"):
                    tokens.append({"tipo": lexema, "lexema": lexema})
                elif lexema in ("AL", "BL"):
                    tokens.append({"tipo": "REGISTRO", "lexema": lexema})
                else:
                    tokens.append({"tipo": "DESCONOCIDO", "lexema": lexema})
                i = j
                continue

            tokens.append({"tipo": "DESCONOCIDO", "lexema": c})
            i += 1

        tokens.append({"tipo": "FIN", "lexema": ""})
        return tokens

    # Validación con la tabla de transiciones
    def validar(self, entrada: str) -> list[dict]:
        """Valida la entrada y retorna tokens (sin FIN)."""
        self.estado_actual = Q0_INICIO
        self.tokens = self._tokenizar(entrada)
        self.operacion_actual = None   # ← reiniciar

        for token in self.tokens:
            if token["tipo"] in ("MOV", "ADD", "STO", "END"):
                self.operacion_actual = token["tipo"]

            clave = (self.estado_actual, token["tipo"])
            if clave in TRANSICIONES:
                self.estado_actual = TRANSICIONES[clave]
            else:
                raise InstruccionInvalidaError(
                    self._mensaje_error(token)
                )

        if self.estado_actual not in ESTADOS_ACEPTACION:
            raise InstruccionInvalidaError(
                "la instrucción está incompleta o tiene operandos sobrantes."
            )

        return [t for t in self.tokens if t["tipo"] != "FIN"]

    # Mensajes de error específicos
    def _mensaje_error(self, token: dict) -> str:
        e = self.estado_actual
        t = token["tipo"]
        op = self.operacion_actual

        if e == Q1_MOV and t != "REGISTRO":
            return "se esperaba un registro (AL o BL) después de MOV."
        
        if e == Q5_REG_MOV and t != "COMA":
            return "falta la coma entre el registro y la dirección."
        
        if e == Q6_COMA: 
            # Mensaje contextual según la operación en curso
            if op == "MOV":
                return "se esperaba una dirección decimal después de la coma."
            if op == "ADD":
                return "se esperaba el registro BL después de la coma."
            return "se esperaba un operando después de la coma."

        if e == Q7_NUMERO and t != "FIN":
            return "hay operandos sobrantes después de la dirección."
        
        if e == Q2_ADD and t != "REGISTRO":
            return "se esperaba el registro AL después de ADD."
        
        if e == Q8_REG_ADD and t not in ("COMA", "FIN"):
            return "se esperaba una coma o el fin de la instrucción."
        
        if e == Q3_STO and t != "NUMERO":
            return "se esperaba una dirección decimal después de STO."
        
        if e == Q4_END and t != "FIN":
            return "END no admite operandos."
        
        if t == "DESCONOCIDO":
            return f"lexema no reconocido: '{token['lexema']}'."
        return f"transición inválida desde {e} con token {t}."