import requests
from bs4 import BeautifulSoup

# URL do histórico de partidas do Bahia na Série A, no site da CBF
url_cbf = "https://www.cbf.com.br/futebol-brasileiro/times/campeonato-brasileiro/serie-a/2025/61377?tab=historico-de-partidas"

# Headers para simular um navegador real
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
    'Accept-Encoding': 'gzip, deflate, br'
}

try:
    response = requests.get(url_cbf, headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')

    # Encontrar todos os blocos de jogos
    # A classe 'styles_gameCardContainer__qbcs6' parece ser o contêiner de cada partida
    blocos_jogos = soup.find_all('div', class_='styles_gameCardContainer__qbcs6')

    if blocos_jogos:
        print("Histórico de jogos do Bahia encontrado:")
        print("-" * 30)
        for bloco in blocos_jogos:
            # Encontrar o placar
            # O placar está em um span com a classe 'styles_gol__wQ4q9'
            placares = bloco.find_all('span', class_='styles_gol__wQ4q9')
            placar1 = placares[0].text.strip() if len(placares) > 0 else 'N/A'
            placar2 = placares[1].text.strip() if len(placares) > 1 else 'N/A'

            # Encontrar os nomes dos times
            # O nome está no atributo 'title' da tag 'strong'
            times_nomes = bloco.find_all('strong')
            time1 = times_nomes[0]['title'] if len(times_nomes) > 0 else 'N/A'
            time2 = times_nomes[1]['title'] if len(times_nomes) > 1 else 'N/A'

            # Encontrar a data e a hora do jogo
            data_hora = bloco.find('p').text.strip().replace('\n', ' ').split('<br/>')
            data_jogo = data_hora[0].strip().split(' - ')[0] if data_hora else 'N/A'

            print(f"Data: {data_jogo}")
            print(f"Jogo: {time1} {placar1} x {placar2} {time2}")
            print("-" * 30)
    else:
        print("Não foram encontrados blocos de jogos.")

except requests.exceptions.RequestException as e:
    print(f"Erro ao acessar a URL: {e}")