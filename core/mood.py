from core.config import PATH_GRAPHICS
from core.youtube import YoutubeAPI
import matplotlib.pyplot as plt
from dostoevsky.tokenization import RegexTokenizer
from dostoevsky.models import FastTextSocialNetworkModel
import random


class Mood:
    @staticmethod
    def analyze(url: str):
        comments = YoutubeAPI.comments(url)
        print(len(comments))
        tokenizer = RegexTokenizer()
        model = FastTextSocialNetworkModel(tokenizer=tokenizer)
        results = model.predict(comments, k=5)
        predictions = list()
        for result in results:
            result = dict(result)
            prediction = max(result, key=result.get)
            predictions.append(prediction)

        predictions_ = list()
        for prediction in predictions:
            predictions_.append(Mood.labels(prediction))

        plt1 = Mood.plot_hist(predictions_, plt)    # predictions
        filename = "graphic_" + str(random.randint(1, 1000000))
        Mood.savepic(PATH_GRAPHICS, filename, plt1)
        photo = Mood.openpic(PATH_GRAPHICS, filename)
        return photo

    @staticmethod
    def labels(value: str):
        if value == 'positive':
            return 'позитивные'
        if value == 'negative':
            return 'негативные'
        if value == 'neutral':
            return 'нейтральные'
        if value == 'skip':
            return 'неопределенные'
        if value == 'speech':
            return 'безэмоциональные'
        return 'none'

    @staticmethod
    def plot_line(x, y, points, plt_):
        fig = plt_.figure()
        ax = plt_.subplot(111)
        ax.plot(points, x, label="positive")
        ax.plot(points, y, label="negative")
        ax.legend(bbox_to_anchor=(0.5, 0.9))
        return plt_

    @staticmethod
    def plot_hist(x, plt_):
        plt.hist(x, density=False)  # density=False would make counts
        plt.ylabel('Количество комментариев')
        plt.xlabel('')
        return plt_



    @staticmethod
    def openpic(path: str, name: str):
        photo = open(path + name + '.png', 'rb')
        return photo

    @staticmethod
    def savepic(path: str, name: str, plot):
        plot.savefig(path + name + '.png')

