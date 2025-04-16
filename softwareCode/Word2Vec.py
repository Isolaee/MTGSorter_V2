import json
import string
from gensim.models import Word2Vec
from nltk.corpus import stopwords
import nltk
import numpy as np

# Ensure you have the NLTK stopwords package downloaded
nltk.download("stopwords")


# Load JSON data
def load_data(json_file):
    """
    Method to load data to var
    Params: json_file -> file to be loaded, r -> mode; defaults as read
    """
    with open(json_file, "r") as file:
        data = json.load(file)
    return data


# Read all fields
def read_fields(json_file):
    data = load_data(json_file)
    for name, type_line, oracle_text, keywords in zip(
        data["name"], data["type_line"], data["oracle_text"], data["keywords"]
    ):
        return name, type_line, oracle_text, keywords


# Preprocess data to remove stopwords and punctuation
def preprocess_data(data):
    stop_words = set(stopwords.words("english"))  # Set of English stopwords
    sentences = []
    # Process 'Text' field
    for text in data["name"]:
        # Remove punctuation
        no_punct = text.translate(str.maketrans("", "", string.punctuation))
        # Split sentences into words and remove stopwords
        words = [word for word in no_punct.split() if word.lower() not in stop_words]
        sentences.append(words)
    # Process 'name' field
    for name in data["type_line"]:
        # Remove punctuation
        no_punct = name.translate(str.maketrans("", "", string.punctuation))
        # Split names into words and remove stopwords
        words = [word for word in no_punct.split() if word.lower() not in stop_words]
        sentences.append(words)
    for name in data["oracle_text"]:
        # Remove punctuation
        no_punct = name.translate(str.maketrans("", "", string.punctuation))
        # Split names into words and remove stopwords
        words = [word for word in no_punct.split() if word.lower() not in stop_words]
        sentences.append(words)
    if not data["keywords"]:
        for name in data["keywords"]:
            # Remove punctuation
            no_punct = name.translate(str.maketrans("", "", string.punctuation))
            # Split names into words and remove stopwords
            words = [word for word in no_punct.split() if word.lower() not in stop_words]
            sentences.append(words)

    return sentences


# Train Word2Vec model
def train_word2vec(sentences):
    """
    Method for training Word2Vec model
    Params: Sentences-> Words that will train the model
    Retruns: Model
    """
    model = Word2Vec(sentences, vector_size=100, window=5, min_count=1, workers=8)
    return model


# Save Word2Vec model
def save_model(model, model_file):
    """
    Method to save the model.
    Params: model-> Model that will get saved,
    model_file-> Name and relative location of the to be file
    """
    model.save(model_file)


# Main function to load data, preprocess, train and save the model
def main(json_file, model_file):
    data = load_data(json_file)
    sentences = preprocess_data(data)
    model = train_word2vec(sentences)
    save_model(model, model_file)


def getWordSimilarity(
    word1, word2, model=Word2Vec.load("MLDataAndModels/word2vec.model")
):
    """
    This method returns similarity of given words in vector format.
    Params: Word1 and Word2
    Returns: int, containing similatiry vector
    """
    # When do this multiple times you may have to preload model once and use it multiple times.
    # model = Word2Vec.load('word2vec.model')
    return model.wv.similarity(word1, word2)


def getWordVec(Word, model=Word2Vec.load("MLDataAndModels/word2vec.model")):
    """
    Method for getting vector of a single word
    Params: str Word, word you need vector of.
    Returns: Vector
    """
    # When do this multiple times you may have to preload model once and use it multiple times.
    # model = Word2Vec.load('word2vec.model')
    return model.wv[Word]


def getSentenceVector(sentence, model=Word2Vec.load("MLDataAndModels/word2vec.model")):
    """
    Method for sentence vectorizing.
    Params: sentence-> sentenco to get vector from,
    model-> word model, defaults to model=Word2Vec.load('MLDataAndModels/word2vec.model')
    Returns: Vector
    """
    cond = None
    if sentence != cond:
        words = sentence.split()
        word_vectors = [model.wv[word] for word in words if word in model.wv]
        if not word_vectors:
            return np.zeros(model.vector_size)
        sentence_vector = np.mean(word_vectors, axis=0)
        return sentence_vector
    else:
        return sentence


# Example usage
# json_file = "Word2VecData.json"  # Replace with your JSON file path
# model_file = "word2vec.model"  # Replace with your desired model file name

# This file is to create word2vec.model, if model already exist, there is no reason to run this.
# main(json_file, model_file)
