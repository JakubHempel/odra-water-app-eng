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

    vis_params: Final = {
        'NDWI': {'min': -1, 'max': 1, 'palette': 'ndwi'},
        'NDVI': {'min': -1, 'max': 1, 'palette': 'ndvi'},
        'NDSI': {'min': -1, 'max': 1, 'palette': 'RdYlBu_r'},
        'SABI': {'min': -1, 'max': 1, 'palette': 'jet_r'},
        'CGI': {'min': 0, 'max': 1, 'palette': 'PuBuGn'},
        'CDOM': {'min': 0, 'max': 5, 'palette': colorScaleHex, 'breaks': [0, 1, 2, 3, 4, 5]},
        'DOC': {'min': 0, 'max': 40, 'palette': colorScaleHex, 'breaks': [0, 5, 10, 20, 30, 40]},
        'Cyanobacteria': {'min': 0, 'max': 100, 'palette': colorScaleHex, 'breaks': [0, 10, 20, 40, 50, 100]},
        'Turbidity': {'min': 0, 'max': 1, 'palette': ['green','white', 'blue']}
    }

    return vis_params
