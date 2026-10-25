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
