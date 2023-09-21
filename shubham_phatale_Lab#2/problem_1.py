from mrjob.job import MRJob
import string

class wordCount(MRJob):

    def mapper(self, _, line):
        words = line.split()
        for word in words:
            word = word.translate(str.maketrans('', '', string.punctuation))
            yield word.lower(), 1

    def reducer(self, word, counts):
        yield word, str(sum(counts))

if __name__ == '__main__':
    wordCount.run()
