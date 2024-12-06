import os
import zipfile

import streamlit as st
import pickle
import requests
from dotenv import load_dotenv

load_dotenv()

API_ACCESS_TOKEN = os.getenv("API_ACCESS_TOKEN")

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?language=en-US".format(movie_id)

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer {}".format(API_ACCESS_TOKEN)
    }

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            if 'poster_path' in data and data['poster_path']:
                return "http://image.tmdb.org/t/p/w500" + data['poster_path']
            else:
                return "Poster not available for this movie."
        elif response.status_code == 404:
            return "Movie not found. Please check the movie ID."
        else:
            return f"An error occurred: {response.status_code} - {response.reason}"
    except requests.exceptions.RequestException as e:
        return f"An error occurred while fetching the poster: {e}"


def recommend(movie):
    movie_index = movies_list[movies_list['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended = []
    recommended_posters = []

    for i in movie_list:
        movie_id = movies_list.iloc[i[0]].id
        # Fetch-Poster from API
        recommended_posters.append(fetch_poster(movie_id))
        recommended.append(movies_list.iloc[i[0]].title)

    return recommended, recommended_posters
with zipfile.ZipFile("Data/movies.zip","r") as zip_ref:
    zip_ref.extractall("Data")
    print("Zipfiles is extracted!!!")
# similarity_data_file = zipfile.ZipFile("Data/movies.zip", "r").extract()

movies_list = pickle.load(open('Data/movies.pkl', 'rb'))
movies = movies_list['title'].values

similarity = pickle.load(open('Data/similarity.pkl', 'rb'))

st.title('Movie Recommender System')

selected_movie_name = st.selectbox('How would you like to connect!',
                    movies)

if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.image(posters[0])
        st.text(names[0])

    with col2:
        st.image(posters[1])
        st.text(names[1])

    with col3:
        st.image(posters[2])
        st.text(names[2])

    with col4:
        st.image(posters[3])
        st.text(names[3])

    with col5:
        st.image(posters[4])
        st.text(names[4])