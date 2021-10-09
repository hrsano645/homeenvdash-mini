import datetime
from dash import Dash, callback, html, dcc, Input, Output

# dashアプリの初期化
app = Dash(
    __name__,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
)
app.title = "Hello Dash App"


def _layout():
    """全体のレイアウト構成とインターバル設定を行う"""

    now_datetime = datetime.datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S")
    return html.Div(
        [
            dcc.Location(id="url", refresh=False),
            html.H2(app.title),
            html.Label(f"Now Time: {now_datetime}"),
            dcc.Interval(
                id="interval-component",
                interval=1 * 60 * 1000,  # ミリ秒
                n_intervals=0,
            ),
        ],
        id="update",
    )


@callback(
    [
        Output("update", "children"),
    ],
    [Input("interval-component", "n_intervals")],
)
def update_sensor_values(run_intreval):
    return run_intreval


if __name__ == "__main__":
    app.layout = _layout
    app.run_server(debug=True, host="0.0.0.0")
