# -*- coding: utf-8 -*-
"""
DACH AfA-Rechner & Abschreibungs-Optimierer 2026.
"""

from .models import AssetInput, YearlyAfaEntry, AfaResult
from .rates import COUNTRY_CONFIGS, ASSET_PRESETS, get_country_config
from .calculator import calculate_afa
from .validator import validate_asset_input

__version__ = "1.0.0"
__author__ = "DACH Digitalwerk"
__all__ = [
    "AssetInput",
    "YearlyAfaEntry",
    "AfaResult",
    "COUNTRY_CONFIGS",
    "ASSET_PRESETS",
    "get_country_config",
    "calculate_afa",
    "validate_asset_input"
]
