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
    Função que lida com a mensagem de ação enviada pelo Web App.
    """
    if update.message.web_app_data:
        try:
            data = json.loads(update.message.web_app_data.data)
            
            if data.get("action") == "analyze":
                teams = data.get("teams")
                league = data.get("league")
                
                # Aqui você executaria a análise real
                await update.message.reply_text(f"Analisando o jogo: {teams} da {league}...")
                
                # Exemplo de resultado de análise
                analysis_result = {
                    "teams": teams,
                    "analysis": "Análise de teste concluída! A IA identificou uma boa oportunidade de Over 2.5 gols com base nas estatísticas recentes."
                }
                
                analysis_json = json.dumps(analysis_result)
                
                # Envia o resultado de volta para o Web App
                await update.message.web_app_data.send_data(analysis_json)
        except json.JSONDecodeError:
            # Caso a mensagem não seja um JSON válido (ex: "ready")
            pass

def main():
    """
    Função principal para rodar o bot.
    """
    application = ApplicationBuilder().token(TOKEN).build()
    web_app_handler = MessageHandler(filters.StatusUpdate.WEB_APP_DATA, handle_web_app_data)
    application.add_handler(web_app_handler)
    application.run_polling()
    
if __name__ == '__main__':
    main()
