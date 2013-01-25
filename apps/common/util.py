class Stadistical(object):

    @staticmethod
    def average(values):
        return reduce(lambda x, y: x + y, values) / len(values)

    @staticmethod
    def median(values):
        n = len(values)
        if n % 2 == 0:
            return (values[(n - 1) / 2] + values[n / 2]) / 2
        else:
            return values[n / 2]

    @staticmethod
    def mode(values):
        tmp = [[0, value] for value in values]
        for value in values:
            for t in tmp:
                if value in t:
                    t[0] += 1
        return max(tmp)
