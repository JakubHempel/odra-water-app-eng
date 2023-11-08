import streamlit as st

st.set_page_config(page_title="📃 Home | OdrApp 💦")

st.markdown("""
<style>
.align-text {
    text-align: justify;
}
</style>
""", unsafe_allow_html=True)

# Customize page title
st.title(
    "Welcome in OdrApp! 💦"
)

st.markdown(
    """
    <p class="align-text"> <i>OdrApp</i> is an application for monitoring water quality in the Oder river. It presents a multitemporal water quality analysis using satellite imagery and Google Earth Engine. It covers the period from 2018 to the present, from April to October.\n
    Explore all the aspects thoroughly and learn more about water pollution in the Oder River.</p>
    """, unsafe_allow_html=True)

st.divider()

st.markdown("""
    #### Suggested actions:
    1. Go to the *Indexes* 🌍 page and learn more about the spectral indices used in the analysis.
    2. Visit the index pages:
        - 💦 - commonly used indicators,
        - 🦠 - related to water pollution and quality.
        Explore maps with index visualizations in the 🗺️ Map tab and a line chart showing the average and median index values over the analyzed period in the 📈 Chart tab.
    3. Visit the *Charts* 📈 page to explore result visualizations on charts, such as:
        - "annual",
        - "monthly",
        - periodic,
        - from the 2022 Oder River ecological disaster.
    4. On the *Ecological Disaster - Oder 2022* page, you will find an extended analysis of water quality in four riverside cities: Ostrava (CZ), Wrocław, Frankfurt (DE), and Szczecin.

    **You can follow these steps in any order you prefer! To start, make sure to read about spectral indices on the *Indexes* 🌍 page.**

    ##### Enjoy your exploration! 💦
    """
)
