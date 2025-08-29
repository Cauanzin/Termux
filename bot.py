import logging
from telegram import Update, WebAppInfo, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler
import urllib.parse
import json

# Importa as funções de raspagem que já temos
from ia import raspar_jogos_do_dia

# Configuração de logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Seu token de acesso do BotFather
TOKEN = "7917940610:AAGbv48jGS3AUhC5Imh7Ck8OhZC6Raz4f2s"

# URL do seu Web App no GitHub Pages
WEB_APP_URL = "https://cauanzin.github.io/Termux/index.html"

# URLs de raspagem
URL_HOJE = "https://www.placardefutebol.com.br/jogos-de-hoje"
URL_AMANHA = "https://www.placardefutebol.com.br/jogos-de-amanha"

# Lista de campeonatos permitidos
CAMPEONATOS_PERMITIDOS = [
    "Copa do Brasil",
    "Campeonato Brasileiro - Série B",
    "Liga Europa da UEFA",
    "Liga Conferência Europa da UEFA",
    "Copa Argentina",
    "Campeonato Espanhol",
    "Campeonato Alemão - Bundesliga",
    "Campeonato Italiano",
    "Campeonato Francês",
    "Campeonato Português",
    "Campeonato Argentino",
    "Copa da Inglaterra",
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Função que responde ao comando /start com um botão que abre o Web App.
    """
    await update.message.reply_text("Buscando jogos...")
    
    # 1. Lista de jogos de teste - VAI IGNORAR O RASPADOR
    jogos_teste = [
        {"league": "Campeonato Teste", "time": "20:00", "teams": "Time A x Time B"},
        {"league": "Copa Teste", "time": "21:30", "teams": "Time C x Time D"},
        {"league": "Liga Teste", "time": "22:00", "teams": "Time E x Time F"},
    ]
    
    # 2. Converte a lista de jogos para uma string para passar na URL
    jogos_json = json.dumps(jogos_teste)
    jogos_str = urllib.parse.quote_plus(jogos_json)

    # 3. Cria a URL do Web App com os dados dos jogos como parâmetro
    web_app_url_com_dados = f"{WEB_APP_URL}?data={jogos_str}"

    # 4. Cria e envia o botão do Web App
    keyboard = [[InlineKeyboardButton("Analisar Jogos", web_app=WebAppInfo(url=web_app_url_com_dados))]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text("Clique no botão abaixo para abrir a nossa ferramenta de análise de jogos.", reply_markup=reply_markup)

# A função analisar_callback será removida/modificada no futuro
async def analisar_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pass

def main():
    """
    Função principal para rodar o bot.
    """
    application = ApplicationBuilder().token(TOKEN).build()

    start_handler = CommandHandler('start', start)
    analisar_handler = CallbackQueryHandler(analisar_callback, pattern=r'^analisar_jogo:')
    
    application.add_handler(start_handler)
    application.add_handler(analisar_handler)

    application.run_polling()
    
if __name__ == '__main__':
    main()

