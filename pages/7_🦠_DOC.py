import streamlit as st

st.set_page_config(layout="wide", page_title="🦠 DOC | OdrApp 💦")

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


index_name: Final = "DOC"

all_layers = get_layers_cache()[index_name]
layers = list(all_layers.keys())

colormap = get_vis_params_cache()[index_name]

st.subheader("🦠 DOC - Dissolved Organic Carbon")

tab1, tab2 = st.tabs(["🗺️ Map", "📈 Chart"])

with tab1:
    if not "layer" in st.session_state:
        st.session_state["layer"] = layers[-1]

    widget = st.empty()
    col1, col2, col3 = st.columns((1, 9, 0.8))
    with col1:
        if st.button("Previous layer", type="primary"):
            if st.session_state.layer == layers[0]:
                st.session_state["layer"] = layers[-1]
            else:
                st.session_state["layer"] = layers[layers.index(st.session_state.layer) - 1]
    with col3:
        if st.button("Next layer", type="primary"):
            if st.session_state.layer == layers[-1]:
                st.session_state["layer"] = layers[0]
            else:
                st.session_state["layer"] = layers[layers.index(st.session_state.layer) + 1]

    try:
        st.session_state["layer"] = widget.select_slider(
            label="Choose imagery date",
            options=layers,
            value=st.session_state.layer,
        )
    except:
        st.session_state["layer"] = layers[-1]

    with st.spinner("Wait for the map ..."):
        try:
            show_map(
                all_layers[st.session_state.layer],
                st.session_state.layer,
                index_name,
                colormap
            )
        except: 
            show_map(
                all_layers[layers[-1]],
                layers[-1],
                index_name,
                colormap
            )


with tab2:
    col1, col2 = st.columns((3, 1))
    with st.container():
        with col1:
            st.subheader(f"{index_name} values across time")
            st.line_chart(get_stats_cache()[index_name])
        with col2:
            st.subheader("Data [mg/l]")
            st.write(get_stats_cache()[index_name])
