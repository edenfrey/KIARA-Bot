import pickle
import re
from nltk.stem import WordNetLemmatizer
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

        filename = 'prediction_model/final_model/text_tfidfconverter.sav'
        self.tfidfconverter = pickle.load(open(filename, 'rb'))

        self.labels = ('FACTREQ','QUESTION','SENTENCE')
    
    def predict(self, input: str) -> int:
        input_arrayy = [input]
        input_np_array = numpy.array(input_arrayy)
        processed_input = self.pre_processing(input_np_array)

        res = self.loaded_model.predict(processed_input)[0]

        print(self.labels[res])


    def pre_processing(self, input):
        input = self.text_pre_processing(input)
        input = self.vectorizer.transform(input)
        input = self.tfidfconverter.transform(input)
        return input

    def text_pre_processing(self, input):
        # Text Pre-Processing
        documents = []

        stemmer = WordNetLemmatizer()

        for sen in range(0, len(input)):
            # Remove all the special characters
            document = re.sub(r'\W', ' ', str(input[sen]))
            
            # remove all single characters
            document = re.sub(r'\s+[a-zA-Z]\s+', ' ', document)
            
            # Remove single characters from the start
            document = re.sub(r'\^[a-zA-Z]\s+', ' ', document) 
            
            # Substituting multiple spaces with single space
            document = re.sub(r'\s+', ' ', document, flags=re.I)
            
            # Removing prefixed 'b'
            document = re.sub(r'^b\s+', '', document)
            
            # Converting to Lowercase
            document = document.lower()
            
            # Lemmatization
            document = document.split()

            document = [stemmer.lemmatize(word) for word in document]
            document = ' '.join(document)
            
            documents.append(document)
        
        input = documents

        return input

if __name__ == "__main__":
    classifier = TextClassifier()
    input = "gimme FACT!"
    classifier.predict(input)