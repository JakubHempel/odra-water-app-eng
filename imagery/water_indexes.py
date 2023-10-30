import ee

def water_indexes(image):
    NDWI = True
    NDVI = True
    NDSI = True
    SABI = True
    CGI = True
    CDOM = True
    DOC = True
    Cya = True
    Turb = True
    
    if NDWI:
        ndwi = image.normalizedDifference(['B3', 'B8']).rename('NDWI')
        image = image.addBands(ndwi)
    
    if NDVI:
        ndvi = image.normalizedDifference(['B8', 'B4']).rename('NDVI')
        image = image.addBands(ndvi)
    
    if NDSI:
        ndsi = image.normalizedDifference(['B4', 'B8']).rename('NDSI')
        image = image.addBands(ndsi)

    range_min = -1
    range_max = 1
    
    if SABI:
        sabi_min = ee.Image.constant(0.07)
        sabi_max = ee.Image.constant(4.09)

        sabi = image.expression('(NIR - RED) / (BLUE + GREEN)', 
                                {'NIR': image.select('B8'),
                                 'RED': image.select('B4'),
                                 'BLUE': image.select('B2'),
                                 'GREEN': image.select('B3')})

        sabi_normalized = sabi.subtract(sabi_min).divide(sabi_max.subtract(sabi_min)).multiply(range_max-range_min).add(range_min).rename('SABI')

        image = image.addBands(sabi_normalized)

    range_min = 0

    if CGI:
        cgi_min = ee.Image.constant(0.48)
        cgi_max = ee.Image.constant(7.36)

        cgi = image.expression('((SWIR/GREEN) - 1)', {'SWIR': image.select('B9'),'GREEN': image.select('B3')})
        
        cgi_normalized = cgi.subtract(cgi_min).divide(cgi_max.subtract(cgi_min)).multiply(range_max-range_min).add(range_min).rename('CGI')
        
        image = image.addBands(cgi_normalized)
    
    range_max = 5

    if CDOM:
        cdom_min = ee.Image.constant(3.07)
        cdom_max = ee.Image.constant(60.69)

        cdom = image.expression('537 * exp(-2.93 * GREEN / RED)',
                               {'GREEN': image.select('B3'),
                               'RED': image.select('B4')})
        
        cdom_normalized = cdom.subtract(cdom_min).divide(cdom_max.subtract(cdom_min)).multiply(range_max-range_min).add(range_min).rename('CDOM')
        
        image = image.addBands(cdom_normalized)
      
    range_max = 40

    if DOC:
        doc_min = ee.Image.constant(8.32)
        doc_max = ee.Image.constant(81.58)
    
        doc = image.expression('432 * exp(-2.24 * GREEN / RED)',
                               {'GREEN': image.select('B3'),
                               'RED': image.select('B4')})
        
        doc_normalized = doc.subtract(doc_min).divide(doc_max.subtract(doc_min)).multiply(range_max-range_min).add(range_min).rename('DOC')
        
        image = image.addBands(doc_normalized)
    
    range_max = 100

    if Cya:
        cya_min = ee.Image.constant(53.19)
        cya_max = ee.Image.constant(27914.79)

        cya = image.expression('115530.31 * (GREEN * RED / BLUE) ** 2.38',
                              {'RED': image.select('B4'),
                               'BLUE': image.select('B2'),
                               'GREEN': image.select('B3')})
        
        cya_normalized = cya.subtract(cya_min).divide(cya_max.subtract(cya_min)).multiply(range_max-range_min).add(range_min).rename('Cyanobacteria')
        
        image = image.addBands(cya_normalized)
        
    range_max = 20

    if Turb:
        turb_min = ee.Image.constant(-1.87)
        turb_max = ee.Image.constant(49.46)

        turb = image.expression('8.93 * (GREEN / UBLUE) - 6.39',
                               {'GREEN': image.select('B3'),
                                'UBLUE': image.select('B1')})
        
        turb_normalized = turb.subtract(turb_min).divide(turb_max.subtract(turb_min)).multiply(range_max-range_min).add(range_min).rename('Turbidity')
        
        image = image.addBands(turb_normalized)
        
    return image
