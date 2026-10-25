import tkinter as tk
from tkinter import ttk, messagebox
from decimal import Decimal, ROUND_HALF_UP, InvalidOperation


# ==========================================
# SISTEMA RH FÁCIL - CÁLCULOS TRABALHISTAS
# ==========================================

def dinheiro(valor):
    return Decimal(str(valor)).quantize(
        Decimal("0.01"),
        rounding=ROUND_HALF_UP
    )


def moeda(valor):
    return (
        f"R$ {valor:,.2f}"
        .replace(",", "X")
        .replace(".", ",")
        .replace("X", ".")
    )


def calcular_inss(salario):
    # Faixas progressivas de contribuição de 2026.
    # Valores de referência sujeitos a atualização oficial.
    faixas = [
        (Decimal("1621.00"), Decimal("0.075")),
        (Decimal("2902.84"), Decimal("0.09")),
        (Decimal("4354.27"), Decimal("0.12")),
        (Decimal("8475.55"), Decimal("0.14")),
    ]

    base_total = min(salario, faixas[-1][0])
    anterior = Decimal("0")
    total = Decimal("0")

    for limite, aliquota in faixas:
        base = max(
            Decimal("0"),
            min(base_total, limite) - anterior
        )
        total += base * aliquota
        anterior = limite

        if base_total <= limite:
            break

    return dinheiro(total)


def calcular_fgts(salario):
    # Regra geral para empregado CLT comum
    return dinheiro(salario * Decimal("0.08"))


def calcular_ferias(salario, dias):
    valor_dias = salario * Decimal(dias) / Decimal("30")
    adicional = valor_dias / Decimal("3")

    return (
        dinheiro(valor_dias),
        dinheiro(adicional),
        dinheiro(valor_dias + adicional)
    )


def executar_calculo():
    nome = entrada_nome.get().strip()
    salario_texto = entrada_salario.get().strip()
    dias_texto = entrada_dias.get().strip()

    if not nome:
        messagebox.showwarning(
            "Atenção", "Informe o nome do funcionário."
        )
        entrada_nome.focus()
        return

    try:
        salario_texto = (
            salario_texto.replace("R$", "")
            .replace(" ", "")
        )

        # Aceita formatos como 3000,00 ou 3.000,00
        if "," in salario_texto:
            salario_texto = (
                salario_texto.replace(".", "")
                .replace(",", ".")
            )

        salario = dinheiro(salario_texto)
        dias = int(dias_texto)

        if salario <= 0:
            raise ValueError("O salário deve ser maior que zero.")

        if not 1 <= dias <= 30:
            raise ValueError("Os dias de férias devem estar entre 1 e 30.")

        inss = calcular_inss(salario)
        fgts = calcular_fgts(salario)

        valor_ferias, adicional, total_ferias = (
            calcular_ferias(salario, dias)
        )

        resultado = (
            f"FUNCIONÁRIO: {nome}\n"
            f"{'=' * 42}\n\n"
            f"Salário bruto:       {moeda(salario)}\n"
            f"INSS estimado:       {moeda(inss)}\n"
            f"FGTS mensal:         {moeda(fgts)}\n\n"
            f"Férias ({dias} dias):\n"
            f"Valor dos dias:      {moeda(valor_ferias)}\n"
            f"Adicional de 1/3:    {moeda(adicional)}\n"
            f"Total bruto férias:  {moeda(total_ferias)}\n\n"
            f"{'=' * 42}\n"
            "SIMULAÇÃO PARA CONFERÊNCIA DO RH"
        )

        campo_resultado.config(state="normal")
        campo_resultado.delete("1.0", tk.END)
        campo_resultado.insert(tk.END, resultado)
        campo_resultado.config(state="disabled")

    except (ValueError, InvalidOperation):
        messagebox.showerror(
            "Dados inválidos",
            "Informe um salário válido e dias de férias "
            "entre 1 e 30."
        )


def limpar_campos():
    entrada_nome.delete(0, tk.END)
    entrada_salario.delete(0, tk.END)
    entrada_dias.delete(0, tk.END)
    entrada_dias.insert(0, "30")

    campo_resultado.config(state="normal")
    campo_resultado.delete("1.0", tk.END)
    campo_resultado.config(state="disabled")

    entrada_nome.focus()


# ==========================================
# INTERFACE GRÁFICA
# ==========================================

janela = tk.Tk()
janela.title("RH Fácil | Cálculos Trabalhistas")
janela.geometry("700x700")
janela.minsize(600, 620)
janela.configure(bg="#F1F5F9")

estilo = ttk.Style()
estilo.theme_use("clam")

estilo.configure(
    "TLabel",
    background="#F1F5F9",
    foreground="#1E293B",
    font=("Arial", 11)
)

estilo.configure(
    "TButton",
    font=("Arial", 11, "bold"),
    padding=10
)

estilo.configure(
    "Calcular.TButton",
    background="#176B45",
    foreground="white"
)

estilo.map(
    "Calcular.TButton",
    background=[("active", "#125437")]
)

