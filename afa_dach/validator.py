# -*- coding: utf-8 -*-
"""
Validation rules for asset depreciation parameters.
"""

from .models import AssetInput


def validate_asset_input(inp: AssetInput) -> None:
    if inp.acquisition_cost <= 0:
        raise ValueError("Anschaffungskosten müssen größer als 0 sein.")

    if inp.useful_life_years < 1 or inp.useful_life_years > 100:
        raise ValueError("Nutzungsdauer muss zwischen 1 und 100 Jahren liegen.")

    if inp.acquisition_month < 1 or inp.acquisition_month > 12:
        raise ValueError("Anschaffungsmonat muss zwischen 1 und 12 liegen.")

    if inp.acquisition_year < 1990 or inp.acquisition_year > 2050:
        raise ValueError("Anschaffungsjahr muss zwischen 1990 und 2050 liegen.")

    valid_methods = ("linear", "degressiv", "degressiv-opt")
    if inp.method not in valid_methods:
        raise ValueError(f"Ungültige AfA-Methode '{inp.method}'. Erlaubt: {valid_methods}")

    valid_countries = ("DE", "AT", "CH")
    if inp.country.upper() not in valid_countries:
        raise ValueError(f"Ungültiger Ländercode '{inp.country}'. Erlaubt: {valid_countries}")

    if inp.salvage_value < 0:
        raise ValueError("Restwert darf nicht negativ sein.")

    if inp.salvage_value >= inp.acquisition_cost:
        raise ValueError("Restwert muss kleiner sein als die Anschaffungskosten.")

    if inp.sonderafa_rate_pct < 0 or inp.sonderafa_rate_pct > 40:
        raise ValueError("Sonderabschreibungssatz (§ 7g Abs. 5 EStG) muss zwischen 0 und 40 Prozent liegen.")
