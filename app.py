import streamlit as st
import pandas as pd
import pickle
from PIL import Image
import os
import requests


# URL of your hosted pickle file
URL = 'https://drive.google.com/uc?export=download&id=1l4WAy3_rt_s1_0gMSOOHJr8z_a4XHdeB'


# Local path where the pickle file will be saved temporarily

import gdown

URL = "https://drive.google.com/uc?export=download&id=1l4WAy3_rt_s1_0gMSOOHJr8z_a4XHdeB"
local_pickle_path = 'similarity.pkl'

if not os.path.exists(local_pickle_path):
    gdown.download(URL, local_pickle_path, quiet=False)

with open(local_pickle_path, 'rb') as f:
    similarity = pickle.load(f)


# load data
books_df = pickle.load(open('books.pkl','rb'))


#Recommend function
def recommend(book_title):
    book_index = books_df[books_df['title']==book_title].index[0]
    distances = similarity[book_index]
    books_list = sorted(list(enumerate(distances)),reverse=True, key=lambda x:x[1])[1:6]
    
    recommended_books = []
    recommended_books_cover = []
    for i in books_list:
        recommended_books.append(books_df.iloc[i[0]].title)
        isbn = str(books_df.iloc[i[0]]['isbn13'])
        cover_paths = f"book_images/{isbn}.jpg"
        recommended_books_cover.append(cover_paths)

    return recommended_books , recommended_books_cover



st.title('𝘽𝙤𝙤𝙠 𝙍𝙚𝙘𝙤𝙢𝙢𝙚𝙣𝙙𝙚𝙧 𝙎𝙮𝙨𝙩𝙚𝙢')
selected_book = st.selectbox("Select a book you like", books_df['title'].values)

if st.button("Recommend"):
    names, cover_paths = recommend(selected_book)
    cols = st.columns(len(names))

    for col, name, img_path in zip(cols, names, cover_paths):
        with col:
            st.image(img_path, use_container_width=True)
            st.markdown(f"**{name}**",unsafe_allow_html=True)