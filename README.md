# ⚽ Football Player Performance Analytics Dashboard

**An interactive dashboard for exploring, comparing, and visualizing football player statistics.**

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B?logo=streamlit)
![Pandas](https://img.shields.io/badge/Pandas-Analysis-150458?logo=pandas)
![Plotly](https://img.shields.io/badge/Plotly-Visualization-3F4F75?logo=plotly)
![Status](https://img.shields.io/badge/Status-Ready%20for%20Local%20Demo-brightgreen)

## Overview

A Streamlit-based football statistics dashboard that turns structured player records into interactive summaries, charts, rankings, and head-to-head comparisons.

> **Dataset notice:** `football_players.csv` contains fictional demonstration records. Names, clubs, nationalities, and statistics are illustrative and must not be presented as real-world facts. Replace the sample with a properly sourced dataset and document its license before making real-player claims.

## Features

- Filter by club, position, age, and player name.
- Summary cards for player count, goals, assists, and average rating.
- Goals by club and player distribution by position.
- Goals compared with expected goals per 90 minutes.
- Position-level metric analysis.
- Compare two players with a normalized radar chart and stat table.
- Rank players by goals, assists, rating, xG/90, xA/90, clean sheets, or minutes.
- Inspect and download filtered records as CSV.

## Technology

- Python 3.10+
- Pandas and NumPy
- Streamlit
- Plotly
- Git and GitHub

## Project structure

```text
football-player-performance-analytics/
├── .streamlit/
│   └── config.toml
├── tests/
│   └── test_dataset.py
├── app.py
├── football_players.csv
├── requirements.txt
├── .gitignore
├── LICENSE
└── README.md
```

## Run locally

### 1. Clone the repository

```bash
git clone https://github.com/kunalpatil-ce/football-player-performance-analytics.git
cd football-player-performance-analytics
```

### 2. Create and activate a virtual environment

**Windows PowerShell:**

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, use Command Prompt:

```bat
.venv\Scripts\activate.bat
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Start the dashboard

```bash
streamlit run app.py
```

Streamlit will print a local URL, usually `http://localhost:8501`.

## Dataset schema

| Column | Description |
|---|---|
| `player` | Demonstration player name |
| `nationality` | Demonstration nationality |
| `club` | Demonstration club |
| `position` | GK, DF, MF, or FW |
| `age` | Age in years |
| `matches` | Matches played |
| `starts` | Starting appearances |
| `minutes` | Minutes played |
| `goals` | Goals scored |
| `assists` | Assists |
| `clean_sheets` | Clean sheets |
| `xg_per90` | Expected goals per 90 minutes |
| `xa_per90` | Expected assists per 90 minutes |
| `rating` | Illustrative rating |

### Replacing the sample dataset

1. Obtain a dataset you are legally allowed to use.
2. Preserve the column names above or update `app.py` to match your schema.
3. Verify units, season coverage, player identity, and missing values.
4. Record the source, license, collection date, and preprocessing steps here.
5. Do not compare metrics from different providers without checking their definitions.

## Data limitations

- Included records are fictional.
- Ratings and expected metrics are illustrative.
- The radar chart rescales selected metrics to a 0–100 range for visual comparison; it is not an official player score.
- Position, competition, playing time, and season context affect interpretation.
- The app is an educational portfolio project, not a scouting or betting tool.

## Testing

Run the basic dataset validation test:

```bash
pytest
```

## Future enhancements

- Add real, licensed league and season datasets.
- Add season and competition filters.
- Introduce per-90 metrics and minutes-adjusted rankings.
- Add position-specific comparison metrics.
- Add automated data validation and unit tests.
- Deploy the app using Streamlit Community Cloud.

## Author

**Kunal Patil** — Computer Engineering Student

- GitHub: [@kunalpatil-ce](https://github.com/kunalpatil-ce)
- LinkedIn: [Kunal Patil](https://linkedin.com/in/kunal-patil-711783332)

## License

Distributed under the MIT License. See [LICENSE](LICENSE).
