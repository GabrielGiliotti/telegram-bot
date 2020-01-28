# coding=utf-8
import telebot
import json
import requests
from telebot import types

# Insira o token aqui
bot = telebot.TeleBot("")

# dados basicos de acesso ao site desejado
username = u'example@example.com.br' # ou u'userExample'
password = u'example'
base_url = u'https://tecExample.com.br/rest/v0/' # Trocar pela url desejada

commands = {
    'start': 'Permite iniciar (e re-iniciar) meu funcionamento.',
    'help': 'Permite acesso à descrição de todos os comandos que posso realizar.',
    'equips': 'Premite a listagem de todos equipamentos disponiveis para o usuario.',
    'dados': 'Permite a listagem de todos os dados que um usuário tem acesso (Por Equipamento).',
    'alarmes': 'Premite a listagem de todos alarmes que um usuário tem acesso (Por Equipamento).',
    'contratos': 'Permite a exibição dos dados de contratos que o usuário tem com o site.',
    'info': 'Permite retornar informações de um equipamento, dado ou alarme especificado por ID. Para utilizar essa '
            + 'função digite "/info equip id" ou "/info dado id" ou "/info alarme id".',

}


# @bot.message_handler(commands=['help'])
# def send_commands(message):

#    msg = '''Os comandos acessiveis são os que estão abaixo,\n
#    Para encontrar qualquer item pelo seu Id ,é necessario digitar o comando especifico + espaço + o Id, por exemplo:\n
#    Para encontrar o equipamento de ID 3, tenho que digitar o comando /equip 3

#    markup = types.ReplyKeyboardMarkup(row_width=1)
#    item1 = types.KeyboardButton('/equip')
#    item2 = types.KeyboardButton('/dados')
#    item3 = types.KeyboardButton('/historico')
#    item4 = types.KeyboardButton('/alarmes')
#    markup.row(item1, item2)
#    markup.row(item3, item4)

#    bot.send_message(
#        message.chat.id,
#        msg,
#        reply_markup=markup
#    )

@bot.message_handler(commands=['start'])
def send_welcome(message):
    chatid = message.chat.id
    welcome_text = "Olá Cliente !. Sou seu novo Bot Telegram integrado ao Site Especificado !"
    welcome_text = welcome_text + "\n\nDigite o texto /help ou Clique no botao para saber mais sobre meu funcionamento."
    markup = types.ReplyKeyboardMarkup(row_width=1)
    item1 = types.KeyboardButton('Help')
    markup.add(item1)
    bot.send_message(chatid, welcome_text, reply_markup=markup)


@bot.message_handler(commands=['help'])
def send_help(message):
    chatid = message.chat.id
    help_text = "Os seguintes comandos estão disponiveis (via texto ou Botão): \n\n"
    for key in commands:  # Itera sobre a dict de commands definida
        help_text += "/" + key + " : "
        help_text += commands[key] + "\n"  # Monta (em help_text) um string de saida com as especificacoes dos comandos

    markup = types.ReplyKeyboardMarkup(row_width=1)
    item1 = types.KeyboardButton('Start')
    item2 = types.KeyboardButton('Help')
    item3 = types.KeyboardButton('Equips')
    item4 = types.KeyboardButton('Dados')
    item5 = types.KeyboardButton('Alarmes')
    item6 = types.KeyboardButton('Contratos')
    markup.row(item1, item2, item3) # Disposição dos botões
    markup.row(item4, item5, item6)
    bot.send_message(chatid, help_text, reply_markup=markup)  # faz envio


@bot.message_handler(commands=['equips'])
def send_equips(message):
    chatid = message.chat.id
    response = requests.get(base_url + 'clps/', auth=requests.auth.HTTPBasicAuth(username, password))
    dados = json.loads(response.content)

    string = ''
    for i in range(0, len(dados)):
        string += 'ID do Equip: ' + str(dados[i]['id']) + '\n' + \
                  'Nome do Equip: ' + dados[i]['nome'] + '\n' + 'Numero de Serie: ' + dados[i]['numero_serie'] + \
                  '\n\n'

    bot.send_message(chatid, 'Equips disponiveis: \n\n' + string)  # faz envio


