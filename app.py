import streamlit as st
import pickle
import pandas as pd
import requests

# Load the pickled data
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Function to fetch movie poster from API
def fetch_poster(movie_id):
    try:
        response = requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=09013c7aec01fb434986b37bf2fdec14", timeout=10)
        data = response.json()
        poster_path = data['poster_path']
        full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
        return full_path
    except requests.exceptions.Timeout:
        st.error("The request timed out")
        return None

# Function to recommend movies
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters


page_bg_img = '''
<style>
.stApp {
  background-image: url("https://i.ibb.co/zhSJ8t3/output-onlinepngtools.png");
  background-size: cover;
}
</style>
'''

st.markdown(page_bg_img, unsafe_allow_html=True)


# Streamlit app
st.title('🎬 Movie Recommendation System')

st.sidebar.title("Menu")
selected_movie_name = st.sidebar.selectbox('Enter Your Favourite Movie', movies['title'].values)

if st.sidebar.button('Recommend'):
    names, posters = recommend(selected_movie_name)
    st.subheader("Here are the top 5 movie recommendations for you")
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(names[0])
        st.image(posters[0])
    with col2:
        st.text(names[1])
        st.image(posters[1])
    with col3:
        st.text(names[2])
        st.image(posters[2])
    with col4:
        st.text(names[3])
        st.image(posters[3])
    with col5:
        st.text(names[4])
        st.image(posters[4])
