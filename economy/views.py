import plotly.express as px
import plotly.graph_objects as go

from django.shortcuts import render

from .services import get_fred_series
from .macro import (
    get_activity_factor,
    get_inflation_factor,
)


SERIES = {
    "INDPRO": "Industrial Production",
    "CPIAUCSL": "Consumer Price Index",
    "UNRATE": "Unemployment Rate",
    "FEDFUNDS": "Federal Funds Rate",
    "M2SL": "M2 Money Supply",
}


def index(request):
    series_id = request.GET.get("series", "INDPRO")

    if series_id not in SERIES:
        series_id = "INDPRO"

    # Existing FRED explorer
    df = get_fred_series(series_id)

    fig = px.line(
        df,
        x="date",
        y="value",
        title=SERIES[series_id],
    )

    fig.update_layout(
        template="plotly_white",
        xaxis_title="",
        yaxis_title="",
    )

    # --------------------------
    # MACRO ACTIVITY MODEL
    # --------------------------

    factor, components = get_activity_factor()

    factor_fig = go.Figure()

    factor_fig.add_trace(
        go.Scatter(
            x=factor.index,
            y=factor,
            mode="lines",
            name="Activity factor",
        )
    )

    factor_fig.add_hline(
        y=0,
        line_dash="dash",
        opacity=0.5,
    )

    factor_fig.update_layout(
        title="US Macro Activity Factor",
        template="plotly_white",
        xaxis_title="",
        yaxis_title="Standard deviations",
        hovermode="x unified",
    )

    latest_factor = factor.iloc[-1]

    if latest_factor > 0:
        activity_position = "Above historical average"
    else:
        activity_position = "Below historical average"

    if len(factor) >= 4 and factor.iloc[-1] > factor.iloc[-4]:
        activity_direction = "Strengthening"
    else:
        activity_direction = "Weakening"

    inflation_factor, inflation_components = get_inflation_factor()
    inflation_fig = go.Figure()

    inflation_fig.add_trace(
        go.Scatter(
            x=inflation_factor.index,
            y=inflation_factor,
            mode="lines",
            name="Inflation pressure",
        )
    )

    inflation_fig.add_hline(
        y=0,
        line_dash="dash",
        opacity=0.5,
    )

    inflation_fig.update_layout(
        title="US Inflation Pressure Factor",
        template="plotly_white",
        xaxis_title="",
        yaxis_title="Standard deviations",
        hovermode="x unified",
    )

    latest_inflation = inflation_factor.iloc[-1]

    if latest_inflation > 0:
        inflation_position = "Above historical average"
    else:
        inflation_position = "Below historical average"

    if len(inflation_factor) >= 4 and inflation_factor.iloc[-1] > inflation_factor.iloc[-4]:
        inflation_direction = "Rising"
    else:
        inflation_direction = "Falling"

    context = {
        "chart": fig.to_html(
            full_html=False,
            include_plotlyjs="cdn",
        ),

        "factor_chart": factor_fig.to_html(
            full_html=False,
            include_plotlyjs=False,
        ),

        "series": SERIES,
        "selected": series_id,

        "activity_factor": round(latest_factor, 2),
        "activity_position": activity_position,
        "activity_direction": activity_direction,

        # NEW
        "inflation_chart": inflation_fig.to_html(
            full_html=False,
            include_plotlyjs=False,
        ),
        "inflation_factor": round(latest_inflation, 2),
        "inflation_position": inflation_position,
        "inflation_direction": inflation_direction,
    }

    return render(
        request,
        "economy/index.html",
        context,
    )


