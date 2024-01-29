from dash import Dash, html, dcc, Output, Input
import dash_bootstrap_components as dbc
from YTDownload import YTDownloader

app = Dash(__name__, 
    external_stylesheets=[dbc.themes.DARKLY])

app.layout = dbc.Container(
    html.Div([
        html.H1("YTDownloader"),
        html.Div(children='Download videos from You Tube at best resolution!'),
        dcc.Input(id="input-link", type="text"), 
        html.Button("Submit", id="submit-link", hidden=True),
        
        # activate when link is provided
        html.Div(children=[
            html.H3(id="video-desc"),
            ],
            id="hidden-info-video",
            style= {'display': 'block'}
        )
    ])
)


@app.callback(
    Output("hidden-info-video", "style"),
    Output("video-desc", "children"),
    Input("input-link", "value"),
    prevent_initial_call=True
    )
def link_to_visible_div(url: str):
    if is_link_empty(url):
        return {"display": "none"}, ""
    
    try:
        yt = YTDownloader(url)
        return {"display": "block"}, f"{yt.get_video_name()} ({yt.get_highest_video_res()})", 

    except Exception:
        return {"display": "block"}, "YouTube url is not correct"
     

def is_link_empty(text: str):
    return text in ["", " "]


if __name__ == '__main__':
    app.run(debug=True)