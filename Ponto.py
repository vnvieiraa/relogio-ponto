import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

# Banco de dados
conexao = sqlite3.connect("ponto.db")
cursor = conexao.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS funcionarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    matricula TEXT UNIQUE NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS pontos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    funcionario_id INTEGER NOT NULL,
    tipo TEXT NOT NULL,
    data_hora TEXT NOT NULL
)
""")

conexao.commit()
conexao.close()


def cadastrar():
    nome = campo_nome.get().strip()
    matricula = campo_matricula.get().strip()

    if not nome or not matricula:
        messagebox.showwarning("Atenção", "Preencha nome e matrícula.")
        return

    try:
        with sqlite3.connect("ponto.db") as db:
            db.execute(
                "INSERT INTO funcionarios (nome, matricula) VALUES (?, ?)",
                (nome, matricula)
            )
        atualizar_funcionarios()
        campo_nome.delete(0, tk.END)
        campo_matricula.delete(0, tk.END)
        messagebox.showinfo("Sucesso", "Funcionário cadastrado!")
    except sqlite3.IntegrityError:
        messagebox.showerror("Erro", "Esta matrícula já está cadastrada.")


def atualizar_funcionarios():
    with sqlite3.connect("ponto.db") as db:
        funcionarios = db.execute(
            "SELECT id, nome, matricula FROM funcionarios ORDER BY nome"
        ).fetchall()

    lista_funcionarios["values"] = [
        f"{id_} - {nome} ({matricula})"
        for id_, nome, matricula in funcionarios
    ]

    if funcionarios:
        lista_funcionarios.current(0)


def registrar(tipo):
    selecionado = lista_funcionarios.get()

    if not selecionado:
        messagebox.showwarning("Atenção", "Selecione um funcionário.")
        return

    funcionario_id = int(selecionado.split(" - ")[0])
    data_hora = datetime.now().astimezone().isoformat(timespec="seconds")

    with sqlite3.connect("ponto.db") as db:
        db.execute(
            """INSERT INTO pontos
               (funcionario_id, tipo, data_hora)
               VALUES (?, ?, ?)""",
            (funcionario_id, tipo, data_hora)
        )

    messagebox.showinfo(
        "Ponto registrado",
        f"{tipo}\n{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}"
    )


# Interface gráfica
janela = tk.Tk()
janela.title("Sistema de Ponto Eletrônico - RH")
janela.geometry("600x430")

ttk.Label(
    janela,
    text="SISTEMA DE PONTO ELETRÔNICO",
    font=("Arial", 16, "bold")
).pack(pady=15)

formulario = ttk.LabelFrame(janela, text="Cadastro de funcionário", padding=12)
formulario.pack(fill="x", padx=15)

ttk.Label(formulario, text="Nome:").grid(row=0, column=0, sticky="w")
campo_nome = ttk.Entry(formulario, width=35)
campo_nome.grid(row=0, column=1, padx=5, pady=5)

ttk.Label(formulario, text="Matrícula:").grid(row=1, column=0, sticky="w")
campo_matricula = ttk.Entry(formulario, width=35)
campo_matricula.grid(row=1, column=1, padx=5, pady=5)

ttk.Button(
    formulario, text="Cadastrar funcionário", command=cadastrar
).grid(row=2, column=1, sticky="e", pady=5)

grupo_ponto = ttk.LabelFrame(janela, text="Registro de ponto", padding=12)
grupo_ponto.pack(fill="x", padx=15, pady=15)

lista_funcionarios = ttk.Combobox(grupo_ponto, state="readonly", width=45)
lista_funcionarios.pack(pady=8)

botoes = ttk.Frame(grupo_ponto)
botoes.pack()

for nome_botao, tipo in [
    ("Entrada", "ENTRADA"),
    ("Saída intervalo", "SAÍDA INTERVALO"),
    ("Retorno", "RETORNO"),
    ("Saída final", "SAÍDA FINAL")
]:
    ttk.Button(
        botoes,
        text=nome_botao,
        command=lambda t=tipo: registrar(t)
    ).pack(side="left", padx=3, pady=5)

atualizar_funcionarios()
janela.mainloop()
