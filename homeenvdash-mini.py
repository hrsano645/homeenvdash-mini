# homeenvdash mini
import datetime
import time
from pathlib import Path
from uuid import NAMESPACE_URL

import board
import digitalio
import pandas
import plotly.express as px
from adafruit_bme280 import basic as adafruit_bme280
# from dash.dependencies import Input, Output
# from dash import Dash, callback, html, dcc, dash_table, Input, Output, State, MATCH, ALL
from dash import Dash, callback, html, dcc, Input, Output
# import dash_bootstrap_components as dbc

# 保存するCSVファイル名

SENSOR_VALUES_FILE = Path("./sensor_values.csv")

# dashアプリの初期化
app = Dash(
    __name__,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
)
app.title = "homeenvdash-mini"
app.config.suppress_callback_exceptions = True

spi = board.SPI()
bme_cs = digitalio.DigitalInOut(board.D5)
bme280 = adafruit_bme280.Adafruit_BME280_SPI(spi, bme_cs)

# change this to match the location's pressure (hPa) at sea level
bme280.sea_level_pressure = 1013.25

def get_sensor_values():
    """センサーの値を取得する。記録は文字列にする"""
    temperature = f"{bme280.temperature:.1f}"
    relative_humidity = f"{bme280.relative_humidity:.1f}"
    pressure = f"{bme280.pressure:.1f}"

    return (temperature, relative_humidity, pressure)

def save_sensor_values(sensor_values: tuple, recode_datetime: datetime.datetime, max_row: int = 2000):
    """
        センサーの値をCSVへ保存する
        CSVの行数はデフォルト2000行で増やしつつ、過去の行は捨てていく
    """

    # sensor_values = (temperature, relative_humidity, pressure)
    temperature = sensor_values[0]
    relative_humidity = sensor_values[1]
    pressure = sensor_values[2]
    # print(sensor_values)

    update_sensor_values_list = []

    # ファイルを開く
    if SENSOR_VALUES_FILE.exists():
        with SENSOR_VALUES_FILE.open(encoding="utf-8") as sensor_values_file:
            sensor_values_list = sensor_values_file.readlines()
        update_sensor_values_list = sensor_values_list[:]

    # Maxな行の場合、先頭を削る（Max-1の行
    if len(sensor_values_list) >= max_row:
        update_sensor_values_list = sensor_values_list[1:max_row]

    # 新しい行を末尾に追加
    add_line_str = f"{recode_datetime.isoformat()},{temperature},{relative_humidity},{pressure}\n"
    update_sensor_values_list.append(add_line_str)

    # ファイルを保存
    with SENSOR_VALUES_FILE.open("w", encoding="utf-8") as sensor_values_file:
        sensor_values_file.writelines(update_sensor_values_list)


def latest_sensor_values(sensor_values: tuple, now_datetime: datetime.datetime):
    """現在のセンサー値を描写する。"""
    
    # TODO:2020-11-24 ここは時間以外はオプション的な扱いにして、列ヘッダを見て設定できるととてもいい
    #    時間だけは絶対に必要にして、その列がない場合は例外を出して終了する
    latest_datetime = now_datetime.strftime("%Y-%m-%d %H:%M:%S")
    latest_temperature = sensor_values[0]
    latest_pressure = sensor_values[1]
    latest_humidity = sensor_values[2]

    return html.Div(
        [
            html.Label(f"更新時間 :{latest_datetime}"),
            html.Div(
                [
                    html.H6(f"気温: {latest_temperature}℃"),
                    html.H6(f"湿度: {latest_pressure}%"),
                    html.H6(f"気圧: {latest_humidity}hPa"),
                ],
            ),
        ],
        id="latest_values",
    )


# def generate_sensors_df():
#     """グラフを描写するためのDataframeを用意する"""
#     pass


def sensor_graphs():
    """過去に記録したセンサー情報の値をグラフにする"""

    sensor_values_df = pandas.read_csv(SENSOR_VALUES_FILE, 
        names=("datetime", "temperature", "pressure", "humidity")
    )

    fig1 = px.line(sensor_values_df, x="datetime", y="temperature", title="温度")
    fig2 = px.line(sensor_values_df, x="datetime", y="pressure", title="気圧")
    fig3 = px.line(sensor_values_df, x="datetime", y="humidity", title="湿度")

    return html.Div(
        [
            dcc.Graph(id="tempature", figure=fig1),
            dcc.Graph(id="pressure", figure=fig2),
            dcc.Graph(id="humidity", figure=fig3),
        ],
        id="graphs"
    )


def _layout():
    """全体のレイアウト構成とインターバル設定を行う"""

    now_dt_str = datetime.datetime.now().astimezone()
    sensor_values = get_sensor_values()

    return html.Div(
        [
            dcc.Location(id="url", refresh=False),
            html.H2(app.title),
            html.Hr(),
            # 現在の値を取得
            latest_sensor_values(sensor_values, now_dt_str ),
            # 温度、湿度、気圧のグラフ（だけ）
            sensor_graphs(), 

            dcc.Interval(
                id="interval-component",
                interval=1 * 60 * 1000,  # in milliseconds
                n_intervals=0,
            ),
        ],
    )

# TODO: 2021/10/07 この先の処理には課題があります。
# スクリプトを起動している状態でないと値の記録が行えません。
# BME280のセンサー情報を定量的に保存したい場合はセンサー記録用のスクリプトを用意すると良いでしょう。
# 今回は機能紹介のために一つのスクリプトにまとめています。

# センサーの値取得とコールバック
@callback(
    [
        Output("latest_values", "children"),
        Output("graphs", "children"),
    ],
    [
        Input("interval-component", "n_intervals")
    ],
)
def update_sensor_values(n):

    # 計測時の時間
    now_dt_str: datetime.datetime = datetime.datetime.now().astimezone()

    # センサーの情報を取得
    sensor_values = get_sensor_values()

    # 現在の値をCSVファイルへ保存
    save_sensor_values(sensor_values, now_dt_str, 30)

    # 現在値やグラフを更新
    latest_values = latest_sensor_values(sensor_values, now_dt_str )
    graphs = sensor_graphs()

    return latest_values, graphs


if __name__ == "__main__":
    app.layout = _layout
    app.run_server(debug=True, host="0.0.0.0")
