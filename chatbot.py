from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer

chatbot = ChatBot("BotMath")

conversa = [
    "Coe",
    "E aí, tranquilo?",
    "Tranquilo",
    "Qual a boa de hoje?",
    "a Hashtag ta ensinando Python e até chatbot",
    "Caraca que doidera",
    "Maneiro né",
    "Irado"
]

trainer = ListTrainer(chatbot)
trainer.train(conversa)

while True:
    mensagem = input("Mande uma mensagem para o chatbot: ")
    if mensagem == "parar":
        break
    resposta = chatbot.get_response(mensagem)
    print(resposta)
 