import streamlit as st
import pickle
import pandas as pd
import requests
import zipfile
import os

#model = pickle.load(open('similarity.pkl', 'rb'))
with zipfile.ZipFile("model.zip","r") as zip_ref:
    print('Extracting all the files now...') 
    zip_ref.extractall("model")
    print('Done!')
    
model = pickle.load(open('model/similarity - Copy.pkl', 'rb'))

movies = pickle.load(open('movies.pkl', 'rb'))
movies_list = movies['title'].values

st.title('Movie Recommender System')
selected_movie_name = st.selectbox('Select a movie:', movies_list)

def fetch_poster(movie_id):
    print("movies id"   , movie_id)
    url = "https://api.themoviedb.org/3/movie/{}?language=en-US".format(movie_id)

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIxN2JhMTc0NjY5ODBlZThhYTY5Mzc3Yzc0ODgyYWY0ZiIsIm5iZiI6MTczMzU2ODg4Ny45NTEsInN1YiI6IjY3NTQyOTc3MmEwZTljNzlmMTliOGQ5OCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.0KQtPV9VHfDGsm5yP8tcEy7UsFsQ4zfzfOzU5tN7ZFg"
    }

    response = requests.get(url, headers=headers)
    print(response.json())
    data = response.json()
    
    if('status_code' in data and data['status_code'] == 34):
        return "https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.123rf.com%2Fphoto_104546151_stock-vector-no-image-available-sign-internet-web-icon-to-indicate-the-absence-of-image-until-it-will-be-download.html&psig=AOvVaw0t8sX0F1VpR5Bt2Z8gj1lY&ust=1633511718963000&source=images&cd=vfe&ved=0CAsQjRxqFwoTCJjX1J6J8fMCFQAAAAAdAAAAABAD"
    
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/original" + poster_path
    return full_path

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(model[index])), reverse=True, key=lambda x: x[1])
    recommended_movies = []
    recommended_movies_posters = []
    
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id	
        recommended_movies_posters.append(fetch_poster(movie_id))
        recommended_movies.append(movies.iloc[i[0]].title)
    return recommended_movies, recommended_movies_posters



if st.button('Recommend'):
    recommended_movies,recommended_movies_posters = recommend(selected_movie_name)
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.image(recommended_movies_posters[0])
        st.text(recommended_movies[0])
    with col2:
        st.image(recommended_movies_posters[1])
        st.text(recommended_movies[1])
    with col3:
        st.image(recommended_movies_posters[2])
        st.text(recommended_movies[2])
    with col4:
        st.image(recommended_movies_posters[3])
        st.text(recommended_movies[3])
    with col5:
        st.image(recommended_movies_posters[4])
        st.text(recommended_movies[4])


