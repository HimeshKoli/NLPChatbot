import random
import json
import torch
from model import NeuralNet
from nltk_preprocessing import tokenize, bag_of_words, stemming

with open('intents.json', 'r') as f:
    intents = json.load(f)  # here we encountered an error termed as UnicodeDecodeError, it was based on certain character in our files which it wasnt able to read, tried giving it various encodings didnt work, then I changed the extension of data.pth to data.h5 suggested in a comment and it worked

DATA_FILE = 'data.h5'
data = torch.load(DATA_FILE)

input_size = data['input_size']  # we gave format like this because data stored in data is in dictionary format
hidden_size = data['hidden_size']
output_size = data['output_size']
all_words = data['all_words']
tags = data['tags']
model_state = data['model_state']

model = NeuralNet(input_size, hidden_size, output_size)
model.load_state_dict(
    model_state)  # we need to load our model_state and all its parameters with the help of load_state_dict function
model.eval()  # we need to evaluate our model's parameters

# now we need to program our bot to initiate the conversation or quit if user dont want to interact

bot_name = "Ekadanta"

# Tags are basically class-labels through which it is going to sense the user's input, even if it doesnt matches from the
# patterns we have, it will try to classify with the help of feed-forward Neural network and after classifying the user
# input it will then give one of the response from that respective tag

# Chatbot file and all other files we need to run only once to get that response function running which we will use in
# app_flask.py file.

# The main two files which we have to run every time are training_data.py which after every edit in intents.json file we
# need to pre-process our patterns and responses again and save it, AND app_flask.py to basically get user input, and
# get that input go through in our response function and give appropriate output.

# So in chatbot.py the response function basically computes user input and deliver one of our intents.json responses as
# output accordingly


def response(msg):
    sentence = tokenize(msg)  # the user input sentence need to be tokenized
    X = bag_of_words(sentence, all_words)  # this gets sentence parameter as a tokenized sentence from above line
    X = X.reshape(1, X.shape[0])
    X = torch.from_numpy(X)  # because our bag_of_words function returns numpy array

    output = model(X)
    _, predicted = torch.max(output, dim=1)
    tag = tags[predicted.item()]  # tag is actual tag from intents.json, predicted.item is class label

    probabilty = torch.softmax(output, dim=1)
    prob = probabilty[0][predicted.item()]

    if prob.item() > 0.75:
        for intent in intents['intents']:
            if tag == intent['tag']:  # if predicted.item's class label matches with our tag in intents.json then it will give one of the sentence as reply from responses which belongs to its respective tag
                return random.choice(intent['responses'])
                # print(f"{bot_name}: {random.choice(intent['responses'])}")

    return "I do not understand"

    # else:
    #     print(f"{bot_name}: I do not understand.")


# The below 'main' block, the reason behind implementing this is due to it is in our main module file chatbot.py which is going to run first to initiate our program

if __name__ == "__main__":
    print("Hii My name is Ekadanta, Let's chat! else type 'quit' to exit")
    while True:
        sentence = input('You: ')  # to check if the sentence by user input has quit then it will exit
        if sentence == 'quit':
            print('Have a nice day :D')
            break

        resp = response(sentence)
        print(resp)

# now we need to implement probability based activation system and softmax activation function does that, so if the prob is greater then threshold then it will enter in intent loop/block and then choose response
# this will be our last step but we will implement it above intent loop/block then it will enter that block