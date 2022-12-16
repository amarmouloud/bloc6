import streamlit as st

st.set_page_config(
    page_title="Home",
    page_icon="🏡",
)

st.write("# Welcome to our App! 👋")

st.sidebar.success("Select a page above.")

st.markdown(
    """
    This application was build for the obtention of the Fullstack Data Science certification by Jedha

    ### What is it about?
    The dataset comes from the [GeoFileCLEF 2020](https://www.kaggle.com/competitions/geolifeclef-2022-lifeclef-2022-fgvc9/overview) Kaggle Competition.
    The goal of this project is to predict the location of plants and animals species.
    The initial dataset provided observations from the United States dand France. This project focus on France.
    ### Who did it ?
    - Amar Mouloud
    - Marion Robin  
 
"""
)