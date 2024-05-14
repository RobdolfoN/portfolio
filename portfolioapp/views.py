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





# Create your views here.


def home_view(request):
    context={}
    return render(request, "portfolioapp/pages/home.html", context)

def dashboard(request):
    context={}
    return render(request, "portfolioapp/pages/dashboard.html", context)

def ecozlounge(request):
    context={}
    return render(request, "portfolioapp/pages/ecozlounge.html", context)

# def bba(request):

#     if request.method == 'POST':
#         form = MapBounds(request.POST)
#         if form.is_valid():
#             south = float(form.cleaned_data['south'])
#             north = float(form.cleaned_data['north'])
#             east = float(form.cleaned_data['east'])
#             west = float(form.cleaned_data['west'])
#             xbounds = [south,south,north,north]
#             ybounds = [east,west,east,west]
#             df = pd.DataFrame(data={'lat':xbounds, 'lon':ybounds})
            
            
#             url = 'https://portal.opentopography.org/API/globaldem?demtype=SRTMGL3&south='+south+'&north='+north+'&west='+west+'&east='+east+'&outputFormat=GTiff&API_Key=5daa4b13bf7dd16f19717383e030f4a1'
#             response = requests.get(url)
#             open('raster.tif','wb').write(response.content)

#             with rasterio.open (response) as src:
#                 elev = src.read()
#             nrows, ncols = elev.shape
#             x, y = np.meshgrid(np.arange(ncols), np.arange(nrows))
#             z = elev
#             mesh = mlab.mesh(x, y, z)
#             pcloud = mlab.show()





#     context={'map':map, 'pcloud':pcloud}
#     return render(request, "portfolioapp/pages/bba.html", context)



# def bba(request):
#     pcloud = None  # Initialize pcloud to None

#     if request.method == 'POST':
#         form = MapBounds(request.POST)
#         if form.is_valid():
#             south = form.cleaned_data['south']
#             north = form.cleaned_data['north']
#             east = form.cleaned_data['east']
#             west = form.cleaned_data['west']

#             # API call to download the DEM file
#             # api_key = '5daa4b13bf7dd16f19717383e030f4a1'  # It's better to store API keys in environment variables or Django settings
#             # url = f'https://portal.opentopography.org/API/globaldem?demtype=SRTMGL3&south='+south+'&north='+north+'&west='+west+'&east='+east+'&outputFormat=GTiff&API_Key=5daa4b13bf7dd16f19717383e030f4a1'
#             url = 'https://portal.opentopography.org/API/globaldem?demtype=SRTMGL3&south=50&north=50.1&west=14.35&east=14.6&outputFormat=GTiff&API_Key=5daa4b13bf7dd16f19717383e030f4a1'
#             response = requests.get(url)
#             if response.status_code == 200:
#                 raster_file = response
                

#                 # Read the raster file
#                 with rasterio.open(raster_file) as src:
#                     elev = src.read(1)  # Read the first band

#                 nrows, ncols = elev.shape
#                 x = np.linspace(0, ncols - 1, ncols)
#                 y = np.linspace(0, nrows - 1, nrows)
#                 x, y = np.meshgrid(x, y)

#                 # Create a Plotly figure
#                 fig = go.Figure(data=[go.Surface(z=elev, x=x, y=y)])
#                 fig.update_layout(title='3D Terrain Visualization', autosize=True)

#                 # Convert the Plotly figure to HTML and include it in the context
#                 pcloud = fig.to_html(full_html=False, include_plotlyjs='cdn')
#             else:
#                 print("Failed to fetch data:", response.status_code)

#     context = {'pcloud': pcloud}
#     return render(request, "portfolioapp/pages/bba.html", context)





# def bba(request):
#     pcloud = None

#     if request.method == 'POST':
#         form = MapBounds(request.POST)
#         if form.is_valid():
#             south = form.cleaned_data['south']
#             north = form.cleaned_data['north']
#             east = form.cleaned_data['east']
#             west = form.cleaned_data['west']

#             url = 'https://portal.opentopography.org/API/globaldem?demtype=SRTMGL3&south=48.779870&north=48.780680&west=-123.504334&east=-123.503104&outputFormat=GTiff&API_Key=5daa4b13bf7dd16f19717383e030f4a1'
#             response = requests.get(url)
#             if response.status_code == 200:
#                 # Use a temporary file to save the response content
#                 with tempfile.NamedTemporaryFile(delete=False, suffix='.tif') as tmp_file:
#                     tmp_file.write(response.content)
#                     tmp_file_path = tmp_file.name

