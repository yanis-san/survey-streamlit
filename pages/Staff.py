import streamlit as st

from supabase import create_client, Client

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns



url = st.secrets["SUPABASE"]["URL"]
key = st.secrets["SUPABASE"]["KEY"]

supabase: Client = create_client(url, key)
is_logged_in = False
def create_bar_plot(data, title, xlabel, ylabel, size=100):
    fig, ax = plt.subplots(figsize=(6*size/100, 4*size/100))
    sns.barplot(x=data.index, y=data.values, ax=ax, palette="viridis")
    for i, value in enumerate(data.values):
        ax.text(i, value/2, str(value), color='white', ha='center', va='center')
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    st.pyplot(fig)

def create_grouped_bar_plot(df, title, xlabel, ylabel, size=100):
    fig, ax = plt.subplots(figsize=(6*size/100, 4*size/100))
    sns.countplot(x="favorite_language", hue="wanted_language", data=df, ax=ax, palette="viridis")
    ax.legend(title="Langue souhaitée pour les livres")
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)

    # Add labels with the exact values in the middle of the bars
    for p in ax.patches:
        ax.annotate(format(p.get_height(), '.0f'), 
                    (p.get_x() + p.get_width() / 2., p.get_height()/2), 
                    ha = 'center', 
                    va = 'center', 
                    color = 'white',
                    xytext = (0, 0), 
                    textcoords = 'offset points')

    st.pyplot(fig)
st.write("# Connexion")


def create_pie_chart(data, title, size=100):
    fig, ax = plt.subplots(figsize=(6*size/100, 6*size/100))
    wedges, texts, autotexts = ax.pie(data.values, labels=data.index, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    ax.set_title(title)
    ax.legend(wedges, data.index,
        title="Langues",
        loc="center left",
        bbox_to_anchor=(1, 0, 0.5, 1))
    st.pyplot(fig)

with st.form("login_form"):
    cols = st.columns(2)
    with cols[0]:
        username = st.text_input("Email")
    with cols[1]:
        password = st.text_input("Mot de passe", type="password")
    submitted = st.form_submit_button("Se connecter")
    if submitted:
        try :
            result = supabase.auth.sign_in_with_password({"email": username, "password": password})
            if result.user:
                st.success("Vous êtes connecté")
                is_logged_in = True
            else:
                st.error("Vous devez être connecté")

        except Exception as e:
   
            st.error(str(e))

if is_logged_in:
    response = supabase.table('survey').select("*").execute()
    
    df = pd.DataFrame(response.data)
    df_students = df[df['is_student'] == "Oui"]

    language_counts = df['wanted_language'].value_counts()
    language_counts_students = df_students['wanted_language'].value_counts()

    create_bar_plot(language_counts, 'Langues favorites', 'Langues', 'Nombre de personnes', size=75)
    create_pie_chart(language_counts, 'Répartition des langues favorites', size=125)
    create_grouped_bar_plot(df, 'Langue favorite en fonction de la langue asiatique préférée', 'Langue asiatique favorite', 'Nombre', size=100)
    create_pie_chart(language_counts_students, 'Répartition des langues favorites pour les étudiants de l\'institut torii', size=150)

    df['created_at'] = (pd.to_datetime(df['created_at']) + pd.Timedelta(hours=3)).dt.strftime('%Y-%m-%d %H:%M:%S')
    cols = df.columns.tolist()
    cols.insert(2, cols.pop(cols.index('username')))
    df = df.reindex(columns=cols)
    st.write(df)