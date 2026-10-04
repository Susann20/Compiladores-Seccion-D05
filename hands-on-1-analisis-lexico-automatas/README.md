# Hands-on 1: Análisis Léxico y Autómatas

**Materia:** Compiladores  
**Alumna:** Susana Hernández Monroy  
**Fecha:** 02/10/2026

---

## Descripción

Programa que valida instrucciones del ISA (`MOV`, `ADD`, `STO`, `END`),
construye el objeto instrucción y genera microoperaciones con una
Máquina de Moore. No ejecuta las microoperaciones.

---

## Estructura

- `errores.py` — Excepción `InstruccionInvalidaError`
- `afd.py` — AFD con estados y transiciones explícitos
- `instruccion.py` — Objeto `Instruccion`
- `moore.py` — Máquina de Moore
- `main.py` — Orquestación
- `evidencias/` — Capturas de ejecución en PDF

---

## Ejecución

Desde la carpeta `hands-on-1-analisis-lexico-automatas/`:

```bash
python main.py 
```

El programa solicita una instrucción y muestra:
Validación mediante AFD.
Tokens reconocidos.
Componentes identificados.
Objeto instrucción.
Microoperaciones generadas por Moore.

## Ejemplos de entrada
**Válidas**
- MOV AL, 6
- MOV BL, 7
- ADD AL, BL
- STO 8
- END

**Inválidas**
- MOV AX, 6 — registro inválido
- MOV AL 6 — falta coma
- ADD AL, — falta segundo registro
- STO — falta dirección
- END 8 — END no admite operandos

## Evidencias
Las capturas de ejecución están en:

**evidencias/Hands-on_1_evidencias.pdf**

Incluyen las 10 entradas (5 válidas y 5 inválidas) con su salida completa

## Conclusiones
- El AFD valida la instrucción con estados y transiciones explícitos.
- El objeto instrucción es la representación alterna que conecta AFD y Moore.
- La Máquina de Moore genera microoperaciones sin reanalizar el texto.
- La separación en módulos aísla responsabilidades y facilita el mantenimiento.
