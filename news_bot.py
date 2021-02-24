import datetime
import requests
from bs4 import BeautifulSoup
import telebot
from telebot import types
from decouple import config

bot = telebot.TeleBot(config('TOKEN'))

# parser

today = str(datetime.datetime.today()).split()[0]

url = 'https://kaktus.media/?date='+today+'&lable=8&order=main#paginator'

def get_html(url):
    res = requests.get(url).text
    return res


def get_titles(html):
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('div', class_ = 'cat_content').find_all('span', class_ = 'n')
    titles = []
    for i in table:
        try:
            title = i.text
            titles.append(title)
        except:
            title = 'no title'
    return titles[:20]


def get_links(html):
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('div', class_ = 'cat_content').find_all('div', class_ = 'f_medium')
    links = []
    for i in table:
        link = i.find('a').get('href')
        links.append(link)
    return links


def get_page_data(html):
    soup = BeautifulSoup(html, 'html.parser')
    description = soup.find('div', class_ = 'topic').find_all('p')
    txts = []
    for i in description:
        txt = i.text
        txts.append(txt)
    text_ = ' '.join(txts)
    return text_[:2000]


def get_page_img(html):
    soup = BeautifulSoup(html, 'html.parser')
    try:
        img = soup.find('div', id = 'topic').find_all('img')
        if len(img)>2:
            return img[2].get('src')
        else:
            return None
    except:
        img = ''


def titles():
    return get_titles(get_html(url))


#bot

titles = titles()
link = get_links(get_html(url))

keybord = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2, one_time_keyboard=True)
btn1 = types.KeyboardButton('Вернуться в главное меню')
btn2 = types.KeyboardButton('Выйти')
keybord.add(btn1, btn2)

nokeybord = types.InlineKeyboardMarkup(row_width=6)
btn1 = types.InlineKeyboardButton('1', callback_data='1')
btn2 = types.InlineKeyboardButton('2', callback_data='2')
btn3 = types.InlineKeyboardButton('3', callback_data='3')
btn4 = types.InlineKeyboardButton('4', callback_data='4')
btn5 = types.InlineKeyboardButton('5', callback_data='5')
btn6 = types.InlineKeyboardButton('->', callback_data='next1')
nokeybord.add(btn1, btn2, btn3, btn4, btn5, btn6)


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message('482090418', f'{message.chat.first_name}, старт')
    bot.send_message(message.chat.id, 'Здраствуйте', reply_markup=keybord)
    bot.send_message(message.chat.id, f'''Новости на сегодня:\n
1){titles[0]}\n\n2){titles[1]}\n\n3){titles[2]}\n
4){titles[3]}\n\n5){titles[4]}\n
Выберите по номеру интересующую статью''', reply_markup=nokeybord)


