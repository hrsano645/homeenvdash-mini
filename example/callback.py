import datetime
from dash import Dash, callback, html, dcc, Input, Output

# dashアプリの初期化
app = Dash(
    __name__,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
)
app.title = "Hello Dash App"

# TODO:2021-10-12 文字列を置き換えるようなcallbackにしておく

def _layout():
    """全体のレイアウト構成とインターバル設定を行う"""

    now_datetime = datetime.datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S")
    return html.Div(
        [
            html.H2(app.title),
            html.Label(f"Now Time: {now_datetime}"),
        ],
        id="update",
    )


@callback(
    [
        Output("update", "children"),
    ],
    [Input("interval-component", "n_intervals")],
)
def update_sensor_values(update):
    
    now_datetime = datetime.datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S")
    return html.Div(
        [
            html.H2(app.title),
            html.Label(f"Now Time: {now_datetime}"),
        ],
        id="update",
    )


if __name__ == "__main__":
    app.layout = _layout
    app.run_server(debug=True, host="0.0.0.0")
