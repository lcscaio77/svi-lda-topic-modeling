import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt
from wordcloud import WordCloud


def get_top_words(lambd, vocab, n_top_words=100):
    """
    Extracts top words per topic from a topic-word matrix.

    Args:
        lambd (np.ndarray): Topic-word distribution matrix.
        vocab (dict): Mapping of words to indices.
        n_top_words (int, optional): Number of top words per topic. Defaults to 100.

    Returns:
        pd.DataFrame: DataFrame of top words per topic, ranked by relevance.
    """
    inv_vocab = {i: w for w, i in vocab.items()}

    dict_top_words = {}
    for k in range(lambd.shape[0]):
        top_word_ids = np.argsort(lambd[k])[::-1][:n_top_words]
        top_words = [inv_vocab[i] for i in top_word_ids]
        dict_top_words[f"Topic {k}"] = top_words

    df_top_words = pd.DataFrame(dict_top_words)
    df_top_words.index += 1
    df_top_words.index.name = "Rank"
    
    return df_top_words


def plot_top_words_wordcloud(lambd, vocab, n_top_words=100, n_wordcloud=1):
    """
    Plots word clouds for the top words of selected topics.

    Args:
        lambd (np.ndarray): Topic-word distribution matrix.
        vocab (dict): Mapping of words to indices.
        n_top_words (int, optional): Number of top words per topic. Defaults to 100.
        n_wordcloud (int, optional): Number of topic word clouds to display. Defaults to 1.

    Returns:
        None
    """
    df_top_words = get_top_words(lambd, vocab, n_top_words)

    wordclouds = {}
    for i in range(n_wordcloud):
        top_words_freq = np.sort(lambd[i])[::-1][:n_top_words]
        min_freq = np.min(top_words_freq)
        max_freq = np.max(top_words_freq)

        top_words_freq_scaled = [(freq - min_freq) / (max_freq - min_freq) for freq in top_words_freq]

        wordcloud = {word:freq for (word, freq) in zip(df_top_words[f"Topic {i}"], top_words_freq_scaled)}
        wordclouds[f"Topic {i}"] = wordcloud

    _, axes = plt.subplots(nrows=n_wordcloud//2, ncols=2, figsize=(12, n_wordcloud*1.5))
    axes = axes.flatten()

    for i, topic in enumerate(wordclouds.keys()):
        wc = WordCloud(background_color="white", colormap="plasma").generate_from_frequencies(wordclouds[topic])

        axes[i].imshow(wc)
        axes[i].axis("off")
        axes[i].set_title(f"Topic {i}")

    plt.show()


def get_topic_distrib_info(doc_topic_distrib, wiki_articles):
    """
    Builds a DataFrame summarizing topic distribution for each document.

    Args:
        doc_topic_distrib (dict): Mapping of article titles to topic distribution arrays.
        wiki_articles (dict): Metadata for articles, including their seed topics.

    Returns:
        pd.DataFrame: DataFrame with article title, seed, top topic, and topic proportions.
    """
    docs_info = []

    for doc_title, theta in doc_topic_distrib.items():
        doc_info = {
            'Article': doc_title,
            'Seed': wiki_articles[doc_title]["seed"],
            'Top topic': np.argmax(theta)
        }
        for i, val in enumerate(theta):
            doc_info[f'Topic {i} proportion'] = np.round(val*100, 2)
        docs_info.append(doc_info)

    return pd.DataFrame(docs_info)


def plot_topics_distrib(docs_info):
    """
    Plots a pie chart showing the distribution of dominant topics across the corpus.

    Args:
        docs_info (pd.DataFrame): DataFrame with a 'Top topic' column for each document.

    Returns:
        None
    """
    topic_counts = docs_info['Top topic'].value_counts().sort_index().reset_index()
    topic_counts.columns = ['Topic', 'Count']
    topic_counts['Topic'] = topic_counts['Topic'].apply(lambda x: f'Topic {x}')

    fig = px.pie(
        topic_counts,
        names='Topic',
        values='Count',
        title="Distribution of dominant topics in the corpus",
        color_discrete_sequence=px.colors.qualitative.Safe
    )

    fig.update_layout(
        title_font_size=20,
        showlegend=False,
        margin_b=20
    )

    fig.update_traces(
        textinfo='label+percent',
        textfont_size=13,
        pull=[0.01]*len(topic_counts)
    )

    fig.show()

def plot_topics_distrib_by_seed(docs_info):
    """
    Plots a stacked bar chart of topic distribution by seed and returns the raw count table.

    Args:
        docs_info (pd.DataFrame): DataFrame containing 'Seed' and 'Top topic' columns.

    Returns:
        pd.DataFrame: Table of topic counts per seed.
    """
    df_topics_by_seed = pd.pivot_table(
        docs_info,
        index="Seed",
        columns="Top topic",
        aggfunc="size",
        fill_value=0
    )
    df_topics_by_seed.columns = [f"Topic {i}" for i in df_topics_by_seed.columns]

    df_topics_by_seed_percent = df_topics_by_seed.div(df_topics_by_seed.sum(axis=1), axis=0)
    df_topics_by_seed_percent = df_topics_by_seed_percent.reset_index()

    df_topics_by_seed_melted = df_topics_by_seed_percent.melt(id_vars='Seed', var_name='Topic', value_name='Proportion')

    fig = px.bar(
        df_topics_by_seed_melted,
        x="Seed",
        y="Proportion",
        color="Topic",
        barmode="stack",
        title="Distribution of Topics per Seed (Proportions)",
        color_discrete_sequence=px.colors.qualitative.Prism
    )

    fig.update_layout(
        xaxis_title="Seed",
        yaxis_title="Proportion",
        legend_title="Topic",
        yaxis_tickformat=".0%",
        template="plotly_white"
    )

    fig.show()

    return df_topics_by_seed
