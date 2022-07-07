#!/usr/bin/env python
# coding: utf-8

# In[1]:


#Empezamos configurando el ambiente de trabajo, es decir, que nos preparamos importando las librerías y comandos necesarios.
from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np

#Además, determinamos el sitio web del cual extraeremos información: el sitio web de la SUNEDU
lista_sunedu="https://www.sunedu.gob.pe/lista-universidades/"
table_id1="tablepress-23" #Universidades Privadas
table_id2="tablepress-22" #Universidades Públicas
response=requests.get(lista_sunedu)
soup=BeautifulSoup(response.text, "html.parser")


# In[8]:


get_ipython().system('pip install pandas')


# In[9]:


get_ipython().system('pip install numpy')


# In[10]:


get_ipython().system('pip install requests')


# In[12]:


get_ipython().system('pip install bs4')


# In[164]:


#Continuamos extrayendo la tabla correspondiente a las universidades privadas. Para ubicarla previamente se le inspecciona.


# In[165]:


#Esto es muy importante dado que en el sitio web hay dos tablas, así que debe prestarse atención para anotar con cuál se trabaja


# In[168]:


#Nótese que tambien se creó la dummy que indica el estado de su licencia [1 = licenciada; 0 = no licenciada]


# In[13]:


privada_table=soup.find("table", attrs={"id": table_id1})
df_privada=pd.read_html(str(privada_table))
df_privada=df_privada[0]
df_privada['TIPO']="Privada"
df_privada['LICENCIADA']= pd.notnull(df_privada['FECHA DE PUB. DIARIO EL PERUANO'])*1
df_privada=df_privada.loc[:, ['UNIVERSIDAD', 'DEPARTAMENTO', 'PROVINCIA','TIPO', 'LICENCIADA']]
df_privada


# In[167]:


#corresponde repetir el proceso, pero con las universidades públicas.
#Nótese que tambien se creó la dummy que indica el estado de su licencia [1 = licenciada; 0 = no licenciada]


# In[20]:


publica_table=soup.find("table", attrs={"id": table_id2})
df_publica=pd.read_html(str(publica_table))
df_publica=df_publica[0]
df_publica['TIPO']="Publica"
df_publica['LICENCIADA']= pd.notnull(df_publica['FECHA DE PUB. DIARIO EL PERUANO'])*1
df_publica=df_publica.loc[:, ['UNIVERSIDAD', 'DEPARTAMENTO', 'PROVINCIA','TIPO', 'LICENCIADA']]
df_publica


# In[169]:


#Ahora se une las dos tablas en un solo dataframe 


# In[21]:


df_universidad=df_privada.append(df_publica, ignore_index=True)
df_universidad=pd.get_dummies(df_universidad, columns=['TIPO'])
df_universidad


# ## Geocoding de las universidades

# In[172]:


#Se inicia configurando el ambiente de trabajo, con lo cual se importa libreríasy comandos a usar.


# In[15]:


# Packages
import pandas as pd
import os
import urllib.request, json
import csv
import numpy as np
from tqdm import tqdm_notebook as tqdm # libreria para contabilizar tiempo de ejecución


# In[173]:


#lo que sigue es importantísimo: vincular con google maps, puesto que de este obtendremos la información geográfica


# In[16]:


import googlemaps
from datetime import datetime
gmaps = googlemaps.Client(key='AIzaSyDr6c93pk9Tepnfr5UqiLxOk_mnwG4Qevo')  # ingreso el Key (token)


# In[174]:


#se define lat como latitud y lng como longitud.


# In[175]:


df_universidad['lat']=None
df_universidad['lng']=None
for index in range(df_universidad.shape[0]):
    df_temp=df_universidad.take([index])
    geocode_result = gmaps.geocode(str(df_temp['UNIVERSIDAD'])+
                                   str(df_temp['DEPARTAMENTO'])+
                                   str(df_temp['PROVINCIA']) ,
                                   region='PE')
    lat=geocode_result[0]['geometry']['location']['lat']
    lng=geocode_result[0]['geometry']['location']['lng']
    df_universidad.loc[index,'lat']=lat
    df_universidad.loc[index,'lng']=lng
df_universidad

#Podemos ahora ver el conjunto de universidades con su respectiva información geográfica


# In[176]:


