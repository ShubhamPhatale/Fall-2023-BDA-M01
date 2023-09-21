from mrjob.job import MRJob
import re

class DocsSeperated(MRJob):

    def configure_args(self):
        super(DocsSeperated, self).configure_args()
        self.add_passthru_arg('--input-folder', help='Input folder containing text files')

    def mapper(self, _, line):
        input_file = self.options.input_folder
        words = re.findall(r"\b\w+\b",line.lower())
        for word in words:
            yield (word, input_file)

    def reducer(self, word, documents):
        documents = sorted(set(documents))
        yield (word, documents)

if __name__ == '__main__':
    DocsSeperated.run()
