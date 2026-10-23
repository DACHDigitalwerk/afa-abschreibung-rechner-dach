# -*- coding: utf-8 -*-
"""
Unit tests for afa_dach.calculator and models.
"""

import pytest
from afa_dach.models import AssetInput, AfaResult
from afa_dach.calculator import calculate_afa


def test_linear_afa_full_year_de():
    """Test standard linear depreciation for full year (Jan) in Germany."""
    res = calculate_afa(
        acquisition_cost=12000.0,
        useful_life_years=3,
        acquisition_month=1,
        acquisition_year=2026,
        method="linear",
        country="DE"
    )
    assert res.linear_rate_pct == 33.33
    assert len(res.schedule) == 3
    assert res.schedule[0].total_yearly_afa == 4000.0
    assert res.schedule[1].total_yearly_afa == 4000.0
    assert res.schedule[2].total_yearly_afa == 4000.0
    assert res.schedule[2].book_value_end == 0.0


def test_linear_afa_prorata_de():
    """Test German pro-rata temporis in acquisition year (July = 6 months)."""
    res = calculate_afa(
        acquisition_cost=12000.0,
        useful_life_years=3,
        acquisition_month=7,
        acquisition_year=2026,
        method="linear",
        country="DE"
    )
    # Year 1: 6 / 12 * 4000 = 2000.0
    assert res.schedule[0].total_yearly_afa == 2000.0
    assert res.schedule[0].book_value_end == 10000.0
    assert res.schedule[1].total_yearly_afa == 4000.0
    assert res.schedule[2].total_yearly_afa == 4000.0


def test_austria_half_year_rule():
    """Test Austrian half-year rule (§ 7 Abs. 2 EStG)."""
    # First half year (April <= 6) -> full year AfA
    res_h1 = calculate_afa(
        acquisition_cost=10000.0,
        useful_life_years=5,
        acquisition_month=4,
        method="linear",
        country="AT"
    )
    assert res_h1.schedule[0].total_yearly_afa == 2000.0

    # Second half year (August > 6) -> half year AfA
    res_h2 = calculate_afa(
        acquisition_cost=10000.0,
        useful_life_years=5,
        acquisition_month=8,
        method="linear",
        country="AT"
    )
    assert res_h2.schedule[0].total_yearly_afa == 1000.0


def test_degressiv_opt_switch_year():
    """Test degressive AfA with optimal switch year to linear (DE, 10 years)."""
    res = calculate_afa(
        acquisition_cost=50000.0,
        useful_life_years=10,
        acquisition_month=1,
        acquisition_year=2026,
        method="degressiv-opt",
        country="DE"
    )
    assert res.degressiv_rate_pct == 20.0
    assert res.schedule[0].total_yearly_afa == 10000.0
    assert res.schedule[1].total_yearly_afa == 8000.0
    assert res.schedule[2].total_yearly_afa == 6400.0
    assert res.schedule[3].total_yearly_afa == 5120.0
    # Optimal switch year must be year 7
    assert res.switch_year_index == 7
    assert res.switch_calendar_year == 2032
    assert res.schedule[6].is_switch_year is True
    assert res.schedule[6].method_used == "linear"


def test_degressiv_pure_without_switch():
    """Test pure degressive AfA without switching."""
    res = calculate_afa(
        acquisition_cost=10000.0,
        useful_life_years=5,
        acquisition_month=1,
        method="degressiv",
        country="DE"
    )
    assert res.degressiv_rate_pct == 20.0
    assert res.switch_year_index is None
    for row in res.schedule:
        assert row.method_used == "degressiv"


def test_sonderafa_7g_de():
    """Test § 7g Abs. 5 EStG Sonderabschreibung (20%) in Germany."""
    res = calculate_afa(
        acquisition_cost=20000.0,
        useful_life_years=5,
        acquisition_month=1,
        method="linear",
        country="DE",
        sonderafa_rate_pct=20.0
    )
    # Regular linear: 4000.0 + Sonder-AfA: 4000.0 = 8000.0
    assert res.schedule[0].sonder_afa == 4000.0
    assert res.schedule[0].total_yearly_afa == 8000.0
    assert res.schedule[0].book_value_end == 12000.0


