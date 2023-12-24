from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from data.training_data import training_data
from responses.greetings import greetings_responses
from chatterbot import languages

languages.ENG.ISO_639_1 = "en_core_web_sm"


tele_bot = ChatBot('TeleBot',
                   storage_adapter='chatterbot.storage.SQLStorageAdapter',
                   logic_adapters=[
                       {
                           'import_path': 'chatterbot.logic.BestMatch',
                           'default_response': "I'm sorry, I didn't understand that. Could you please rephrase?",
                           'maximum_similarity_threshold': 1
                       }
                   ])

# Training the bot
trainer = ListTrainer(tele_bot)
trainer.train(training_data)

# Training with specific response categories
trainer.train(greetings_responses)


print("TeleBot: Hello! I'm here to assist you. Although I strive to help, my responses might sometimes be incomplete or unclear.")

while True:
    user_input = input("Message TeleBot... ")
    if user_input.lower() == 'exit':
        break
    bot_response = tele_bot.get_response(user_input)
    print("TeleBot:", bot_response)
    # print("Bot confidence:",bot_response.confidence)
    # print("Similarity threshold:", tele_bot.logic_adapters[0].maximum_similarity_threshold)

