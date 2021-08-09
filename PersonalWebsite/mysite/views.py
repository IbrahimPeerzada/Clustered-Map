# used for text
# Create your views here.

# from django.http import HttpResponse
 
# def index(request):
#     return HttpResponse('hello, ibrahim')

import folium 
import pandas as pd
import folium.plugins
import branca
import branca.colormap as cm
from folium.plugins import MarkerCluster
import folium.plugins as plugins
from folium.plugins import MousePosition
from branca.element import Element
import leaflet as L

col_names= ['Cluster',
            'C_coor',
            'C_lat',
           'C_long',
            
           'Region',
           'R_coor',
           'R_lat',
           'R_long',
           
           'District',
           'D_coor',
           'D_lat',
           'D_long',
            
           'Branch_code',
           'Branch_name',
           'B_coor',
           'B_lat',
           'B_long',
           'B_Balance']

name = pd.read_csv("D:\learningjupitornotebook\Branch_Coordinates3.csv",names=col_names,skiprows=[0],encoding='cp1252')
df= pd.DataFrame(name)
df.head()
df.shape
df.describe()

# Map

loca=(30.3753,69.3451)
map_osm = folium.Map(location = loca, zoom_start =5)

# Marker Locations

df_all_locations = df[['B_lat','B_long']]
all_location_list = df_all_locations.values.tolist()
all_location_list_size = len(all_location_list)
all_location_list_size

# ColorBar

colormap = cm.LinearColormap(colors=['darkblue','purple','orange','red'],
                            index=[50000,200000,500000,800000],
#                             Scale_width=800 ,Scale_height=20,
                            vmin=0 , vmax=800000,
                            caption='Deposited Balance[rs]').add_to(map_osm)

# Cluster Locations

cluster = df[["C_lat","C_long"]].values.tolist()
MC = folium.plugins.MarkerCluster(name='MC',loc=cluster).add_to(map_osm)


# Markers Placing with color 

for point in range(0,all_location_list_size):
    if df['B_Balance'][point] < 50000:
        folium.Marker(all_location_list[point],
                      popup='Branchname:'+df['Branch_name'][point]+' Balance:'+df['B_Balance'][point].astype(str),
                      tooltip='Branchname:'+df['Branch_name'][point]+'<br>Balance:'+df['B_Balance'][point].astype(str),
                      icon=folium.Icon(color='darkblue',icon_color='white',icon='university',angle=0,prefix='fa')).add_to(MC)
    
    elif df['B_Balance'][point] > 50000 and df['B_Balance'][point] <= 200000:
        folium.Marker(all_location_list[point],
                      popup='Branchname:'+df['Branch_name'][point]+' Balance:'+df['B_Balance'][point].astype(str),
                      tooltip='Branchname:'+df['Branch_name'][point]+'<br>Balance:'+df['B_Balance'][point].astype(str),
                      icon=folium.Icon(color='purple',icon_color='white',icon='university',angle=0,prefix='fa')).add_to(MC)
    
    elif df['B_Balance'][point] > 200000 and df['B_Balance'][point] <= 500000:
        folium.Marker(all_location_list[point],
                      popup='Branchname:'+df['Branch_name'][point]+' Balance:'+df['B_Balance'][point].astype(str),
                      tooltip='Branchname:'+df['Branch_name'][point]+'<br>Balance:'+df['B_Balance'][point].astype(str),
                      icon=folium.Icon(color='orange',icon_color='white',icon='university',angle=0,prefix='fa')).add_to(MC)
    
    else:
        folium.Marker(all_location_list[point],
                      popup='Branchname:'+df['Branch_name'][point]+' Balance:'+df['B_Balance'][point].astype(str),
                      tooltip='Branchname:'+df['Branch_name'][point]+'<br>Balance:'+df['B_Balance'][point].astype(str),
                      icon=folium.Icon(color='red',icon_color='white',icon='university',angle=0,prefix='fa')).add_to(MC)
        
folium.raster_layers.TileLayer('Open Street Map').add_to(map_osm)
folium.raster_layers.TileLayer('Stamen Terrain').add_to(map_osm) 
folium.raster_layers.TileLayer('Stamen Toner').add_to(map_osm)
folium.raster_layers.TileLayer('Stamen Watercolor').add_to(map_osm)
folium.raster_layers.TileLayer('CartoDB Positron').add_to(map_osm)
folium.raster_layers.TileLayer('CartoDB Dark_Matter').add_to(map_osm)

folium.LayerControl().add_to(map_osm)        


# Mini Map Plugin
minimap = plugins.MiniMap(toggle_display=True)

#adding minimap to the orignal map 
map_osm.add_child(minimap)

#adding scroll zooming 
plugins.ScrollZoomToggler().add_to(map_osm)

#adding full screen button to original map 
plugins.Fullscreen(position='topleft').add_to(map_osm)

formatter = "function(num) {return L.Util.formatNum(num, 3) + ' º ';};"

MousePosition(
    position="topright",
    separator=" | ",
    empty_string="NaN",
    lat_first=True,
    num_digits=20,
    prefix="Coordinates:",
    lat_formatter=formatter,
    lng_formatter=formatter,        
).add_to(map_osm)

# This is one of the way to use JS in python 

# my_js= '''

# 		var markers = new L.MarkerClusterGroup();
# 		var markersList = [];

# 		function populate() {
# 			for (var i = 0; i < 100; i++) {
# 				var m = new L.Marker(getRandomLatLng(map_osm));
# 				markersList.push(m);
# 				markers.addLayer(m);
# 			}
# 			return false;
# 		}
# 		function populateRandomVector() {
# 			for (var i = 0, latlngs = [], len = 20; i < len; i++) {
# 				latlngs.push(getRandomLatLng(map_osm));
# 			}
# 			var path = new L.Polyline(latlngs);
# 			map.addLayer(path);
# 		}
# 		function getRandomLatLng(map_osm) {
# 			var bounds = map_osm.getBounds(),
# 				southWest = bounds.getSouthWest(),
# 				northEast = bounds.getNorthEast(),
# 				lngSpan = northEast.lng - southWest.lng,
# 				latSpan = northEast.lat - southWest.lat;

# 			return new L.LatLng(
# 					southWest.lat + latSpan * Math.random(),
# 					southWest.lng + lngSpan * Math.random());
# 		}

# 		markers.on('clusterclick', function (a) {
# 			alert('cluster ' + a.layer.getAllChildMarkers().length);
# 		});
# 		markers.on('click', function (a) {
# 			alert('marker ' + a.layer);
# 		});

# 		populate();
# 		map.addLayer(markers);

# 		L.DomUtil.get('populate').onclick = function () {
# 			var bounds = map.getBounds(),
# 			southWest = bounds.getSouthWest(),
# 			northEast = bounds.getNorthEast(),
# 			lngSpan = northEast.lng - southWest.lng,
# 			latSpan = northEast.lat - southWest.lat;
# 			var m = new L.Marker(new L.LatLng(
# 					southWest.lat + latSpan * 0.5,
# 					southWest.lng + lngSpan * 0.5));
# 			markersList.push(m);
# 			markers.addLayer(m);
# 		};
# 		L.DomUtil.get('remove').onclick = function () {
# 			markers.removeLayer(markersList.pop());
# 		};
# '''
# map_osm.get_root().script.add_child(Element(my_js))


# Save the file in HTML to save the file s

# map_osm.save('D:/learningjupitornotebook/PersonalWebsite/PersonalWebsite/mysite/templates/mysite/index.html')




from django.shortcuts import render

def index(request):
    return render(request,'mysite/index.html')