import torch
import torch.nn as nn

class NeuralNet(nn.Module):
    def __init__(self, input_size, hidden_size, num_classes):
        super(NeuralNet, self).__init__() # basically super method is affiliated with pytorch so we have to use it
        self.l1 = nn.Linear(input_size, hidden_size)  # for this layer input_size as input and hidden_size as output
        self.l2 = nn.Linear(hidden_size, hidden_size)  # for this layer hidden_size as input and hidden_size as output
        self.l3 = nn.Linear(hidden_size, num_classes)  # for this layer hidden_size as input and num_classes as output
        self.relu = nn.ReLU()  # we use ReLU as activation function here

    def forward(self, x):
        out = self.l1(x)
        out = self.relu(out)
        out = self.l2(out)
        out = self.relu(out)
        out = self.l3(out)
        # no activation for layer 3 as we gonna use CrossEntropy for optimization that will be already applied by CrossEntropyLoss
        return out