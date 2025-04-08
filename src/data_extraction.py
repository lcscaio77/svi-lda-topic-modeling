import os, sys
import json
import warnings
from bs4 import GuessedAtParserWarning

import wikipedia
from wikipedia.exceptions import DisambiguationError, PageError


warnings.filterwarnings("ignore", category=GuessedAtParserWarning)


def get_wikipedia_page(title):
    try:
        page = wikipedia.page(title, auto_suggest=False)
        return page
    
    except DisambiguationError as e:
        print(f'Warning: "{title}" topic is ambigious, replaced by "{e.options[0]}".')
        return wikipedia.page(e.options[0], auto_suggest=False)
    
    except PageError:
        print(f'Error: Page "{title}" not found.')
        return None


def create_wikipedia_corpus(topics, n_articles_per_topics, folder_path="../data", output_file_name="wikipedia_corpus", verbose=True):
    articles = {}

    for topic in topics:
        linked_topics = wikipedia.search(topic, results=n_articles_per_topics)

        if verbose:
            print(f'Pages linked with "{topic}":')
        for linked_topic in linked_topics:
            if verbose:
                print(f"\t- {linked_topic}")

            page = get_wikipedia_page(linked_topic)

            articles[page.title] = {
                "title": page.title,
                "url": page.url,
                "content": page.content
            }

    with open(f"{folder_path}/{output_file_name}.json", "w", encoding="utf-8") as f:
        json.dump(articles, f, ensure_ascii=False, indent=2)

    print(f'Corpus saved as "{output_file_name}.json" in : {os.path.abspath(folder_path)}.')


if __name__ == "__main__":
    topics = [
        "culture",
        "history",
        "nature",
        "politics",
        "sports"
    ]

    create_wikipedia_corpus(topics, 10)
