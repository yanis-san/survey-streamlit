import streamlit as st
import os
from supabase import create_client, Client

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


url = st.secrets["SUPABASE"]["URL"]
key = st.secrets["SUPABASE"]["KEY"]

supabase: Client = create_client(url, key)


with st.form(key='my_form'):
    st.write('### Etes-vous étudiant chez nous ?')
    is_student = st.radio('Etudiant', ['Oui', 'Non'], key='is_student', label_visibility='hidden')
    
    st.write('### Si oui, quel cours avez-vous déjà suivi ?')
    which_course = st.radio('Cours suivi', ['Japonais', 'Chinois', 'Coréen','Je ne suis pas étudiant chez vous mais je souhaite donner mon avis'], key='which_course', label_visibility='hidden')
    
    st.write('### Quelle langue vous intéresse le plus chez nous ?')
    favorite_language = st.radio('Langue préférée', ['Japonais', 'Chinois', 'Coréen'], key='favorite_language', label_visibility='hidden')
    
    st.write('### Avez-vous déjà appris une langue avec un livre ?')
    learn_with_books = st.radio('Appris avec un livre', ['Oui', 'Non'], key='learn_with_books', label_visibility='hidden')
    
    st.write('### Vous préférez que les livres soient dans quelle langue ?')
    wanted_language = st.radio('Langue des livres', ['Arabe', 'Anglais', 'Français'], key='wanted_language', label_visibility='hidden')
    
    submit_button = st.form_submit_button(label='Soumettre')
if submit_button:
    try:
        data, count = supabase.table('survey').insert([
            {
                'is_student': is_student,
                'which_course': which_course,
                'favorite_language': favorite_language,
                'learn_with_books': learn_with_books,
                'wanted_language': wanted_language
            }
        ]).execute()

        if count == 0:
            st.error('Une erreur est survenue lors de l\'insertion des données dans la base de données.')
        else:
            st.success('Merci pour votre participation ! Nous avons bien reçu vos réponses.')
    except Exception as e:
        st.error('Une erreur est survenue lors de l\'insertion des données dans la base de données.')