#                 # Read the raster file
#                 with rasterio.open(tmp_file_path) as src:
#                     elev = src.read(1)  # Read the first band

#                 # Process elevation data...
#                 x = np.linspace(0, src.width - 1, src.width).tolist()
#                 y = np.linspace(0, src.height - 1, src.height).tolist()
#                 z = elev.tolist()

#                 # Create a Plotly figure
#                 fig = go.Figure(data=[go.Surface(z=elev, x=x, y=y)])
#                 fig.update_layout(title='3D Terrain Visualization', autosize=True)

#                 # Convert the Plotly figure to HTML and include it in the context
#                 pcloud = fig.to_html(full_html=False, include_plotlyjs='cdn')
                

#                 # Remove the temporary file
#                 os.remove(tmp_file_path)
#             else:
#                 print("Failed to fetch data:", response.status_code)

#     context = {'pcloud': pcloud}
#     return render(request, "portfolioapp/pages/bba.html", context)



# def bba(request):
#     pcloud_html = None
#     pcloud_json = None

#     if request.method == 'POST':
#         # Load JSON data from the request
#         data = json.loads(request.body)
#         south = data['south']
#         north = data['north']
#         east = data['east']
#         west = data['west']

#         # Construct the API URL with the provided bounds
#         url = f'https://portal.opentopography.org/API/globaldem?demtype=SRTMGL3&south={south}&north={north}&west={west}&east={east}&outputFormat=GTiff&API_Key==5daa4b13bf7dd16f19717383e030f4a1'

#         response = requests.get(url)
#         if response.status_code == 200:
#             # Use a temporary file to save the response content
#             with tempfile.NamedTemporaryFile(delete=False, suffix='.tif') as tmp_file:
#                 tmp_file.write(response.content)
#                 tmp_file_path = tmp_file.name

#             # Read the raster file
#             with rasterio.open(tmp_file_path) as src:
#                 elev = src.read(1)  # Read the first band

#             # Process elevation data...
#             nrows, ncols = elev.shape
#             x = np.linspace(0, ncols - 1, ncols)
#             y = np.linspace(0, nrows - 1, nrows)
#             x, y = np.meshgrid(x, y)

#             # Create a Plotly figure
#             fig = go.Figure(data=[go.Surface(z=elev, x=x, y=y)])
#             fig.update_layout(title='3D Terrain Visualization', autosize=True)

#             # Convert the Plotly figure to JSON
#             pcloud_json = fig.to_json()

#             # Convert the Plotly figure to HTML for embedding
#             pcloud_html = fig.to_html(full_html=False, include_plotlyjs='cdn')

#             # Remove the temporary file
#             os.remove(tmp_file_path)
#         else:
#             print("Failed to fetch data:", response.status_code)

#         # If the request is AJAX, return the JSON representation of the plot
#         if request.headers.get('x-requested-with') == 'XMLHttpRequest':
#             return JsonResponse({'pcloud': pcloud_json}, safe=False)

#     # If it's not an AJAX request, continue to render the page normally
#     context = {'pcloud': pcloud_html}
#     return render(request, "portfolioapp/pages/bba.html", context)




# def bba(request):
#     if request.method == 'POST':
#         try:
#             data = json.loads(request.body.decode('utf-8'))  # Properly decode the JSON from the request body
#             south = data['south']
#             north = data['north']
#             east = data['east']
#             west = data['west']

#             url = f'https://portal.opentopography.org/API/globaldem?demtype=SRTMGL3&south=48.76961524181706&north=48.78961524181706&west=-123.51468313303894&east=-123.49468313303894&outputFormat=GTiff&API_Key=5daa4b13bf7dd16f19717383e030f4a1'

#             response = requests.get(url)
#             if response.status_code == 200:
#                 with tempfile.NamedTemporaryFile(delete=True, suffix='.tif') as tmp_file:
#                     tmp_file.write(response.content)
#                     tmp_file_path = tmp_file.name

#                 with rasterio.open(tmp_file_path) as src:
#                     elev = src.read(1)

