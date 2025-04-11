# 📚 LDA Topic Modeling with Stochastic Variational Inference

This project implements the **Stochastic Variational Inference (SVI)** algorithm for **Latent Dirichlet Allocation (LDA)**, as introduced in the paper:

> **Hoffman, M. D., Blei, D. M., Wang, C., & Paisley, J. (2013)**. Stochastic Variational Inference. *Journal of Machine Learning Research*.

The algorithm is implemented from scratch in Python and applied to a custom corpus of **Wikipedia articles** to discover latent semantic topics.

---

## 📂 Project Structure

```
.
├── src/
│   ├── data_preparation.py     # Text cleaning, tokenization, vectorization
│   ├── lda_utils.py            # Core functions: Dirichlet, ELBO helpers, top words
│   ├── svi.py                  # Main SVI algorithm for LDA
│   └── visualization.py        # Plotting functions (wordclouds, pie charts, bar plots)
├── data/
│   └── wikipedia_corpus.json   # Pre-extracted and cleaned Wikipedia articles
├── notebook/
│   └── lda_svi_analysis.ipynb  # Main report with code, results, and commentary
├── README.md
└── requirements.txt
```

---

## 🧪 Setup & Installation

1. Clone the repository:
```bash
git clone https://github.com/your-username/lda-svi-project.git
cd lda-svi-project
```

2. Create a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

Dependencies include:
- `numpy`
- `nltk`
- `matplotlib`, `plotly`
- `wordcloud`
- `pandas`

---

## 🚀 How to Run

1. Prepare or load your Wikipedia dataset (already available as `wikipedia_corpus.json`)
2. Launch the notebook:

```bash
jupyter notebook notebook/lda_svi_analysis.ipynb
```

3. Follow the notebook to:
   - Load and vectorize the data
   - Run the SVI algorithm
   - Visualize the topics and interpret the results

---

## 📊 Sample Outputs

### 🧠 Top Words per Topic

Each topic is represented by its most probable words, extracted from the variational posterior $\lambda$.

### 🌫 Word Clouds

Word clouds are generated to visualize the dominant terms of each topic:

![wordclouds](./screenshots/wordclouds.png)

### 📈 Topic Distributions

Pie chart showing dominant topic frequencies across the corpus:

![piechart](./screenshots/piechart.png)

### 📊 Seed-wise Topic Breakdown

Bar chart showing how topics vary across thematic seeds:

![barplot](./screenshots/barplot.png)

---

## ✍️ Notes

- The training corpus includes ~1200 articles from 8 Wikipedia seeds (e.g. history, art, internet).
- Topics are inferred using 500 iterations of SVI with:
  - $K=10$ topics
  - $\alpha = \eta = 1.0$
  - Learning schedule: $\tau = 100$, $\kappa = 0.7$

---

## 🧠 About

This project was developed as part of the “Modèles génératifs” specialization course in the M2 Master program.

It aims to combine:
- **Probabilistic modeling**
- **Variational inference**
- **Natural language understanding**
- **Data visualization**

---

## 📜 License

MIT License. See `LICENSE` file for details.
