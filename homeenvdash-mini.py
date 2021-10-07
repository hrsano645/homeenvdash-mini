# homeenvdash mini
import datetime
import time
from pathlib import Path

import board
import dash
import dash_core_components as dcc
import dash_html_components as html
import digitalio
import pandas
import plotly.express as px
from adafruit_bme280 import basic as adafruit_bme280
from dash.dependencies import Input, Output

# import dash_bootstrap_components as dbc

# 保存するCSVファイル名

SENSOR_VALUES_FILE = Path("./sensor_values.csv")

# dashアプリの初期化
app = dash.Dash(
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
    temperature = f"{bme280.temperature:.1g}"
    relative_humidity = f"{bme280.relative_humidity:.1g}"
    pressure = f"{bme280.pressure:.1g}"
    
    # print(f"Temperature: {temperature} C")
    # print(f"Humidity: {relative_humidity} %%")
    # print(f"Pressure: {pressure} hPa")

    return (temperature, relative_humidity, pressure)

def save_sensor_values(sensor_values, recode_datetime, max_row=2000):
    """
        センサーの値をCSVへ保存する
        CSVの行数はデフォルト2000行で増やしつつ、過去の行は捨てていく
    """

    # sensor_values = (temperature, relative_humidity, pressure)
    temperature = sensor_values[0]
    relative_humidity = sensor_values[1]
    pressure = sensor_values[2]

    # ファイルを開く
    with SENSOR_VALUES_FILE.open(encoding="utf-8") as sensor_values_file:
        sensor_values_list = list(sensor_values_file.readlines)
    update_sensor_values_list = sensor_values_list[:]
    # Maxな行の場合、先頭を削る（Max-1の行
    if len(sensor_values_list) >= max_row:
        update_sensor_values_list = sensor_values_list[1:]

    # 新しい行を末尾に追加
    add_line_str = f"{recode_datetime},{temperature},{relative_humidity},{pressure}"
    update_sensor_values_list.append(add_line_str)
    # ファイルを保存
    with SENSOR_VALUES_FILE.open("w", encoding="utf-8") as sensor_values_file:
        sensor_values_file.writelines(sensor_values_list)

    # pass

def latest_sensor_values(sensor_values, now_datetime):
    """現在のセンサー値を描写する。"""
    
    # TODO:2020-11-24 ここは時間以外はオプション的な扱いにして、列ヘッダを見て設定できるととてもいい
    #    時間だけは絶対に必要にして、その列がない場合は例外を出して終了する
    latest_datetime = now_datetime
    latest_temperature = sensor_values[0]
    latest_pressure = sensor_values[1]
    latest_humidity = sensor_values[2]

    return html.Div(
        [
            html.Div(
                [
                    html.H6(f"気温: {latest_temperature}℃"),
                    html.H6(f"湿度: {latest_humidity}%"),
                    html.H6(f"気圧: {latest_pressure}hPa"),
                ],
                body=True,
            ),
            html.Label(f"更新時間 :{latest_datetime}"),
        ],
        id="latest_values",
    )


def sensor_graphs():
    """過去に記録したセンサー情報の値をグラフにする"""
    pass


def generate_sensors_df():
    """グラフを描写するためのDataframeを用意する"""
    pass


def _layout():
    """全体のレイアウト構成とインターバル設定を行う"""

    now_dt_str = datetime.datetime.now().isoformat()
    sensor_values = get_sensor_values()

    return html.Div(
        [
            dcc.Location(id="url", refresh=False),
            html.H2(app.title),
            html.Hr(),
            # 現在の値を取得
            latest_sensor_values(sensor_values, now_dt_str ),
            # 温度、湿度、気圧のグラフ（だけ）

            # dcc.Interval(
            #     id="interval-component",
            #     interval=10 * 60 * 1000,  # in milliseconds
            #     n_intervals=0,
            # ),
        ],
    )


# 自動リロードとドロップダウンリストでのコールバック
@app.callback(
    [
        Output("latest_values", "children"),
        Output("graphs", "children"),
    ],
    [
        Input("interval-component", "n_intervals")
    ],
)
def update_sensor_values(n):
    # now = datetime.datetime.now().astimezone()
    # print(f"リロード時間:{now} 日付:{date_dd_value} 場所:{location_dd_value}")

    # センサーの情報を取得
    # TODO: 2021/10/07 この先の処理には穴があります。スクリプトを起動している状態でないと値の記録が行えないため、
    # BME280のセンサー情報を定量的に保存したい場合はセンサー記録用のスクリプトを用意すると良いでしょう。

    # 今回は機能紹介のために一つのスクリプトにまとめています。


    # 計測時の時間
    # TODO: 2021/10/07 タイムゾーン何も考えていないので注意
    now_dt_str = datetime.datetime.now().isoformat()

    sensor_values = (temperature, relative_humidity, pressure)

    # 現在の値をCSVファイルへ保存
    save_sensor_values(sensor_values, now_dt_str)


    # 過去に記録された値をグラフで表示
    # sensor_df = generate_df(location_dd_value, date_dd_value)
    latest_values = generate_latest_view(sensor_df)
    # graphs = generate_graph_tabs(sensor_df)

    return graphs


if __name__ == "__main__":

    app.layout = _layout
    app.run_server(debug=True, host="0.0.0.0")
