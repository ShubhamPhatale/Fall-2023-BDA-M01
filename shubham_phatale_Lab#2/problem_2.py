from mrjob.job import MRJob
import string

stopwords = set(["the", "and", "of", "a", "to", "in", "is", "it"])

class WCStopwords(MRJob):

    def mapper(self, _, line):
        words = line.split()
        for word in words:
            word = word.translate(str.maketrans('', '', string.punctuation))
            if word.lower() not in stopwords:
                yield word.lower(), 1

    def reducer(self, word, counts):
        yield word, str(sum(counts))

if __name__ == '__main__':
    WCStopwords.run()
