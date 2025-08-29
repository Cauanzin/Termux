import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
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

async def handle_web_app_data(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Função que lida com a mensagem enviada pelo Web App.
    """
    if update.message.web_app_data and update.message.web_app_data.data == "ready":
        # Quando o Web App envia "ready", o bot envia os dados
        jogos_teste = [
            {"league": "Campeonato Teste", "time": "20:00", "teams": "Time A x Time B"},
            {"league": "Copa Teste", "time": "21:30", "teams": "Time C x Time D"},
            {"league": "Liga Teste", "time": "22:00", "teams": "Time E x Time F"},
        ]
        
        jogos_json = json.dumps(jogos_teste)
        
        # Envia os dados de volta para o Web App
        await update.message.reply_text("Buscando jogos...")
        await update.message.web_app_data.send_data(jogos_json)

def main():
    """
    Função principal para rodar o bot.
    """
    application = ApplicationBuilder().token(TOKEN).build()

    # O bot apenas espera pela mensagem "ready" do Web App
    web_app_handler = MessageHandler(filters.StatusUpdate.WEB_APP_DATA, handle_web_app_data)
    
    application.add_handler(web_app_handler)

    application.run_polling()
    
if __name__ == '__main__':
    main()
