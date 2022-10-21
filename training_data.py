import json
from nltk_preprocessing import tokenize, stemming, bag_of_words
import numpy as np

import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader

from model import NeuralNet

with open ('intents.json', 'r') as f:
    intents = json.load(f)

# print(intents) # It will print whole intents file contents

# now we need to get all our intents to be converted into numbers of our training data which will help our machine to identify those words
all_words = []
tags = []  # tags are our labels
xy = []  # it will hold tags+patterns so basically our training data

for intent in intents['intents']:
    tag = intent['tag']
    tags.append(tag)  # here we basically put all our tags from intents.json in tags variable declared above
    for pattern in intent['patterns']:
        p = tokenize(pattern)  # pattern sentences somehow loosely compares to users input so need to tokenize them
        all_words.extend(p)  # we used extend function here instead of append because all_words already is a list and we will again get list in p by tokenize because tokenize returns list so extend and we need patterns in all_words
        xy.append((p, tag))  # we appended tags as well as all tokenized patterns here and in all_words we only appended all tokenized patterns

ignore = ['?', '!', ',', '.']  # punctuations to ignore in all_words

all_words = [stemming(p) for p in all_words if p not in ignore]
# print(all_words)

# now we want only unique words in all_words, ie no duplicates and will return a list, so we use sorted function

all_words = sorted(set(all_words))
tags = sorted(set(tags))

X_train = []
y_train = []

for (pattern_sentence, tag) in xy: # we unpacked the tuple of xy in our way which consisted tokenized pattern=p and tag
    bag = bag_of_words(pattern_sentence, all_words)  # pattern sentence (loosely) means the input user will give in which we are interested and all_words contains all the tokenized words from intents[patterns] from json file
    X_train.append(bag)

    labels = tags.index(tag) # we get labels according to their index value, so if we have 'tags' in order in list and in it we have 'tag' Facts at 0th position then its label is 0
    y_train.append(labels)

# now we need to have our X_train and y_train in numpy array, so we convert it by importing numpy

X_train = np.array(X_train)
y_train = np.array(y_train)

# Now below in 2nd part we are creating a pytorch dataset to store our data

class ChatBotDataset(Dataset):
    def __init__(self):
        self.n_samples = len(X_train)
        self.x_data = X_train
        self.y_data = y_train

    #dataset[idx]
    def __getitem__(self, index):
        return self.x_data[index], self.y_data[index]

    def __len__(self):
        return self.n_samples

# Hyperparameters
batch_size = 8
hidden_size = 8
output_size = len(tags)  # no of total classes which are tags
input_size = len(X_train[0])  # 0 or 1 because we take length of bag which is same as all_words
# print(input_size, len(all_words)) # all words which is there in array X_train will contain every array of same no of elements with 1s and 0s so will take first array and give its len to input_size
# print(output_size, tags) # tags will be our classes so their len will be our output #working
learning_rate = 0.003
num_epochs = 1000

dataset = ChatBotDataset()
training_loader = DataLoader(dataset=dataset, batch_size=batch_size, shuffle=True, num_workers=0) # num_workers for windows should be 0 not gretaer then 0, its just basically used to fasten the process using multi-thread proc

# device = torch.device('cuda' if torch.cuda.is_available() else 'cpu') # its just if your pc has cuda based gpu then it will do processing faster
model = NeuralNet(input_size, hidden_size, output_size) #.to(device) # cuda related function to(device)

# loss and optimizer
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

# now are training loop to determine the loss at each point in our epochs
for epoch in range(num_epochs):
    for (words, labels) in training_loader: # we unpacked training_loader in our way as words and labels
        words = words #.to(device)
        labels = labels.to(dtype=torch.long) #.to(device)

        # forward pass
        outputs = model(words)
        loss = criterion(outputs, labels)

        # backward and optimizer step
        optimizer.zero_grad() # in this step we basically empty the gradient first which is necessary in pytorch
        loss.backward() # to calculate the back propogation
        optimizer.step()

    if (epoch+1) % 100 == 0:
        print(f'epoch {epoch+1}/{num_epochs}, loss={loss.item():.4f}') # .4f for 4 decimal value of loss, epoch+1 basically epochs start with 0 so +1, loss.item is value os loss

print(f'final loss, loss={loss.item():.4f}')

# Now we need to move main components to a dedicated file and save that file, this file is in dictionary format meaning
# when we want its contents in chatbot.py we need to give dictionary formatting to get data

data = {
    "model_state": model.state_dict(),
    "input_size": input_size,
    "output_size": output_size,
    "hidden_size": hidden_size,
    "all_words": all_words,
    "tags": tags
}

DATA_FILE = "data.h5" # h5 an extension for pytorch file to cover all types of responses in intents.json
torch.save(data, DATA_FILE) # this will serialise it and save it to the pickle file, torch.save is a pytorch file saving function

print(f'training is done. file saved to {DATA_FILE}')
