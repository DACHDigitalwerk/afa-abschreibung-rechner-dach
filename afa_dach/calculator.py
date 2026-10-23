# -*- coding: utf-8 -*-
"""
Depreciation calculation engine for linear, degressive and optimal switch AfA.
"""

from typing import Union, List, Optional
from .models import AssetInput, YearlyAfaEntry, AfaResult
from .validator import validate_asset_input
from .rates import get_country_config


def calculate_afa(
    input_data: Union[AssetInput, dict] = None,
    acquisition_cost: float = None,
    useful_life_years: int = None,
    asset_name: str = "Wirtschaftsgut",
    acquisition_month: int = 1,
    acquisition_year: int = 2026,
    method: str = "degressiv-opt",
    country: str = "DE",
    salvage_value: float = 0.0,
    sonderafa_rate_pct: float = 0.0
) -> AfaResult:
    """
    Compute asset depreciation schedule (Anlagenspiegel) for DE, AT or CH.
    """
    if isinstance(input_data, AssetInput):
        inp = input_data
    elif isinstance(input_data, dict):
        inp = AssetInput(**input_data)
    else:
        inp = AssetInput(
            acquisition_cost=float(acquisition_cost) if acquisition_cost is not None else 0.0,
            useful_life_years=int(useful_life_years) if useful_life_years is not None else 1,
            asset_name=str(asset_name),
            acquisition_month=int(acquisition_month),
            acquisition_year=int(acquisition_year),
            method=str(method),
            country=str(country).upper(),
            salvage_value=float(salvage_value),
            sonderafa_rate_pct=float(sonderafa_rate_pct)
        )

    validate_asset_input(inp)
    cfg = get_country_config(inp.country)

    # 1. GWG Check
    cost = inp.acquisition_cost
    is_gwg = False
    gwg_type = None
    gwg_note = ""

    if inp.country == "DE":
        if cost <= cfg["gwg_bagatell_limit"]:
            is_gwg = True
            gwg_type = "bagatell"
            gwg_note = "Sofortabzug als Betriebsausgabe ohne gesondertes Verzeichnis (§ 6 Abs. 2 Satz 3 EStG)."
        elif cost <= cfg["gwg_sofort_limit"]:
            is_gwg = True
            gwg_type = "sofort"
            gwg_note = "Sofortabschreibung als GWG im Anschaffungsjahr (§ 6 Abs. 2 EStG)."
        elif cost <= cfg["gwg_pool_limit"]:
            gwg_type = "pool"
            gwg_note = "Wahlrecht Sammelposten: Poolabschreibung über 5 Jahre à 20 % (§ 6 Abs. 2a EStG)."
    elif inp.country == "AT":
        if cost <= cfg["gwg_sofort_limit"]:
            is_gwg = True
            gwg_type = "sofort"
            gwg_note = "Sofortabschreibung als geringwertiges Wirtschaftsgut (§ 13 EStG bis 1.000 €)."
    elif inp.country == "CH":
        if cost <= cfg["gwg_sofort_limit"]:
            is_gwg = True
            gwg_type = "sofort"
            gwg_note = "Direkte Verbuchung als Kleininventar / Betriebsaufwand (Art. 960a OR Praxis)."

    # 2. Rates
    linear_rate = 100.0 / inp.useful_life_years
    degressiv_rate = min(linear_rate * cfg["degressiv_multiplier"], cfg["max_degressiv_cap"])

    # 3. First year fraction
    if inp.country == "AT":
        first_year_fraction = 1.0 if inp.acquisition_month <= 6 else 0.5
    else:
        first_year_fraction = (13 - inp.acquisition_month) / 12.0

    # 4. Sonder-AfA
    has_sonderafa = (inp.country == "DE" and inp.sonderafa_rate_pct > 0)
    sonder_amount = round(cost * (inp.sonderafa_rate_pct / 100.0), 2) if has_sonderafa else 0.0

    schedule: List[YearlyAfaEntry] = []
    current_book_value = cost
    cumulated_afa = 0.0
    active_method = "linear" if inp.method == "linear" else "degressiv"
    switch_idx: Optional[int] = None

    for y in range(1, inp.useful_life_years + 1):
        cal_year = inp.acquisition_year + y - 1
        start_val = current_book_value
        fraction = first_year_fraction if y == 1 else 1.0
        rem_years = inp.useful_life_years - y + 1

        if inp.method == "linear":
            rate_applied = linear_rate
            regular_afa = (cost / inp.useful_life_years) * fraction
        elif inp.method == "degressiv":
            rate_applied = degressiv_rate
            regular_afa = (start_val * (degressiv_rate / 100.0)) * fraction
        elif inp.method == "degressiv-opt":
            linear_rem = start_val / rem_years
            degressiv_now = (start_val * (degressiv_rate / 100.0)) * fraction

            if active_method == "degressiv" and linear_rem > degressiv_now and y > 1:
                active_method = "linear"
                if switch_idx is None:
                    switch_idx = y

            if active_method == "linear":
                rate_applied = 100.0 / rem_years
                regular_afa = linear_rem
            else:
                rate_applied = degressiv_rate
                regular_afa = degressiv_now

        total_year = regular_afa
        s_afa = sonder_amount if (y == 1 and has_sonderafa) else 0.0
        total_year += s_afa

        # Respect salvage value
        if start_val - total_year < inp.salvage_value:
            total_year = max(0.0, start_val - inp.salvage_value)

        total_year = round(total_year, 2)
        regular_afa = round(total_year - s_afa, 2)
        end_val = round(start_val - total_year, 2)
        cumulated_afa = round(cumulated_afa + total_year, 2)
        current_book_value = end_val

        is_sw = (y == switch_idx)
        entry = YearlyAfaEntry(
            year_index=y,
            calendar_year=cal_year,
            book_value_start=round(start_val, 2),
            method_used=active_method,
            rate_applied_pct=round(rate_applied, 2),
            regular_afa=regular_afa,
            sonder_afa=s_afa,
            total_yearly_afa=total_year,
            cumulated_afa=cumulated_afa,
            book_value_end=end_val,
            is_switch_year=is_sw
        )
        schedule.append(entry)

        if end_val <= inp.salvage_value:
            break

    switch_cal = (inp.acquisition_year + switch_idx - 1) if switch_idx else None
    first_year_afa = schedule[0].total_yearly_afa if schedule else 0.0

    return AfaResult(
        input_data=inp,
        is_gwg=is_gwg,
        gwg_type=gwg_type,
        gwg_note=gwg_note,
        linear_rate_pct=round(linear_rate, 2),
        degressiv_rate_pct=round(degressiv_rate, 2),
        switch_year_index=switch_idx,
        switch_calendar_year=switch_cal,
        schedule=schedule,
        total_afa_first_year=first_year_afa
    )
