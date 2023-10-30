import streamlit as st
st.set_page_config(layout="wide", page_title="🦠 SABI | OdrApp 💦")

from maps.show_map import show_map
from maps.visualizationparams import get_vis_params
from imagery.sentinel_imagery import get_all_layers
from stats import get_images_stats
from typing import Final


@st.cache_data
def get_stats_cache():
    return get_images_stats()


@st.cache_data
def get_layers_cache():
    return get_all_layers()


@st.cache_data
def get_vis_params_cache():
    return get_vis_params()


index_name: Final = "SABI"

all_layers = get_layers_cache()[index_name]
layers = list(all_layers.keys())

colormap = get_vis_params_cache()[index_name]

if not "layer" in st.session_state:
    st.session_state["layer"] = layers[-1]

tab1, tab2 = st.tabs(["🗺️ Map", "📈 Chart"])

with tab1:
    widget = st.empty()
    col1, col2, col3 = st.columns((1, 9, 0.8))
    with col1:
        if st.button("Previous layer", type="primary"):
            if st.session_state.layer == layers[0]:
                st.session_state["layer"] = layers[-1]
            else:
                st.session_state["layer"] = layers[
                    layers.index(st.session_state.layer) - 1
                ]
    with col3:
        if st.button("Next layer", type="primary"):
            if st.session_state.layer == layers[-1]:
                st.session_state["layer"] = layers[0]
            else:
                st.session_state["layer"] = layers[
                    layers.index(st.session_state.layer) + 1
                ]

    st.session_state["layer"] = widget.select_slider(
        label="Wybierz datę zobrazowania", options=layers, value=st.session_state.layer
    )

    show_map(all_layers[st.session_state.layer], index_name, colormap)

with tab2:
    col1, col2 = st.columns((3, 1))
    with st.container():
        with col1:
            st.subheader(f"{index_name} line plot")
            st.line_chart(get_stats_cache()[index_name]["mean"])
        with col2:
            st.subheader("Data")
            st.write(get_stats_cache()[index_name])
