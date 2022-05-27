import telebot, requests, time, threading, os

admin = ["id"] # Тут должен быть id администратора
token = "token" # Тут должен быть токен бота
file = open("ids.txt", 'r')
idsAll = []
for i in file.readlines():
    idsAll.append(i.replace('\n', ''))
file.close()

print (idsAll)

def hhh():
    while True:
        hour = time.localtime(time.time()).tm_hour 
        if hour >= 10 and hour < 22:
            req = requests.get("https://github.com").text # Тут должна быть ссылка на сайт, который надо обновлять
            req = req[req.find("от"):req.find("до")] # Ограничения поиска по HTML сайта
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

            with open("1.txt", "w+") as text1:
                text1.write(inFile)

            with open("1.txt", "r") as fileText:
                txt1 = fileText.readlines()
            with open("2.txt", "r") as fileText:
                txt2 = fileText.readlines()

            if txt1 != txt2:
                newRefs = []
                for i in txt1:
                    if txt2.count(i)==0:
                        newRefs.append(i)
                newRef = newRefs[0]
                for i in idsAll:
                    try:
                        bot.send_message(i, newRef)
                    except:
                        bot.send_message(admin[0], f'Не удалось отправить пользователю {i}')
                        idsAll.remove(i)
                        with open('ids.txt', 'w') as f:
                            for n in idsAll:
                                f.write(n)

        time.sleep(120) # Период обновления

bot = telebot.TeleBot(token)

@bot.message_handler(commands=["start"])
def handle_command(command, res=False):
    bot.send_message(command.chat.id, 'Чтобы получать рассылку напишите "/yes", чтобы больше не получать "/no"') # Тут должно быть дефолтное сообщение

@bot.message_handler(commands=["yes"])
def handle_command(message, res=False):
    if str(message.chat.id) not in idsAll:
        idsAll.append(str(message.chat.id))
        with open("ids.txt", "a") as f:
            f.write(str(message.chat.id)+'\n')
        bot.send_message(message.chat.id, "Вы подписались на рассылку")
        bot.send_message(admin[0], f"Новый пользователь: {message.chat.username}[{message.chat.id}]")
    else:
        bot.send_message(message.chat.id, "Вы уже были подписаны на рассылку")

@bot.message_handler(commands=["no"])
def handle_command(message, res=False):
    if str(message.chat.id) in idsAll:
        idsAll.remove(str(message.chat.id))
        with open("ids.txt", 'w') as f:
            for i in idsAll:
                f.write(i+'\n')
        bot.send_message(message.chat.id, "Вы отписались от рассылки")
        bot.send_message(admin[0], f"Удалён пользователь: {message.chat.username}[{message.chat.id}]")
    else:
        bot.send_message(message.chat.id, "Вы уже были отписаны от рассылки")

@bot.message_handler(content_types=["text"])
def handle_text(message):
    print(f"{message.chat.username}: {message.text}")
    bot.send_message(admin[0], f"{message.chat.username}[{str(message.chat.id)}]: {message.text}")
    if (message.text.lower()=="рассылка") and (str(message.chat.id) in admin):
        for i in idsAll:
            bot.send_message(i, 'Тест')
    elif (message.text.lower()=="users") and (str(message.chat.id) in admin):
        users = "Пользователей: %d \n" % len(idsAll)
    #    for i in idsAll:
    #       users += i + '\n'
        bot.send_message(message.chat.id, users)
        print(users)
    else:
        bot.send_message(message.chat.id, 'Чтобы получать рассылку напишите "/yes", чтобы больше не получать "/no"') # Тут должно быть дефолтное сообщение

t1 = threading.Thread(target=hhh, args=())
t1.start()

bot.polling(none_stop=True, interval=0)