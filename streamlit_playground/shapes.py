# streamlit app that draws shapes on a canvas based on matplotlib
import math

import streamlit as st
import matplotlib.pyplot as plt

MAX_EXTENT = 100
COLOR = 'r'


def create_canvas():
    fig, ax = plt.subplots()
    ax.autoscale()
    ax.set_ylim(-MAX_EXTENT, MAX_EXTENT)
    ax.set_xlim(-MAX_EXTENT, MAX_EXTENT)
    ax.grid(True)
    return fig, ax


def add_circle_to_canvas(ax, x, y, radius, steps):
    xs = []
    ys = []
    for i in range(steps):
        x = radius * math.cos(2 * math.pi / steps * i)
        y = radius * math.sin(2 * math.pi / steps * i)
        xs.append(x)
        ys.append(y)
    # add the first point to close the circle
    xs.append(xs[0])
    ys.append(ys[0])
    ax.plot(xs, ys, color=COLOR)


def add_rectangle_to_canvas(ax, width, height):
    rectangle = plt.Rectangle((-width/2, -height/2), width, height, edgecolor=COLOR, facecolor="none")
    ax.add_artist(rectangle)


def add_triangle_to_canvas(ax, base, height):
    triangle = plt.Polygon([(-base/2, -height/2), (base/2, -height/2), (0, height/2)], edgecolor=COLOR, facecolor="none")
    ax.add_artist(triangle)


def add_rhombe_to_canvas(ax, width, height):
    rhombe = plt.Polygon([(-width/2, 0), (0, -height/2), (width/2, 0), (0, height/2)], edgecolor=COLOR, facecolor="none")
    ax.add_artist(rhombe)


def add_trapesoid_to_canvas(ax, base1, base2, height):
    trapezoid = plt.Polygon([(-base1/2, -height/2), (base1/2, -height/2), (base2/2, height/2), (-base2/2, height/2)], edgecolor=COLOR, facecolor="none")
    ax.add_artist(trapezoid)


st.title('Shapes')

shape = st.selectbox('Select a shape', ['Circle', 'Rectangle', 'Triangle', 'Rhombe', 'Trapesoid'])

# canvas
fig, ax = create_canvas()

if shape == 'Circle':
    radius = st.slider('Radius', 1, MAX_EXTENT, 10)
    steps = st.slider('Steps', 3, 100, 50)
    ax = add_circle_to_canvas(ax, 0, 0, radius, steps)
elif shape == 'Rectangle':
    width = st.slider('Width', 1, 100, 10)
    height = st.slider('Height', 1, 100, 10)
    ax = add_rectangle_to_canvas(ax, width, height)
elif shape == 'Triangle':
    base = st.slider('Base', 1, 100, 10)
    height = st.slider('Height', 1, 100, 10)
    ax = add_triangle_to_canvas(ax, base, height)
elif shape == 'Rhombe':
    width = st.slider('Width', 1, 100, 10)
    height = st.slider('Height', 1, 100, 10)
    ax = add_rhombe_to_canvas(ax, width, height)
elif shape == 'Trapesoid':
    base1 = st.slider('Base 1', 1, 100, 10)
    base2 = st.slider('Base 2', 1, 100, 10)
    height = st.slider('Height', 1, 100, 10)
    ax = add_trapesoid_to_canvas(ax, base1, base2, height)
else:
    raise KeyError('Invalid shape')

st.pyplot(fig)
