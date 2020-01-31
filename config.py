import telebot

#configuração do TOKEN do bot gerado no BotFather
bot = telebot.TeleBot("")

#dados de acesso ao Portal
username = 'exemplo.exemplo@exemplo.com.br'
password = 'exemploExemplo'
version = 'v1' # v2, v3 ... vn
base_url = 'https://exemplo.tecnology.com.br/rest/{}/'.format(version)