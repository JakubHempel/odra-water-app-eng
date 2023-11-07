from typing import Final

def get_vis_params():
    # Visualization parameters for indexes
    colorScaleHex = [
        '#496FF2',
        '#82D35F',
        '#FEFD05',
        '#FD0004',
        '#8E2026',
        '#D97CF5'
    ]

    vis_params = {
        'NDWI': {'min': -1, 'max': 1, 'palette': 'ndwi', 'breaks': [-1.0, -0.8, -0.6, -0.4, -0.2, 0.0, 0.2, 0.4, 0.6, 0.8, 1.0]},
        'NDVI': {'min': -1, 'max': 1, 'palette': 'ndvi', 'breaks': [-1.0, -0.8, -0.6, -0.4, -0.2, 0.0, 0.2, 0.4, 0.6, 0.8, 1.0]},
        'NDSI': {'min': -1, 'max': 1, 'palette': 'RdYlBu_r', 'breaks': [-1.0, -0.8, -0.6, -0.4, -0.2, 0.0, 0.2, 0.4, 0.6, 0.8, 1.0]},
        'SABI': {'min': -1, 'max': 1, 'palette': 'jet_r', 'breaks': [-1.0, -0.8, -0.6, -0.4, -0.2, 0.0, 0.2, 0.4, 0.6, 0.8, 1.0]},
        'CGI': {'min': 1, 'max': 5, 'palette': 'PuBuGn'},
        'CDOM': {'min': 5, 'max': 50, 'palette': colorScaleHex},
        'DOC': {'min': 10, 'max': 70, 'palette': colorScaleHex},
        'Cyanobacteria': {'min': 100, 'max': 1000, 'palette': colorScaleHex},
        'Turbidity': {'min': 0, 'max': 20, 'palette': ['green','white', 'blue']}
    }

    return vis_params
