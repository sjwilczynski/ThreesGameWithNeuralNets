from __future__ import absolute_import
import numpy as np
import torch
from torch.autograd import Variable
from torch import nn

MOVES = [0, 1, 2, 3]
CUDA = False


def train(model, data_loaders, optimizer, num_epochs=100, log_every=100, verbose=True):
    # Initialize momentum variables
    velocities = [Variable(torch.FloatTensor(p.data.size()).zero_(), requires_grad=False) for p in model.parameters]
    if CUDA:
        model.network.cuda()

    iter_ = 0
    epoch = 0
    if verbose:
        print u'Training the model!'
        print u'Interrupt at any time to get current model'
    try:
        while epoch < num_epochs:
            epoch += 1
            for x in data_loaders.get():
                future = x[:, 21:]
                future_scores = np.zeros((x.shape[0], len(MOVES)))
                for i, move in enumerate(MOVES):
                    future_scores[:, i] = model.Q(np.hstack((future, np.full((x.shape[0], 1), move))))
                y = x[:, 20] + np.max(future_scores, axis=0)
                x = x[:, :20]
                if CUDA:
                    x = x.cuda()
                    y = y.cuda()
                iter_ += 1

                optimizer.zero_grad()
                out = model.forward(x)
                loss = model.loss(out, y)
                loss.backward()
                optimizer.step()

                if iter_ % log_every == 0 and verbose:
                    print u"Minibatch {0: >6}  | loss {1: >5.2f} ".format(iter_, loss.data[0])

    except KeyboardInterrupt:
        pass
    # TODO Save model parameters


class QLearningNet(object):
    def __init__(self, network, criterion):
        self.network = network
        self.criterion = criterion

    def Q(self, batch):
        batch = Variable(torch.FloatTensor(batch), requires_grad=False)
        return self.network.forward(batch)

    def loss(self, out, y):
        out = Variable(torch.FloatTensor(out), requires_grad=False)
        y = Variable(torch.FloatTensor(y), requires_grad=False)
        return self.criterion(y, out)


#network = nn.Sequential(nn.Linear(20,100), nn.ReLu(), nn.Linear(100,1))
#optimizer = torch.optim.Adam([image], lr=0.001)  #, momentum=0.5)
#optimizer = torch.optim.LBFGS([image])