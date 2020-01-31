from telebot import types
from config import bot, base_url, username, password

import json
import requests

#variaveis para guardar informações de ids
data = []
alarm = []
id_equip = []

# Obs: Os botões inline foram pensados colocando o parametro
# callback com uma string ou lista com parametros para que
# as funcões callback possam ser executadas

# Executa com comando /start
@bot.message_handler(commands=['start'])
def send_commands(message):
    keyboard = types.InlineKeyboardMarkup()
    msg = '''Bem vindo, para listar todos os equipamentos clique em *equip*
    '''

    # Insere um botão na tela que lista todos os equipamentos
    keyboard.add(
        types.InlineKeyboardButton(
            "equip",
            callback_data='equip'
        )
    )

    bot.send_message(
        message.chat.id,
        msg,
        reply_markup=keyboard,
        parse_mode='Markdown'
    )

# Não deixa qualquer comando que não seja /start executar, listando os equipamentos
@bot.message_handler(func=lambda message: True, content_types=['text'])
def default_command(message):
    # Verifica se algum comando foi executado
    if message.text != '' and message.text.strip()[:1] == '/':
        keyboard = types.InlineKeyboardMarkup()
        bot.send_message(
            message.chat.id,
            "*Comando invalido*\nFavor usar o menu\n\n",
            reply_markup=keyboard,
            parse_mode="MARKDOWN"
        )
        send_equipments(message)

# Lista todos os equipamentos que o usuario tem acesso
def send_equipments(message):
    keyboard = types.InlineKeyboardMarkup()
    response = requests.get(
        base_url + 'clps/', auth=requests.auth.HTTPBasicAuth(
            username, password
        )
    )
    equip = json.loads(response.content)
    # Lista todos os equipamentos como botões na tela
    for i in range(0, len(equip)):
        keyboard.add(
            types.InlineKeyboardButton(
                equip[i]['nome'],
                callback_data='equip_id{}'.format(equip[i]['id'])
            )
        )

    bot.send_message(
        message.chat.id,
        "*Lista de equipamentos liberada para acesso:*\n\n",
        reply_markup=keyboard,
        parse_mode="MARKDOWN"
    )

# Lista todos os dados que usuario tem acesso em relação ao Equipamento selecionado
def send_data(message, id):
    # obtem lista de equipamentos de um usuario
    keyboard = types.InlineKeyboardMarkup()
    response = requests.get(
        base_url + 'dados/',
        auth=requests.auth.HTTPBasicAuth(
            username,
            password
        )
    )
    data_equip = json.loads(response.content)
    string = ''
    data.clear()
    for i in range(0, len(data_equip)):
        data_config = data_equip[i]['config_dados']
        for d in range(0, len(data_equip[i]['config_dados'])):
            # Verifica se o id do equipamento essta correto
            if data_equip[i]['id'] == int(id):
                data.append('dados{}'.format(str(data_config[d]['id'])))
                # verifica se tem dados no equipamento
                if len(data_config[d]["dados"]) != 0:
                    keyboard.add(
                        types.InlineKeyboardButton(
                            data_config[d]['nome'],
                            callback_data=data[i]
                        )
                    )
                    string = "*Lista de dados liberada para acesso:*\n"
                else:
                    string = 'Listar de dados vazia'
    keyboard.row(
        # Volta para a listagem dos equipamentos
        types.InlineKeyboardButton(
            'Equipamentos',
            callback_data='equip'
        ),
        # Volta para o equipamento selecionado
        types.InlineKeyboardButton(
            'Voltar',
            callback_data='equip_id{}'.format(str(id_equip[0]))
        )
    )
    bot.send_message(
        message.chat.id,
        string,
        reply_markup=keyboard,
        parse_mode="MARKDOWN"
    )

