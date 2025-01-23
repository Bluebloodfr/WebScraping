import plotly.express as px
from src import geojson

def print_density(df):
    fig = px.density_mapbox(df, 
        lat='latitude', lon='longitude', radius=4,
        center={"lat": 46.037763, "lon": 4.4}, 
        zoom=4, color_continuous_midpoint=5,
        mapbox_style='carto-positron', 
        color_continuous_scale=['grey', 'darkgrey', 'grey', 'red', 'red'],
        title='Density Map of Tourism Data'
    )
    fig.update_layout(
        coloraxis_showscale=True,
        coloraxis_colorbar=dict(
            title="Density",
            titleside="right"
        ),
        margin=dict(l=0, r=0, b=0, t=30, pad=4)
    )
    fig.update_traces(hoverinfo='skip', hovertemplate=None)
    return fig

def print_choropleth(df):
    # Prepare the data
    df['dept_code'] = df['codepostal'].str[:2]
    counts = df['dept_code'].value_counts().reset_index()
    counts.columns = ['code_departement', 'count']

    # Choropleth map
    fig = px.choropleth_mapbox(
        counts,
        geojson=geojson,                 # Your geojson file
        locations='code_departement',       # Match with geojson keys
        color='count',                      # Count of occurrences
        featureidkey='properties.code',     # Match geojson property
        opacity=1,
        center={"lat": 46.037763, "lon": 2.062783},
        mapbox_style="carto-positron",
        zoom=4,
        title='Choropleth Map of Tourism Data'
    )

    fig.update_layout(
        coloraxis_showscale=True,
        coloraxis_colorbar=dict(
            title="Count",
            titleside="right"
        ),
        margin={"r":0, "t":30, "l":0, "b":0}
    )
    return fig