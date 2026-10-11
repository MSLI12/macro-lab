<<<<<<< HEAD
# initial
a basic combination of time series analysis
=======
# Macro Lab

Macro Lab is an experimental Django application for exploring macroeconomic data, extracting broader economic signals, and eventually building user-controlled economic scenarios.

The long-term goal is to create a public-data economic laboratory where historical time series can be explored together and hypothetical future paths can be imposed on selected variables.

Rather than relying on opaque prediction models, the project focuses on transparent economic data, statistical relationships, and explicit user-defined scenarios.

## Current Features

The current version includes:

- FRED economic time-series retrieval
- Local persistence of economic observations using Django models
- Interactive Plotly charts
- A macro activity factor estimated from several real-activity indicators
- An inflation-pressure factor estimated from several price indicators
- Basic exploration of individual economic series

The project is still at an early stage.

## Economic Data

Initial data comes from the Federal Reserve Economic Data (FRED) service.

Examples currently used include:

- Industrial production
- Manufacturing production
- Employment
- Real personal income
- CPI and core CPI
- PCE prices
- Producer prices
- Interest rates
- Money supply

Downloaded observations are stored locally through Django's ORM.

## Direction

Macro Lab is intended to grow into a broader economic scenario environment.

Historical observations will remain separate from hypothetical scenario paths. Users will eventually be able to modify future trajectories of economic variables and study the implications through multiple transparent statistical and economic models.

Potential future areas include financial conditions, labor markets, commodities, housing, credit, international trade, scenario comparison, and conditional macroeconomic simulations.

## Technology

- Python
- Django
- pandas
- NumPy
- statsmodels
- Plotly
- SQLite during development
- FRED economic data

## Local Setup

Clone the repository:

```bash
git clone <repository-url>
cd macro-lab
```

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run database migrations:

```bash
python manage.py migrate
```

Start the development server:

```bash
python manage.py runserver
```

Then open:

```text
http://127.0.0.1:8000/
```

## Status

Early development / research prototype.

The current implementation establishes the data and modeling foundation. Scenario construction and broader economic-model integration are planned for later iterations.

## Data Disclaimer

Macro Lab is an experimental research project. It is not intended to provide investment advice, trading recommendations, or official economic forecasts.