#Mediante el siguiente comando se exporta a EXCEL. Este archivo resultante ha sido subido al repositorio


# In[21]:


df_universidad = df_universidad.to_excel("universidades grupo_6.xlsx")


# In[23]:


import pandas as pd
from pandas import Series, DataFrame
import numpy as np
import matplotlib.pyplot as plt 
import chardet


# In[71]:





# In[47]:


get_ipython().system('pip install shapely')


# In[62]:


get_ipython().system('pip install folium')


# In[67]:


from IPython.display import display, HTML


# In[11]:


import geopandas as gpd


# In[21]:


# objects from Geopandas 

import geopandas as gpd
from geopandas import GeoSeries


# In[1]:


import geopandas as gpd


# In[6]:


get_ipython().system('pip install plotly')


# In[10]:


import json


# In[12]:


get_ipython().system('pip install gdal')


# In[15]:


get_ipython().system('pip install folium')


# In[24]:


import folium


# In[31]:


import pandas as pd


# In[177]:


#Lo previo también sirvió para configurar el ambiente de trabajo. 


# In[178]:


#En lo que sigue se obtiene la coordenada del Perú, el cual será el punto de partida para la ubicación de las universidades
#contenidas en sus fronteras, sean privadas o públicas


# In[179]:


#-10.40639427007711, -75.3383822662524 son las coordenadas del Perú


# In[180]:


world = folium.Map(
    zoom_start=5,
    location=[-10.40639427007711, -75.33838226625241])

world


# In[182]:


#El siguiente ploteo es una primera visualización que permite confirmar si vamos (o no) por buen camino


# In[181]:


world = folium.Map(
    zoom_start=6,
    location=[-10.40639427007711, -75.33838226625241]
)

for _, universidad in df_universidad.iterrows():
    folium.Marker(
        location=[universidad['lat'], universidad['lng']],
    ).add_to(world)

world


# In[183]:


#Lo siguiente es crear subsets para diferencias universidades públicas de privadas; y crear un mapa para cada caso


# In[134]:


temp_priv = df_universidad[df_universidad.TIPO_Privada==1]
temp_publ = df_universidad[df_universidad.TIPO_Privada==0]


# In[184]:


def select_marker_color(row):
    if row['LICENCIADA'] == 1 and row['TIPO_Privada'] ==1:
        return 'pink'
    elif row['LICENCIADA'] == 0 and row['TIPO_Privada'] ==1:
        return 'blue'
    elif row['LICENCIADA'] == 1 and row['TIPO_Publica'] ==1:
        return 'darkgreen' 
    elif row['LICENCIADA'] == 0 and row['TIPO_Publica'] ==1:
        return 'darkred'
temp_priv['colors'] = temp_priv.apply(select_marker_color, axis=1)
temp_priv.head(10)
world_all_cities_colored = folium.Map(
    zoom_start=4.5
,
    location=[-10.40639427007711, -75.33838226625241]
)

for _, universidad in temp_priv.iterrows():
    folium.Marker(
        location=[universidad['lat'], universidad['lng']],
          popup=universidad[0],
        icon=folium.Icon(color=universidad['colors'], prefix='fa', icon='circle')
    ).add_to(world_all_cities_colored)
    
world_all_cities_colored


# In[185]:


def select_marker_color(row):
    if row['LICENCIADA'] == 1 and row['TIPO_Privada'] ==1:
        return 'pink'
    elif row['LICENCIADA'] == 0 and row['TIPO_Privada'] ==1:
        return 'blue'
    elif row['LICENCIADA'] == 1 and row['TIPO_Publica'] ==1:
        return 'darkgreen' 
    elif row['LICENCIADA'] == 0 and row['TIPO_Publica'] ==1:
        return 'darkred'
temp_publ['colors'] = temp_publ.apply(select_marker_color, axis=1)
temp_publ.head(10)
world_all_cities_colored = folium.Map(
    zoom_start=5
,
    location=[-10.40639427007711, -75.33838226625241]
)

for _, universidad in temp_publ.iterrows():
    folium.Marker(
        location=[universidad['lat'], universidad['lng']],
        popup=universidad[0],
        icon=folium.Icon(color=universidad['colors'], prefix='fa', icon='circle')
    ).add_to(world_all_cities_colored)
    
world_all_cities_colored