@bot.message_handler(commands=['dados'])
def send_dados(message):
    chatid = message.chat.id
    # obtem lista de equipamentos de um usuario
    response = requests.get(base_url + 'dados/', auth=requests.auth.HTTPBasicAuth(username, password))
    equips = json.loads(response.content)  # lista de equipamentos

    string1 = ''
    for i in range(0, len(equips)):  # Percorre todos os equips
        data = equips[i]['config_dados']
        string1 += 'Nome do Equipa: ' + equips[i]['nome'] + '\n\n'
        for j in range(0, len(data)):
            if data[j]['dados']:
                string1 += 'ID do Dado: ' + str(data[j]['id']) + '\nNome do Dado: ' + \
                           data[j]['nome'] + '\nTipo do Dado: ' + data[j]['tipo'] + '\nValor do Dado: ' + \
                           data[j]['dados'][0]['valor'] + '\nData/Hora da última atualização: ' + \
                           data[j]['dados'][0]['data_hora'] + '\n\n'
            else:
                string1 += 'ID do Dado: ' + str(data[j]['id']) + '\nNome do Dado: ' + \
                           data[j]['nome'] + '\nTipo do Dado: ' + data[j]['tipo']

    bot.send_message(chatid, 'Dados disponíveis para acesso (Por Equip): \n\n\n' + string1)  # faz envio


@bot.message_handler(commands=['alarmes'])
def send_alarmes(message):
    chatid = message.chat.id
    # obtem lista de equipamentos de um usuario
    response = requests.get(base_url + 'alarmes/', auth=requests.auth.HTTPBasicAuth(username, password))
    equips = json.loads(response.content)  # lista de alarmes

    string = ''
    for i in range(0, len(equips)):  # Percorre todos os equips
        alarmes = equips[i]['config_alarms']
        string += 'Nome do Equipamento: ' + equips[i]['nome'] + '\n\n'
        for j in range(0, len(alarmes)):
            string += 'ID do Alarme: ' + str(alarmes[j]['id']) + '\nNome do Alarme: ' + alarmes[j]['nome'] + \
                      '\nID do Dado Associado ao Alarme: ' + str(
                alarmes[j]['config_dado']) + '\nNome do Dado Associado' + \
                      alarmes[j]['dado_nome'] + '\nValor atual do dado: ' + str(alarmes[j]['dado_valor_atual']) + \
                      '\nCondição de acionamento: ' + str(
                alarmes[j]['condicao']) + '\nValor limite para acionamento: ' + \
                      str(alarmes[j]['limite']) + '\n\n'

    bot.send_message(chatid, 'Alarmes disponveis para acesso (Por Equipamento): \n\n\n' + string)  # faz envio


@bot.message_handler(commands=['contratos'])
def send_contratos(message):
    chatid = message.chat.id
    response = requests.get(base_url + 'contratos/', auth=requests.auth.HTTPBasicAuth(username, password))
    dadoscontrato = json.loads(response.content)
    string = ''
    for i in range(0, len(dadoscontrato)):
        #try:
            string += 'Dados de Contratos:\n\nID do Contrato: ' + str(dadoscontrato[i]['id']) + '\nEstado do contrato: ' \
                      + dadoscontrato[i]['estado'] + '\nData de Inicio do contrato: ' + dadoscontrato[i]['inicio'] + \
                      '\nData de Validade do contrato: ' + dadoscontrato[i]['validade'] + '\nN° máximo de equips permitdos: ' \
                      + str(dadoscontrato[i]['max_equipamentos']) + '\nN° máximo de equips de terceiros: ' + \
                      str(dadoscontrato[i]['max_equipamentos_terceiros']) + '\nN° máximo de dados: ' + \
                      str(dadoscontrato[i]['max_dados']) + '\nN° máximo de alarmes: ' + str(dadoscontrato[i]['max_alarmes']) + \
                      '\nN° máximo de históricos: ' + str(dadoscontrato[i]['max_historicos']) + '\nTipo de Plano: ' + \
                      dadoscontrato[i]['plano'] + '\nValor do plano: ' + dadoscontrato[i]['valor'] + '\nSeu saldo atual: ' + \
                      dadoscontrato[i]['saldo'] + '\n'
        #except:
            #string += 'Nenhum contrato foi encontrado.'

    bot.send_message(chatid, string)



