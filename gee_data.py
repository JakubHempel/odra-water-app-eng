import ee
import streamlit as st
import geemap.foliumap as geemap


@st.cache_data
def ee_authenticate(token_name="EARTHENGINE_TOKEN"):
    geemap.ee_initialize(token_name=token_name)


ee_authenticate(token_name="EARTHENGINE_TOKEN")

# Area of interest
odra = ee.FeatureCollection("projects/jakub-hempel/assets/odra")

wroclaw = ee.FeatureCollection("projects/jakub-hempel/assets/wroclaw")
wroclaw_buffer = ee.FeatureCollection("projects/jakub-hempel/assets/wroclaw_buffer")
szczecin = ee.FeatureCollection("projects/jakub-hempel/assets/szczecin")
frankfurt = ee.FeatureCollection("projects/jakub-hempel/assets/frankfurt")
frankfurt_buffer = ee.FeatureCollection("projects/jakub-hempel/assets/frankfurt_buffer")
ostrava = ee.FeatureCollection("projects/jakub-hempel/assets/ostrava")
ostrava_buffer = ee.FeatureCollection("projects/jakub-hempel/assets/ostrava_buffer")

wroclaw_points = ee.FeatureCollection("projects/jakub-hempel/assets/wroclaw_points_100")
szczecin_points = ee.FeatureCollection("projects/jakub-hempel/assets/szczecin_points_100")
frankfurt_points = ee.FeatureCollection("projects/jakub-hempel/assets/frankfurt_points_100")
ostrava_points = ee.FeatureCollection("projects/jakub-hempel/assets/ostrava_points_100")

city_boundaries = {
    "Ostrava": ostrava,
    "Wroclaw": wroclaw,
    "Frankfurt": frankfurt,
    "Szczecin": szczecin,
}

pois = {
    "Ostrava": ostrava_points,
    "Wroclaw": wroclaw_points,
    "Frankfurt": frankfurt_points,
    "Szczecin": szczecin_points,
}
