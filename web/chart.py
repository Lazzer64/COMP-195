from collections import namedtuple
from random import sample

Color = namedtuple('Point', ['r', 'g', 'b'])
red    = Color(255, 99, 132)
blue   = Color(54, 162, 235)
yellow = Color(255, 206, 86)
green  = Color(75, 192, 192)
purple = Color(153, 102, 255)
orange = Color(255, 159, 64)


def _data(labels, title, colors, borders, data):
    return {"labels": labels,
            "datasets": [{
                "label": title,
                "backgroundColor": colors,
                "borderColor": borders,
                "borderWidth": 1,
                "data": data}]}


def _random_colors(num, opacity=1):
    colors = [red, blue, yellow, green, purple, orange] * int(1 + num / num)
    return [f"rgba({c.r}, {c.g}, {c.b}, {opacity})" for c in colors][:num]


def _base(title, labels, data, *, colors=None, borders=None):
    colors = colors if colors is not None else _random_colors(len(labels), 0.4)
    borders = borders if borders is not None else _random_colors(len(labels), 1)
    return {"data": _data(labels, title, colors, borders, data), "options": {}}


def bar(*args, **kwargs):
    chart = _base(*args, **kwargs)
    chart["type"] = 'bar'
    chart["options"]["scales"] = {"yAxes": [{"ticks": {"beginAtZero": True}}]}
    return chart


def line(*args, **kwargs):
    chart = _base(*args, **kwargs)
    chart["type"] = 'line'
    chart["options"]["scales"] = {"yAxes": [{"ticks": {"beginAtZero": True}}]}
    return chart


def random(func):
    labels = ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange']
    data = sample(range(1, 7), 6)
    return func("# of votes", labels, data)
