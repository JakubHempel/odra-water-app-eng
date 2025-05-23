import ee
import geemap.foliumap as geemap
from datetime import datetime
import gee_data as gd
from imagery.water_indexes import water_indexes


# Define the function to set DATE_ACQUIRED property to each image
def add_date_property(image):
    date_acquired = image.date().format("YYYY-MM")
    return image.set("DATE_ACQUIRED", date_acquired)


def clouds_remove(sentinel_image, replacement_image=None):
    cloud_shadow = sentinel_image.select("SCL").eq([3])
    cloud_low = sentinel_image.select("SCL").eq([7])
    cloud_med = sentinel_image.select("SCL").eq([8])
    cloud_high = sentinel_image.select("SCL").eq([9])
    cloud_cirrus = sentinel_image.select("SCL").eq([10])

    cloud_mask = (
        cloud_shadow.add(cloud_low).add(cloud_med).add(cloud_high).add(cloud_cirrus)
    )

    invert_mask = cloud_mask.eq(0).selfMask()
    cloud_mask = cloud_mask.eq(1).selfMask()

    image_cm = sentinel_image.updateMask(invert_mask)

    if replacement_image is not None:
        image_replace = replacement_image.updateMask(cloud_mask)
    else:
        image_replace = sentinel_image.updateMask(cloud_mask)

    sentinel_image = (
        ee.ImageCollection([image_cm, image_replace]).median().divide(10000)
    )

    return sentinel_image


def clip_to_odra(image):
    image = image.clipToCollection(gd.odra)
    return image


def clip_sentinel_disaster(image, aoi, date, name=None):
    sentinel_image = clouds_remove(image.clipToCollection(aoi))
    sentinel_image = sentinel_image.set("DATE_ACQUIRED", date)
    sentinel_image = sentinel_image.set("NAME", name)

    return sentinel_image


def get_sentinel_images(start_year, end_year, months):
    # Create an empty list to store all the collected images
    images_all = []

    # Loop through each year and month
    for year in range(start_year, end_year):
        for month in months:
            start_date = f"{year}-{month}-01"
            end_date = f"{year}-{month}-30"

            sentinel_image = (
                ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED")
                .filterDate(start_date, end_date)
                .filter(ee.Filter.lt("CLOUDY_PIXEL_PERCENTAGE", 90))
                .median()
                .divide(10000)
                .clipToCollection(gd.odra)
            )

            # sentinel_image = clouds_remove(sentinel_image, replacement_image)

            # Set the DATE_ACQUIRED property to the landsat image
            date_acquired = (
                ee.String(str(year))
                .cat("-")
                .cat(ee.String(ee.Number(month).format("%02d")))
            )
            system_index = ee.String("S2_L2A").cat("_").cat(date_acquired)

            sentinel_image = sentinel_image.set("DATE_ACQUIRED", date_acquired)
            sentinel_image = sentinel_image.set("system:index", system_index)

            if start_date != "2025-05-01":
                # Append the landsat image to the list
                images_all.append(sentinel_image)

    return images_all

