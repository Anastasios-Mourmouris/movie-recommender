import streamlit as st
import requests
import pandas as pd
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
API_KEY = os.getenv("TMDB_API_KEY")

# Constants
BASE_URL = 'https://api.themoviedb.org/3'
GENRE_URL = f'{BASE_URL}/genre/movie/list'
MOVIE_URL = f'{BASE_URL}/discover/movie'
DATA_FILE = "MoviesOnStreamingPlatforms.csv"

# App Config
st.set_page_config(page_title="🎬 Movie Recommender", layout="centered")
st.title("🎬 Movie Recommender")
st.markdown("Choose your movie style and get recommendations from the TMDb API + local streaming data.")


@st.cache_data
def load_movie_platform_data():
    df = pd.read_csv(DATA_FILE)
    return df.loc[:, ~df.columns.str.contains('^Unnamed')]


movie_data_df = load_movie_platform_data()


def get_movie_platforms(title):
    movie = movie_data_df[movie_data_df['Title'] == title]
    if movie.empty:
        return ["Buy movie online"]
    platforms = [p for p in ['Netflix', 'Hulu', 'Prime Video', 'Disney+'] if movie.iloc[0][p] == 1]
    return platforms or ["Buy movie online"]


def display_movie(movie):
    st.subheader(movie['title'])
    st.markdown(f"⭐ **Rating:** {movie['vote_average']:.1f}")
    st.markdown(f"🎯 **Where to watch:** {', '.join(get_movie_platforms(movie['title']))}")
    if movie.get('overview'):
        st.markdown(f"📝 **Overview:** {movie['overview']}")


def genre_recommendation():
    st.session_state.setdefault('genre_page', 0)
    st.session_state.setdefault('genre_results', [])

    genre_response = requests.get(GENRE_URL, params={'api_key': API_KEY})
    genres = genre_response.json().get('genres', [])
    genre_names = [g['name'] for g in genres]

    selected_genre = st.selectbox("🎞️ Select a genre:", genre_names)

    if st.button("Show Movies"):
        st.session_state['genre_page'] = 0
        st.session_state['selected_genre'] = selected_genre
        st.session_state['genre_results'] = []

    if 'selected_genre' in st.session_state:
        genre_id = next((g['id'] for g in genres if g['name'] == st.session_state['selected_genre']), None)
        if genre_id:
            movies = []
            for page in range(1, 4):  # limit to 60 movies for performance
                response = requests.get(MOVIE_URL, params={
                    'api_key': API_KEY,
                    'with_genres': genre_id,
                    'page': page,
                    'sort_by': 'vote_average.desc',
                    'vote_count.gte': 1000
                })
                movies.extend(response.json().get('results', []))

            sorted_movies = sorted(movies, key=lambda x: x['vote_average'], reverse=True)
            end = (st.session_state['genre_page'] + 1) * 10
            st.session_state['genre_results'] = sorted_movies[:end]

            for movie in st.session_state['genre_results']:
                display_movie(movie)
                st.divider()

            if end < len(sorted_movies):
                if st.button("🎬 Show More"):
                    st.session_state['genre_page'] += 1
                    st.rerun()


def title_recommendation():
    st.session_state.setdefault('title_page', 0)
    st.session_state.setdefault('title_results', [])
    title_input = st.text_input("🎥 Enter a movie title:")

    if st.button("Search"):
        st.session_state['title_input'] = title_input
        st.session_state['title_page'] = 0
        st.session_state['title_results'] = []

    if 'title_input' in st.session_state and st.session_state['title_input']:
        search_url = f"{BASE_URL}/search/movie"
        response = requests.get(search_url, params={"api_key": API_KEY, "query": st.session_state['title_input']})
        results = response.json().get("results", [])

        if not results:
            st.error("🚫 Movie not found.")
            return

        movie_id = results[0]["id"]
        similar_url = f"{BASE_URL}/movie/{movie_id}/similar"
        similar_movies = []
        for page in range(1, 4):
            r = requests.get(similar_url, params={"api_key": API_KEY, "page": page})
            similar_movies.extend(r.json().get("results", []))

        sorted_movies = sorted(similar_movies, key=lambda x: x['vote_average'], reverse=True)
        end = (st.session_state['title_page'] + 1) * 10
        st.session_state['title_results'] = sorted_movies[:end]

        for movie in st.session_state['title_results']:
            display_movie(movie)
            st.divider()

        if end < len(sorted_movies):
            if st.button("🎬 Show More Recommendations"):
                st.session_state['title_page'] += 1
                st.rerun()


# --- UI Layout ---
option = st.sidebar.radio("📂 Navigation", ["Genre-based Recommendations", "Title-based Recommendations"])

if option == "Genre-based Recommendations":
    genre_recommendation()
elif option == "Title-based Recommendations":
    title_recommendation()



