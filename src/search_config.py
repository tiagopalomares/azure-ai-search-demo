import os
import logging
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from dotenv import load_dotenv

# Configurar o logging
logging.basicConfig(level=logging.INFO)

# Carregar variáveis do .env
load_dotenv()

# Configurar credenciais
search_endpoint = os.getenv("AZURE_SEARCH_ENDPOINT")
search_key = os.getenv("AZURE_SEARCH_KEY")
index_name = os.getenv("AZURE_SEARCH_INDEX")

# Verificar se as variáveis de ambiente foram carregadas corretamente
if not all([search_endpoint, search_key, index_name]):
    raise ValueError("Faltando uma ou mais variáveis de ambiente: AZURE_SEARCH_ENDPOINT, AZURE_SEARCH_KEY, AZURE_SEARCH_INDEX")

# Criar cliente de pesquisa
search_client = SearchClient(endpoint=search_endpoint, index_name=index_name, credential=AzureKeyCredential(search_key))

# Função para realizar busca e exibir resultados
def search_documents(search_term: str, top_results: int = 10):
    logging.info(f"Realizando busca pelo termo: {search_term}")
    try:
        results = search_client.search(search_text=search_term, top=top_results)
        results = list(results)
        logging.info(f"Total de documentos encontrados para '{search_term}': {len(results)}")
        if len(results) == 0:
            logging.info(f"Nenhum documento encontrado para '{search_term}'.")
        for result in results:
            # Aqui, acessamos o conteúdo e a localização, que são campos válidos nos documentos
            content = result.get('content', 'Sem conteúdo disponível')
            locations = result.get('locations', 'Sem localização especificada')
            logging.info(f"Conteúdo: {content}")
            logging.info(f"Localizações: {locations}")
    except Exception as e:
        logging.error(f"Erro ao buscar pelo termo '{search_term}': {e}")

# Loop interativo para o usuário inserir os termos de pesquisa
while True:
    search_term = input("Digite o termo de pesquisa (ou 'sair' para encerrar): ").strip()
    if search_term.lower() == 'sair':
        logging.info("Encerrando a pesquisa.")
        break
    elif search_term:
        search_documents(search_term)
    else:
        logging.info("Termo de pesquisa vazio. Tente novamente.")
