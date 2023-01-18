# distracted_driver_detection
Academic Project to detect distracted drivers on the basis of their actions while driving
import numpy as np
import pandas as pd
import more_itertools as mit
import re
import zipfile
import os
import time

import streamlit as st
from plotly.subplots import make_subplots
import plotly.graph_objects as go


df = pd.read_csv('d.csv')
dock = pd.read_csv('dock1.csv')
zones = pd.read_csv('zones1.csv')


# Dropdown for selecting ID
id = st.selectbox('Select an ID', sorted(df['ACTIONBLOCKID'].unique()), index = 0)
df = df[(df['ACTIONBLOCKID'] == id)]

col1, col2, col3 = st.columns([1.85,7.5, 1.4])

show_circles = st.checkbox('Show Circles', value = True)
show_rectangle = st.checkbox('Show rectangle', value = True)

plot_placeholder = col2.empty()

def buffer(min, max):
        diff = max - min
        if diff > 100:
                return 0
        else: return (100 - diff)/2

def circle(df, X, Y, fig, radius = 30):

    df['X0'] = df[X] - radius
    df['Y0'] = df[Y] - radius
    df['X1'] = df[X] + radius
    df['Y1'] = df[Y] + radius

    for row in range(len(df)):
        fig.add_shape(
            type = 'circle', xref = 'x', yref = 'y', 
            x0 = df['X0'][row],
            y0 = df['Y0'][row],
            x1 = df['X1'][row],
            y1 = df['Y1'][row],
            line = dict(color = '#A9A9A9', width = 1, dash = 'longdashdot')
        )

def route_plot(dock, zones):

    fig = make_subplots(
            shared_xaxes = True, 
            shared_yaxes = True, 
            figure = go.Figure(
                    layout = go.Layout(
                            yaxis = dict(scaleanchor = 'x', scaleratio = 0.95, tick0 = 119, dtick = 25, showticklabels = False),
                            xaxis = dict(tick0 = 96.7, dtick = 48, showticklabels = False),
                            height = 600, 
                            # title = dict(text = '<br>'.join(textwrap.wrap('<b>' + title + '</b>', width = 100)), font = dict(size = 17)), title_x = 0.5,  
                            legend = dict(yanchor ='bottom', xanchor ='left', orientation = 'h', x = 0, y = 1),
                            margin = dict(l=20, r=20, t=20, b=20),
                            # plot_bgcolor = 'rgb(10,10,10)'
                    )
            )
    )

    fig.add_trace(
        go.Scatter(
            name = 'Dock', x = dock['CENTER_X'], y = dock['CENTER_Y'], 
            mode = 'text', 
            text = dock['ZONE'], textfont = dict(color = '#C1CDCD', size = 12), textposition = 'middle center', 
            showlegend = False, #textfont = dict(size = 12)
        )
    )


    if show_circles:
        startloc = ', '.join(df['STARTLOC_CIRCLE'].dropna().unique()).split(', ')
        startloc = pd.DataFrame(pd.Series(startloc, name = 'STARTLOC')).drop_duplicates()
        startloc = startloc.merge(zones[['LOC', 'LOC_X', 'LOC_Y']], left_on = 'STARTLOC', right_on = 'LOC')
        circle(startloc, 'LOC_X', 'LOC_Y', fig)

        endloc = ', '.join(df['ENDLOC_CIRCLE'].dropna().unique()).split(', ')
        endloc = pd.DataFrame(pd.Series(endloc, name = 'ENDLOC')).drop_duplicates()
        endloc = endloc.merge(zones[['LOC', 'LOC_X', 'LOC_Y']], left_on = 'ENDLOC', right_on = 'LOC')
        circle(endloc, 'LOC_X', 'LOC_Y', fig)

    plot = plot_placeholder.plotly_chart(fig, use_container_width = True, theme = None)

    plot = plot_placeholder.plotly_chart(fig, use_container_width = True, theme = None)

# Plotting Full Route
route_plot(dock, zones)
