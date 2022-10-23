# NLPChatbot

## Table of Contents
1) Use case of project
2) Basics of NLP
3) Workflow of our Analysis
4) Software and tools requirement for end to end implementation
5) References
6) Production stage of model (complete CI-CD pipeline integration through GitHub with Docker container over Heroku cloud service)
7) Problems I encountered during coding stage
8) Problems I encountered during deployment stage

## Use case of project:
The project's use case was to make an interactive chatbot which will guide user about Ganesh Chaturthi festival which is 
widely celebrated in India and features about our website based on this festival.
<br>This was a team project wherein 4 people worked on frontend of website, 4 people worked on gathering data from 
different sources and generating a proper csv file and I (Himesh Koli) was solely responsible for chatbot related work.
<br>[Our website - head over to Aboutus page to see our team](https://travelwithbappa.web.app/)

## Basics of NLP
Natural Language Processing is a specialized field which deals with Human language text based data. We first imported ```nltk``` library 
to have access to its various functions which will help us pre-process our input messages in a way the system will 
understand. The functions we used from ```nltk``` library for our project are as follows:

**Tokenization**

The tokenizer is actually downloaded from ```punkt``` package through ```nltk.download('punkt')```. What it does is it 
will basically separate each word, punctuation, number, special character in a sentence and make a list of it which we 
will use later in *Bag_of_Words* concept.

**Stemming**

Stemming is a concept in which the suffix part is cut from words in the context of pre-processing, which further reduces
the corpus size and results in fast processing. For example: `information` will become `inform` which provides same context. 

It is almost similar to Lemmatization, but in stemmer in some cases if the word has 2 different meanings and is cut then 
it does not decide with respect to context of the sentence what meaning it should use. This results in low accuracy but 
in some applications it may not be that fatal and can be used for its fast processing as compare to lemmatization. We 
import PorterStemmer```from nltk.stem.porter``` which is a type of stemmer function for our model needs.

**Removal of punctuation**

This is not a function in nltk, but we need to remove any punctuation or any special chars from list of stemmed words 
to pass it in all words, for preprocessing.

**Bag_of_Words**

BoW too is not some function to be imported from nltk library rather it is a concept which is used to give vector 
identification to our text. The reason behind this is that our system cannot process text inputs directly, so giving our 
text some sort of identification in terms of numbers can help preprocess the data efficiently.

BoW needs two parameters 1.All words 2.The words in which we are interested.
<br>All words ignore punctuations and duplicate words in a paragraph or list of sentences, and it compares with words in 
which we are interested and gives them number according to their occurrence in all words. For example:
```
sent1 = ['my', 'hobby', 'is', 'dancing']
sent2 = ['my', 'favorite', 'dish', 'is', 'pizza']
all_words = ['my', 'hobby', 'is', 'dancing', 'favorite', 'dish', 'pizza']
bang = bag_of_words(sent2, words)
o/p: [1. 0. 1. 0. 1. 1. 1.]
```
Now sent2 here is sentence we are interested and the o/p we got is its vector identification.

In our project's case All_words are all patterns from json file and when user will pass something it will then use 
our nltk functions to preprocess and bring it in vector form like the example above and then use it to classify among 
which specific tag it belongs, in which the vector form will be differentiating factor.

## Workflow of our analysis:

1) Firstly made a json file which contains all our tags, patterns(user inputs) and responses which will help us identify what type
of question user is asking and based on that the respective response under same tag will get trigger in the form of 
output. (intents.json)
2) Then we imported all our basic NLP related functions which will help us preprocess our unstructured text and make it
computable to our system. (nltk_preprocessing.py)
3) Then pre-processing our data (intents.json) by using nltk function, getting BoW (vector form) of every pattern to 
categorize user response with that pattern tag, with the help of implemented Neural network and saving it in 
h5 extension file, using an inbuilt function torch.save in PyTorch.(training_data.py). This will be our X (Training 
dataset) and Tags Y (class-labels) output which is further passed through softmax activation function getting real output.
4) After this we will implement a simple Feed forward Neural Network model with the help of PyTorch to compute user 
responses. (model.py)
<br> `sentence(BoW of pattern)(Training data) as input --> No. of patterns --> Hiiden layers --> no. of classes(tags) --> softmax activation function --> Target tag (Y) output`
5) It is a UI based application which requires heavy front end, so it is better to first make a demo model to test it 
out in terminal. We first load our data and create a `response` function which will compute user input (pattern) and 
classify with respect to our tags (labels) which will then give responses from that tag appropriately (chatbot.py). 
This `response`function will be used in flask framework too.
6) Now on to its frontend, we need html, css, javascript code to render the UI of our model on webpage.
7) After creating all rendering and code files now we will create a flask instance to run it on our localhost and to display 
the UI of our chatbot to test it out.