# Lista um dado escolhido que usuario em relação ao Equipamento selecionado
def data_id(message, id):
    keyboard = types.InlineKeyboardMarkup()
    response = requests.get(
        base_url + 'dados/{0}/'.format(int(id)),
        auth=requests.auth.HTTPBasicAuth(
            username,
            password
        )
    )
    data_config = json.loads(response.content)

    # Verifica se existe algum dado no Id informado
    if bool(data_config):
        string = '*Dado:* {}\n'.format(data_config[0]['nome'])
        string += '*Unidade Eng.:* {}\n'.format(str(data_config[0]['unidade_eng']))
        string += '*Endereço:* {}\n'.format(str(data_config[0]['endereco']))
        string += '*Tamanho:* {}\n'.format(str(data_config[0]['tamanho']))
        string += '*Tipo:* {}\n'.format(data_config[0]['tipo'])
        if data_config[0]['dados']:
            string += '*Valor:* {}\n'.format(data_config[0]['dados'][0]['valor'])
            string += '*Data:* {}\n'.format(data_config[0]['dados'][0]['data_hora'])
    else:
        string = 'Id invalido'
    data.clear()
    data.append('dado{}'.format(data_config[0]['id']))
    keyboard.row(
        # Volta para listagem dos equipamentos
        types.InlineKeyboardButton(
            'Equipamentos',
            callback_data='equip'
        ),
        # Volta para a listagem dos dados do equipamento selecionado
        types.InlineKeyboardButton(
            'Voltar',
            callback_data=data[0]
        )
    )
    bot.send_message(
        message.chat.id,
        "*dados liberado para acesso*:\n\n{}".format(string),
        reply_markup=keyboard,
        parse_mode="MARKDOWN"
    )

# Lista todos os dados que usuario tem acesso em relação ao Equipamento selecionado
def send_alarms(message, id):
    keyboard = types.InlineKeyboardMarkup()
    response = requests.get(
        base_url + '/alarmes/',
        auth=requests.auth.HTTPBasicAuth(
            username,
            password
        )
    )
    alarm_equip = json.loads(response.content)
    string =''
    # Apaga a lista de alarmes para evitar duplicidade
    alarm.clear()
    for i in range(0, len(alarm_equip)):
        alarm_config = alarm_equip[i]["config_alarms"]
        # Verifica se o id do equipamento essta correto
        if alarm_equip[i]['id'] == int(id):
            for d in range(0, len(alarm_equip[i]['config_alarms'])):
                alarm.append('alarmes{}'.format(alarm_config[d]["id"]))
                # Verifica se tem alarmes no equipamento
                if len(str(alarm_config[d]["id"])) != 0:
                    keyboard.add(
                        types.InlineKeyboardButton(
                            alarm_config[d]['nome'],
                            callback_data=alarm[i]
                        )
                    )
                    string = "Lista de alarmes liberados para acesso:\n"
                else:
                    string = "*Lista de alarmes vazia:*"
    keyboard.row(
        # Volta para a listagem dos equipamentos
        types.InlineKeyboardButton(
            'Equipamentos',
            callback_data='equip'
        ),
        # Volta para o equipamento selecionado
        types.InlineKeyboardButton(
            'Voltar',
            callback_data='equip_id{}'.format(str(id_equip[0]))
        )
    )
    bot.send_message(
        message.chat.id,
        string,
        reply_markup=keyboard
    )

# Lista um alarme escolhido que usuario em relação ao Equipamento selecionado
def alarm_id(message, id):
    keyboard = types.InlineKeyboardMarkup()
    response = requests.get(
        base_url + 'alarmes/{0}/'.format(int(id)),
        auth=requests.auth.HTTPBasicAuth(
            username, password
        )
    )
    alarms = json.loads(response.content)
    string = ''
    # Verifica se existe alarme dado no Id informado
    if bool(alarms):
        string += '*Nome:* {}\n'.format(alarms[0]['dado_nome'])
        string += '*Valor atual:* {}\n'.format(
            str(alarms[0]['dado_valor_atual']))
        string += '*ondição de alarme:* {}\n'.format(
            alarms[0]['condicao'] + str(alarms[0]['limite']))
        if alarms[0]['habilita_reconhecimento']:
            if alarms[0]['estado_reconhecimento']:
                string += '*Reconhecido:* Sim\n'
            else:
                string += '*Reconhecido:* Não\n'
        else:
            string += '*Reconhecimento não habilitado*\n'
            string += '*Estado:* {}\n'.format(
                alarms[0]['alarm_state_identity_name'])
    else:
        string = 'Id do alarme invalido'
    alarm.clear()
    alarm.append('alarme{}'.format(str(id_equip[0])))
    keyboard.row(
        # Volta para a listagem de esquipamentos
        types.InlineKeyboardButton(
            'Equipamentos',
            callback_data='equip'
        ),
        # Volta para a lista de alarmes do equipamento selecionado
        types.InlineKeyboardButton(
            'Volta',
            callback_data=alarm[0]
        )
    )
    bot.send_message(
        message.chat.id,
        "*Alarme liberado para acesso:*\n\n{}".format(string),
        reply_markup=keyboard,
        parse_mode="MARKDOWN"
    )