def test_sonderafa_ignored_outside_de():
    """Ensure Sonder-AfA is only applied for Germany."""
    res = calculate_afa(
        acquisition_cost=20000.0,
        useful_life_years=5,
        country="AT",
        sonderafa_rate_pct=20.0
    )
    assert res.schedule[0].sonder_afa == 0.0


def test_gwg_de_bagatell():
    """Test German Bagatellgrenze (<= 250 €)."""
    res = calculate_afa(acquisition_cost=220.0, useful_life_years=1, country="DE")
    assert res.is_gwg is True
    assert res.gwg_type == "bagatell"


def test_gwg_de_sofort():
    """Test German classic GWG (<= 800 €)."""
    res = calculate_afa(acquisition_cost=650.0, useful_life_years=1, country="DE")
    assert res.is_gwg is True
    assert res.gwg_type == "sofort"


def test_gwg_de_pool():
    """Test German Sammelposten (<= 1.000 €)."""
    res = calculate_afa(acquisition_cost=950.0, useful_life_years=5, country="DE")
    assert res.is_gwg is False
    assert res.gwg_type == "pool"


def test_gwg_austria_1000():
    """Test Austrian GWG limit (§ 13 EStG up to 1.000 €)."""
    res = calculate_afa(acquisition_cost=990.0, useful_life_years=1, country="AT")
    assert res.is_gwg is True
    assert res.gwg_type == "sofort"


def test_gwg_switzerland_1500():
    """Test Swiss practice limit (up to 1.500 CHF)."""
    res = calculate_afa(acquisition_cost=1200.0, useful_life_years=1, country="CH")
    assert res.is_gwg is True
    assert res.gwg_type == "sofort"


def test_salvage_value_cap():
    """Ensure asset is not depreciated below salvage value (e.g. 1.00 €)."""
    res = calculate_afa(
        acquisition_cost=3000.0,
        useful_life_years=3,
        acquisition_month=1,
        salvage_value=1.00,
        method="linear"
    )
    last_row = res.schedule[-1]
    assert last_row.book_value_end == 1.00


def test_dataclass_input():
    """Test passing AssetInput instance."""
    inp = AssetInput(
        acquisition_cost=8000.0,
        useful_life_years=4,
        asset_name="Server",
        method="linear",
        country="DE"
    )
    res = calculate_afa(inp)
    assert res.input_data.asset_name == "Server"
    assert res.linear_rate_pct == 25.0


def test_dict_input():
    """Test passing dict input."""
    d = {
        "acquisition_cost": 5000.0,
        "useful_life_years": 5,
        "method": "linear"
    }
    res = calculate_afa(d)
    assert res.input_data.acquisition_cost == 5000.0
    assert res.linear_rate_pct == 20.0


def test_validation_cost_zero():
    """Ensure acquisition cost <= 0 is rejected."""
    with pytest.raises(ValueError, match="Anschaffungskosten"):
        calculate_afa(acquisition_cost=0.0, useful_life_years=3)


def test_validation_years_zero():
    """Ensure useful life < 1 is rejected."""
    with pytest.raises(ValueError, match="Nutzungsdauer"):
        calculate_afa(acquisition_cost=1000.0, useful_life_years=0)


def test_validation_invalid_month():
    """Ensure month not in 1..12 is rejected."""
    with pytest.raises(ValueError, match="Anschaffungsmonat"):
        calculate_afa(acquisition_cost=1000.0, useful_life_years=3, acquisition_month=13)


def test_validation_invalid_method():
    """Ensure invalid method is rejected."""
    with pytest.raises(ValueError, match="AfA-Methode"):
        calculate_afa(acquisition_cost=1000.0, useful_life_years=3, method="unknown")


def test_validation_salvage_exceeds_cost():
    """Ensure salvage value >= cost is rejected."""
    with pytest.raises(ValueError, match="Restwert"):
        calculate_afa(acquisition_cost=1000.0, useful_life_years=3, salvage_value=1200.0)
