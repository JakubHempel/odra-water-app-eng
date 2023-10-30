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
        'SABI': {'min': -1.3, 'max': 1, 'palette': 'jet_r', 'breaks': [-1.0, -0.8, -0.6, -0.4, -0.2, 0.0, 0.2, 0.4, 0.6, 0.8, 1.0]},
        'CGI': {'min': -0.5, 'max': 1, 'palette': 'PuBuGn', 'breaks': [-0.5, -0.3, -0.1, 0.0, 0.1, 0.3, 0.5, 0.7, 1.0]},
        'CDOM': {'min': 0, 'max': 5, 'palette': colorScaleHex, 'breaks': [0, 1, 2, 3, 4, 5]},
        'DOC': {'min': 0, 'max': 40, 'palette': colorScaleHex, 'breaks': [0, 5, 10, 20, 30, 40]},
        'Cyanobacteria': {'min': 0, 'max': 5, 'palette': colorScaleHex, 'breaks': [0, 1, 2, 3, 4, 5]},
        'Turbidity': {'min': 0, 'max': 12, 'palette': ['green','white', 'blue'], 'breaks': [0, 3, 6, 9, 12]}
    }

    return vis_params
