import requests
from bs4 import BeautifulSoup
import logging

def raspar_jogos_do_dia(url, campeonatos_permitidos):
    """
    Função que raspa o site de jogos, buscando por partidas nos campeonatos permitidos.
    """
    jogos = []
    try:
        logging.info(f"Iniciando a raspagem de jogos em {url}...")
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        # Encontra todos os blocos de jogos
        partidas_hoje = soup.find_all('div', class_='partida-item')

        for partida in partidas_hoje:
            liga_element = partida.find('div', class_='liga-item')
            if liga_element:
                liga_nome = liga_element.find('span', class_='text-bold').get_text(strip=True)
                
                # Filtra os jogos pelos campeonatos permitidos
                if liga_nome in campeonatos_permitidos:
                    hora_element = partida.find('div', class_='text-time').find('span')
                    hora = hora_element.get_text(strip=True) if hora_element else "Não definido"
                    
                    time_a_element = partida.find('div', class_='time-a')
                    time_b_element = partida.find('div', class_='time-b')

                    time_a = time_a_element.find('span', class_='text-bold').get_text(strip=True) if time_a_element else "Time A"
                    time_b = time_b_element.find('span', class_='text-bold').get_text(strip=True) if time_b_element else "Time B"
                    
                    jogo = {
                        "league": liga_nome,
                        "time": hora,
                        "teams": f"{time_a} x {time_b}"
                    }
                    jogos.append(jogo)
        
        logging.info(f"Raspagem de {len(jogos)} jogos concluída para {url}.")
        return jogos
    
    except requests.exceptions.RequestException as e:
        logging.error(f"Erro na requisição: {e}")
        return []
