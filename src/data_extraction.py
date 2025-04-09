import os
import json
import warnings
from pathlib import Path
from bs4 import GuessedAtParserWarning

import wikipedia
from wikipedia.exceptions import DisambiguationError, PageError


warnings.filterwarnings("ignore", category=GuessedAtParserWarning)

parent_dir = Path(__file__).resolve().parent.parent
os.chdir(parent_dir)


def get_wikipedia_page(title):
    try:
        page = wikipedia.page(title, auto_suggest=False)
        return page
    
    except DisambiguationError as e:
        print(f'Warning: "{title}" is ambigious, replaced by "{e.options[0]}".')
        if e.options[0] == title:
             print(f'Warning: Couldn\'t resolve "{e.options[0]}".')
             return None
        else:
            return get_wikipedia_page(e.options[0])
    
    except PageError:
        print(f'Error: Page "{title}" not found.')
        return None


def create_wikipedia_corpus(seeds, n_articles_per_seed, output_file_name="wikipedia_corpus", verbose=True):
    articles = {}

    for seed in seeds:
        linked_topics = wikipedia.search(seed, results=n_articles_per_seed)

        if verbose:
            print(f'Pages linked with "{seed}":')
        for linked_topic in linked_topics:
            if verbose:
                print(f"\t- {linked_topic}")

            page = get_wikipedia_page(linked_topic)
            if page is None:
                continue

            articles[page.title] = {
                "title": page.title,
                "seed": seed,
                "url": page.url,
                "content": page.content
            }

    with open(f"data/{output_file_name}.json", "w", encoding="utf-8") as f:
        json.dump(articles, f, ensure_ascii=False, indent=2)

    print(f'Corpus saved as "{output_file_name}.json" in : {os.path.abspath("data")}.')


if __name__ == "__main__":
    seeds = [
        "business",
        "culture",
        "history",
        "internet",
        "language",
        "nature",
        "politics",
        "sports"
    ]

    create_wikipedia_corpus(seeds, n_articles_per_seed=150)
