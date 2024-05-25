from django.shortcuts import render, redirect 
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import plotly
from .models import *
from .forms import MapBounds
import pathlib
import pandas as pd 
import numpy as np 
import rasterio
import requests
import plotly.graph_objects as go
import os
import tempfile
import json


# def demplot(south, north, east, west, api_key):
#     url = f'https://portal.opentopography.org/API/globaldem?demtype=SRTMGL3&south={south}&north={north}&west={west}&east={east}&outputFormat=GTiff&API_Key={api_key}'
#     response = requests.get(url)
    
#     if response.status_code == 200:
#         with tempfile.NamedTemporaryFile(delete=False, suffix='.tif') as tmp_file:
#             tmp_file.write(response.content)
#             tmp_file_path = tmp_file.name

#         with rasterio.open(tmp_file_path) as src:
#             elev = src.read(1)
#             bounds = src.bounds
#             transform = src.transform

#         nrows, ncols = elev.shape

#         mid_latitude = (south + north) / 2.0
#         m_per_deg_lat = 111320  # meters per degree latitude
#         m_per_deg_lon = m_per_deg_lat * np.cos(np.radians(mid_latitude))  # meters per degree longitude

#         x_range_m = (east - west) * m_per_deg_lon  # Convert longitudinal range to meters
#         y_range_m = (north - south) * m_per_deg_lat  # Convert latitudinal range to meters
#         x_coords, y_coords = np.meshgrid(np.arange(ncols), np.arange(nrows))
#         x_geo, y_geo = rasterio.transform.xy(transform, y_coords.flatten(), x_coords.flatten())
#         x_geo = np.array(x_geo).reshape(nrows, ncols)
#         y_geo = np.array(y_geo).reshape(nrows, ncols)
#         z_min, z_max = elev.min(), elev.max()
#         z_range_m = z_max - z_min

#         fig = go.Figure(data=[go.Surface(z=elev, x=x_geo, y=y_geo)])
#         max_range = np.array([x_range_m, y_range_m, z_range_m]).max()
#         aspect_ratio = dict(
#             x=x_range_m / max_range,
#             y=y_range_m / max_range,
#             z=z_range_m / max_range
#         )
#         fig.update_layout(
#             scene=dict(
#                 aspectmode='manual',
#                 aspectratio=aspect_ratio,
#                 zaxis=dict(nticks=4, range=[z_min, z_max]),
#                 camera=dict(eye=dict(x=0.75, y=0.75, z=0.75)),
#                 xaxis_title='Longitude',
#                 yaxis_title='Latitude',
#                 zaxis_title='Elevation (m)'
#             ),
#             title='3D Terrain Visualization - Actual Elevation Scale',
#             autosize=True,
#         )
#         # pcloud = json.dumps(fig.to_dict(), cls=plotly.utils.PlotlyJSONEncoder)
#         pcloud = fig.to_html(full_html=False, include_plotlyjs='cdn')
#         os.remove(tmp_file_path)
#         return pcloud
#     else:
#         raise Exception(f"Failed to fetch data: {response.status_code}")



# def demplot ():
#     z1 = np.array([
#         [8.83,8.89,8.81,8.87,8.9,8.87],
#         [8.89,8.94,8.85,8.94,8.96,8.92],
#         [8.84,8.9,8.82,8.92,8.93,8.91],
#         [8.79,8.85,8.79,8.9,8.94,8.92],
#         [8.79,8.88,8.81,8.9,8.95,8.92],
#         [8.8,8.82,8.78,8.91,8.94,8.92],
#         [8.75,8.78,8.77,8.91,8.95,8.92],
#         [8.8,8.8,8.77,8.91,8.95,8.94],
#         [8.74,8.81,8.76,8.93,8.98,8.99],
#         [8.89,8.99,8.92,9.1,9.13,9.11],
#         [8.97,8.97,8.91,9.09,9.11,9.11],
#         [9.04,9.08,9.05,9.25,9.28,9.27],
#         [9,9.01,9,9.2,9.23,9.2],
#         [8.99,8.99,8.98,9.18,9.2,9.19],
#         [8.93,8.97,8.97,9.18,9.2,9.18]
#     ])