#                 x = np.linspace(0, src.width - 1, src.width).tolist()
#                 y = np.linspace(0, src.height - 1, src.height).tolist()
#                 z = elev.tolist()

#                 fig = go.Figure(data=[go.Surface(z=z, x=x, y=y)])
#                 fig.update_layout(title='3D Terrain Visualization', autosize=True)

#                 pcloud_html = fig.to_html(full_html=False, include_plotlyjs='cdn')
#                 return JsonResponse({'pcloud_html': pcloud_html})

#             else:
#                 return JsonResponse({'error': 'Failed to fetch DEM data', 'status_code': response.status_code}, status=500)

#         except json.JSONDecodeError:
#             return JsonResponse({'error': 'Malformed data received'}, status=400)
#         except KeyError:
#             return JsonResponse({'error': 'Missing data fields'}, status=400)
#         except Exception as e:
#             return JsonResponse({'error': str(e)}, status=500)

#     else:
#         # If it's not a POST request, just render the page normally
#         return render(request, "portfolioapp/pages/bba.html")



######################### view working ###########################



# def bba(request):
#     pcloud = None

#     if request.method == 'POST':
#         form = MapBounds(request.POST)
#         if form.is_valid():
#             south = float(form.cleaned_data['south'])
#             north = float(form.cleaned_data['north'])
#             east = float(form.cleaned_data['east'])
#             west = float(form.cleaned_data['west'])

#             url = f'https://portal.opentopography.org/API/globaldem?demtype=SRTMGL3&south={south}&north={north}&west={west}&east={east}&outputFormat=GTiff&API_Key=5daa4b13bf7dd16f19717383e030f4a1'
#             response = requests.get(url)
#             if response.status_code == 200:
#                 # Use a temporary file to save the response content
#                 with tempfile.NamedTemporaryFile(delete=False, suffix='.tif') as tmp_file:
#                     tmp_file.write(response.content)
#                     tmp_file_path = tmp_file.name

#                 # Read the raster file
#                 with rasterio.open(tmp_file_path) as src:
#                     elev = src.read(1)  # Read the first band

                

#                 nrows, ncols = elev.shape
                
#                 x, y = np.meshgrid(np.arange(ncols), np.arange(nrows))

#                 # Create a Plotly figure
#                 fig = go.Figure(data=[go.Surface(z=elev, x=x, y=y)])
#                 fig.update_layout(title='3D Terrain Visualization', autosize=False, width=800, height=800)

#                 # Convert the Plotly figure to HTML and include it in the context
#                 pcloud = fig.to_html(full_html=False, include_plotlyjs='cdn')
                

#                 # Remove the temporary file
#                 os.remove(tmp_file_path)
#             else:
#                 print("Failed to fetch data:", response.status_code)

#     context = {'pcloud': pcloud}
#     return render(request, "portfolioapp/pages/bba.html", context)




#################################### aspect ratio adjusted #######################33


# south = float(50)
# north = float(50.5)
# east = float(-90)
# west = float(-91)

# url = f'https://portal.opentopography.org/API/globaldem?demtype=SRTMGL3&south={south}&north={north}&west={west}&east={east}&outputFormat=GTiff&API_Key=5daa4b13bf7dd16f19717383e030f4a1'

# # %%
# response = requests.get(url)

# # %%
# with tempfile.NamedTemporaryFile(delete=False, suffix='.tif') as tmp_file:
#                     tmp_file.write(response.content)
#                     tmp_file_path = tmp_file.name

# # %%
# with rasterio.open(tmp_file_path) as src:
#                     bounds = src.bounds
#                     elev = src.read(1)
#                     transform = src.transform

# # %%
# # Convert the bounds to actual ranges in meters using a rough conversion factor.
# mid_latitude = (south + north) / 2.0
# m_per_deg_lat = 111320  # meters per degree latitude
# m_per_deg_lon = m_per_deg_lat * np.cos(np.radians(mid_latitude))  # meters per degree longitude

# # %%
# x_range_m = (east - west) * m_per_deg_lon  # Convert longitudinal range to meters
# y_range_m = (north - south) * m_per_deg_lat  # Convert latitudinal range to meters

