from huginn.core import logger

CONFIRM_VALUES = {"", "y", "Y", "yes", "s", "sim"}


def confirm_authorization(domain):
    logger.warn(f"Você está prestes a executar RECONHECIMENTO ATIVO contra: {domain}")
    logger.warn("Isso envolve interação direta com a infraestrutura do alvo (scans, requisições HTTP, etc).")
    logger.warn("Só prossiga se você tiver autorização explícita e por escrito para testar este alvo.")
    resp = input("Confirma que possui autorização para testar este alvo? [Y/n] ")
    return resp.strip().lower() in CONFIRM_VALUES