@bot.callback_query_handler(func=lambda c: True)
def inline(c):

    chat_id = c.message.chat.id

    if c.data.isdigit():
        bot.send_message('482090418', f'{c.message.chat.first_name}, статья')
        nokeybord = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton('Описание', callback_data=f'd{c.data}')
        btn2 = types.InlineKeyboardButton('Фото', callback_data=f'i{c.data}')
        nokeybord.add(btn1, btn2)
        bot.send_message(chat_id, f'{titles[int(c.data)-1]}\n\nВы можете просмотреть статью или фото на выбор', reply_markup=nokeybord)

    if c.data.startswith('d'):
        data_ = get_page_data(get_html(link[int(c.data[1])-1]))
        bot.send_message(chat_id, f'{data_}')
    if c.data.startswith('i'):
        try:
            data_ = get_page_img(get_html(link[int(c.data[1])-1]))
            if data_ != None:
                bot.send_photo(chat_id, data_)
            else:
                bot.send_message(chat_id, 'В этой статье нет фотографий')
        except:
            bot.send_message(chat_id, 'В этой статье нет фотографий')


    if c.data == "next1":
        nokeybord = types.InlineKeyboardMarkup(row_width=7)
        btn = types.InlineKeyboardButton('<-', callback_data='back1')
        btn1 = types.InlineKeyboardButton('6', callback_data='6')
        btn2 = types.InlineKeyboardButton('7', callback_data='7')
        btn3 = types.InlineKeyboardButton('8', callback_data='8')
        btn4 = types.InlineKeyboardButton('9', callback_data='9')
        btn5 = types.InlineKeyboardButton('10', callback_data='10')
        btn6 = types.InlineKeyboardButton('->', callback_data='next2')
        nokeybord.add(btn, btn1, btn2, btn3, btn4, btn5, btn6)
        bot.edit_message_text(f'''Новости на сегодня:\n
6){titles[5]}\n\n7){titles[6]}\n\n8){titles[6]}\n
9){titles[8]}\n\n10){titles[9]}\n
Выберите по номеру интересующую статью''', chat_id, c.message.message_id, reply_markup= nokeybord)

    if c.data == "back1":
        nokeybord = types.InlineKeyboardMarkup(row_width=6)
        btn1 = types.InlineKeyboardButton('1', callback_data='1')
        btn2 = types.InlineKeyboardButton('2', callback_data='2')
        btn3 = types.InlineKeyboardButton('3', callback_data='3')
        btn4 = types.InlineKeyboardButton('4', callback_data='4')
        btn5 = types.InlineKeyboardButton('5', callback_data='5')
        btn6 = types.InlineKeyboardButton('->', callback_data='next1')
        nokeybord.add(btn1, btn2, btn3, btn4, btn5, btn6)
        bot.edit_message_text(f'''Новости на сегодня:\n
1){titles[0]}\n\n2){titles[1]}\n\n3){titles[2]}\n
4){titles[3]}\n\n5){titles[4]}\n
Выберите по номеру интересующую статью''', chat_id, c.message.message_id, reply_markup= nokeybord)

    if c.data == "next2":
        nokeybord = types.InlineKeyboardMarkup(row_width=7)
        btn = types.InlineKeyboardButton('<-', callback_data='back2')
        btn1 = types.InlineKeyboardButton('11', callback_data='11')
        btn2 = types.InlineKeyboardButton('12', callback_data='12')
        btn3 = types.InlineKeyboardButton('13', callback_data='13')
        btn4 = types.InlineKeyboardButton('14', callback_data='14')
        btn5 = types.InlineKeyboardButton('15', callback_data='15')
        btn6 = types.InlineKeyboardButton('->', callback_data='next3')
        nokeybord.add(btn, btn1, btn2, btn3, btn4, btn5, btn6)
        bot.edit_message_text(f'''Новости на сегодня:\n
11){titles[10]}\n\n12){titles[11]}\n\n13){titles[12]}\n
14){titles[13]}\n\n15){titles[14]}\n
Выберите по номеру интересующую статью''', chat_id, c.message.message_id, reply_markup= nokeybord)

    if c.data == "back2":
        nokeybord = types.InlineKeyboardMarkup(row_width=7)
        btn = types.InlineKeyboardButton('<-', callback_data='back1')
        btn1 = types.InlineKeyboardButton('6', callback_data='6')
        btn2 = types.InlineKeyboardButton('7', callback_data='7')
        btn3 = types.InlineKeyboardButton('8', callback_data='8')
        btn4 = types.InlineKeyboardButton('9', callback_data='9')
        btn5 = types.InlineKeyboardButton('10', callback_data='10')
        btn6 = types.InlineKeyboardButton('->', callback_data='next2')
        nokeybord.add(btn, btn1, btn2, btn3, btn4, btn5, btn6)
        bot.edit_message_text(f'''Новости на сегодня:\n
6){titles[5]}\n\n7){titles[6]}\n\n3){titles[7]}\n
4){titles[8]}\n\n5){titles[9]}\n
Выберите по номеру интересующую статью''', chat_id, c.message.message_id, reply_markup= nokeybord)

    if c.data == "next3":
        nokeybord = types.InlineKeyboardMarkup(row_width=6)
        btn = types.InlineKeyboardButton('<-', callback_data='back3')
        btn1 = types.InlineKeyboardButton('16', callback_data='16')
        btn2 = types.InlineKeyboardButton('17', callback_data='17')
        btn3 = types.InlineKeyboardButton('18', callback_data='18')
        btn4 = types.InlineKeyboardButton('19', callback_data='19')
        btn5 = types.InlineKeyboardButton('20', callback_data='20')
        nokeybord.add(btn, btn1, btn2, btn3, btn4, btn5)
        bot.edit_message_text(f'''Новости на сегодня:\n
16){titles[15]}\n\n17){titles[16]}\n\n18){titles[17]}\n
19){titles[18]}\n\n20){titles[19]}\n
Выберите по номеру интересующую статью''', chat_id, c.message.message_id, reply_markup= nokeybord)

    if c.data == "back3":
        chat = c.message.chat.id
        nokeybord = types.InlineKeyboardMarkup(row_width=7)
        btn = types.InlineKeyboardButton('<-', callback_data='back2')
        btn1 = types.InlineKeyboardButton('11', callback_data='11')
        btn2 = types.InlineKeyboardButton('12', callback_data='12')
        btn3 = types.InlineKeyboardButton('13', callback_data='13')
        btn4 = types.InlineKeyboardButton('14', callback_data='14')
        btn5 = types.InlineKeyboardButton('15', callback_data='15')
        btn6 = types.InlineKeyboardButton('->', callback_data='next3')
        nokeybord.add(btn, btn1, btn2, btn3, btn4, btn5, btn6)
        bot.edit_message_text(f'''Новости на сегодня:\n
11){titles[10]}\n\n12){titles[11]}\n\n13){titles[12]}\n
14){titles[13]}\n\n15){titles[14]}\n
Выберите по номеру интересующую статью''', chat_id, c.message.message_id, reply_markup= nokeybord)
        

@bot.message_handler(content_types=['text'])
def send_text(message):
    chat_id = message.chat.id
    if message.text.title() == 'Выйти':
        bot.send_message('482090418', f'{message.chat.first_name}, выход')
        bot.send_message(chat_id, 'До свидания')
    if message.text == 'Вернуться в главное меню':
        bot.send_message('482090418', f'{message.chat.first_name}, меню')
        bot.send_message(message.chat.id, f'''Новости на сегодня:\n
1){titles[0]}\n\n2){titles[1]}\n\n3){titles[2]}\n
4){titles[3]}\n\n5){titles[4]}\n
Выберите по номеру интересующую статью''', reply_markup=nokeybord)



bot.polling()