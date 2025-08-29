import requests
from bs4 import BeautifulSoup
import re

def raspar_pagina(url):
    """Função genérica para raspar uma URL."""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br'
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return BeautifulSoup(response.text, 'html.parser')
    except requests.exceptions.RequestException as e:
        print(f"Erro ao acessar a URL {url}: {e}")
        return None

def raspar_jogos_do_dia(url):
    """
    Raspa a lista de jogos de uma página do Placar de Futebol.
    """
    print(f"Iniciando a raspagem de jogos em {url}...")
    soup = raspar_pagina(url)
    
    if not soup:
        return []

    lista_jogos = []
    
    # Encontra todos os blocos de jogos
    blocos_ligas = soup.find_all('a', href=re.compile(r'/[a-z0-9\-]+$'))
    
    for bloco in blocos_ligas:
        if bloco.find('h3', class_='match-list_league-name'):
            campeonato = bloco.find('h3', class_='match-list_league-name').text.strip()
            
            # Encontra os jogos dentro de cada bloco de liga
            parent_div = bloco.find_next_sibling('div', class_='container content')
            jogos_da_liga = parent_div.find_all('a', href=re.compile(r'/[a-z0-9\-]+/\d{2}-\d{2}-\d{4}'))
            
            for jogo_tag in jogos_da_liga:
                times_tags = jogo_tag.find_all('h5', class_='team_link')
                
                if len(times_tags) == 2:
                    time_casa = times_tags[0].text.strip()
                    time_fora = times_tags[1].text.strip()
                    url_partida = "https://www.placardefutebol.com.br" + jogo_tag['href']
                    
                    data_hora_tag = jogo_tag.find('span', class_='status-name')
                    data_hora = data_hora_tag.text.strip() if data_hora_tag else "N/A"
                    
                    lista_jogos.append({
                        'campeonato': campeonato,
                        'time_casa': time_casa,
                        'time_fora': time_fora,
                        'data_hora': data_hora,
                        'url_placarfutebol': url_partida
                    })

    return lista_jogos

# --- Main Script ---
URL_HOJE = "https://www.placardefutebol.com.br/jogos-de-hoje"
URL_AMANHA = "https://www.placardefutebol.com.br/jogos-de-amanha"

jogos_hoje = raspar_jogos_do_dia(URL_HOJE)
jogos_amanha = raspar_jogos_do_dia(URL_AMANHA)

jogos_completos = jogos_hoje + jogos_amanha

if jogos_completos:
    print("\nLista de jogos encontrados:")
    print("-" * 50)
    for i, jogo in enumerate(jogos_completos):
        print(f"{i+1}. {jogo['campeonato']}: {jogo['time_casa']} x {jogo['time_fora']}")
        print(f"   Data: {jogo['data_hora']}")
        print(f"   URL: {jogo['url_placarfutebol']}")
    print("-" * 50)
else:
    print("Nenhum jogo encontrado nas páginas de hoje ou amanhã.")

