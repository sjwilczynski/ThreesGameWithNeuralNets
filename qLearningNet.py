import torch
from torch.autograd import Variable
from torch import nn

FILENAME = "saved_parameters"
INPUT_SIZE = 19
HIDDEN_SIZE = 256
CUDA = False


class QLearningNet(object):
    def __init__(self, network=None, criterion=None):
        if network is not None and criterion is not None:
            self.network = network
            self.criterion = criterion
        else:
            self.network = nn.Sequential(nn.Linear(INPUT_SIZE, HIDDEN_SIZE), nn.Tanh(), nn.Linear(HIDDEN_SIZE, 4))
            self.criterion = nn.MSELoss()

    def Q(self, batch, as_variable=False):
        batch = Variable(torch.FloatTensor(batch), requires_grad=False)
        if as_variable:
            return self.network.forward(batch)
        else:
            return self.network.forward(batch).data.numpy()

    def loss(self, out, y):
        y = Variable(torch.FloatTensor(y), requires_grad=False)
        return self.criterion(out, y)

    def save_parameters(self, filename):
        torch.save(self.network.state_dict(), filename)

    def load_parameters(self, filename):
        self.network.load_state_dict(torch.load(filename))
