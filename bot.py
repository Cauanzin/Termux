import logging
from telegram import Update, WebAppInfo, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler

# Importa a função de raspagem do seu script 'ia.py'
from ia import raspar_jogos_do_dia

# Configuração de logging para ver as atividades do bot
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Seu token de acesso do BotFather
TOKEN = "7917940610:AAGbv48jGS3AUhC5Imh7Ck8OhZC6Raz4f2s"

# URL do seu Web App
# ATENÇÃO: A URL abaixo precisa ser alterada.
# Por enquanto, use "https://google.com" apenas para testar o botão.
# Depois, vamos usar um servidor local.
WEB_APP_URL = "https://192.168.1.104:8000/index.html"

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
    keyboard = [[InlineKeyboardButton("Analisar Jogos", web_app=WebAppInfo(url=WEB_APP_URL))]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text("Clique no botão abaixo para abrir a nossa ferramenta de análise de jogos.", reply_markup=reply_markup)

async def analisar_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Esta função será removida ou modificada no futuro
    # Por enquanto, a deixamos aqui para evitar erros
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