## Software and tools requirement for end to end implementation

Python Version = 3.8
1) [PyCharmIDE](https://www.jetbrains.com/pycharm/download/#section=windows)
2) [PyTorch](https://pytorch.org/get-started/locally/)
3) [GitHub](https://github.com/)
4) [Git-CLI v2](https://git-scm.com/downloads)
5) [Heroku for deployment](https://dashboard.heroku.com/)

## References:
Although I relied on these videos for implementation of chatbot, this practice did really help me to write my own 
function based code from scratch for GDP prediction project. Before doing this chatbot project, my GDP prediction code 
was only limited to jupyter notebook which was very unstructured and informal. It was very nice experience doing this 
chatbot project, and I really learned alot.

1) [Knowledge about NLP terms and its syllabus I learned in my institution from ITVedant]
2) [Online resource 1 - Machine Learning Mastery](https://machinelearningmastery.com)
3) [Online resource 2 - Analytics Vidhya](https://www.analyticsvidhya.com/)
4) [Videos I referred while building this chatbot - Python Engineer](https://www.youtube.com/watch?v=RpWeNzfSUHw&list=PLqnslRFeH2UrFW4AUgn-eY37qOAWQpJyg)
5) [Knowledge on implementing PyTorch framework - Python Engineer](https://www.youtube.com/watch?v=EMXfZB8FVUA&list=PLqnslRFeH2UrcDBWF5mfPGpqQDSta6VK4)
6) [Referred this video to make a CI-CD pipeline to push code to Heroku platform - Krish Naik](https://youtu.be/Gs15V79cauo)

## Production stage of model:
1) Set up my project's files for my GitHub repo using Git commands
2) Created Heroku account and in it created an app through which deployment will happen
3) Now create docker file with all your contents.
4) Now important step, for to build our docker container in GitHub and to push it over heroku we need a .yaml file which will 
have a workflow dedicated to build, push and release docker container over heroku.
5) Create a .GitHub directory in your root project folder, in it create workflows directory and in that create main.yaml file
which will contain that workflow. (You can just copy the content from my main.yaml file from my repo)
6) Now we will need 3 secret keys which will help my GitHub repo to interact with docker account and app created in it.
    1) Secret HEROKU_API_KEY(refer yaml file) - go to your project repo in GitHub >> settings >> secrets >> actions >> New repository secret >> 
    from yaml file copy this `HEROKU_API_KEY` and paste in Name section in New secret section.
        1. And in value you need to put api_key for that head over your heroku account >> account settings >> and below you 
        will find api_key reveal it, copy and paste in value section below name >> Add.
    2. Secret HEROKU_EMAIL - select New repository after creating secret api_key therein and add `HEROKU_EMAIL` from 
    yaml file and paste in name section and for value enter your emailid related to your docker account
    <br>This 2 steps will basically configure your GitHub repo with your docker account.
    3. Now last Secret HEROKU_APP_NAME - select new repository therein and add `HEROKU_APP_NAME` from 
    yaml file and paste in name section and for its value add your app name from your heroku account which you have created
    in it.
7) Once setting up secret keys now push your .github directory which contains yaml file to your GitHub and once pushed 
automatically it will start to build container with all the files you configured above
8) After it's done building, it directly pushes it to heroku account, and you need to click Open app in your app section 
of heroku to see the deployed version of your project.


## Problems I encountered during coding stage
1) First and foremost challenge was to gather user patterns(user inputs) to put into json file, so took suggestions from 
people, ask them for feedback on what would they like to know from chatbot regarding this festival. 
<br>I was very much limited by the front end of website on what responses I should add with respect to features of 
website, so added some of my own tags and responses such as facts, doubts regarding payments, etc. 
<br>Although this project is done I'm still working on ways to improve this bot more and make it more interactive.
2) Another problem I ran into was to make responses more readable in UI through json file, so as we all know json file 
is made for system to read and not for general purposes, it was hard to find solution but then stumbled upon one stack 
overflow article in it user mentioned to use `<br>` tags to break lines, and use `<href>` tags to provide links, which 
was very useful.
3) Lastly ran into some issues while saving the file in `training_data.py` using PyTorch `save` function. The extension `.pth` 
was unsupported due to some type of characters in json responses. So solved this by using `.h5` extension which supported
those characters.

## Problems I encountered during deployment stage
1) I have already deployed this project
