import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go

# ----------------------------
# DATA LOADING
# ----------------------------
USE_SAMPLE_DATA = True  # Set to False when DuckDB is ready

if USE_SAMPLE_DATA:
    df = pd.read_parquet("visualization/sample_data.parquet")
else:
    import duckdb
    con = duckdb.connect("data/warehouse/apppulse.duckdb", read_only=True)
    df = con.execute("""
        SELECT app, category, avg_rating, installs, reviews_count, 
               price, sentiment_score, last_updated
        FROM fact_app_metrics
        WHERE avg_rating IS NOT NULL
    """).fetchdf()
    con.close()

df['last_updated'] = pd.to_datetime(df['last_updated'])
categories = df['category'].unique()

# ----------------------------
# THEME HELPER
# ----------------------------
def get_theme_style(theme):
    if theme == 'light':
        return {
            'bg': '#f8f9fa',
            'card': '#ffffff',
            'text': '#2c3e50',
            'plot_bg': 'white',
            'grid': '#ddd',
            'paper_bg': 'rgba(0,0,0,0)'
        }
    else:
        return {
            'bg': '#1e1e1e',
            'card': '#2d2d2d',
            'text': '#f0f0f0',
            'plot_bg': '#1e1e1e',
            'grid': '#444',
            'paper_bg': 'rgba(0,0,0,0)'
        }

# ----------------------------
# APP
# ----------------------------
app = dash.Dash(__name__)
app.title = "AppPulse Analytics"

# ----------------------------
# LAYOUT
# ----------------------------
app.layout = html.Div([
    # Theme Toggle
    html.Div([
        dcc.RadioItems(
            id='theme-toggle',
            options=[
                {'label': '☀️ Light', 'value': 'light'},
                {'label': '🌙 Dark', 'value': 'dark'}
            ],
            value='light',
            inline=True,
            labelStyle={'margin-right': '20px', 'cursor': 'pointer'}
        )
    ], style={'position': 'absolute', 'top': '20px', 'right': '20px', 'zIndex': '10'}),

    # Dynamic Content
    html.Div(id='page-content')
])

# ----------------------------
# PAGE CONTENT CALLBACK
# ----------------------------
@app.callback(
    Output('page-content', 'children'),
    Input('theme-toggle', 'value')
)
def update_page_theme(theme):
    style = get_theme_style(theme)
    return [
        # Header
        html.Div([
            html.H1("🚀 AppPulse Analytics Dashboard", 
                    style={'textAlign': 'center', 'color': style['text'], 'marginBottom': '5px', 'fontSize': '2.3rem'}),
            html.P("Insights into Google Play Store app performance & user sentiment",
                   style={'textAlign': 'center', 'color': '#7f8c8d' if theme == 'light' else '#aaa', 'marginBottom': '20px'})
        ], style={'backgroundColor': style['bg'], 'padding': '20px', 'borderBottom': f'1px solid {"#eaeaea" if theme == "light" else "#333"}'}),

        # Filter
        html.Div([
            html.Label("FilterWhere by Category:", style={'fontWeight': 'bold', 'fontSize': '1.1rem', 'color': style['text'], 'marginBottom': '10px'}),
            dcc.Dropdown(
                id='category-filter',
                options=[{'label': cat, 'value': cat} for cat in categories],
                value=categories.tolist(),
                multi=True,
                placeholder="Select one or more categories...",
                style={'width': '100%'}
            )
        ], style={'width': '60%', 'margin': '0 auto 20px', 'padding': '0 20px', 'backgroundColor': style['bg']}),

        # KPI Cards
        html.Div(id='kpi-cards', style={'padding': '0 20px', 'marginBottom': '30px', 'backgroundColor': style['bg']}),

        # Charts
        html.Div([
            dcc.Graph(id='top-apps', config={'displayModeBar': False}),
            dcc.Graph(id='growth-trend', config={'displayModeBar': False}),
            dcc.Graph(id='price-rating', config={'displayModeBar': False}),
            dcc.Graph(id='sentiment-gauge', config={'displayModeBar': False})
        ], style={'padding': '0 20px', 'backgroundColor': style['bg']})
    ]

# ----------------------------
# KPI CARDS CALLBACK
# ----------------------------
@app.callback(
    Output('kpi-cards', 'children'),
    [Input('category-filter', 'value'), Input('theme-toggle', 'value')]
)
def update_kpi_cards(selected_categories, theme):
    if not selected_categories:
        filtered_df = df.head(0)
    else:
        filtered_df = df[df['category'].isin(selected_categories)]

    style = get_theme_style(theme)

    total_apps = len(filtered_df) if not filtered_df.empty else 0
    avg_rating = round(filtered_df['avg_rating'].mean(), 2) if not filtered_df.empty else 0
    total_installs = f"{filtered_df['installs'].sum():,}" if not filtered_df.empty else "0"
    avg_sentiment = round(filtered_df['sentiment_score'].mean(), 2) if not filtered_df.empty else 0

    kpi_data = [
        ("📱 Total Apps", total_apps, "#3498db"),
        ("⭐ Avg Rating", avg_rating, "#f39c12"),
        ("📥 Total Installs", total_installs, "#2ecc71"),
        ("😊 Avg Sentiment", avg_sentiment, "#9b59b6")
    ]

    return html.Div([
        html.Div([
            html.H3(title, style={'color': color, 'margin': '0'}),
            html.H2(str(value), style={'color': style['text'], 'margin': '10px 0'})
        ], style={
            'backgroundColor': style['card'],
            'padding': '15px',
            'borderRadius': '8px',
            'textAlign': 'center',
            'boxShadow': '0 2px 5px rgba(0,0,0,0.1)',
            'flex': '1',
            'minWidth': '200px'
        }) for title, value, color in kpi_data
    ], style={'display': 'flex', 'justifyContent': 'space-between', 'gap': '15px', 'flexWrap': 'wrap'})

