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

kanal_gliwicki = ee.FeatureCollection('projects/jakub-hempel/assets/kanal_gliwicki_wgs84')

geojson = {
    'type': 'Polygon',
    'coordinates': [[[14.483845, 52.564113],
                     [14.78914, 52.58696],
                     [14.80168, 54.005695],
                     [13.686192, 53.950777],
                     [13.922478, 52.982902],
                     [14.153269, 52.657586],
                     [14.483845, 52.56113]]]}

warta = ee.FeatureCollection(ee.Geometry(geojson))

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
