import time



def aviso_previo_para_colaborador():
    mensagem = """
    ⚠ AVISO PRÉVIO ⚠
    
    Prezado Colaborador,
    
    Informamos que este é o aviso prévio referente à sua posição atual.
    O prazo para as devidas providências é de 30 dias, conforme acordado desde data proposta não fará mais parte do quadro da empresa.
    No caso solicitante requisitar a antecipação do término do contrato, favor entrar em contato com o departamento de Recursos Humanos.
    Estaremos a disposição para prestar quaisquer esclarecimentos necessários.
    
    Atenciosamente,
    Equipe de Recursos Humanos!
    """
    print("Preparando para enviar aviso prévio...")
    time.sleep(2)
    print(mensagem)
    print("Mensagem enviada com sucesso ✅")


aviso_previo_para_colaborador()