# ----------------------------
# CHARTS CALLBACK
# ----------------------------
@app.callback(
    [Output('top-apps', 'figure'),
     Output('growth-trend', 'figure'),
     Output('price-rating', 'figure'),
     Output('sentiment-gauge', 'figure')],
    [Input('category-filter', 'value'), Input('theme-toggle', 'value')]
)
def update_charts(selected_categories, theme):
    if not selected_categories:
        filtered_df = df.head(0)
    else:
        filtered_df = df[df['category'].isin(selected_categories)].copy()

    style = get_theme_style(theme)
    color_discrete_map = {cat: px.colors.qualitative.Bold[i % len(px.colors.qualitative.Bold)] for i, cat in enumerate(categories)}

    # Helper for empty charts
    def empty_fig(title):
        fig = go.Figure()
        fig.add_annotation(text="No data available", x=0.5, y=0.5, showarrow=False, font=dict(color=style['text']))
        fig.update_layout(title=title, plot_bgcolor=style['plot_bg'], paper_bgcolor=style['paper_bg'], font_color=style['text'])
        return fig

    # 1. Top Apps
    if filtered_df.empty:
        fig1 = empty_fig("⭐ Top-Rated Apps by Category")
    else:
        top_apps = filtered_df.nlargest(10, 'avg_rating')
        fig1 = px.bar(top_apps, x='app', y='avg_rating', color='category', color_discrete_map=color_discrete_map, title="⭐ Top-Rated Apps by Category")
        fig1.update_layout(
            xaxis_tickangle=-45,
            plot_bgcolor=style['plot_bg'],
            paper_bgcolor=style['paper_bg'],
            font_color=style['text'],
            title_x=0.5,
            xaxis=dict(gridcolor=style['grid'], showgrid=True),
            yaxis=dict(gridcolor=style['grid'], showgrid=True)
        )

    # 2. Growth Trend
    if filtered_df.empty:
        fig2 = empty_fig("📈 Category Growth Over Time (Total Installs)")
    else:
        filtered_df['month'] = filtered_df['last_updated'].dt.to_period('M').astype(str)
        trend = filtered_df.groupby('month')['installs'].sum().reset_index()
        fig2 = px.line(trend, x='month', y='installs', title="📈 Category Growth Over Time (Total Installs)")
        fig2.update_layout(
            plot_bgcolor=style['plot_bg'],
            paper_bgcolor=style['paper_bg'],
            font_color=style['text'],
            title_x=0.5,
            xaxis=dict(gridcolor=style['grid'], showgrid=True),
            yaxis=dict(gridcolor=style['grid'], showgrid=True)
        )

    # 3. Price vs Rating
    if filtered_df.empty:
        fig3 = empty_fig("💰 Price vs Rating (Bubble = Installs)")
    else:
        fig3 = px.scatter(filtered_df, x='price', y='avg_rating', size='installs', color='category', color_discrete_map=color_discrete_map,
                          title="💰 Price vs Rating (Bubble = Installs)", size_max=60)
        fig3.update_layout(
            plot_bgcolor=style['plot_bg'],
            paper_bgcolor=style['paper_bg'],
            font_color=style['text'],
            title_x=0.5,
            xaxis=dict(gridcolor=style['grid'], showgrid=True),
            yaxis=dict(gridcolor=style['grid'], showgrid=True)
        )

    # 4. Sentiment Gauge
    avg_sent = filtered_df['sentiment_score'].mean() if not filtered_df.empty else 0
    fig4 = go.Figure(go.Indicator(
        mode="gauge+number",
        value=round(avg_sent, 2),
        title={'text': "😊 Average User Sentiment", 'font': {'size': 24, 'color': style['text']}},
        gauge={
            'axis': {'range': [0, 1], 'tickcolor': style['text'], 'tickfont': {'color': style['text']}},
            'bar': {'color': "#3498db"},
            'bgcolor': "white" if theme == 'light' else "#333",
            'borderwidth': 2,
            'bordercolor': "#3498db",
            'steps': [
                {'range': [0, 0.3], 'color': '#e74c3c'},
                {'range': [0.3, 0.7], 'color': '#f39c12'},
                {'range': [0.7, 1], 'color': '#2ecc71'}
            ]
        }
    ))
    fig4.update_layout(
        height=400,
        margin=dict(l=20, r=20, t=60, b=20),
        paper_bgcolor=style['paper_bg'],
        font_color=style['text']
    )

    return fig1, fig2, fig3, fig4

# ----------------------------
if __name__ == '__main__':
    app.run(debug=True, port=8050)