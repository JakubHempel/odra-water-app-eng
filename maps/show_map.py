import ee
import streamlit as st
import geemap.foliumap as geemap
import gee_data as gd
from maps.visualizationparams import get_vis_params
import time
from folium import plugins


@st.cache_data
def get_vis_params_cache():
    return get_vis_params()


def show_map(cache_image, index_name, vis_param):
    image = cache_image
    layer_name = image.get("system:index").getInfo()

    Map = geemap.Map(
        layer_ctrl=True, basemap="Esri.WorldGrayCanvas", control_scale=True
    )
    minimap = plugins.MiniMap()
    Map.add_child(minimap)
    Map.addLayer(image.select(index_name), vis_param, f"{index_name} - {layer_name}")
    Map.add_colorbar(vis_param, label=f"{index_name} Index")

    with st.spinner("Wait for the map ..."):
        time.sleep(1)

    Map.setCenter(17.036, 51.111, 11)
    Map.to_streamlit(height=800)


def disaster_map(cache_image, index_name, city, vis_param, zoom):
    Map = geemap.Map(basemap="Esri.WorldGrayCanvas", control_scale=True)
    minimap = plugins.MiniMap()
    Map.add_child(minimap)

    boundries_style = {
        "color": "#CD5C5C",
        "width": 1.5,
        "lineType": "solid",
        "fillColor": "96969612",
    }
    points_style = {
        "color": "000000a8",
        "pointSize": 4,
        "pointShape": "diamond",
        "width": 0.7,
        "lineType": "solid",
        "fillColor": "#FFFF99",
    }
    river_style = {
        "color": "#4682B4",
        "fillColor": "#E0FFFF",
        "width": 0.2,
        "lineType": "solid",
    }

    Map.addLayer(gd.odra.style(**river_style), {}, "Odra")

    image = cache_image
    date_acquired = image.get("DATE_ACQUIRED").getInfo()

    Map.addLayer(image, vis_param, f"{index_name} - {city} - {date_acquired}")
    Map.addLayer(gd.city_boundaries[city].style(**boundries_style), {}, city)
    Map.addLayer(gd.pois[city].style(**points_style), {}, f"POIs - {city}", False)

    Map.add_colorbar(vis_param, label=f"{index_name} Index")

    with st.spinner("Wait for the map ..."):
        time.sleep(1)

    Map.setCenter(*zoom)
    Map.to_streamlit(height=800)


def sections_map(warta_collection, kanal_gliwicki_collection, ran):
    sections_collection = warta_collection.merge(kanal_gliwicki_collection)
    sections_list = sections_collection.toList(6)

    Map = geemap.Map(basemap="Esri.WorldGrayCanvas", control_scale=True)
    minimap = plugins.MiniMap()
    Map.add_child(minimap)

    indexes = ["SABI", "CDOM", "DOC", "Cyanobacteria"]
    vis_params = get_vis_params_cache()

    for i in ran:
        image = ee.Image(sections_list.get(i))
        name = image.get("NAME").getInfo()
        date_acquired = image.get("DATE_ACQUIRED").getInfo()
        for index_name in indexes:
            Map.addLayer(
                image.select(index_name),
                vis_params[index_name],
                f"{index_name} - {name} - {date_acquired}",
                False,
            )

    with st.spinner("Wait for the map ..."):
        time.sleep(1)

    Map.setCenter(16.355, 51.988, zoom=7)

    Map.to_streamlit(height=700)