def get_disaster_images():
    # Function to get all landsat images for City AOI near date to ecological disaster
    pre_disaster = (
        ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED")
        .filterDate("2022-07-01", "2022-07-24")
        .filter(ee.Filter.lt("CLOUDY_PIXEL_PERCENTAGE", 40))
        .median()
    )

    dur_disaster = (
        ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED")
        .filterDate("2022-07-25", "2022-08-20")
        .filter(ee.Filter.lt("CLOUDY_PIXEL_PERCENTAGE", 30))
        .median()
    )

    post_disaster = (
        ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED")
        .filterDate("2022-08-21", "2022-09-11")
        .filter(ee.Filter.lt("CLOUDY_PIXEL_PERCENTAGE", 40))
        .median()
    )

    wroclaw_pre = clip_sentinel_disaster(pre_disaster, gd.wroclaw_buffer, "2022-07-20")
    wroclaw_dur = clip_sentinel_disaster(dur_disaster, gd.wroclaw_buffer, "2022-07-31")
    wroclaw_post = clip_sentinel_disaster(
        post_disaster, gd.wroclaw_buffer, "2022-08-25"
    )

    wroclaw_collection = (
        ee.ImageCollection.fromImages([wroclaw_pre, wroclaw_dur, wroclaw_post])
        .map(clip_to_odra)
        .map(water_indexes)
    )

    szczecin_pre = clip_sentinel_disaster(pre_disaster, gd.szczecin, "2022-07-20")
    szczecin_dur = clip_sentinel_disaster(dur_disaster, gd.szczecin, "2022-07-31")
    szczecin_post = clip_sentinel_disaster(post_disaster, gd.szczecin, "2022-08-25")

    szczecin_collection = (
        ee.ImageCollection.fromImages([szczecin_pre, szczecin_dur, szczecin_post])
        .map(clip_to_odra)
        .map(water_indexes)
    )

    frankfurt_pre = clip_sentinel_disaster(
        pre_disaster, gd.frankfurt_buffer, "2022-07-20"
    )
    frankfurt_dur = clip_sentinel_disaster(
        dur_disaster, gd.frankfurt_buffer, "2022-07-31"
    )
    frankfurt_post = clip_sentinel_disaster(
        post_disaster, gd.frankfurt_buffer, "2022-08-25"
    )

    frankfurt_collection = (
        ee.ImageCollection.fromImages([frankfurt_pre, frankfurt_dur, frankfurt_post])
        .map(clip_to_odra)
        .map(water_indexes)
    )

    ostrava_pre = clip_sentinel_disaster(pre_disaster, gd.ostrava_buffer, "2022-07-20")
    ostrava_dur = clip_sentinel_disaster(dur_disaster, gd.ostrava_buffer, "2022-07-31")
    ostrava_post = clip_sentinel_disaster(
        post_disaster, gd.ostrava_buffer, "2022-08-25"
    )

    ostrava_collection = (
        ee.ImageCollection.fromImages([ostrava_pre, ostrava_dur, ostrava_post])
        .map(clip_to_odra)
        .map(water_indexes)
    )

    warta_pre = clip_sentinel_disaster(pre_disaster, gd.warta, '2022-07-20', 'Ujscie Warty')
    warta_dur = clip_sentinel_disaster(dur_disaster, gd.warta, '2022-07-31', 'Ujscie Warty')
    warta_post = clip_sentinel_disaster(post_disaster, gd.warta, '2022-08-25', 'Ujscie Warty')

    warta_collection = (
        ee.ImageCollection.fromImages([warta_pre, warta_dur, warta_post])
        .map(clip_to_odra)
        .map(water_indexes)
    )

    kanal_gliwicki_pre = clip_sentinel_disaster(pre_disaster, gd.kanal_gliwicki, '2022-07-20', 'Kanal Gliwicki')
    kanal_gliwicki_dur = clip_sentinel_disaster(dur_disaster, gd.kanal_gliwicki, '2022-07-31', 'Kanal Gliwicki')
    kanal_gliwicki_post = clip_sentinel_disaster(post_disaster, gd.kanal_gliwicki, '2022-08-25', 'Kanal Gliwicki')

    kanal_gliwicki_collection = ee.ImageCollection.fromImages(
        [kanal_gliwicki_pre, kanal_gliwicki_dur, kanal_gliwicki_post]
    ).map(water_indexes)

    return {
        "Wroclaw": wroclaw_collection,
        "Szczecin": szczecin_collection,
        "Frankfurt": frankfurt_collection,
        "Ostrava": ostrava_collection,
        "UjscieWarty": warta_collection,
        "KanalGliwicki": kanal_gliwicki_collection,
    }


# Explicitly set the desired years and months
start_year = 2018
end_year = 2025  # 2025 inclusive

# Create images from April to October for 2018-2024
months_4_to_10 = list(range(4, 11))
sentinel_images = get_sentinel_images(start_year, end_year, months_4_to_10)

months_4_to_4 = list(range(4, 5))
sentinel_images += get_sentinel_images(2025, 2026, months_4_to_4)

# Convert the images list to an ImageCollection
sentinel2_collection = ee.ImageCollection.fromImages(sentinel_images)

# Calculate indices for each image
water_collection = sentinel2_collection.map(water_indexes)


def get_all_layers():
    data = {}

    index_names = [
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

    current_date = datetime.now()
    L_date = []

    # Start date
    start_date = datetime(2018, 4, 1)

    # End date
    end_date = datetime(current_date.year, current_date.month+1, 1)

    # Generate dates and filter months from April to October
    while start_date < end_date:
        if start_date.month >= 4 and start_date.month <= 10:
            L_date.append(start_date.strftime('%Y-%m'))
        new_month = start_date.month + 1
        new_year = start_date.year + 1 if new_month > 12 else start_date.year
        start_date = start_date.replace(year=new_year, month=new_month if new_month <= 12 else 1)

    for index_name in index_names:
        data[index_name] = {}

        for date in L_date:
            filtered_collection = water_collection.filter(
                ee.Filter.eq("DATE_ACQUIRED", date)
            )

            first_image = filtered_collection.first().select(index_name)
            data[index_name][date] = first_image

    return data


def get_all_disaster_layers():
    disaster_collections = get_disaster_images()
    data = {}

    index_names = [
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

    L_date = ["2022-07-20", "2022-07-31", "2022-08-25"]

    for city in disaster_collections.keys():
        data[city] = {}
        for index_name in index_names:
            data[city][index_name] = {}
            for date in L_date:
                filtered_collection = disaster_collections[city].filter(
                    ee.Filter.eq("DATE_ACQUIRED", date)
                )
                first_image = filtered_collection.first().select(index_name)
                data[city][index_name][date] = first_image

    return data
