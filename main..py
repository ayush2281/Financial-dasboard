import math
import datetime as dt

import day
import numpy as np
import yfinance as yf

from bokeh.io import curdoc
from bokeh.plotting import figure

from bokeh.layouts import row, column
from bokeh.models import TextInput, Button, DatePicker, MultiChoice  # Corrected import

def load_data(ticker1, ticker2, start, end):
    df1 = yf.download(ticker1, start, end)
    df2 = yf.download(ticker2, start, end)
    return df1, df2


def plot_data(data, indicators, sync_axis=None):
    df = data
    gain = df.Close > df.Open
    loss = df.Open> df.Close
    width = 12 * 60 * 60 * 1000

    if sync_axis is not None:
        p = figure(x_axis_type="datetime", tools="pan, wheel_zoom,boc_zoom,rest,save", width=1000,
                   x_range=sync_axis)
    else:
        p= figure(x_axis_type="datetime", tools="pan, wheel_zoom,boc_zoom,rest,save", width=1000)

    p.xaxis.major_label_orientation = math.pi / 4
    p.grid.grid_line_alpha = 0.25
    p.segment(df.index, df.High, df.index, df.Low, color="black")
    p.vbar(df.index[gain], width, df.open[gain], df.Close[gain], fill_color="#00ff00", line_clor="#00ff00")
    p.vbar(df.index[loss], width, df.open[loss], df.Close[loss], fill_color="#ff0000", line_clor="#ff0000")

    return p
def on_button_click(ticker1, ticker2, start, end, indicator):
    df1, df2 = load_data(ticker1, ticker2, start, end)
    p1 = plot_data(df1, indicator)
    p2 = plot_data(df2, indicator, sync_axis=p1.x_range)
    curdoc().clear()
    curdoc().add_root(layout)
    curdoc().add_root(row(p1, p2))
stock1_text = TextInput(title="Stock 1")
stock2_text = TextInput(title="Stock 2")
date_picker_from = DatePicker(title="Start Date", value="2024-02-17", min_date="2005-01-01",
                              max_date=dt.datetime.now().strftime("%Y-%m-%d"))

date_picker_to = DatePicker(title="End Date", value="2024-02-17", min_date="2005-01-01",
                              max_date=dt.datetime.now().strftime("%Y-%m-%d"))

indicator_choice = MultiChoice(options=["100 Day SMA", "30 Day SMA", "linear Regression Line"])

load_button = Button(label="Load Data", button_type="success")
load_button.on_click(lambda: on_button_click(stock1_text.value, stock2_text.value,
                                             date_picker_from.value, date_picker_to.value,
                                             indicator_choice.value))
layout = column(stock1_text, stock2_text, date_picker_from, date_picker_to, indicator_choice, load_button)


curdoc().clear()
curdoc().add_root(layout)