from os import name
from textwrap import fill
from turtle import color, fillcolor
import folium
import pandas

data = pandas.read_csv("Volcanoes.txt")
Lat = list(data["LAT"])
Lon = list(data["LON"])
Ele = list(data["ELEV"])
map = folium.Map(location=[38.58, -99.09], zoom_start=5)  

def colorElevation(Elevation):
    if Elevation <1000:
        return 'green'
    elif 1000 <= Elevation < 3000:
        return 'orange'
    else:
        return 'red'

html = """<h4>Volcano information:</h4>
Height: %s m
"""

fg = folium.FeatureGroup(name="Home Location")
for coordinates in [[28.7041, 77.1025]]:
    fg.add_child(folium.Marker(location=coordinates, popup="Hi I am\na Marker!", icon=folium.Icon(color='green', icon_color='white')))
map.add_child(fg)

fg1 = folium.FeatureGroup(name="Volcanoes in US")
for lat,lon,el in zip(Lat,Lon,Ele):
    iframe = folium.IFrame(html=html % str(el), width=200, height=100)
    # fg1.add_child(folium.Marker(location=[lat,lon], popup=str(el)+" m", icon=folium.Icon(color=colorElevation(el),icon='circle-dot')))
    fg1.add_child(folium.CircleMarker(location=[lat,lon],radius=9,popup=str(el)+" m",fill_color=colorElevation(el),color='grey', fill=True,fill_opacity=0.8))
    # fg1.add_child(folium.Marker(location=[lat,lon], popup=folium.Popup(iframe), icon=folium.Icon(color=colorElevation(el),icon='circle-dot')))

fg2 = folium.FeatureGroup(name="Population")
fg2.add_child( folium.GeoJson(data=open('world.json','r',encoding='utf-8-sig').read(),
style_function=lambda x: {'fillColor':'light green' if x['properties']['POP2005'] < 10000000 
else 'yellow' if 10000000<= x['properties']['POP2005'] <= 20000000 else 'red'}))

data1 = pandas.read_csv("Book1.csv")
lon1=list(data1["Longitude"])
lat1=list(data1["Latitude"])

fg3 = folium.FeatureGroup(name='Nuclear Plants in India')
for lat,lon in zip(lat1,lon1):
    fg3.add_child(folium.CircleMarker(location=[lat,lon], radius=10, popup='Nuclear Plant', fill_color='red',color='grey', fill=True,fill_opacity=0.8))

map.add_child(fg3)
map.add_child(fg2)
map.add_child(fg1)

map.add_child(folium.LayerControl())
map.save("Map1.html")
