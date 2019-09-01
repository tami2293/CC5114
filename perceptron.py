import random
import numpy as np
import matplotlib.pyplot as plt

class Perceptron(object):
    def __init__(self, w, b):
        """
        :param w:
        :param b:

        >>> P = Perceptron([1, 0], 3)
        >>> P.feed([-2, -2])
        1
        """
        self.w = w
        self.b = b

    def feed(self, input):
        out = 0
        for i in range(0, len(input)):
            out += input[i] * self.w[i]
        out += self.b
        return 1 if out > 0 else 0

    def learn(self, inp, desired_output, learning_rate):
        """
        :param learning_rate: 
        :param inp:
        :param desired_output:
        :return:
        >>> P = Perceptron([-1, 0], -1.5)
        >>> for i in range(0, 50):
        ...     P.learn([1, 0], 1)
        >>> P.feed([1, 0])
        1
        """
        # calculate real_output
        real_out = self.feed(inp)

        # learning algorithm
        diff = desired_output - real_out
        for i in range(0, len(self.w)):
            self.w[i] = self.w[i] + (learning_rate * inp[i] * diff)
        self.b = self.b + (learning_rate * diff)

class PerceptronOr(Perceptron):
    def __init__(self):
        """
        >>> OR = PerceptronOr()
        >>> OR.feed([0, 0])
        0

        >>> OR.feed([0, 1])
        1

        >>> OR.feed([1, 0])
        1

        >>> OR.feed([1, 1])
        1
        """
        self.w = [1, 1]
        self.b = 0

class PerceptronAnd(Perceptron):
    def __init__(self):
        """
        >>> AND = PerceptronAnd()
        >>> AND.feed([0, 0])
        0

        >>> AND.feed([0, 1])
        0

        >>> AND.feed([1, 0])
        0

        >>> AND.feed([1, 1])
        1
        """
        self.w = [1, 1]
        self.b = -1

class PerceptronNand(Perceptron):
    def __init__(self):
        """
        >>> NAND = PerceptronNand()
        >>> NAND.feed([0, 0])
        1

        >>> NAND.feed([0, 1])
        1

        >>> NAND.feed([1, 0])
        1

        >>> NAND.feed([1, 1])
        0
        """
        self.w = [-2, -2]
        self.b = 3

class SumGate(object):
    def __init__(self):
        self.NAND = PerceptronNand()

    def sum(self, input):
        """
        :param input:
        :return:

        >>> SG = SumGate()
        >>> SG.sum([0, 0])
        [0, 0]

        >>> SG.sum([0, 1])
        [1, 0]

        >>> SG.sum([1, 0])
        [1, 0]

        >>> SG.sum([1, 1])
        [0, 1]
        """
        y1 = self.NAND.feed(input)
        z1 = self.NAND.feed([input[0], y1])
        z2 = self.NAND.feed([input[1], y1])
        sum = self.NAND.feed([z1, z2])
        carry = self.NAND.feed([y1, y1])
        return [sum, carry]

def space_pos(n_training, n_test, m, n, n_iter, learning_rate):
    training = [] # training set
    desired_output = []
    test = [] # test set
    real_output = []

    # generate random training points
    for i in range(0, n_training):
        training.append([random.uniform(0, 10000), random.uniform(0, 10000)])

    # generate random test points
    for i in range(0, n_test):
        test.append([random.uniform(0, 10000), random.uniform(0, 10000)])

    # calculate desired output (related function: y = mx + n)
    for i in range(0, n_training):
        if training[i][1] > m*training[i][0] + n:
            desired_output.append(1)
        else:
            desired_output.append(0)

    # learn training
    P = Perceptron([0.5, 0], 0.6)

    # iterate over the learning rate list
    for k in range(0, len(learning_rate)):
        for j in range(0, n_iter):
            for i in range(0, n_training):
                P.learn(training[i], desired_output[i], learning_rate[k])
        print(P.w, P.b)
        # get results
        for i in range(0, n_test):
            real_output.append(P.feed(test[i]))

        plt.subplot(121)
        training = np.array(training)
        test = np.array(test)
        plt.scatter(training[:, 0], training[:, 1], c=desired_output)
        plt.subplot(122)
        plt.scatter(test[:, 0], test[:, 1], c=real_output)
        plt.show()

        real_output = []

if __name__ == "__main__":
    space_pos(100, 100, 1, 0, 10, [0.1, 40, 500])
