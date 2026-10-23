# -*- coding: utf-8 -*-
"""
Quickstart example for afa_dach.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from afa_dach import calculate_afa, AssetInput

def main():
    print("--- 1. Degressive AfA mit optimalem Wechselzeitpunkt (Deutschland) ---")
    res1 = calculate_afa(
        acquisition_cost=50000.0,
        useful_life_years=10,
        asset_name="CNC-Bearbeitungszentrum",
        acquisition_month=1,
        acquisition_year=2026,
        method="degressiv-opt",
        country="DE"
    )
    print(f"Anlagegut:            {res1.input_data.asset_name}")
    print(f"Anschaffungskosten:   {res1.input_data.acquisition_cost:,.2f} €")
    print(f"Degressiver AfA-Satz: {res1.degressiv_rate_pct:.1f} % p.a.")
    print(f"Optimaler Wechsel:    Jahr {res1.switch_year_index} ({res1.switch_calendar_year}) zu linear")
    print(f"AfA im Jahr 1:        {res1.total_afa_first_year:,.2f} €\n")

    print(f"{'Jahr':<6} {'Buchwert Start':<16} {'Methode/Satz':<16} {'Jahres-AfA':<14} {'Restwert':<14}")
    print("-" * 68)
    for row in res1.schedule:
        sw = " *" if row.is_switch_year else ""
        print(f"{row.calendarYear if hasattr(row, 'calendarYear') else row.calendar_year:<6} {row.book_value_start:>10,.2f} €    {row.method_used[:3]} {row.rate_applied_pct:>4.1f}%{sw:<2}    {row.total_yearly_afa:>10,.2f} €   {row.book_value_end:>10,.2f} €")

    print("\n--- 2. Österreichische Halbjahres-AfA ---")
    res_at = calculate_afa(
        acquisition_cost=15000.0,
        useful_life_years=5,
        asset_name="Lieferfahrzeug",
        acquisition_month=8,  # August -> Halbjahresregel greift
        country="AT",
        method="linear"
    )
    print(f"AfA Jahr 1 (Halbjahres-AfA): {res_at.total_afa_first_year:,.2f} € (50% der Jahres-AfA)")

if __name__ == "__main__":
    main()