@bot.callback_query_handler(lambda query: query.data in alarm)
def callback_alarms(query):
    # Faz a verificação do parametro passado chamando a função para informar o alarme pelo id
    if query.data.strip()[:7] == 'alarmes':
        alarm_id(
            query.message,
            query.data.strip()[7:]
        )
    # Caso não seja pelo id, chama a função que lista todos os alarmes
    else:
        send_alarms(
            query.message,
            query.data.strip()[6:]
        )

@bot.callback_query_handler(lambda query: query.data in data)
def callback_data(query):
    # Faz a verificação do parametro passado chamando a função para informar o dado pelo id
    if query.data.strip()[:5] == 'dados':
        data_id(
            query.message,
            query.data.strip()[5:]
        )
    # Caso não seja pelo id, chama a função que lista todos os dados
    else:
        send_data(
            query.message,
            query.data.strip()[4:]
        )

@bot.callback_query_handler(lambda query: query.data =='equip')
def callback_equips(query):
    # Chama a função que lista todos os equipamentos
    send_equipments(query.message)

@bot.callback_query_handler(lambda query: query.data.strip()[:8] == 'equip_id')
def callback_equip_id(query):

        keyboard = types.InlineKeyboardMarkup()
        response = requests.get(
            base_url + 'clps/{0}/'.format(int(query.data.strip()[8:])),
            auth=requests.auth.HTTPBasicAuth(
                username,
                password
            )
        )
        equip = json.loads(response.content)

        string = '*Equipamento:* {}\n'.format(equip['nome'])
        string += '*Localização:* {}\n'.format(equip['localizacao'])
        string += '*Estado:* {}\n '.format(equip['estado'])
        if equip['possui_alarmes_ativos']:
            string += '*Possui alarmes Ativos* \n'
            string += '*Quantidade de alarmes ativos:* {}\n'.format(
                equip['quantidade_alarmes_ativos'])
        else:
            string += '*Sem alarmes ativos*\n'

        if len(id_equip) < 2:
            id_equip.append(equip['id'])
        data.clear()
        alarm.clear()
        data.append('dado{}'.format(equip['id']))
        alarm.append('alarme{}'.format(equip['id']))
        keyboard.row(
            # Lista dados para o equipamento informado
            types.InlineKeyboardButton(
                'Dados',
                callback_data=data[0]
            ),
            # Lista alarmes para o equipamento informado
            types.InlineKeyboardButton(
                'Alarmes',
                callback_data=alarm[0]
            )
        )
        # Volta para a lista de equipamentos
        keyboard.row(
            types.InlineKeyboardButton(
                'Equipamentos',
                callback_data='equip'
            )
        )
        bot.send_message(
            query.message.chat.id,
            "*Equipamento liberado para acesso:*\n\n{}".format(string),
            reply_markup=keyboard,
            parse_mode='MARKDOWN'
        )

# Upon calling this function, TeleBot starts polling the Telegram servers for new messages.
# - none_stop: True/False (default False) - Don't stop polling when receiving an error from the Telegram servers
# - interval: True/False (default False) - The interval between polling requests
#           Note: Editing this parameter harms the bot's response time
# - timeout: integer (default 10) - Timeout in seconds for long polling.
bot.polling(none_stop=True, interval=0, timeout=10)