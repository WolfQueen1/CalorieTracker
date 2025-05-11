from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import date

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('data.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def index():
    conn = get_db_connection()
    alimente = conn.execute("SELECT * FROM alimente").fetchall()
    mese = conn.execute("SELECT m.id, a.nume, m.portii, m.data, a.calorii_pe_portie FROM mese m JOIN alimente a ON m.aliment_id = a.id ORDER BY m.data DESC").fetchall()
    conn.close()
    calorii_totale = {}
    for masa in mese:
        zi = masa['data']
        calorii_totale[zi] = calorii_totale.get(zi, 0) + masa['portii'] * masa['calorii_pe_portie']
    return render_template("index.html", alimente=alimente, mese=mese, calorii=calorii_totale, date=date)

@app.route("/adauga-aliment", methods=["POST"])
def adauga_aliment():
    nume = request.form["nume"]
    calorii = request.form["calorii"]
    categorie = request.form["categorie"]
    conn = get_db_connection()
    conn.execute("INSERT INTO alimente (nume, calorii_pe_portie, categorie) VALUES (?, ?, ?)", (nume, calorii, categorie))
    conn.commit()
    conn.close()
    return redirect("/")

@app.route("/adauga-masa", methods=["POST"])
def adauga_masa():
    aliment_id = request.form["aliment_id"]
    portii = request.form["portii"]
    data_masa = request.form["data"]
    conn = get_db_connection()
    conn.execute("INSERT INTO mese (aliment_id, portii, data) VALUES (?, ?, ?)", (aliment_id, portii, data_masa))
    conn.commit()
    conn.close()
    return redirect("/")

@app.route("/sterge-masa/<int:id>")
def sterge_masa(id):
    conn = get_db_connection()
    conn.execute("DELETE FROM mese WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
