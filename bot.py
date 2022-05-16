import telebot, requests, time, threading, os

admin = ["563330939"]
file = open("ids.txt", 'r')
idsAll = []
for i in file.readlines():
    idsAll.append(i.replace('\n', ''))
file.close()

print (idsAll)

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
            for i in idsAll:
                bot.send_message(i, newRef)

        time.sleep(120)

bot = telebot.TeleBot('5319148067:AAG9FJP6kWK8W12qHUKGpeFCRYYiKXPPvRA')
# Функция, обрабатывающая команду /start
@bot.message_handler(commands=["start"])
def start(m, res=False):
    bot.send_message(m.chat.id, 'Чтобы получать расписание МГКИТ напишите "Да", чтобы больше не получать "Нет"')
# Получение сообщений от юзера
@bot.message_handler(content_types=["text"])
def handle_text(message):
    if message.text.lower()=="да":
        
        if str(message.chat.id) not in idsAll:
            idsAll.append(str(message.chat.id))
            f = open("ids.txt", "r+")
            f.write(str(message.chat.id)+'\n')
            f.close()
            bot.send_message(message.chat.id, "Вы подписались на рассылку")
        else:
            bot.send_message(message.chat.id, "Вы уже были подписаны на рассылку")
    elif message.text.lower()=="нет":
        if str(message.chat.id) in idsAll:
            idsAll.remove(str(message.chat.id))
            f = open("ids.txt", 'w')
            for i in idsAll:
                f.write(i+'\n')
            f.close()
            bot.send_message(message.chat.id, "Вы отписались от рассылки")
        else:
            bot.send_message(message.chat.id, "Вы уже были отписаны от рассылки")
    elif (message.text.lower()=="рассылка")and(str(message.chat.id)) in admin:
        for i in idsAll:
            bot.send_message(i, 'Тест')
    else:
        bot.send_message(message.chat.id, 'Чтобы получать расписание МГКИТ напишите "Да", чтобы больше не получать "Нет"')

# Запускаем бота
t1 = threading.Thread(target=hhh, args=())
t1.start()
bot.polling(none_stop=True, interval=0)