import telebot, requests, time, threading, os

#admin = "id tg"

def hhh():
    while True:
        req = requests.get("https://www.mgkit.ru/studentu/raspisanie-zanatij").text
        req = req[req.find("Изменения в расписании"):req.find("Подписывайтесь")]
        req = req.split('"')
        refs = []
        for i in req:
            if i[:4]=="http":
                if refs.count(i)==0:
                    refs.append(i)

        inFile = ""

        for i in refs:
            inFile += i + '\n'

        os.remove("2.txt")
        os.rename("1.txt", "2.txt")

        text1 = open("1.txt", "w+")
        text1.write(inFile)
        text1.close()

        fileText = open("1.txt", "r")
        txt1 = fileText.readlines()
        fileText.close()
        fileText = open("2.txt", "r")
        txt2 = fileText.readlines()
        fileText.close()

        if txt1 != txt2:
            newRefs = []
            for i in txt1:
                if txt2.count(i)==0:
                    newRefs.append(i)
            newRef = newRefs[0]
            idsFile = open("ids.txt", "r")
            ids = idsFile.readlines()
            idsFile.close()
            for i in ids:
                bot.send_message(i.replace("\n", ''), newRef)

        time.sleep(120)

bot = telebot.TeleBot('token')
# Функция, обрабатывающая команду /start
@bot.message_handler(commands=["start"])
def start(m, res=False):
    bot.send_message(m.chat.id, 'Чтобы получать расписание МГКИТ напишите "Да", чтобы больше не получать "Нет"')
# Получение сообщений от юзера
@bot.message_handler(content_types=["text"])
def handle_text(message):
    if message.text.lower()=="да":
        f = open("ids.txt", "r+")
        if str(message.chat.id)+"\n" not in f.readlines():
            f.write(str(message.chat.id)+'\n')
        f.close()
        bot.send_message(message.chat.id, "Вы подписались или уже были подписаны на рассылку")
    elif message.text.lower()=="нет":
        f = open("ids.txt", "r+")
        if str(message.chat.id)+"\n" in f.readlines():
            f.close()
            f = open("ids.txt", "r+")
            text = f.read()
            f.close()
            os.remove("ids.txt")
            f = open("ids.txt", 'w')
            print(text)
            f.write(text.replace(str(message.chat.id)+"\n", ''))
        f.close()
        bot.send_message(message.chat.id, "Вы отписались или уже были отписаны от рассылки")
    elif (message.text.lower()=="рассылка")and(str(message.chat.id))==admin:
        file = open('ids.txt', 'r+')
        text = file.readlines()
        file.close()
        for i in text:
            print(i.replace('\n', ''))
            bot.send_message(i.replace('\n', ''), 'Тест')
    else:
        bot.send_message(message.chat.id, 'Чтобы получать расписание МГКИТ напишите "Да", чтобы больше не получать "Нет"')

# Запускаем бота
t1 = threading.Thread(target=hhh, args=())
t1.start()
bot.polling(none_stop=True, interval=0)