from dash import Dash, html, dcc, Output, Input, State
import dash_bootstrap_components as dbc
from YTDownload import YTDownloader
import jsonpickle
import re

app = Dash(__name__, 
    external_stylesheets=[dbc.themes.DARKLY])

app.layout = dbc.Container(
    html.Div([
        html.H1("YTDownloader", className="display-3"),
        html.P('Download videos from You Tube at best resolution.', className="lead"),
        html.Hr(className="my-2"),
        html.P("Enter the link of the YouTube video to download."),
        dbc.Input(id="input-link", type="text", placeholder="Enter link..."),
        dcc.Store(id="stored-yt-object"), 
        
        # activate when link is provided, with loading and info about the video
        dcc.Loading(
            id="loading-info",
            type="default",
            children = dbc.Collapse(children=[
                            dbc.CardGroup([
                                dbc.CardImg(src ="assets/YT.png", top=True, style={"height": "5vh", "width": "5vh"}),
                                dbc.Card(
                                    [
                                    html.H5(id="video-desc", className="card-title"),
                                    html.P(id="res", className = "card-text pl-15")
                                    ],
                                    className="d-flex justify-content-center",
                                    style={"padding-left": "10px"},
                                    color="dark"
                                ),
                            ], className="card border-light mb-3", style={"margin-top": "20px"})
                            ],
                            id="hidden-info-video",
                            is_open=True,
                            style= {'display': 'none'}
                            )
        ),
        dbc.Button("Download", id="btn-download", style= {'display': 'none'}, n_clicks=0, color="primary"),
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
    State("video-desc", "children"),
    prevent_initial_call=True
    )
def button_download_visible_from_desc(style_desc, video_desc: str):
    """
    Callback to make the Download button visible once the Div with the video name is visible.
    """
    if style_desc != dict(display="none") and video_desc != "Youtube link is incorrect":
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