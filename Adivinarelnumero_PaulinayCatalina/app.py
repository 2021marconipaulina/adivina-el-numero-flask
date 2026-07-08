from flask import Flask, render_template, request, session
import random

app = Flask(__name__)
app.secret_key = "clave_secreta"


def verificar(numero, intento):
    if intento < numero:
        return "mayor"
    elif intento > numero:
        return "menor"
    else:
        return "Adivinaste"


@app.route("/", methods=["GET", "POST"])
def inicio():

    # Iniciar una nueva partida
    if "numero" not in session:
        session["numero"] = random.randint(1, 100)
        session["contador"] = 0

    mensaje = ""

    if request.method == "POST":
        intento = int(request.form["intento"])
        session["contador"] += 1

        resultado = verificar(session["numero"], intento)

        if resultado == "mayor":
            mensaje = "El número secreto es mayor."

        elif resultado == "menor":
            mensaje = "El número secreto es menor."

        else:
            mensaje = f"¡Adivinaste! Lo lograste en {session['contador']} intentos."

            # Reiniciar el juego
            session.pop("numero")
            session.pop("contador")

            return render_template("index.html", mensaje=mensaje)

        if session["contador"] == 7:
            mensaje = f"Perdiste. El número secreto era {session['numero']}."

            # Reiniciar el juego
            session.pop("numero")
            session.pop("contador")

    return render_template("index.html", mensaje=mensaje)


if __name__ == "__main__":
    app.run(debug=True)