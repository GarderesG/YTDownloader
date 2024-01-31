from dash import Dash, html, dcc, Output, Input, State
import dash_bootstrap_components as dbc
from YTDownload import YTDownloader
import jsonpickle
import re

app = Dash(__name__, 
    external_stylesheets=[dbc.themes.DARKLY])

app.layout = dbc.Container(
    html.Div([
        html.H1("YTDownloader"),
        html.Div(children='Download videos from You Tube at best resolution!'),
        dcc.Input(id="input-link", type="text", size="60"),
        dcc.Store(id="stored-yt-object"), 
        
        # activate when link is provided, with loading and info about the video
        dcc.Loading(
            id="loading-info",
            type="default",
            children = html.Div(children=[
                            html.H4(id="video-desc"),
                            ],
                            id="hidden-info-video",
                            style= {'display': 'none'}
                            )
        ),
        html.Button("Download", id="btn-download", style= {'display': 'none'}, n_clicks=0),
    ])
)

@app.callback(
    Output("hidden-info-video", "style"),
    Output("video-desc", "children", allow_duplicate=True), 
    Output("stored-yt-object", "data"),
    Input("input-link", "value"),
    prevent_initial_call=True,
    )
def link_to_visible_div(url: str):
    """
    Whenever a new link is provided in the text area, show div with video title and resoltution.
    """
    if is_link_empty(url) is None:
        return {"display": "none"}, "", ""
    try:
        yt = YTDownloader(url)
        return {"display": "block"}, f"{yt.get_video_name()} ({yt.get_highest_video_res()})", jsonpickle.encode(yt)

    except Exception:
        return {"display": "block"}, f"Youtube link is incorrect", ""


def is_link_empty(text: str):
    """
    Basic function to check that an URL is not empty.
    """
    # At least contains letters
    return re.search(r'[a-zA-Z]+', text.replace(" ", ""))


@app.callback(
    Output("btn-download", "style", allow_duplicate=True),
    Input("hidden-info-video", "style"),
    prevent_initial_call=True
    )
def button_download_visible_from_desc(style_desc):
    """
    Callback to make the Download button visible once the Div with the video name is visible.
    """
    if style_desc != dict(display="none"):
        # If video information is visible and button was not clicked, show Download button
        return dict(display="block")
    else:
        # else 
        return dict(display="none")

@app.callback(
    Output("btn-download", "style"),
    Input("btn-download", "n_clicks")
    )
def button_download_visible_from_btn(n_clicks):
    """
    Callback to hide the Download button whenevr it is clicked.
    """
    return dict(display="none")
    

@app.callback(
    Output("video-desc", "children"),
    Input("btn-download", "n_clicks"),
    State("stored-yt-object", "data")
    )
def download_file(n_clicks, yt):
    """
    Callback to download the YouTube video once the Download button is pushed.
    Uses the YTDownloader object created in link_to_visible_div callback
    """
    if n_clicks > 0 and yt is not None:
        yt = jsonpickle.decode(yt)
        yt.download_video_hq()
        return f"Download was successful ({yt.download_time:.0f} sec)"

        
if __name__ == '__main__':
    app.run(debug=True)