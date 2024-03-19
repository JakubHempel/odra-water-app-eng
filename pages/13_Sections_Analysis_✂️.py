import streamlit as st

st.set_page_config(
    layout="wide", page_title="Sections Analysis ✂️ | OdrApp 💦"
)

from imagery.sentinel_imagery import get_disaster_images
from maps.show_map import sections_map
from stats import get_sections_stats
import urllib.request
from PIL import Image

@st.cache_data
def get_sections_layers_cache():
    return get_disaster_images()

@st.cache_data
def get_sections_stats_cache():
    return get_sections_stats()

st.info(
        "Select the appropriate date in the form to display a visualization of index values from the disaster period. **Remember to select image from layer control panel in the top right corner of the map**",
        icon="ℹ️",
    )
st.header("\n")

warta_collection = get_sections_layers_cache()["UjscieWarty"]
kanal_gliwicki_collection = get_sections_layers_cache()["KanalGliwicki"]

col1, col2, col3 = st.columns((1.5, 5, 2))

with col1:
    disaster_date = st.empty()
    disaster_layer = st.radio(
        "Choose the date of the layer",
        ["Before disaster", "During disaster", "After disaster"],
        captions=["2022-07-20", "2022-07-31", "2022-08-25"],
    )

with col2:
    with st.spinner("Wait for the map ..."):
        if disaster_layer == "Before disaster":
            sections_map(warta_collection, kanal_gliwicki_collection, range(0, 4, 3))
        elif disaster_layer == "During disaster":
            sections_map(warta_collection, kanal_gliwicki_collection, range(1, 5, 3))
        elif disaster_layer == "After disaster":
            sections_map(warta_collection, kanal_gliwicki_collection, range(2, 6, 3))

with col3:
    urllib.request.urlretrieve(
        "https://imgur.com/a/yz2bCkq",
        "legend.jpg",
    )
    image = Image.open("legend.jpg")
    st.image(image)

chart1, chart2 = st.columns(2)

with chart1:
    st.header("\n")
    st.subheader("SABI Median Disaster Values")
    st.line_chart(get_sections_stats_cache()["SABI"])

    st.subheader("DOC Median Disaster Values [mg/l]")
    st.line_chart(get_sections_stats_cache()["DOC"])

with chart2:
    st.header("\n")
    st.subheader("CDOM Median Disaster Values [mg/l]")
    st.line_chart(get_sections_stats_cache()["CDOM"])

    st.subheader("Cyanobacteria Median Disaster Values [10^3 cell/ml]")
    st.line_chart(get_sections_stats_cache()["Cyanobacteria"])