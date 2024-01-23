from SentenceAnalysis import SentenceAnalysis
from ltp import StnSplit




class ParagraphAnalysis:
    def __init__(self, text,task):
        self.unsplitted_text=text

        self.text = self._merge_short_sentences()

        self.sentences = [SentenceAnalysis(sentence,task) for sentence in self.text]
        self.sent_count = len(self.sentences)
        self.sent_length={index: sentence.length for index, sentence in enumerate(self.sentences)}
        self.length=self._count_length()
        self.sent_analysis = {index: sentence.result_dic for index, sentence in enumerate(self.sentences)}
        self.score={}
    def _merge_short_sentences(self):
        """
        Merges sentences in a list if a sentence is shorter than 3 characters.
        It merges such a sentence with the following sentence in the list.
        """
        i = 0
        sentences = StnSplit().split(self.unsplitted_text)
        while i < len(sentences):
            # Check if the current sentence is shorter than 3 characters
            if len(sentences[i]) <=3:
                # If it's not the last sentence, merge it with the next one
                if i + 1 < len(sentences):
                    sentences[i] += sentences[i + 1]
                    del sentences[i + 1]
                else:  # If it's the last sentence, there's nothing to merge with
                    break
            else:
                i += 1

        return sentences


    def _count_length(self):
        length=0
        for sent in self.sentences:
            length+=sent.length
        return length


    def __str__(self):
        for sent in self.sentences:
            print(sent)
        return (f"Text: {self.text}\n")