# # %%
# x_coords, y_coords = np.meshgrid(np.arange(ncols), np.arange(nrows))
# x_geo, y_geo = rasterio.transform.xy(transform, y_coords.flatten(), x_coords.flatten())
# x_geo = np.array(x_geo).reshape(nrows, ncols)
# y_geo = np.array(y_geo).reshape(nrows, ncols)
# # Calculate the elevation range in meters
# z_min, z_max = elev.min(), elev.max()
# z_range_m = z_max - z_min

# # %%
# # Plot with plotly
# fig = go.Figure(data=[go.Surface(z=elev, x=x_geo, y=y_geo)])

# # Update the aspect ratio to reflect real-world distances
# max_range = np.array([x_range_m, y_range_m, z_range_m]).max()
# aspect_ratio = dict(
#     x=x_range_m / max_range,
#     y=y_range_m / max_range,
#     z=z_range_m / max_range
# )

# fig.update_layout(
#     scene=dict(
#         aspectmode='manual',
#         aspectratio=aspect_ratio,
#         zaxis=dict(nticks=4, range=[z_min, z_max]),
#         xaxis_title='Longitude',
#         yaxis_title='Latitude',
#         zaxis_title='Elevation (m)'
#     ),
#     title='3D Terrain Visualization - Actual Elevation Scale',
#     autosize=False,
#     width=800,
#     height=800
# )

# # Show figure
# fig.show()

# # %%



##############################################################################################



def dem(request):
    # pcloud = None

    if request.method == 'POST':
        form = MapBounds(request.POST)
        if form.is_valid():
            south = float(form.cleaned_data['south'])
            north = float(form.cleaned_data['north'])
            east = float(form.cleaned_data['east'])
            west = float(form.cleaned_data['west'])
            api_key = os.environ.get('TOPO_API_key')
            

            url = f'https://portal.opentopography.org/API/globaldem?demtype=SRTMGL3&south={south}&north={north}&west={west}&east={east}&outputFormat=GTiff&API_Key={api_key}'
            response = requests.get(url)
            if response.status_code == 200:
                # Use a temporary file to save the response content
                with tempfile.NamedTemporaryFile(delete=False, suffix='.tif') as tmp_file:
                    tmp_file.write(response.content)
                    tmp_file_path = tmp_file.name

                # Read the raster file
                with rasterio.open(tmp_file_path) as src:
                    elev = src.read(1)
                    bounds = src.bounds
                    transform = src.transform 
                
                nrows, ncols = elev.shape

                

                # # Convert the bounds to actual ranges in meters using a rough conversion factor.
                mid_latitude = (south + north) / 2.0
                m_per_deg_lat = 111320  # meters per degree latitude
                m_per_deg_lon = m_per_deg_lat * np.cos(np.radians(mid_latitude))  # meters per degree longitude
                
                x_range_m = (east - west) * m_per_deg_lon  # Convert longitudinal range to meters
                y_range_m = (north - south) * m_per_deg_lat  # Convert latitudinal range to meters
                x_coords, y_coords = np.meshgrid(np.arange(ncols), np.arange(nrows))
                x_geo, y_geo = rasterio.transform.xy(transform, y_coords.flatten(), x_coords.flatten())
                x_geo = np.array(x_geo).reshape(nrows, ncols)
                y_geo = np.array(y_geo).reshape(nrows, ncols)
                # Calculate the elevation range in meters
                z_min, z_max = elev.min(), elev.max()
                z_range_m = z_max - z_min

                # Create a Plotly figure
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
                        camera=dict(
                            eye=dict(x=0.75, y=0.75, z=0.75)  # Use smaller values to zoom in
                        ),
                        xaxis_title='Longitude',
                        yaxis_title='Latitude',
                        zaxis_title='Elevation (m)'
                    ),
                    title='3D Terrain Visualization - Actual Elevation Scale',
                    autosize=False,
                    # width=1200,
                    # height=500
                )
                # Convert the Plotly figure to JSON
                pcloud = json.dumps(fig.to_dict(), cls=plotly.utils.PlotlyJSONEncoder)
                # pcloud = fig.to_html(full_html=False, include_plotlyjs='cdn')
                

                # Remove the temporary file
                os.remove(tmp_file_path)
            else:
                print("Failed to fetch data:", response.status_code)

    context = {'pcloud': pcloud}
    return render(request, "portfolioapp/pages/dem.html", context)