# Cabeçalho
cabecalho = tk.Frame(janela, bg="#17365D", height=100)
cabecalho.pack(fill="x")
cabecalho.pack_propagate(False)

tk.Label(
    cabecalho,
    text="RH FÁCIL",
    bg="#17365D",
    fg="white",
    font=("Arial", 24, "bold")
).pack(pady=(18, 2))

tk.Label(
    cabecalho,
    text="Sistema de Cálculos Trabalhistas",
    bg="#17365D",
    fg="#DCE8F5",
    font=("Arial", 11)
).pack()

# Área principal
principal = ttk.Frame(janela, padding=24)
principal.pack(fill="both", expand=True)

ttk.Label(
    principal,
    text="Dados do funcionário",
    font=("Arial", 15, "bold")
).pack(anchor="w", pady=(0, 15))

ttk.Label(principal, text="Nome completo").pack(anchor="w")

entrada_nome = ttk.Entry(principal, font=("Arial", 12))
entrada_nome.pack(fill="x", pady=(5, 12))

ttk.Label(principal, text="Salário bruto mensal (R$)").pack(
    anchor="w"
)

entrada_salario = ttk.Entry(principal, font=("Arial", 12))
entrada_salario.pack(fill="x", pady=(5, 12))

ttk.Label(principal, text="Dias de férias (1 a 30)").pack(
    anchor="w"
)

entrada_dias = ttk.Entry(principal, font=("Arial", 12))
entrada_dias.insert(0, "30")
entrada_dias.pack(fill="x", pady=(5, 18))

# Botões
linha_botoes = ttk.Frame(principal)
linha_botoes.pack(fill="x", pady=(0, 18))

ttk.Button(
    linha_botoes,
    text="Calcular valores",
    style="Calcular.TButton",
    command=executar_calculo
).pack(side="left", fill="x", expand=True, padx=(0, 6))

ttk.Button(
    linha_botoes,
    text="Limpar",
    command=limpar_campos
).pack(side="left", fill="x", expand=True, padx=(6, 0))

# Resultado
ttk.Label(
    principal,
    text="Resultado do cálculo",
    font=("Arial", 14, "bold")
).pack(anchor="w", pady=(0, 8))

campo_resultado = tk.Text(
    principal,
    height=12,
    font=("Consolas", 11),
    bg="white",
    fg="#1E293B",
    relief="solid",
    borderwidth=1,
    padx=12,
    pady=12,
    wrap="word"
)
campo_resultado.pack(fill="both", expand=True)
campo_resultado.config(state="disabled")

tk.Label(
    janela,
    text="Valores estimados. Confira as regras vigentes antes "
         "de utilizar em folha de pagamento.",
    bg="#F1F5F9",
    fg="#64748B",
    font=("Arial", 9),
    wraplength=650
).pack(pady=(0, 12))

entrada_nome.focus()
janela.mainloop()
# Sistema de cálculo do INSS - Tabela 2026


def calcular_inss(salario):
    if salario < 0:
        raise ValueError("O salário não pode ser negativo.")

    # Faixas progressivas de contribuição
    faixas = [
        (1621.00, 0.075),
        (2902.84, 0.09),
        (4354.27, 0.12),
        (8475.55, 0.14)
    ]

    desconto = 0.0
    limite_anterior = 0.0

    for limite, aliquota in faixas:
        if salario > limite_anterior:
            parcela = min(salario, limite) - limite_anterior
            desconto += parcela * aliquota
            limite_anterior = limite

        if salario <= limite:
            break

    return round(desconto, 2)


def main():
    print("=" * 40)
    print(" SISTEMA TRABALHISTA - INSS 2026")
    print("=" * 40)

    try:
        salario = float(
            input("Digite o salário bruto (R$): ")
            .replace(",", ".")
        )

        if salario < 0:
            print("Erro: informe um salário válido.")
            return

        inss = calcular_inss(salario)
        salario_liquido = salario - inss

        print("\n--- RESULTADO DO CÁLCULO ---")
        print(f"Salário bruto: R$ {salario:.2f}")
        print(f"Desconto INSS: R$ {inss:.2f}")
        print(f"Salário após INSS: R$ {salario_liquido:.2f}")
        print("=" * 40)

    except ValueError:
        print("Erro: digite um valor numérico válido.")


if __name__ == "__main__":
    main()
    # Calculadora de FGTS - 2026


def calcular_fgts(salario, tipo_contrato="clt"):
    if salario < 0:
        raise ValueError("O salário não pode ser negativo.")

    tipo_contrato = tipo_contrato.lower()

    if tipo_contrato == "clt":
        aliquota = 0.08
    elif tipo_contrato == "aprendiz":
        aliquota = 0.02
    else:
        raise ValueError("Use 'clt' ou 'aprendiz'.")

    return round(salario * aliquota, 2)


salario = float(input("Digite o salário bruto: R$ ").replace(",", "."))
tipo = input("Tipo de contrato (clt ou aprendiz): ")

fgts = calcular_fgts(salario, tipo)

print(f"Salário bruto: R$ {salario:.2f}")
print(f"Depósito mensal do FGTS: R$ {fgts:.2f}")
