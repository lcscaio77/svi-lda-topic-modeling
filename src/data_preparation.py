import json
from collections import Counter

from nltk.corpus import stopwords
from nltk.tokenize import WordPunctTokenizer


def vectorize_texts(texts, language="english"):
    """
    Tokenizes and vectorizes texts into a bag-of-words corpus.

    Args:
        texts (list of str): Input text documents.
        language (str, optional): Language for stopword removal. Defaults to "english".

    Returns:
        tuple: 
            - bow_corpus (list of list of int): Tokenized documents as word index sequences.
            - vocab (dict): Mapping of words to their indices.
    """
    tokenizer = WordPunctTokenizer()
    stop_words = set(stopwords.words(language))
    tokenized_documents = []

    for text in texts:
        tokenized_doc = tokenizer.tokenize(text.lower())
        cleaned_tokenized_doc = [t for t in tokenized_doc if t.isalpha() and t not in stop_words and len(t) > 2]
        tokenized_documents.append(cleaned_tokenized_doc)
    
    word_counts = Counter(word for doc in tokenized_documents for word in doc)
    vocab = {word: i for i, (word, _) in enumerate(word_counts.most_common(10000))}
    bow_corpus = [[vocab[word] for word in doc if word in vocab] for doc in tokenized_documents]

    return bow_corpus, vocab


if __name__ == "__main__":
    with open(f"../data/wikipedia_corpus.json", "r", encoding="utf-8") as f:
        wiki_articles = json.load(f)

    texts = [wiki_articles[article]["content"] for article in wiki_articles]
    
    bow_corpus, vocab = vectorize_texts(texts)
