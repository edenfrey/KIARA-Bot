import pickle
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
import numpy
class TextClassifier(object):
    def __init__(self) -> None:
        filename = 'prediction_model/final_model/text_classifier.sav'
        self.loaded_model = pickle.load(open(filename, 'rb'))

        filename = 'prediction_model/final_model/text_vectorizer.sav'
        self.vectorizer = pickle.load(open(filename, 'rb'))

        self.labels = ('FACTREQ','QUESTION','SENTENCE')
    
    def predict(self, input: str) -> int:
        input_arrayy = [input]
        input_np_array = numpy.array(input_arrayy)
        processed_input = self.pre_processing(input_np_array)

        res = self.loaded_model.predict(processed_input)[0]

        print(self.labels[res])


    def pre_processing(self, input):
        return self.vectorizer.transform(input)

if __name__ == "__main__":
    classifier = TextClassifier()
    input = "a potato is best roasted"
    classifier.predict(input)