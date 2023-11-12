import streamlit as st

st.set_page_config(
    layout="wide", page_title="Ecological Disaster - Oder 2022 | OdrApp 💦"
)

import plotly.graph_objects as go
import pandas as pd
from imagery.sentinel_imagery import get_all_disaster_layers, get_disaster_images
from maps.show_map import disaster_map, sections_map
from maps.visualizationparams import get_vis_params
from stats import get_disaster_stats, get_sections_stats
import urllib.request
from PIL import Image


@st.cache_data
def get_vis_params_cache():
    return get_vis_params()


@st.cache_data
def get_disaster_layers_cache():
    return get_all_disaster_layers()


@st.cache_data
def get_sections_layers_cache():
    return get_disaster_images()


@st.cache_data
def get_disaster_stats_cache():
    return get_disaster_stats()


@st.cache_data
def get_sections_stats_cache():
    return get_sections_stats()


tab1, tab2, tab3 = st.tabs(["🏙️ Cities", "✂️ Sections", "📈 Chart"])


cities = ["Ostrava", "Wroclaw", "Frankfurt", "Szczecin"]
indexes = [
    "NDWI",
    "NDVI",
    "NDSI",
    "SABI",
    "CGI",
    "CDOM",
    "DOC",
    "Cyanobacteria",
    "Turbidity",
]
coords = {
    "Ostrava": [18.248, 49.812, 11],
    "Wroclaw": [17.036, 51.111, 11],
    "Frankfurt": [14.496, 52.329, 11],
    "Szczecin": [14.605, 53.439, 11],
}
city_colors = {
    "Ostrava": "#FFA07A",
    "Wroclaw": "#B6D79A",
    "Frankfurt": "#E6E6FA",
    "Szczecin": "#87CEEB",
}

with tab1:
    if not "city" in st.session_state:
        st.session_state["city"] = None

    if not "index_name" in st.session_state:
        st.session_state["index_name"] = None

    if not "zoom" in st.session_state:
        st.session_state["zoom"] = None

    col1, col2, col3 = st.columns((2, 1.5, 5))

    with col1:
        st.session_state["city"] = st.selectbox(
            "Choose city", ("Ostrava", "Wroclaw", "Frankfurt", "Szczecin"), index=None
        )

        st.divider()

        st.session_state["index_name"] = st.selectbox(
            "Choose index",
            (
                "NDWI",
                "NDVI",
                "NDSI",
                "SABI",
                "CGI",
                "CDOM",
                "DOC",
                "Cyanobacteria",
                "Turbidity",
            ),
            index=None,
        )

    if st.session_state.city and st.session_state.index_name is not None:
        disaster_layers = get_disaster_layers_cache()[st.session_state.city][
            st.session_state.index_name
        ]
        layers = list(disaster_layers.keys())
        colormap = get_vis_params_cache()[st.session_state.index_name]

    if not "disaster_layer" in st.session_state:
        st.session_state["disaster_layer"] = None

    with col1:
        st.divider()
        disaster_date = st.radio(
            "Choose the layer you want to see",
            ["Before disaster", "During disaster", "After disaster"],
            captions=["2022-07-20", "2022-07-31", "2022-08-25"],
            index=None,
        )

    try:
        if disaster_date == "Before disaster":
            st.session_state["disaster_layer"] = layers[0]
        elif disaster_date == "During disaster":
            st.session_state["disaster_layer"] = layers[1]
        elif disaster_date == "After disaster":
            st.session_state["disaster_layer"] = layers[2]
    except:
        with col3:
            st.header("\n")
            st.warning("Please fill all selectboxes", icon="⚠️")

    if st.session_state.city is not None:
        st.session_state["zoom"] = coords[st.session_state.city]

    disaster_stats = get_disaster_stats_cache()

    if st.session_state.index_name and disaster_date is not None:
        with col1:
            st.divider()
            hover_template = "Value: %{y:.2f}<extra></extra>"

            fig = go.Figure()

            for city in cities:
                data = {
                    "City": [city] * 3,
                    "Time": ["Before disaster", "During disaster", "After disaster"],
                    "Value": [
                        disaster_stats["before"].at[city, st.session_state.index_name],
                        disaster_stats["during"].at[city, st.session_state.index_name],
                        disaster_stats["after"].at[city, st.session_state.index_name],
                    ],
                }
                city_df = pd.DataFrame(data)

                fig.add_trace(
                    go.Bar(
                        x=city_df["Time"],
                        y=city_df["Value"],
                        name=city,
                        hovertemplate=hover_template,
                        marker_color=city_colors[city],
                        marker_line_color="black",
                        marker_line_width=0.75,
                    )
                )

            fig.update_layout(
                title=f"{st.session_state.index_name} - median values from 100 POIs",
                yaxis_title="Value",
                height=550,
                width=610,
            )

            st.plotly_chart(fig)

    with col3:
        try:
            if (
                st.session_state.city
                and st.session_state.index_name
                and st.session_state.disaster_layer is not None
            ):
                disaster_map(
                    disaster_layers[st.session_state.disaster_layer],
                    st.session_state.index_name,
                    st.session_state.city,
                    colormap,
                    st.session_state.zoom,
                )
        except:
            st.header("\n")
            st.warning("Make sure you have filled in all the fields", icon="⚠️")
        finally:
            st.session_state["city"] = None
            st.session_state["index_name"] = None
            st.session_state["disaster_layer"] = None

with tab2:
    # st.write(
    #    "Here is presented the extended analysis of the water condition in two sections of Oder. Firstly, *Kanal Gliwicki*, when the disaster had started, and secondly the part from the place where the Warta River flows into the river up to its estuary to the Baltic Sea."
    # )
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
        if disaster_layer == "Before disaster":
            sections_map(warta_collection, kanal_gliwicki_collection, range(0, 4, 3))
        elif disaster_layer == "During disaster":
            sections_map(warta_collection, kanal_gliwicki_collection, range(1, 5, 3))
        elif disaster_layer == "After disaster":
            sections_map(warta_collection, kanal_gliwicki_collection, range(2, 6, 3))

    with col3:
        urllib.request.urlretrieve(
            "https://i.imgur.com/xHV5fgI.jpg",
            "xHV5fgI.jpg",
        )
        image = Image.open("xHV5fgI.jpg")
        st.image(image)

    chart1, chart2 = st.columns(2)

    with chart1:
        st.header("\n")
        st.subheader("SABI Median Disaster Values")
        st.line_chart(get_sections_stats_cache()["SABI"])

        st.subheader("DOC Median Disaster Values")
        st.line_chart(get_sections_stats_cache()["DOC"])

    with chart2:
        st.header("\n")
        st.subheader("CDOM Median Disaster Values")
        st.line_chart(get_sections_stats_cache()["CDOM"])

        st.subheader("Cyanobacteria Median Disaster Values")
        st.line_chart(get_sections_stats_cache()["Cyanobacteria"])

with tab3:
    st.info(
        "**Page in progress**",
        icon="ℹ️",
    )
