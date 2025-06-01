# 🎬 Movie Recommender App

A simple Streamlit app that recommends movies using the [TMDb API](https://developer.themoviedb.org/) and a local dataset with streaming availability.

## 🚀 Features

- 🔍 **Genre-based** recommendations using TMDb genres
- 🎯 **Title-based** search that finds similar movies
- 📺 Platform info: Netflix, Hulu, Prime Video, Disney+
- 📝 Overviews, ratings, and streaming links for each result
- Cached data loading for speed optimization

## 🛠️ Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Anastasios-Mourmouris/movie-recommender.git
   cd movie-recommender
   ```

2. **Set up virtual environment (optional but recommended)**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Create `.env` file**:
   Rename `.env.example` to `.env` and add your TMDb API key.

5. **Run the app**:
   ```bash
   streamlit run your_script_name.py
   ```

## 🧠 Tech Stack

- [Streamlit](https://streamlit.io/)
- [TMDb API](https://developer.themoviedb.org/)
- [Pandas](https://pandas.pydata.org/)
- [dotenv](https://pypi.org/project/python-dotenv/)
