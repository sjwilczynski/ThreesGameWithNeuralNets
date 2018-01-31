import numpy as np


class ReplayMemory(object):
    def __init__(self, max_size, entry_len=40):
        self.max_size = max_size
        self.data = np.zeros((1, entry_len))

    def add(self, new_data):
        self.data = np.append(self.data, new_data, axis=0)
        to_cut = self.data.shape[0] - self.max_size
        if to_cut > 0:
            self.data = self.data[to_cut:, :]

    def choose(self, how_many):
        indices = np.random.randint(1, len(self.data), how_many)
        return self.data[indices, :]
