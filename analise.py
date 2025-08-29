import requests
from bs4 import BeautifulSoup
import re

# Dicionário para mapear os nomes dos times entre a CBF e o Placar de Futebol
mapa_times = {
    'Atlético Mineiro Saf': 'atletico-mg',
    'Santos Fc': 'santos',
    'Fortaleza Ec Saf': 'fortaleza',
    'Bahia': 'bahia',
    'Corinthians': 'corinthians',
    'Fluminense': 'fluminense',
    'Sport': 'sport',
    'Juventude': 'juventude',
    'Red Bull Bragantino': 'bragantino',
    'São Paulo': 'sao-paulo',
    'Grêmio': 'gremio',
    'Vitória': 'vitoria',
    'Flamengo': 'flamengo',
    'Botafogo': 'botafogo',
    'Palmeiras': 'palmeiras',
    'Ceará': 'ceara',
    'Cruzeiro Saf': 'cruzeiro',
    'Mirassol': 'mirassol',
    'Paysandu': 'paysandu',
    'The Strongest': 'the-strongest',
    'Boston River': 'boston-river',
    'Internacional': 'internacional',
    'Nacional': 'nacional',
    'Atletico Nacional': 'atletico-nacional',
    'América de Cali': 'america-de-cali',
    'Retro FC': 'retro-fc',
    'Vasco da Gama': 'vasco-da-gama'
}

# Função para raspar os jogos da página da CBF usando HTML
def raspar_jogos_cbf(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br'
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        blocos_jogos = soup.find_all('div', class_='styles_gameCardContainer__qbcs6')

        lista_jogos = []
        for bloco in blocos_jogos:
            data_jogo_bruta = bloco.find('p').text.strip().split(' - ')[0] if bloco.find('p') else 'N/A'
            times_nomes = [strong['title'] for strong in bloco.find_all('strong')]

            if len(times_nomes) >= 2:
                lista_jogos.append({
                    'data': data_jogo_bruta,
                    'time_casa_bruto': times_nomes[0],
                    'time_fora_bruto': times_nomes[1],
                    'campeonato': 'Campeonato Brasileiro'
                })
        return lista_jogos

    except requests.exceptions.RequestException as e:
        print(f"Erro ao acessar a URL da CBF: {e}")
        return []

# Função para raspar as estatísticas de um jogo no Placar de Futebol
def raspar_stats_placarfutebol(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br'
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        tabela_estatisticas = soup.find('table', class_='table standing-table')

        if tabela_estatisticas:
            dados_jogo = {}
            linhas = tabela_estatisticas.find_all('tr')
            for linha in linhas:
                colunas = linha.find_all('td')
                if len(colunas) == 3:
                    categoria = colunas[1].find('small').text.strip() if colunas[1].find('small') else ''
                    valor_time_casa = colunas[0].find('small').text.strip() if colunas[0].find('small') else 'N/A'
                    valor_time_visitante = colunas[2].find('small').text.strip() if colunas[2].find('small') else 'N/A'
                    dados_jogo[categoria] = {'casa': valor_time_casa, 'fora': valor_time_visitante}
            return dados_jogo

    except requests.exceptions.HTTPError as e:
        print(f"  Erro HTTP ao acessar a URL: {e}")
        return None
    except Exception as e:
        print(f"  Ocorreu um erro ao raspar a página do jogo: {e}")
        return None

# --- Main Script ---

URL_CBF = "https://www.cbf.com.br/futebol-brasileiro/times/campeonato-brasileiro/serie-a/2025/61377?tab=historico-de-partidas"
URL_BASE_PLACARFUTEBOL = "https://www.placardefutebol.com.br/"

print("Iniciando a raspagem de dados...")
print("1. Pegando lista de jogos da CBF...")

jogos_cbf = raspar_jogos_cbf(URL_CBF)

if jogos_cbf:
    print(f"Lista de jogos encontrada. Processando {len(jogos_cbf)} partidas.")
    print("-" * 50)
    for jogo in jogos_cbf:
        data_formatada = jogo['data'].replace('/', '-')

        time_casa_puro = jogo['time_casa_bruto']
        time_fora_puro = jogo['time_fora_bruto']
        campeonato_puro = jogo['campeonato']

        campeonato_slug = 'brasileirao-serie-a'

        time_casa_slug = mapa_times.get(time_casa_puro, re.sub(r'[^a-zA-Z0-9]', '', time_casa_puro).lower().replace(' ', '-'))
        time_fora_slug = mapa_times.get(time_fora_puro, re.sub(r'[^a-zA-Z0-9]', '', time_fora_puro).lower().replace(' ', '-'))

        url_completa = f"{URL_BASE_PLACARFUTEBOL}{campeonato_slug}/{data_formatada}-{time_casa_slug}-x-{time_fora_slug}.html"

        print(f"Analisando o jogo: {jogo['data']} - {time_casa_puro} x {time_fora_puro} ({campeonato_puro})")
        print(f"URL de estatísticas: {url_completa}")

        stats = raspar_stats_placarfutebol(url_completa)

        if stats:
            # Imprimir as estatísticas mais importantes
            escanteios = stats.get('Escanteios')
            chutes_no_gol = stats.get('Chutes no gol')
            total_chutes = stats.get('Total de chutes')
            faltas = stats.get('Faltas cometidas')
            posse_bola = stats.get('Posse de bola (%)')
            total_passes = stats.get('Total de passes')

            print(f"  Escanteios: {escanteios['casa']} ({time_casa_puro}) vs {escanteios['fora']} ({time_fora_puro})")
            print(f"  Chutes no gol: {chutes_no_gol['casa']} ({time_casa_puro}) vs {chutes_no_gol['fora']} ({time_fora_puro})")
            print(f"  Total de chutes: {total_chutes['casa']} ({time_casa_puro}) vs {total_chutes['fora']} ({time_fora_puro})")
            print(f"  Faltas: {faltas['casa']} ({time_casa_puro}) vs {faltas['fora']} ({time_fora_puro})")
            print(f"  Posse de bola: {posse_bola['casa']}% ({time_casa_puro}) vs {posse_bola['fora']}% ({time_fora_puro})")
            print(f"  Total de passes: {total_passes['casa']} ({time_casa_puro}) vs {total_passes['fora']} ({time_fora_puro})")

        else:
            print("  Não foi possível obter as estatísticas do jogo.")

        print("-" * 50)
else:
    print("Não foi possível obter a lista de jogos da CBF.")