#     z2 = z1 + 1
#     z3 = z1 - 1

#     fig = go.Figure(data=[
#         go.Surface(z=z1),
#         go.Surface(z=z2, showscale=False, opacity=0.9),
#         go.Surface(z=z3, showscale=False, opacity=0.9)

#     ])

#     pcloud = fig.to_html(full_html=False, include_plotlyjs='cdn')
#     return pcloud

def demplot(south, north, east, west, api_key):
    print(f"Starting demplot with bounds: south={south}, north={north}, east={east}, west={west}")
    url = f'https://portal.opentopography.org/API/globaldem?demtype=SRTMGL3&south={south}&north={north}&west={west}&east={east}&outputFormat=GTiff&API_Key={api_key}'
    print(f"Requesting data from URL: {url}")
    response = requests.get(url)
    
    if response.status_code == 200:
        print("Data fetched successfully from API")
        with tempfile.NamedTemporaryFile(delete=False, suffix='.tif') as tmp_file:
            tmp_file.write(response.content)
            tmp_file_path = tmp_file.name
            print(f"Temporary file created at {tmp_file_path}")

        with rasterio.open(tmp_file_path) as src:
            elev = src.read(1)
            bounds = src.bounds
            transform = src.transform
            print(f"Elevation data read with bounds: {bounds} and transform: {transform}")

        nrows, ncols = elev.shape
        print(f"Elevation data shape: {nrows}x{ncols}")

        mid_latitude = (south + north) / 2.0
        m_per_deg_lat = 111320  # meters per degree latitude
        m_per_deg_lon = m_per_deg_lat * np.cos(np.radians(mid_latitude))  # meters per degree longitude

        x_range_m = (east - west) * m_per_deg_lon  # Convert longitudinal range to meters
        y_range_m = (north - south) * m_per_deg_lat  # Convert latitudinal range to meters
        x_coords, y_coords = np.meshgrid(np.arange(ncols), np.arange(nrows))
        x_geo, y_geo = rasterio.transform.xy(transform, y_coords.flatten(), x_coords.flatten())
        x_geo = np.array(x_geo).reshape(nrows, ncols)
        y_geo = np.array(y_geo).reshape(nrows, ncols)
        z_min, z_max = elev.min(), elev.max()
        z_range_m = z_max - z_min

        fig = go.Figure(data=[go.Surface(z=elev, x=x_geo, y=y_geo)])
        max_range = np.array([x_range_m, y_range_m, z_range_m]).max()
        aspect_ratio = dict(
            x=x_range_m / max_range,
            y=y_range_m / max_range,
            z=z_range_m / max_range
        )
        fig.update_layout(
            scene=dict(
                aspectmode='manual',
                aspectratio=aspect_ratio,
                zaxis=dict(nticks=4, range=[z_min, z_max]),
                camera=dict(eye=dict(x=0.75, y=0.75, z=0.75)),
                xaxis_title='Longitude',
                yaxis_title='Latitude',
                zaxis_title='Elevation (m)'
            ),
            title='3D Terrain Visualization - Actual Elevation Scale',
            autosize=True,
        )
        print("Plot generated successfully")
        # pcloud = json.dumps(fig.to_dict(), cls=plotly.utils.PlotlyJSONEncoder)
        pcloud = fig.to_html(full_html=False, include_plotlyjs='cdn')
        os.remove(tmp_file_path)
        print(f"Temporary file {tmp_file_path} removed")
        return pcloud
    else:
        error_msg = f"Failed to fetch data: {response.status_code}"
        print(error_msg)
        raise Exception(error_msg)