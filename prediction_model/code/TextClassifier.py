import pickle
import re
from nltk.stem import WordNetLemmatizer
import numpy
from typing import List, Set, Dict, Tuple, Optional
class TextClassifier(object):
    """
    A class used to represent a trained TextClassifier.

    ...

    Attributes
    ----------
    model : Model
        A trianed model classifier to perform text classification.
    vectorizer : Vectorizer
        Vectorizer to convert words to numbers
    tfidfconverter : TFIDFConverter
        TFIDF multiplies the term frequency of a word by the inverse document frequency
    labels : (str)
        A tuple of strings that contains the different text types.
    """

    def __init__(self) -> None:
        """
        Parameters
        ----------
        """

        # Load Model
        filename = 'prediction_model/final_model/text_classifier.sav'
        self.model = pickle.load(open(filename, 'rb'))

        # Load Vectorizer
        filename = 'prediction_model/final_model/text_vectorizer.sav'
        self.vectorizer = pickle.load(open(filename, 'rb'))

        # Load TFIDF Converter
        filename = 'prediction_model/final_model/text_tfidfconverter.sav'
        self.tfidfconverter = pickle.load(open(filename, 'rb'))
        
        # Create predicition labels
        self.labels = ('FACTREQ','QUESTION','SENTENCE')
    
    def predict(self, input: str) -> str:
        """
        Predicts what text type the input is using the trained model.

        Parameters
        ----------
        input : str
            The string in which we want to perform classification
            
        output : res
            The predicted classification of the input string
        """
        
        # Convert input string to numpy array
        input = [input]
        input = numpy.array(input)

        # Call helper function to perform pre-processing
        processed_input = self.pre_processing(input)

        # Use processed input to classify and predict text type
        res = self.model.predict(processed_input)[0]

        # Return result
        return self.labels[res]


    def pre_processing(self, input):
        """
        Performs pre-processing to the input data by first performing text processing and then converting strings to numbers.

        Parameters
        ----------
        input
            The numpy array string in which we wish to perform pre-processing on.
            
        output
            The processed input
        """
        
        input = self.text_pre_processing(input)
        input = self.vectorizer.transform(input)
        input = self.tfidfconverter.transform(input)
        return input

    def text_pre_processing(self, input):
        """
        Performs pre-processing to the input data by first performing text processing and then converting strings to numbers.

        Parameters
        ----------
        input
            The numpy array string in which we wish to perform pre-processing on.
            
        output
            The processed input numpy array.
        """
        
        # Text Pre-Processing
        documents = []

        stemmer = WordNetLemmatizer()

        for sen in range(0, len(input)):
            # Remove all the special characters
            document = re.sub(r'\W', ' ', str(input[sen]))
            
            # Remove all single characters
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
    input = "i like pineapples that are not pine and apples"
    print(classifier.predict(input))