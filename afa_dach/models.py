# -*- coding: utf-8 -*-
"""
Data models for DACH AfA-Rechner & Abschreibungs-Optimierer 2026.
"""

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class AssetInput:
    """Input parameters for depreciable fixed asset."""
    acquisition_cost: float
    useful_life_years: int
    asset_name: str = "Wirtschaftsgut"
    acquisition_month: int = 1
    acquisition_year: int = 2026
    method: str = "degressiv-opt"  # 'linear', 'degressiv', 'degressiv-opt'
    country: str = "DE"            # 'DE', 'AT', 'CH'
    salvage_value: float = 0.0
    sonderafa_rate_pct: float = 0.0


@dataclass
class YearlyAfaEntry:
    """Single row in the depreciation schedule (Anlagenspiegel)."""
    year_index: int
    calendar_year: int
    book_value_start: float
    method_used: str
    rate_applied_pct: float
    regular_afa: float
    sonder_afa: float
    total_yearly_afa: float
    cumulated_afa: float
    book_value_end: float
    is_switch_year: bool = False


@dataclass
class AfaResult:
    """Full calculation outcome."""
    input_data: AssetInput
    is_gwg: bool
    gwg_type: Optional[str]
    gwg_note: str
    linear_rate_pct: float
    degressiv_rate_pct: float
    switch_year_index: Optional[int]
    switch_calendar_year: Optional[int]
    schedule: List[YearlyAfaEntry]
    total_afa_first_year: float
