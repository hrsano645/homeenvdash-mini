from dash import Dash, callback, html, dcc, Input, Output

# dashアプリの初期化
app = Dash(
    __name__,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
)
app.title = "Hello Dash Callback"


def _layout():
    return html.Div(
        [
            html.H1(app.title),
            html.Hr(),
            html.P("文字を入力すると、出力の部分が更新されます"),
            html.Div(
                [
                    html.Span("入力: "),
                    dcc.Input(id="input-form", value="Callbackを試しています", type="text"),
                ]
            ),
            html.P(id="output-p", style={"background-color": "#ddd"}),
        ]
    )


@app.callback(Output("output-p", "children"), Input("input-form", "value"))
def update_output_text(input_value):
    # 引数がInputのvalueの値を取得
    # return側に更新したいコンポーネントを指定する。childrenは指定コンポーネントの子要素の事
    return f"出力: {input_value}"


if __name__ == "__main__":
    app.layout = _layout
    app.run_server(debug=True, host="0.0.0.0")
