import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer, strip_accents_unicode, ENGLISH_STOP_WORDS
from sklearn.metrics.pairwise import cosine_similarity

def calculate_correlation_matrix(lyrics):
    vectorizer = TfidfVectorizer(stop_words=list(ENGLISH_STOP_WORDS))
    features = vectorizer.fit_transform(lyrics, strip_accents_unicode)
    correlation_matrix = cosine_similarity(features)
    return correlation_matrix.tolist()
