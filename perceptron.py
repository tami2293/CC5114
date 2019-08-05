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