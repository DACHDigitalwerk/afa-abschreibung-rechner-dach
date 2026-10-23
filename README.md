# DACH AfA-Rechner & Abschreibungs-Optimierer 2026 (Python & CLI `dach-afa`)

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-emerald.svg)](LICENSE)
[![Tests](https://img.shields.io/badge/tests-28%20passed-success.svg)](tests/)
[![Online Tool](https://img.shields.io/badge/Online%20Web--App-Live%20Rechner-indigo.svg)](https://dach-digitalwerk.netlify.app/afa-abschreibungs-rechner/)

Offizielles Open-Source-Repository der browserbasierten Web-Applikation auf **[DACH Digitalwerk: AfA-Rechner & Abschreibungs-Optimierer 2026](https://dach-digitalwerk.netlify.app/afa-abschreibungs-rechner/)**.

Berechnet prüffähige Abschreibungsverläufe (Anlagenspiegel) für **Deutschland**, **Österreich** und die **Schweiz**. Unterstützt lineare AfA, die reaktivierte **degressive AfA nach dem Wachstumschancengesetz (max. 20 %)**, die Ermittlung des mathematisch **optimalen Wechseljahres zu linear (§ 7 Abs. 3 EStG)**, die **§ 7g Abs. 5 EStG Sonderabschreibung (bis 40 %)** sowie **GWG-Prüfungen**.

---

## 💡 Warum degressive AfA & optimaler Wechselzeitpunkt?

Mit dem Wachstumschancengesetz können bewegliche Wirtschaftsgüter des Anlagevermögens degressiv abgeschrieben werden:
- **Höchstsatz Deutschland (§ 7 Abs. 2 EStG):** Maximal das Zweifache der linearen AfA, gedeckelt auf höchstens **20 % pro Jahr**.
- **Höchstsatz Österreich (§ 7 Abs. 1a EStG):** Bis zu **30 % pro Jahr**.
- **Schweiz (Art. 960a OR / ESTV):** Bis zu **40 % vom Restbuchwert**.

### Die Wechsel-Regel (§ 7 Abs. 3 EStG):
Da die degressive AfA asymptotisch sinkt, ist der Wechsel zur linearen AfA steuerlich zulässig und wirtschaftlich geboten in genau dem Jahr, in dem gilt:

$$\frac{\text{Restbuchwert}}{\text{verbleibende Restnutzungsdauer}} > \text{Restbuchwert} \times \text{Degressiv-Satz}$$

Das Tool und die Python-Bibliothek berechnen dieses Übergangsjahr vollautomatisch!

---

## 📊 Abschreibungsverlauf (Muster: 50.000 € Maschine, 10 Jahre ND, degressiv-opt)

| Jahr | Buchwert Beginn | Methode / Satz | Jahres-AfA | Restbuchwert (31.12.) | Bemerkung |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **2026 (J1)** | 50.000,00 € | Degressiv 20,0 % | **10.000,00 €** | 40.000,00 € | +5.000 € mehr Aufwand als linear! |
| **2027 (J2)** | 40.000,00 € | Degressiv 20,0 % | **8.000,00 €** | 32.000,00 € | +3.000 € mehr Aufwand als linear |
| **2028 (J3)** | 32.000,00 € | Degressiv 20,0 % | **6.400,00 €** | 25.600,00 € | +1.400 € mehr Aufwand als linear |
| **2029 (J4)** | 25.600,00 € | Degressiv 20,0 % | **5.120,00 €** | 20.480,00 € | Höher als linear |
| **2030 (J5)** | 20.480,00 € | Degressiv 20,0 % | **4.096,00 €** | 16.384,00 € | Degressiv noch günstiger |
| **2031 (J6)** | 16.384,00 € | Degressiv 20,0 % | **3.276,80 €** | 13.107,20 € | Linear rem = 3.276,80 € |
| **2032 (J7)** | 13.107,20 € | **Linear 25,0 % \*** | **3.276,80 €** | 9.830,40 € | **Optimales Wechseljahr!** |
| **2033 (J8)** | 9.830,40 € | Linear 33,3 % | **3.276,80 €** | 6.553,60 € | Konstante Restverteilung |
| **2034 (J9)** | 6.553,60 € | Linear 50,0 % | **3.276,80 €** | 3.276,80 € | Konstante Restverteilung |
| **2035 (J10)**| 3.276,80 € | Linear 100,0 % | **3.276,80 €** | **0,00 €** | Vollständig abgeschrieben |

*\* = Jahr des optimalen Wechsels von degressiver zu linearer AfA.*

---

## ⚖️ GWG-Schwellenwerte 2026 im DACH-Vergleich

- **Deutschland (§ 6 Abs. 2 / 2a EStG):**
  - Bis 250 € Netto: Bagatellgrenze (Sofortaufwand ohne Verzeichnis).
  - Bis 800 € Netto: GWG-Sofortabschreibung im Anschaffungsjahr.
  - Bis 1.000 € Netto: Wahlrecht Sammelposten (Auflösung über 5 Jahre à 20 %).
- **Österreich (§ 13 EStG):**
  - Bis 1.000 € Netto: Vollständige Sofortabschreibung im Anschaffungsjahr.
- **Schweiz (Art. 960a OR):**
  - Bis 1.500 CHF: Direkte Verbuchung als Kleininventar / Betriebsaufwand.

---

## 🚀 Installation & CLI Verwendung

```bash
# Aus dem Repository installieren
git clone https://github.com/DACHDigitalwerk/afa-abschreibung-rechner-dach.git
cd afa-abschreibung-rechner-dach
pip install -e .
```

### CLI Verwendung (`dach-afa`)

```bash
# 10.000 € Wirtschaftsgut, 5 Jahre ND, degressiv mit linearem Wechsel
dach-afa --cost 10000 --years 5 --method degressiv-opt

# 50.000 € Maschine mit optimalem Wechselzeitpunkt und JSON-Export
dach-afa --cost 50000 --years 10 --method degressiv-opt --json

# Österreichische Rechnung (Halbjahres-AfA bei Anschaffung im August)
dach-afa --cost 20000 --years 5 --month 8 --country AT --method linear

# KMU Sonder-AfA (§ 7g Abs. 5 EStG mit 20 % zusätzlich in Deutschland)
dach-afa --cost 30000 --years 5 --sonderafa 20.0
```

#### Beispiel CLI-Ausgabe:

```text
============================================================================
 DACH AFA-RECHNER & ANLAGENSPIEGEL 2026 [Deutschland]
============================================================================
 Wirtschaftsgut:         CNC-Fräsmaschine
 Anschaffungskosten:     50.000,00 €
 Nutzungsdauer:          10 Jahre (01/2026)
 AfA-Methode:            degressiv-opt (Linear: 10.0% | Degressiv: 20.0%)
 Optimaler Wechsel:      Jahr 7 (2032) zu linear
----------------------------------------------------------------------------
Jahr   Buchwert Start   Methode/Satz     Jahres-AfA     Restwert      
----------------------------------------------------------------------------
2026   50.000,00 €      deg 20.0%        10.000,00 €    40.000,00 €   
2027   40.000,00 €      deg 20.0%        8.000,00 €     32.000,00 €   
2028   32.000,00 €      deg 20.0%        6.400,00 €     25.600,00 €   
2029   25.600,00 €      deg 20.0%        5.120,00 €     20.480,00 €   
2030   20.480,00 €      deg 20.0%        4.096,00 €     16.384,00 €   
2031   16.384,00 €      deg 20.0%        3.276,80 €     13.107,20 €   
2032   13.107,20 €      lin 25.0% *      3.276,80 €     9.830,40 €    
2033   9.830,40 €       lin 33.3%        3.276,80 €     6.553,60 €    
2034   6.553,60 €       lin 50.0%        3.276,80 €     3.276,80 €    
2035   3.276,80 €       lin 100.0%       3.276,80 €     0,00 €        
============================================================================
 * = Optimaler Wechsel von degressiver zu linearer AfA
 AfA im Anschaffungsjahr: 10.000,00 €
============================================================================
```

---

## 🐍 Python Library API

```python
from afa_dach import calculate_afa, AssetInput

# 1. Direkte Berechnung
res = calculate_afa(
    acquisition_cost=50000.0,
    useful_life_years=10,
    method="degressiv-opt",
    country="DE"
)

print(f"Optimaler Wechsel im Jahr: {res.switch_year_index} ({res.switch_calendar_year})")
print(f"AfA im 1. Jahr: {res.total_afa_first_year:.2f} €")

# 2. Typed Dataclass Input
inp = AssetInput(
    acquisition_cost=20000.0,
    useful_life_years=5,
    asset_name="Server-Infrastruktur",
    acquisition_month=4,
    method="linear",
    country="DE"
)
result = calculate_afa(inp)
for row in result.schedule:
    print(f"{row.calendar_year}: AfA {row.total_yearly_afa:.2f} €, Rest {row.book_value_end:.2f} €")
```

---

## 🧪 Tests ausführen

Das Repository enthält eine vollständige Testsuite mit 28 automatisierten Unit-Tests:

```bash
pytest tests/ -v
```

---

## 🌐 Online-Werkzeuge & Ratgeber

Besuchen Sie unsere kostenlosen B2B-Online-Werkzeuge für den deutschsprachigen Wirtschaftsraum:
- **[Online AfA-Rechner & Abschreibungs-Optimierer 2026](https://dach-digitalwerk.netlify.app/afa-abschreibungs-rechner/)**
- **[Ratgeber: Amtliche AfA-Tabelle 2026 & Nutzungsdauern](https://dach-digitalwerk.netlify.app/afa-tabelle-abschreibung-nutzungsdauer-2026.html)**
- **[Ratgeber: Degressive AfA nach Wachstumschancengesetz](https://dach-digitalwerk.netlify.app/degressive-afa-wachstumschancengesetz-2026-rechner.html)**
- **[Ratgeber: GWG-Grenzen 2026: DE vs. AT vs. CH](https://dach-digitalwerk.netlify.app/gwg-grenzen-deutschland-oesterreich-schweiz-vergleich.html)**
- **[DACH Digitalwerk Hub](https://dach-digitalwerk.netlify.app/)**

---

## 📄 Lizenz & Rechtlicher Hinweis

Dieses Projekt ist unter der **MIT License** lizenziert.

*Rechtlicher Hinweis:* Dieses Tool dient ausschließlich mathematischen Berechnungen und betriebswirtschaftlichen Simulationen gemäß § 2 RDG / § 5 StBerG. Es stellt keine Rechts- oder Steuerberatung dar.
