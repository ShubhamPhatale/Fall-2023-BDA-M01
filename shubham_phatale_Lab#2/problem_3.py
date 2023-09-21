from mrjob.job import MRJob
import re
import string

class MRBiagrams(MRJob):

    def mapper(self, _, line):
        words = re.findall(r"[\w']+|[.,!?;]", line)
        for i in range(len(words) - 1):
            outputWords = f"{words[i].lower()},{words[i+1].lower()}"
            yield outputWords, 1

    def reducer(self, outputWords, counts):
        yield outputWords, str(sum(counts))

if __name__ == '__main__':
    MRBiagrams.run()
