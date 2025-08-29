import requests
from bs4 import BeautifulSoup

# URL do jogo específico no Placar de Futebol
url_jogo = "https://www.placardefutebol.com.br/brasileirao-serie-a/24-08-2025-bahia-x-santos.html"

# Headers para simular um navegador
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
    'Accept-Encoding': 'gzip, deflate, br'
}

try:
    response = requests.get(url_jogo, headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')

    # Encontrar a tabela de estatísticas
    tabela_estatisticas = soup.find('table', class_='table standing-table')

    if tabela_estatisticas:
        # Encontrar todas as linhas da tabela (<tr>)
        linhas = tabela_estatisticas.find_all('tr')
        
        dados_jogo = {}

        for linha in linhas:
            # Encontrar as colunas (<td>) em cada linha
            colunas = linha.find_all('td')
            if len(colunas) == 3:
                # O nome da estatística está na coluna do meio
                categoria_tag = colunas[1].find('small')
                if categoria_tag:
                    categoria = categoria_tag.text.strip()
                    
                    # O valor dos times está nas colunas laterais
                    valor_time_casa_tag = colunas[0].find('small')
                    valor_time_visitante_tag = colunas[2].find('small')
                    
                    if valor_time_casa_tag and valor_time_visitante_tag:
                        valor_time_casa = valor_time_casa_tag.text.strip()
                        valor_time_visitante = valor_time_visitante_tag.text.strip()
                        
                        dados_jogo[categoria] = {
                            "Bahia": valor_time_casa,
                            "Santos": valor_time_visitante
                        }

        # Imprimir os dados de escanteios
        escanteios = dados_jogo.get('Escanteios')
        if escanteios:
            print("Estatísticas do jogo:")
            print(f"Bahia x Santos")
            print(f"Escanteios: Bahia {escanteios['Bahia']} | Santos {escanteios['Santos']}")
            print(f"Total de escanteios: {int(escanteios['Bahia']) + int(escanteios['Santos'])}")
        else:
            print("Dados de escanteios não encontrados.")
            
        # Imprimir outras estatísticas importantes
        chutes_no_gol = dados_jogo.get('Chutes no gol')
        if chutes_no_gol:
            print(f"Chutes no gol: Bahia {chutes_no_gol['Bahia']} | Santos {chutes_no_gol['Santos']}")
            
        faltas_cometidas = dados_jogo.get('Faltas cometidas')
        if faltas_cometidas:
            print(f"Faltas cometidas: Bahia {faltas_cometidas['Bahia']} | Santos {faltas_cometidas['Santos']}")
            
    else:
        print("Tabela de estatísticas não encontrada.")

except requests.exceptions.RequestException as e:
    print(f"Erro ao acessar a URL: {e}")
except Exception as e:
    print(f"Ocorreu um erro: {e}")