def extract_arg(arg):
    return arg.split()[1:]


@bot.message_handler(commands=['info'])
def send_infos(message):
    if bool(extract_arg(message.text)):
        tipo = extract_arg(message.text)[0]
        if tipo == 'equip':
            if len(extract_arg(message.text)) == 2:
                idinp = extract_arg(message.text)[1]
                response = requests.get(base_url + 'clps/{0}/'.format(int(idinp)),
                                        auth=requests.auth.HTTPBasicAuth(username, password))
                dado = json.loads(response.content)
                string = ''
                try:
                    string += 'ID do Equip: ' + str(dado['id']) + '\nNome do Equip: ' + dado['nome'] + \
                              '\nNumero de Serie do Equip: ' + dado['numero_serie'] + '\n'
                    bot.send_message(message.chat.id, 'Informações do Equip:\n\n' + string)
                except:
                    string += 'Equip não encontrado.'
                    bot.send_message(message.chat.id, string)
            else:
                bot.send_message(message.chat.id, "Parâmetro ID não informado.")

        elif tipo == 'dado':
            if len(extract_arg(message.text)) == 2:
                idinp = extract_arg(message.text)[1]
                response = requests.get(base_url + 'dados/{0}/'.format(int(idinp)),
                                        auth=requests.auth.HTTPBasicAuth(username, password))
                dado = json.loads(response.content)
                string = ''
                if bool(dado):
                    string += 'Informações do Dado:\n\n' + 'Nome Dado: ' + dado[0]['nome'] + '\n' \
                              + 'Tipo do Dado: ' + dado[0]['tipo'] + '\n'
                    for i in range(0, len(dado[0]['dados'])):
                        string += 'Valor do dado: ' + dado[0]['dados'][i]['valor'] + '\n' \
                                  + 'Data/Hora da ultima atualização: ' + dado[0]['dados'][i]['data_hora'] + '\n'
                        bot.send_message(message.chat.id, string)
                else:
                    bot.send_message(message.chat.id, "Dado não encontrado.")
            else:
                bot.send_message(message.chat.id, "Parâmetro ID não informado.")

        elif tipo == 'alarme':
            if len(extract_arg(message.text)) == 2:
                idinp = extract_arg(message.text)[1]
                response = requests.get(base_url + 'alarmes/{0}/'.format(int(idinp)),
                                        auth=requests.auth.HTTPBasicAuth(username, password))
                dado = json.loads(response.content)
                string = ''
                if bool(dado):
                    string += 'Informações do Alarme:\n\n'
                    for i in range(0, len(dado)):
                        string += 'Nome do Alarme: ' + dado[0]['nome'] + '\nValor que aciona alarme: ' + \
                                  str(dado[0]['dado_valor_atual']) + '\nCondicao de acionamento do alarme: ' + \
                                  dado[0]['condicao'] + '\nValor limite para acionamento do alarme: ' + \
                                  str(dado[0]['limite']) + '\n'
                        bot.send_message(message.chat.id, string)
                else:
                    bot.send_message(message.chat.id, "Alarme não encontrado.")
            else:
                bot.send_message(message.chat.id, "Parâmetro ID não informado.")
        else:
            bot.send_message(message.chat.id, "Parâmetro (equip/dado/alarme) não informado ou inexistente. ")
    else:
        bot.send_message(message.chat.id, "Nenhum parâmetro foi informado para o comando.")


@bot.message_handler(func=lambda m: True, content_types=['text'])
def echo_all(message):
    if message.text == 'Start':
        send_welcome(message)
    if message.text == 'Help':
        send_help(message)
    if message.text == 'Equips':
        send_equips(message)
    if message.text == 'Dados':
        send_dados(message)
    if message.text == 'Alarmes':
        send_alarmes(message)
    if message.text == 'Contratos':
        send_contratos(message)


bot.polling()
