import streamlit as st
import time

# ==========================================
#  MÁQUINA DE TURING PARA LA NUEVA GRAMÁTICA
#  S → N X
#  X → + N X | - N X | * N X | ε
#  N → D N | D
# ==========================================

class TuringMachineGrammar:
    def __init__(self, tape, blank="_"):
        self.tape = list(tape) + [blank] * 10
        self.blank = blank
        self.head = 0
        self.state = "q0"
        self.final_states = {"q_accept"}
        self.history = []

        # ======== TRANSICIONES ========
        self.transitions = {
            # q0 : iniciar con un dígito (N)
            ("q0", "0"): ("qN", "0", "R"),
            ("q0", "1"): ("qN", "1", "R"),
            ("q0", "2"): ("qN", "2", "R"),
            ("q0", "3"): ("qN", "3", "R"),
            ("q0", "4"): ("qN", "4", "R"),
            ("q0", "5"): ("qN", "5", "R"),
            ("q0", "6"): ("qN", "6", "R"),
            ("q0", "7"): ("qN", "7", "R"),
            ("q0", "8"): ("qN", "8", "R"),
            ("q0", "9"): ("qN", "9", "R"),

            # qN : consumir dígitos del primer número
            ("qN", "0"): ("qN", "0", "R"),
            ("qN", "1"): ("qN", "1", "R"),
            ("qN", "2"): ("qN", "2", "R"),
            ("qN", "3"): ("qN", "3", "R"),
            ("qN", "4"): ("qN", "4", "R"),
            ("qN", "5"): ("qN", "5", "R"),
            ("qN", "6"): ("qN", "6", "R"),
            ("qN", "7"): ("qN", "7", "R"),
            ("qN", "8"): ("qN", "8", "R"),
            ("qN", "9"): ("qN", "9", "R"),
            # al terminar número → operador o blank
            ("qN", "+"): ("qOp", "+", "R"),
            ("qN", "-"): ("qOp", "-", "R"),
            ("qN", "*"): ("qOp", "*", "R"),
            ("qN", "_"): ("q_accept", "_", "R"),

            # qOp: luego de un operador debe venir el primer dígito del siguiente N
            ("qOp", "0"): ("qN2", "0", "R"),
            ("qOp", "1"): ("qN2", "1", "R"),
            ("qOp", "2"): ("qN2", "2", "R"),
            ("qOp", "3"): ("qN2", "3", "R"),
            ("qOp", "4"): ("qN2", "4", "R"),
            ("qOp", "5"): ("qN2", "5", "R"),
            ("qOp", "6"): ("qN2", "6", "R"),
            ("qOp", "7"): ("qN2", "7", "R"),
            ("qOp", "8"): ("qN2", "8", "R"),
            ("qOp", "9"): ("qN2", "9", "R"),

            # qN2: consumir dígitos del siguiente número
            ("qN2", "0"): ("qN2", "0", "R"),
            ("qN2", "1"): ("qN2", "1", "R"),
            ("qN2", "2"): ("qN2", "2", "R"),
            ("qN2", "3"): ("qN2", "3", "R"),
            ("qN2", "4"): ("qN2", "4", "R"),
            ("qN2", "5"): ("qN2", "5", "R"),
            ("qN2", "6"): ("qN2", "6", "R"),
            ("qN2", "7"): ("qN2", "7", "R"),
            ("qN2", "8"): ("qN2", "8", "R"),
            ("qN2", "9"): ("qN2", "9", "R"),
            # Fin del número → si hay operador, volver a qOp; si blanco, aceptar
            ("qN2", "+"): ("qOp", "+", "R"),
            ("qN2", "-"): ("qOp", "-", "R"),
            ("qN2", "*"): ("qOp", "*", "R"),
            ("qN2", "_"): ("q_accept", "_", "R"),
        }

    def step(self):
        """Ejecuta una única transición."""
        # Asegurar índice válido
        while self.head >= len(self.tape):
            self.tape.append(self.blank)

        symbol = self.tape[self.head]
        key = (self.state, symbol)

        if self.state == "q_reject" or self.state in self.final_states:
            return

        if key not in self.transitions:
            # No hay transición → rechazo
            self.history.append(
                f"({self.state}, {symbol}) → (q_reject, {symbol}, R) [NO DEFINIDA]"
            )
            self.state = "q_reject"
            return

        new_state, new_symbol, move = self.transitions[key]

        self.history.append(
            f"({self.state}, {symbol}) → ({new_state}, {new_symbol}, {move})"
        )

        # Actualizar cinta y estado
        self.tape[self.head] = new_symbol
        self.state = new_state

        # Mover cabezal
        if move == "R":
            self.head += 1
            if self.head == len(self.tape):
                self.tape.append(self.blank)
        else:
            self.head -= 1

        # Extender cinta a la izquierda si es necesario
        if self.head < 0:
            self.tape.insert(0, self.blank)
            self.head = 0


# ==========================================
# VISUALIZACIÓN DE CINTA (MISMO ESTILO TUYO)
# ==========================================

def render_tape_html(tape, head):
    base = "display:flex;justify-content:center;align-items:center;width:40px;height:50px;border-radius:8px;font-size:24px;font-weight:700;margin:2px;color:#E0E0E0;background-color:#262626;border:2px solid #555;box-shadow:0 4px 6px rgba(0,0,0,0.3);"
    active = "border-color:#33F6A6;background-color:#1C4B3A;color:#FFFFFF;transform:scale(1.1);"

    html = '<div style="display:flex;justify-content:center;padding:20px 0;">'

    window = 7
    start = max(0, head - window)
    end = min(len(tape), head + window + 1)

    for i in range(start, end):
        style = base + (active if i == head else "")
        symbol = tape[i]
        html += f'<div style="{style}">{symbol}</div>'

    html += "</div>"
    return html


# ==========================================
# INTERFAZ STREAMLIT
# ==========================================

st.set_page_config(layout="wide")
st.title("Máquina de Turing – Nueva Gramática Aritmética (Animada)")

entrada = st.text_input("Ingresa cadena:", "23+7*5-9")
start = st.button("▶ Ejecutar Simulación", type="primary")

tape_ph = st.empty()
state_ph = st.empty()
result_ph = st.empty()

st.subheader("Historial de Transiciones")
hist_ph = st.empty()

if start:
    if not all(c in "0123456789+-*" for c in entrada):
        st.error("La cadena contiene símbolos inválidos.")
    else:
        mt = TuringMachineGrammar(entrada)
        history = "-- Inicio de simulación --\n"
        hist_ph.code(history)

        step = 0
        max_steps = 400

        while mt.state not in mt.final_states and mt.state != "q_reject" and step < max_steps:

            tape_ph.markdown(render_tape_html(mt.tape, mt.head), unsafe_allow_html=True)
            state_ph.markdown(f"**Estado:** `{mt.state}` | **Cabezal sobre:** `{mt.tape[mt.head]}`")

            mt.step()
            step += 1

            if mt.history:
                history += f"Paso {step}: {mt.history[-1]}\n"
                hist_ph.code(history)

            time.sleep(0.35)

        tape_ph.markdown(render_tape_html(mt.tape, mt.head), unsafe_allow_html=True)
        state_ph.markdown(f"**Estado:** `{mt.state}`")

        if mt.state == "q_accept":
            result_ph.success(f"✔ CADENA ACEPTADA en {step} pasos")
        elif mt.state == "q_reject":
            result_ph.error(f"✘ CADENA RECHAZADA en {step} pasos")
        else:
            result_ph.warning("La simulación superó el límite de pasos.")

