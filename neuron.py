import random
import matplotlib.pyplot as plt
import numpy as np
import numbers


class Neuron(object):
    def __init__(self, w, b, activation):
        """
        :param w: List of int or float. Represents weights list.
        :param b: Int or float. Represents bias.
        :param activation: ActivationFunction object.
        """
        assert isinstance(b, numbers.Number), "b must be numeric"
        self.w = w
        self.b = b
        self.activation = activation

    def feed(self, input):
        """
        Evaluates input.
        :param input: Input list.
        :return: Int or float. Evaluation result.
        """
        assert len(input) == len(self.w), "Lengths of weights and input list must be equal"
        out = 0
        for i in range(0, len(input)):
            out += input[i] * self.w[i]
        out += self.b
        return self.activation.activate(out)

    def learn(self, input, desired_output, learning_rate):
        """
        Training function. Calculates new weights list and bias.
        :param input: Numeric list.
        :param desired_output: Numeric list.
        :return:

        >>> Step = Step()
        >>> N = Neuron([-1, 0], -1.5, Step)
        >>> for i in range(0, 50):
        ...     N.learn([1, 0], 1, 0.1)
        >>> N.feed([1, 0])
        1

        >>> Sigmoid = Sigmoid()
        >>> N = Neuron([-1, 0], -1.5, Sigmoid)
        >>> for i in range(0, 50):
        ...     N.learn([1, 0], 1, 0.1)
        >>> N.feed([1, 0])
        1
        """
        # calculate real_output
        real_out = self.feed(input)

        # learning algorithm
        diff = desired_output - real_out
        for i in range(0, len(self.w)):
            self.w[i] = self.w[i] + (learning_rate * input[i] * diff)
        self.b = self.b + (learning_rate * diff)


class NeuronOr(Neuron):
    """
    >>> A = Step()
    >>> OR = NeuronOr([1, 1], 0, A)
    >>> OR.feed([0, 0])
    0

    >>> OR.feed([0, 1])
    1

    >>> OR.feed([1, 0])
    1

    >>> OR.feed([1, 1])
    1

    >>> A = Sigmoid(threshold=0.6)
    >>> OR = NeuronOr([1, 1], 0, A)
    >>> OR.feed([0, 0])
    0

    >>> OR.feed([0, 1])
    1

    >>> OR.feed([1, 0])
    1

    >>> OR.feed([1, 1])
    1
    """


class NeuronAnd(Neuron):
    """
    >>> A = Step()
    >>> AND = NeuronAnd([1, 1], -1, A)
    >>> AND.feed([0, 0])
    0

    >>> AND.feed([0, 1])
    0

    >>> AND.feed([1, 0])
    0

    >>> AND.feed([1, 1])
    1

    >>> A = Sigmoid(threshold=0.6)
    >>> AND = NeuronAnd([1, 1], -1, A)
    >>> AND.feed([0, 0])
    0

    >>> AND.feed([0, 1])
    0

    >>> AND.feed([1, 0])
    0

    >>> AND.feed([1, 1])
    1
    """


class NeuronNand(Neuron):
    """
    >>> A = Step()
    >>> NAND = NeuronNand([-2, -2], 3, A)
    >>> NAND.feed([0, 0])
    1

    >>> NAND.feed([0, 1])
    1

    >>> NAND.feed([1, 0])
    1

    >>> NAND.feed([1, 1])
    0

    >>> A = Sigmoid(threshold=0.6)
    >>> NAND = NeuronNand([-2, -2], 3, A)
    >>> NAND.feed([0, 0])
    1

    >>> NAND.feed([0, 1])
    1

    >>> NAND.feed([1, 0])
    1

    >>> NAND.feed([1, 1])
    0
    """


class ActivationFunction(object):
    def __init__(self):
        """

        """
    def activate(self, input):
        """
        Calculates activation function output.
        :param input: Numeric.
        :return:
        """
        return None


class Step(ActivationFunction):
    def __init__(self):
        """

        """

    def activate(self, z):
        """
        Calculates activation function output.
        :param z: Numeric.
        :return: Output. Int.
        """
        return 1 if z > 0 else 0


class Sigmoid(ActivationFunction):
    def __init__(self, threshold=None):
        """

        :param threshold: Boundary to determine wether output belongs to one class or another.
        """
        self.threshold = threshold

    def activate(self, z):
        """
        Calculates activation function output.
        :param z: Numeric.
        :return: Output. Numeric.
        """
        out = 1/(1 + np.exp(-z))
        if self.threshold:
            return 1 if out > self.threshold else 0
        return out


class Tanh(ActivationFunction):
    def __init__(self, threshold=None):
        """

        :param threshold: Boundary to determine wether output belongs to one class or another.
        """
        self.threshold = threshold

    def activate(self, z):
        """
        Calculates activation function output.
        :param z: Numeric.
        :return: Output. Numeric.
        """
        out = np.tanh(z)
        if self.threshold:
            return 1 if out > self.threshold else 0
        return out


def space_pos(n_training, n_test, m, n, n_iter, learning_rate):
    """
    Space position training problem. Besides, makes classification and plots the results.
    :param n_training: Training set size. Int.
    :param n_test: Test set size. Int.
    :param m: Slop of the line that will separate the two classes.
    :param n: Position coefficient of the line.
    :param n_iter: Number of iterations.
    :param learning_rate:
    :return:
    """
    training = [] # training set
    desired_output = []
    test = [] # test set
    real_output = []

    # generate random training points
    for i in range(0, n_training):
        training.append([random.uniform(0, 50), random.uniform(0, 50)])

    # generate random test points
    for i in range(0, n_test):
        test.append([random.uniform(0, 50), random.uniform(0, 50)])

    # calculate desired output (related function: y = mx + n)
    for i in range(0, n_training):
        if training[i][1] > m*training[i][0] + n:
            desired_output.append(1)
        else:
            desired_output.append(0)

    # learn training
    A = Step()
    P = Neuron([0.5, 0], 0.6, A)

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
    space_pos(100, 100, 1, 0, 10, [0.1])

