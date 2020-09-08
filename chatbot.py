from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ChatterBotCorpusTrainer

# Creating Instance
chatbot = ChatBot(
    'EdzeetaBot',
    logic_adapters=[

        {
            'import_path': 'chatterbot.logic.BestMatch',
            'maximum_similarity_threshold': 0.65,
            'default_response': 'Sorry , I dont know this, you can mail my team and get it clear:)',

        }
    ],

    input_adapter="chatterbot.input.VariableInputTypeAdapter",
    output_adapter="chatterbot.output.OutputAdapter",
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    database_uri='sqlite:///database.sqlite3'
) 

def get_bot_response():
    userText = request.args.get('msg')
    botReply = str(bot.get_response(userText))
    if botReply == "default_value":
        botReply = str(bot.get_response('default_response'))

training_data_quesans = open('training_data/ques_ans.txt').read().splitlines()
training_data_personal = open('training_data/personal_ques.txt').read().splitlines()

training_data = training_data_quesans + training_data_personal

trainer = ListTrainer(chatbot)
trainer.train(training_data)  

# Training
trainer_corpus = ChatterBotCorpusTrainer(chatbot)
trainer_corpus.train('chatterbot.corpus.english') 
trainer.train("chatterbot.corpus.english.conversations")
