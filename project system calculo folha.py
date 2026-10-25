from decimal import Decimal, ROUND_HALF_UP

# Sistema de cálculo trabalhista - RH
# Valores monetários com precisão de centavos


def dinheiro(valor):
    return Decimal(str(valor)).quantize(
        Decimal("0.01"),
        rounding=ROUND_HALF_UP
    )


def calcular_inss(salario):
    # Faixas progressivas do INSS para empregados em 2026
    faixas = [
        (Decimal("1621.00"), Decimal("0.075")),
        (Decimal("2902.84"), Decimal("0.09")),
        (Decimal("4354.27"), Decimal("0.12")),
        (Decimal("8475.55"), Decimal("0.14")),
    ]

    salario = min(salario, Decimal("8475.55"))
    limite_anterior = Decimal("0")
    inss = Decimal("0")

    for limite, aliquota in faixas:
        base = max(
            Decimal("0"),
            min(salario, limite) - limite_anterior
        )
        inss += base * aliquota
        limite_anterior = limite

        if salario <= limite:
            break

    return dinheiro(inss)


def calcular_fgts(salario, percentual=8):
    # Empregado CLT comum: normalmente 8%
    return dinheiro(salario * Decimal(str(percentual)) / 100)


def calcular_ferias(salario, dias=30):
    if dias < 1 or dias > 30:
        raise ValueError("Informe de 1 a 30 dias de férias.")

    valor_ferias = salario * Decimal(dias) / 30
    adicional_um_terco = valor_ferias / 3

    bruto = valor_ferias + adicional_um_terco

    # Estimativa simplificada, sem descontos
    return (
        dinheiro(valor_ferias),
        dinheiro(adicional_um_terco),
        dinheiro(bruto)
    )


def formatar(valor):
    return (
        f"R$ {valor:,.2f}"
        .replace(",", "X")
        .replace(".", ",")
        .replace("X", ".")
    )


def executar():
    print("\n=== SISTEMA DE CÁLCULO TRABALHISTA ===")

    nome = input("Nome do funcionário: ").strip()

    try:
        salario_texto = input(
            "Salário bruto (ex.: 3000.00): "
        ).strip().replace(",", ".")

        salario = dinheiro(salario_texto)

        if salario <= 0:
            raise ValueError("O salário deve ser maior que zero.")

        dias = int(input("Dias de férias (1 a 30): "))

        inss = calcular_inss(salario)
        fgts = calcular_fgts(salario)

        valor_ferias, terco, ferias_brutas = (
            calcular_ferias(salario, dias)
        )

        print("\n======= RELATÓRIO DO RH =======")
        print(f"Funcionário: {nome}")
        print(f"Salário bruto: {formatar(salario)}")
        print(f"INSS estimado: {formatar(inss)}")
        print(f"FGTS mensal: {formatar(fgts)}")
        print(f"Férias proporcionais aos dias: "
              f"{formatar(valor_ferias)}")
        print(f"Adicional de 1/3: {formatar(terco)}")
        print(f"Total bruto das férias: "
              f"{formatar(ferias_brutas)}")
        print("===============================")

        print("\nObservação: cálculo demonstrativo.")
        print("Não inclui IRRF, médias variáveis,")
        print("abono pecuniário ou outras particularidades.")

    except (ValueError, ArithmeticError) as erro:
        print(f"Erro nos dados informados: {erro}")


if __name__ == "__main__":
    executar()
