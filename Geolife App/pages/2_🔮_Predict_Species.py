import pandas as pd
import streamlit as st
import joblib
import sklearn
import requests

### Config
st.set_page_config(
    page_title="Predict species",
    page_icon="🔮",
    layout="wide"
)


### App
st.header("Predict species 🔮")

@st.cache(allow_output_mutation=True, show_spinner=False)
def load_model_classes():
    model = joblib.load('model/RF_model.sav')
    species_details = pd.read_csv('data/species_details.csv', delimiter=';', index_col=0)
    classes = {species_id : species_details.loc[species_id, 'GBIF_species_name'] for species_id in model.classes_}
    classes = pd.DataFrame.from_dict(classes, orient='index').rename(columns={0:'specie'})
    return model, classes

@st.cache
def predict_top30(model, classes, input):
    classes['proba']= model.predict_proba([input])[0]
    results = classes.sort_values(by='proba', ascending=False).iloc[:30, 0]
    return results

@st.cache
def get_image(specie):
    s = requests.Session()
    url = 'https://api.wikimedia.org/core/v1/wikipedia/en/search/page?'

    params = {
        'q': specie,
        'project': 'wikispecies',
        'limit':1
    }

    r = s.get(url=url, params=params)
    image_url = r.json()['pages'][0]['thumbnail']['url'][2:]
    return 'https://' + image_url


with st.spinner(text="Model and data loading in progress...") : 
    model, classes = load_model_classes()
    st.success('Model loaded', icon="✅")

default_values = [14.8375,
 8.175,
 34.63983,
 562.34546,
 27.5,
 3.9,
 23.6,
 11.983334,
 21.983334,
 22.033333,
 8.45,
 852.0,
 129.0,
 16.0,
 43.632095,
 329.0,
 96.0,
 127.0,
 256.0,
 1591.0,
 1375.0,
 15.0,
 23.0,
 20.0,
 69.0,
 34.0,
 43.0,
 43.6017875671387,
 6.9401950836181605]

st.subheader('Input:')

col1, col2, col3, col4 = st.columns(4)

with col1:
    bio_1 = st.number_input('Annual Mean Temperature', value=default_values[0])
    bio_2 = st.number_input('Mean Diurnal Range (Mean of monthly (max temp - min temp))', value=default_values[1])
    bio_3 = st.number_input('Isothermality (bio_2/bio_7) (* 100)', value=default_values[2])
    bio_4 = st.number_input('Temperature Seasonality (standard deviation * 100)', value=default_values[3])
    bio_5 = st.number_input('Max Temperature of Warmest Month', value=default_values[4])
    bio_6 = st.number_input('Min Temperature of Coldest Month', value=default_values[5])
    bio_7 = st.number_input('Temperature Annual Range', value=default_values[6])
    bio_8 = st.number_input('Mean Temperature of Wettest Quarter', value=default_values[7])

with col2:  
    bio_9 = st.number_input('Mean Temperature of Driest Quarter', value=default_values[8])
    bio_10 = st.number_input('Mean Temperature of Warmest Quarter', value=default_values[9])
    bio_11 = st.number_input('Mean Temperature of Coldest Quarter', value=default_values[10])
    bio_12 = st.number_input('Annual Precipitation', value=default_values[11])
    bio_13 = st.number_input('Precipitation of Wettest Month', value=default_values[12])
    bio_14 = st.number_input('Precipitation of Driest Month', value=default_values[13])
    bio_15 = st.number_input('Precipitation Seasonality (Coefficient of Variation)', value=default_values[14])

with col3:
    bio_16 = st.number_input('Precipitation of Wettest Quarter', value=default_values[15])
    bio_17 = st.number_input('Precipitation of Driest Quarter', value=default_values[16])
    bio_18 = st.number_input('Precipitation of Warmest Quarter', value=default_values[17])
    bio_19 = st.number_input('Precipitation of Coldest Quarter', value=default_values[18])
    bdticm = st.number_input('Absolute Depth to Bedrock in cm', value=default_values[19])
    bldfie = st.number_input('Bulk Density in kg/m3 at 15cm depth', value=default_values[20])
    cecsol = st.number_input('Cation Exchange Capacity of Soil in cmolc/kg 15cm depth', value=default_values[21])

with col4:
    clyppt = st.number_input('Clay (0-2 micro meter) Mass Fraction at 15cm depth', value=default_values[22])
    orcdrc = st.number_input('Soil Organic Carbon Content (g/kg at 15cm depth)', value=default_values[23])
    phihox = st.number_input('Ph x 10 in H20 (at 15cm depth)', value=default_values[24])
    sltppt = st.number_input('Silt Mass Fraction at 15cm depth', value=default_values[25])
    sndppt = st.number_input('Sand Mass Fraction at 15cm depth', value=default_values[26])
    latitude = st.number_input('Latitude', value=default_values[27])
    longitude = st.number_input('Longitude', value=default_values[28])


    

if st.button('Predict species') :
    top30 = predict_top30(model, classes, default_values)

    st.subheader('Results:')

    col1_r, col2_r, col3_r, col4_r, col5_r = st.columns(5)
    
    for specie in top30[:6]:
        with col1_r:
            image = get_image(specie)
            st.image(image, caption=specie)
        
    for specie in top30[6:12]:
        with col2_r:
            image = get_image(specie)
            st.image(image, caption=specie)
        
    for specie in top30[12:18]:
        with col3_r:
            image = get_image(specie)
            st.image(image, caption=specie)

    for specie in top30[18:24]:
        with col4_r:
            image = get_image(specie)
            st.image(image, caption=specie)
    
    for specie in top30[24:]:
        with col5_r:
            image = get_image(specie)
            st.image(image, caption=specie)