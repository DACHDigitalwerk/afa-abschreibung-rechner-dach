# -*- coding: utf-8 -*-
"""
Statutory rules, caps, GWG limits and BMF/ESTV presets for 2026.
"""

from typing import Dict, Any

COUNTRY_CONFIGS: Dict[str, Dict[str, Any]] = {
    "DE": {
        "name": "Deutschland",
        "currency": "EUR",
        "currency_symbol": "€",
        "max_degressiv_cap": 20.0,
        "degressiv_multiplier": 2.0,
        "gwg_sofort_limit": 800.0,
        "gwg_bagatell_limit": 250.0,
        "gwg_pool_limit": 1000.0,
        "max_sonderafa_pct": 40.0,
        "pro_rata_first_year": True,
        "half_year_rule": False,
        "legal_basis": "§ 7 EStG (Wachstumschancengesetz 2026) / BMF-AfA-Tabelle"
    },
    "AT": {
        "name": "Österreich",
        "currency": "EUR",
        "currency_symbol": "€",
        "max_degressiv_cap": 30.0,
        "degressiv_multiplier": 2.0,
        "gwg_sofort_limit": 1000.0,
        "gwg_bagatell_limit": 0.0,
        "gwg_pool_limit": 0.0,
        "max_sonderafa_pct": 0.0,
        "pro_rata_first_year": False,
        "half_year_rule": True,
        "legal_basis": "§ 7 Abs. 1 & 1a, § 13 EStG 1988 (Halbjahres-AfA)"
    },
    "CH": {
        "name": "Schweiz",
        "currency": "CHF",
        "currency_symbol": "CHF",
        "max_degressiv_cap": 40.0,
        "degressiv_multiplier": 2.0,
        "gwg_sofort_limit": 1500.0,
        "gwg_bagatell_limit": 0.0,
        "gwg_pool_limit": 0.0,
        "max_sonderafa_pct": 0.0,
        "pro_rata_first_year": True,
        "half_year_rule": False,
        "legal_basis": "Art. 960a OR / ESTV-Merkblatt für Abschreibungen"
    }
}

ASSET_PRESETS: Dict[str, Dict[str, Any]] = {
    "computer": {
        "name": "Computer, Notebook & Workstation",
        "years": 3,
        "cost_de": 3500.0,
        "note": "BMF-Schreiben: Wahlrecht 1 Jahr Sofort-AfA oder 3 Jahre linear"
    },
    "smartphone": {
        "name": "Smartphone & Mobiltelefon",
        "years": 3,
        "cost_de": 1200.0,
        "note": "Betriebsgewöhnliche ND: 3 Jahre"
    },
    "car": {
        "name": "Geschäfts-Pkw",
        "years_de": 6,
        "years_at": 8,
        "years_ch": 6,
        "cost_de": 45000.0,
        "note": "DE/CH 6 Jahre, AT zwingend 8 Jahre (§ 8 Abs. 6 EStG)"
    },
    "furniture": {
        "name": "Büromöbel (Schreibtisch, Schrank)",
        "years": 13,
        "cost_de": 1800.0,
        "note": "BMF-AfA-Tabelle AV: 13 Jahre"
    },
    "server": {
        "name": "Server & Netzwerktechnik",
        "years": 3,
        "cost_de": 12000.0,
        "note": "3 Jahre (oder 1 Jahr Digital-AfA)"
    },
    "software": {
        "name": "Software & ERP-Lizenzen",
        "years": 3,
        "cost_de": 6000.0,
        "note": "3 Jahre"
    },
    "machine": {
        "name": "Maschinen & Produktionsanlagen",
        "years": 10,
        "cost_de": 80000.0,
        "note": "8 bis 15 Jahre je nach Branche"
    },
    "tools": {
        "name": "Werkzeuge & Handwerksgeräte",
        "years": 5,
        "cost_de": 2500.0,
        "note": "5 Jahre"
    },
    "pv": {
        "name": "Photovoltaikanlage & Speicher",
        "years": 20,
        "cost_de": 28000.0,
        "note": "20 Jahre linear (5 % p.a.)"
    },
    "gwg": {
        "name": "Monitor / Kleingerät (GWG)",
        "years": 1,
        "cost_de": 450.0,
        "note": "Sofortabschreibung im Anschaffungsjahr"
    }
}


def get_country_config(country: str) -> Dict[str, Any]:
    c = country.upper()
    return COUNTRY_CONFIGS.get(c, COUNTRY_CONFIGS["DE"])
