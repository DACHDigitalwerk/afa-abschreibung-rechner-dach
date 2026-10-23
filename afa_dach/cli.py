# -*- coding: utf-8 -*-
"""
Command-Line Interface (CLI) for DACH AfA-Rechner 2026.
Entrypoint: dach-afa
"""

import sys
import argparse
import json
from typing import List, Optional
from .models import AssetInput
from .calculator import calculate_afa
from .rates import get_country_config


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="dach-afa",
        description="DACH AfA-Rechner & Abschreibungs-Optimierer 2026 (DE, AT, CH)"
    )
    parser.add_argument(
        "--cost", "-c",
        type=float,
        required=True,
        help="Anschaffungskosten netto (z.B. 10000.0)"
    )
    parser.add_argument(
        "--years", "-y",
        type=int,
        required=True,
        help="Nutzungsdauer in Jahren (z.B. 3 oder 10)"
    )
    parser.add_argument(
        "--name",
        type=str,
        default="Wirtschaftsgut",
        help="Bezeichnung des Anlageguts"
    )
    parser.add_argument(
        "--month", "-m",
        type=int,
        default=1,
        help="Anschaffungsmonat (1 bis 12, Standard: 1)"
    )
    parser.add_argument(
        "--year",
        type=int,
        default=2026,
        help="Anschaffungsjahr (Standard: 2026)"
    )
    parser.add_argument(
        "--method",
        choices=["linear", "degressiv", "degressiv-opt"],
        default="degressiv-opt",
        help="Abschreibungsmethode: linear, degressiv oder degressiv-opt (Standard: degressiv-opt mit Wechseljahr)"
    )
    parser.add_argument(
        "--country",
        choices=["DE", "AT", "CH", "de", "at", "ch"],
        default="DE",
        help="Laendercode: DE (Deutschland), AT (Oesterreich), CH (Schweiz)"
    )
    parser.add_argument(
        "--sonderafa",
        type=float,
        default=0.0,
        help="Sonderabschreibung nach Paragraph 7g Abs. 5 EStG in Prozent (nur DE, bis zu 40 Prozent)"
    )
    parser.add_argument(
        "--salvage",
        type=float,
        default=0.0,
        help="Restwert / Erinnerungswert am Ende (Standard: 0.0)"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Ausgabe als maschinenlesbares JSON-Format"
    )
    return parser


def format_currency(val: float, symbol: str) -> str:
    return f"{val:,.2f} {symbol}".replace(",", "X").replace(".", ",").replace("X", ".")


def run_cli(args: Optional[List[str]] = None) -> int:
    parser = create_parser()
    try:
        parsed = parser.parse_args(args)
    except SystemExit as e:
        return e.code if isinstance(e.code, int) else 0

    country = parsed.country.upper()
    cfg = get_country_config(country)
    sym = cfg["currency_symbol"]

    try:
        res = calculate_afa(
            acquisition_cost=parsed.cost,
            useful_life_years=parsed.years,
            asset_name=parsed.name,
            acquisition_month=parsed.month,
            acquisition_year=parsed.year,
            method=parsed.method,
            country=country,
            salvage_value=parsed.salvage,
            sonderafa_rate_pct=parsed.sonderafa
        )
    except Exception as err:
        sys.stderr.write(f"Fehler: {err}\n")
        return 1

    if parsed.json:
        data = {
            "country": country,
            "currency": cfg["currency"],
            "currency_symbol": sym,
            "asset_name": res.input_data.asset_name,
            "acquisition_cost": res.input_data.acquisition_cost,
            "useful_life_years": res.input_data.useful_life_years,
            "acquisition_month": res.input_data.acquisition_month,
            "acquisition_year": res.input_data.acquisition_year,
            "method": res.input_data.method,
            "is_gwg": res.is_gwg,
            "gwg_type": res.gwg_type,
            "gwg_note": res.gwg_note,
            "linear_rate_pct": res.linear_rate_pct,
            "degressiv_rate_pct": res.degressiv_rate_pct,
            "switch_year_index": res.switch_year_index,
            "switch_calendar_year": res.switch_calendar_year,
            "total_afa_first_year": res.total_afa_first_year,
            "schedule": [
                {
                    "year_index": e.year_index,
                    "calendar_year": e.calendar_year,
                    "book_value_start": e.book_value_start,
                    "method_used": e.method_used,
                    "rate_applied_pct": e.rate_applied_pct,
                    "regular_afa": e.regular_afa,
                    "sonder_afa": e.sonder_afa,
                    "total_yearly_afa": e.total_yearly_afa,
                    "cumulated_afa": e.cumulated_afa,
                    "book_value_end": e.book_value_end,
                    "is_switch_year": e.is_switch_year
                }
                for e in res.schedule
            ]
        }
        print(json.dumps(data, indent=2, ensure_ascii=False))
        return 0

    # Human readable output
    print("=" * 76)
    print(f" DACH AFA-RECHNER & ANLAGENSPIEGEL 2026 [{cfg['name']}]")
    print("=" * 76)
    print(f" Wirtschaftsgut:         {res.input_data.asset_name}")
    print(f" Anschaffungskosten:     {format_currency(res.input_data.acquisition_cost, sym)}")
    print(f" Nutzungsdauer:          {res.input_data.useful_life_years} Jahre ({parsed.month:02d}/{parsed.year})")
    print(f" AfA-Methode:            {res.input_data.method} (Linear: {res.linear_rate_pct:.1f}% | Degressiv: {res.degressiv_rate_pct:.1f}%)")
    if res.switch_calendar_year:
        print(f" Optimaler Wechsel:      Jahr {res.switch_year_index} ({res.switch_calendar_year}) zu linear")
    if res.is_gwg:
        print(f" GWG-Hinweis:            {res.gwg_note}")
    print("-" * 76)
    print(f"{'Jahr':<6} {'Buchwert Start':<16} {'Methode/Satz':<16} {'Jahres-AfA':<14} {'Restwert':<14}")
    print("-" * 76)
    for e in res.schedule:
        sw_mark = " *" if e.is_switch_year else ""
        rate_str = f"{e.method_used[:3]} {e.rate_applied_pct:.1f}%{sw_mark}"
        print(f"{e.calendar_year:<6} {format_currency(e.book_value_start, sym):<16} {rate_str:<16} {format_currency(e.total_yearly_afa, sym):<14} {format_currency(e.book_value_end, sym):<14}")
    print("=" * 76)
    if res.switch_year_index:
        print(f" * = Optimaler Wechsel von degressiver zu linearer AfA")
    print(f" AfA im Anschaffungsjahr: {format_currency(res.total_afa_first_year, sym)}")
    print("=" * 76)
    return 0


def main():
    sys.exit(run_cli())


if __name__ == "__main__":
    main()
