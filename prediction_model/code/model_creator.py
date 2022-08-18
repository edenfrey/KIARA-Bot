# Import Libraries
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from nltk.corpus import stopwords
import pickle
from nltk.stem import WordNetLemmatizer
import pandas as pd
from sklearn.preprocessing import LabelEncoder
import re
import nltk
nltk.download('stopwords')


# Importing Data Set
df = pd.read_csv('prediction_model/datasets/data.csv')

# Converting labeled data to targets
lb_make = LabelEncoder()
df["target"] = lb_make.fit_transform(df["label"])

# Baseline Model
sentences = df['sentence'].values
y = df['target'].values

# Text Pre-Processing
documents = []

stemmer = WordNetLemmatizer()

for sen in range(0, len(sentences)):
    # Remove all the special characters
    document = re.sub(r'\W', ' ', str(sentences[sen]))

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

# Create vectorizer
vectorizer = CountVectorizer(
    max_features=1500, stop_words=stopwords.words('english'))
vectorizer.fit(documents)
sentences = vectorizer.transform(documents)

# Bag of Words Model - Convert Values
tfidfconverter = TfidfTransformer()
tfidfconverter.fit(sentences)
sentences = tfidfconverter.transform(sentences)

# Splitting Data Set
sentences_train, sentences_test, y_train, y_test = train_test_split(
    sentences, y, test_size=0.2, random_state=0)

# Training Model
classifier = RandomForestClassifier(n_estimators=1000, random_state=0)
classifier.fit(sentences_train, y_train)

# Testing Model
y_pred = classifier.predict(sentences_test)

# Evaluating Results
print(confusion_matrix(y_test, y_pred))
print(classification_report(y_test, y_pred))
print(accuracy_score(y_test, y_pred))

# Saving Model
filename = 'prediction_model/final_model/text_classifier.sav'
pickle.dump(classifier, open(filename, 'wb'))

# Saving Vectorizer
filename = 'prediction_model/final_model/text_vectorizer.sav'
pickle.dump(vectorizer, open(filename, 'wb'))

# Saving TFIDF Converter
filename = 'prediction_model/final_model/text_tfidfconverter.sav'
pickle.dump(tfidfconverter, open(filename, 'wb'))
