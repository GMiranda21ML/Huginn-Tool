from huginn.core import logger

AUTH_PHRASE = "EU TENHO AUTORIZACAO"


def confirm_authorization(domain):
    logger.warn(f"Você está prestes a executar RECONHECIMENTO ATIVO contra: {domain}")
    logger.warn("Isso envolve interação direta com a infraestrutura do alvo (scans, requisições HTTP, etc).")
    logger.warn("Só prossiga se você tiver autorização explícita e por escrito para testar este alvo.")
    resp = input(f'Digite exatamente "{AUTH_PHRASE}" para confirmar e continuar: ')
    return resp.strip() == AUTH_PHRASE
