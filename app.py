import pickle
import streamlit as st
import requests

import requests
from bs4 import BeautifulSoup

def get_anime_poster(anime_id,anime_list):
    # Send a GET request to the anime page
    anime_url = f"https://myanimelist.net/anime/{anime_id}/{anime_list}"
    response = requests.get(anime_url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the poster image element
        poster_img = soup.find('img', class_='ac')

        # Check if the poster image element exists
        if poster_img:
            if 'src' in poster_img.attrs:
                poster_url = poster_img['src']
            else:
                # If 'src' attribute is not present, try 'data-src'
                poster_url = poster_img.get('data-src')

            return poster_url

        else:
             print("Poster image not found.")
    else:
        print("Failed to retrieve anime page.")


# Example usage

# poster_url = get_anime_poster(anime_url)
# if poster_url:
#     print("Poster URL:", poster_url)


def recommend(anime):
    index = animes[animes['name'] == anime].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_anime_names = []
    recommended_anime_posters = []
    for i in distances[1:6]:
        # fetch the movie poster
        anime_id = animes.iloc[i[0]].anime_id
        recommended_anime_posters.append(get_anime_poster(anime_id,anime_list))
        recommended_anime_names.append(animes.iloc[i[0]]['name'])

    return recommended_anime_names,recommended_anime_posters



st.header('Anime Recommender System')
animes = pickle.load(open('anime_list.pkl','rb'))
similarity = pickle.load(open('similarity.pkl','rb'))

anime_list = animes['name'].values
selected_anime = st.selectbox(
    "Type or select a movie from the dropdown",
    anime_list
)

if st.button('Show Recommendation'):
    recommended_anime_names,recommended_anime_posters = recommend(selected_anime)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(recommended_anime_names[0])
        st.image(recommended_anime_posters[0])
    with col2:
        st.text(recommended_anime_names[1])
        st.image(recommended_anime_posters[1])

    with col3:
        st.text(recommended_anime_names[2])
        st.image(recommended_anime_posters[2])

    with col4:
        st.text(recommended_anime_names[3])
        st.image(recommended_anime_posters[3])
    with col5:
        st.text(recommended_anime_names[4])
        st.image(recommended_anime_posters[4])