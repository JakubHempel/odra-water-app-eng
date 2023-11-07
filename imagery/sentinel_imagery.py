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
        ee.ImageCollection([image_cm, image_replace])
        .median()
        .divide(10000)
        .clipToCollection(gd.odra)
    )

    return sentinel_image


def clip_sentinel_disaster(image, aoi, date):
    sentinel_image = clouds_remove(image.clipToCollection(aoi))
    sentinel_image = sentinel_image.set("DATE_ACQUIRED", date)

    return sentinel_image


def get_sentinel_images(start_year, end_year, months):
    # Create an empty list to store all the collected images
    images_all = []

    # Loop through each year and month
    for year in range(start_year, end_year + 1):
        for month in months:
            start_date = ee.Date.fromYMD(year, month, 1)
            end_date = start_date.advance(1, "month")

            sentinel_image = (
                ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED")
                .filterDate(start_date, end_date)
                .filter(ee.Filter.lt("CLOUDY_PIXEL_PERCENTAGE", 50))
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

    wroclaw_collection = ee.ImageCollection.fromImages(
        [wroclaw_pre, wroclaw_dur, wroclaw_post]
    ).map(water_indexes)

    szczecin_pre = clip_sentinel_disaster(pre_disaster, gd.szczecin, "2022-07-20")
    szczecin_dur = clip_sentinel_disaster(dur_disaster, gd.szczecin, "2022-07-31")
    szczecin_post = clip_sentinel_disaster(post_disaster, gd.szczecin, "2022-08-25")

    szczecin_collection = ee.ImageCollection.fromImages(
        [szczecin_pre, szczecin_dur, szczecin_post]
    ).map(water_indexes)

    frankfurt_pre = clip_sentinel_disaster(
        pre_disaster, gd.frankfurt_buffer, "2022-07-20"
    )
    frankfurt_dur = clip_sentinel_disaster(
        dur_disaster, gd.frankfurt_buffer, "2022-07-31"
    )
    frankfurt_post = clip_sentinel_disaster(
        post_disaster, gd.frankfurt_buffer, "2022-08-25"
    )

    frankfurt_collection = ee.ImageCollection.fromImages(
        [frankfurt_pre, frankfurt_dur, frankfurt_post]
    ).map(water_indexes)

    ostrava_pre = clip_sentinel_disaster(pre_disaster, gd.ostrava_buffer, "2022-07-20")
    ostrava_dur = clip_sentinel_disaster(dur_disaster, gd.ostrava_buffer, "2022-07-31")
    ostrava_post = clip_sentinel_disaster(
        post_disaster, gd.ostrava_buffer, "2022-08-25"
    )

    ostrava_collection = ee.ImageCollection.fromImages(
        [ostrava_pre, ostrava_dur, ostrava_post]
    ).map(water_indexes)

    return {
        "Wroclaw": wroclaw_collection,
        "Szczecin": szczecin_collection,
        "Frankfurt": frankfurt_collection,
        "Ostrava": ostrava_collection,
    }


# Define the year range (from 2018 to present)
start_year = 2018
end_year = datetime.now().year

# Define the months from April to October
months = list(range(4, 11))

# Call the function to create landsat images for the years 2018 to 2022 (April to October) and 2023 (April to present month)
sentinel_images = get_sentinel_images(start_year, end_year, months)

# Convert the landsat_images list to an ImageCollection
sentinel2_collection = ee.ImageCollection.fromImages(sentinel_images)

# Calculate indices for each image
water_collection = sentinel2_collection.map(water_indexes)


def get_all_layers():
    # Initialize the nested directory structure
    data = {}

    # List of index names
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

    L_date = [
        "2018-04",
        "2018-05",
        "2018-06",
        "2018-07",
        "2018-08",
        "2018-09",
        "2018-10",
        "2019-04",
        "2019-05",
        "2019-06",
        "2019-07",
        "2019-08",
        "2019-09",
        "2019-10",
        "2020-04",
        "2020-05",
        "2020-06",
        "2020-07",
        "2020-08",
        "2020-09",
        "2020-10",
        "2021-04",
        "2021-05",
        "2021-06",
        "2021-07",
        "2021-08",
        "2021-09",
        "2021-10",
        "2022-04",
        "2022-05",
        "2022-06",
        "2022-07",
        "2022-08",
        "2022-09",
        "2022-10",
        "2023-04",
        "2023-05",
        "2023-06",
        "2023-07",
        "2023-08",
        "2023-09",
        "2023-10",
    ]

    # Iterate through the index names
    for index_name in index_names:
        # Initialize a sub-dictionary for the index
        data[index_name] = {}

        # Iterate through the available dates (yyyy-mm format)
        for date in L_date:  # Replace with your list of dates
            # Filter the Image Collection by date
            filtered_collection = water_collection.filter(
                ee.Filter.eq("DATE_ACQUIRED", date)
            )

            # Get the first image from the filtered collection (you can adjust this logic if needed)
            first_image = filtered_collection.first().select(index_name)

            # Add the image to the sub-dictionary
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
