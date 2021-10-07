# homeenvdash mini
import datetime

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas
import plotly.express as px
from dash.dependencies import Input, Output
# import dash_bootstrap_components as dbc

import time
import board
from adafruit_bme280 import basic as adafruit_bme280

# dashアプリの初期化
app = dash.Dash(
    __name__,
    # external_stylesheets=[dbc.themes.BOOTSTRAP],
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
)
app.title = "homeenvdash-mini"
app.config.suppress_callback_exceptions = True


# # Create sensor object, using the board's default I2C bus.
# i2c = board.I2C()  # uses board.SCL and board.SDA
# bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c)

# # OR create sensor object, using the board's default SPI bus.
# # spi = board.SPI()
# # bme_cs = digitalio.DigitalInOut(board.D10)
# # bme280 = adafruit_bme280.Adafruit_BME280_SPI(spi, bme_cs)

# # change this to match the location's pressure (hPa) at sea level
# bme280.sea_level_pressure = 1013.25

# while True:
#     print("\nTemperature: %0.1f C" % bme280.temperature)
#     print("Humidity: %0.1f %%" % bme280.relative_humidity)
#     print("Pressure: %0.1f hPa" % bme280.pressure)
#     print("Altitude = %0.2f meters" % bme280.altitude)
#     time.sleep(2)

def _layout():
    """
    全体のレイアウト
    """

    return html.Div(
        [
            dcc.Location(id="url", refresh=False),
            html.H2(app.title),
            html.Hr(),
            # dcc.Interval(
            #     id="interval-component",
            #     interval=10 * 60 * 1000,  # in milliseconds
            #     n_intervals=0,
            # ),
        ],
    )


# # 自動リロードとドロップダウンリストでのコールバック
# @app.callback(
#     [
#         Output("latest_view", "children"),
#         Output("graph_tabs", "children"),
#     ],
#     [
#         Input("interval-component", "n_intervals"),
#         Input("date-range-dd", "value"),
#         Input("location-dd", "value"),
#     ],
# )
# def update_contents(n, date_dd_value, location_dd_value):
#     # now = datetime.datetime.now().astimezone()
#     # print(f"リロード時間:{now} 日付:{date_dd_value} 場所:{location_dd_value}")

#     sensor_df = generate_df(location_dd_value, date_dd_value)
#     sidebar = generate_latest_view(sensor_df)
#     graph_tab = generate_graph_tabs(sensor_df)

#     return sidebar, graph_tab


if __name__ == "__main__":

    app.layout = _layout
    app.run_server(debug=True, host="0.0.0.0")