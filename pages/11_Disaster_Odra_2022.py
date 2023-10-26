import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from sentinel_imagery import get_all_disaster_layers
from show_map import disaster_map
from visualizationparams import get_vis_params
from stats import get_disaster_stats


@st.cache_data
def get_vis_params_cache():
    return get_vis_params()


@st.cache_data
def get_disaster_layers_cache():
    return get_all_disaster_layers()


@st.cache_data
def get_disaster_stats_cache():
    return get_disaster_stats()


st.set_page_config(layout="wide")


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
    "Ostrava": "#7CB3FE",
    "Wroclaw": "#FCAE78",
    "Frankfurt": "#64E789",
    "Szczecin": "#A65FDB",
}

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

if not "layer" in st.session_state:
    st.session_state["layer"] = None

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
        st.session_state["layer"] = layers[0]
    elif disaster_date == "During disaster":
        st.session_state["layer"] = layers[1]
    elif disaster_date == "After disaster":
        st.session_state["layer"] = layers[2]
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
                )
            )

        fig.update_layout(
            title=f"{st.session_state.index_name} - median values from POIs",
            yaxis_title="Value",
            height=550,
            width=610,
        )

        st.plotly_chart(fig)

with col3:
    if (
        st.session_state.city
        and st.session_state.index_name
        and st.session_state.layer is not None
    ):
        disaster_map(
            disaster_layers[st.session_state.layer],
            st.session_state.index_name,
            st.session_state.city,
            colormap,
            st.session_state.zoom,
        )
