
# A very simple Flask Hello World app for you to get started with...

# A very simple Flask Hello World app for you to get started with...

from flask import Flask,render_template,request,flash
import flask
from flask import *
from werkzeug import secure_filename
import urllib.request
import json,os,folium,requests
import pandas as pd
from azure.storage.blob import BlockBlobService, PublicAccess
from geopy.geocoders import Nominatim
import xlrd,datetime
from os.path import isdir, isfile
from datetime import datetime
import runpy
from PIL import Image
import glob
# Web scraping package
from pyvirtualdisplay import Display
from selenium import webdriver
# Language Translator
from googletrans import Translator  # Import Translator module from googletrans package


app = Flask(__name__)


@app.route('/')
def hello():
    return render_template('index.html')
'''
@app.route('/log', methods =['GET', 'POST'])
def log():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid credentials'
        else:
            return redirect(url_for('hello'))
    return render_template('log.html', error= error)
'''
@app.route('/upload')
def upload():
   files_values = blobService()
   return render_template('service.html',radio_form=files_values)

def blobService():
    blb_names=[]
    block_blob_service = BlockBlobService(account_name='isuzupredmaintenance', account_key='jsUq8mN4NIHahxj4xOXs4tHtS62cEkGvryEZfE3H3FGtr8tQ+lf3YSaophd1kuCyyAE2257QtJreh1AV7FkQ8A==')
    container_name ='isuzu'
    generator = block_blob_service.list_blobs(container_name)
    for blob in generator:
        blb_names.append(blob.name)
    return blb_names

@app.route('/uploader', methods=['GET','POST'])
def upload_file():
   if request.method == 'POST':
      checked_files = request.form.getlist("options")
      print("checked files : ",checked_files)
      local_path='./spreadsheets'
      container_name ='isuzu'
      block_blob_service = BlockBlobService(account_name='isuzupredmaintenance', account_key='jsUq8mN4NIHahxj4xOXs4tHtS62cEkGvryEZfE3H3FGtr8tQ+lf3YSaophd1kuCyyAE2257QtJreh1AV7FkQ8A==')
      for i in checked_files:
          full_path_to_file2 = os.path.join(local_path, i)
          print("\nDownloading blob to " + full_path_to_file2)
          block_blob_service.get_blob_to_path(container_name, i, full_path_to_file2)
      print(checked_files[-1])
      wb = xlrd.open_workbook('./spreadsheets/' + checked_files[-1])
      sheet = wb.sheet_by_index(0)
      print(sheet)
      nrow=sheet.nrows
      print(sheet.cell_value(0, 0))
      lat=sheet.cell_value(nrow-1,1)
      lon=sheet.cell_value(nrow-1,2)
      temp=sheet.cell_value(nrow-1,3)
      pres=sheet.cell_value(nrow-1,4)
      humidity=sheet.cell_value(nrow-1,5)
      windspeed=sheet.cell_value(nrow-1,6)
      desc=sheet.cell_value(nrow-1,7)
      sunrise=sheet.cell_value(nrow-1,8)
      sunset=sheet.cell_value(nrow-1,9)
      curr_time=sheet.cell_value(nrow-1,0)
      #========================================================================Location=================================================
      dataframe=pd.read_excel('./spreadsheets/' + checked_files[-1])
      locations = dataframe[['Latitude', 'Longitude']]
      locationlist = locations.values.tolist()
      map = folium.Map(location=locationlist[0], zoom_start=12,tiles='openstreetmap')
      for point in range(0, len(locationlist)):
          folium.Marker(locationlist[point], color='#3186cc',fill=True,fill_color='#3186cc').add_to(map)
      #folium.Marker(location=[lat,lon],radius=50,color='#3186cc',fill=True,fill_color='#3186cc').add_to(m)
      map.save("./templates/location.html")
      geolocator = Nominatim(user_agent="my-application")
      location = geolocator.reverse(""+str(lat)+","+str(lon)+"")
      print(location.address)

      return render_template('ResultsWeb.html',curr_time=curr_time,temp=temp, pres=pres, humidity=humidity,ws=windspeed, desc=desc,location=location.address,sunrise=sunrise,sunset=sunset)

@app.route('/blog', methods=['GET','POST'])
def blog():
    if request.method == 'GET':
        return render_template('blog.html')

@app.route('/map', methods=['GET','POST'])
def map():
    if request.method == 'GET':
        return render_template('location.html')

@app.route('/technology', methods=['GET','POST'])
def technology():
    if request.method == 'GET':
        event_post = []
        trainings = []
        chrome_path = r"C:\Users\akadam\Desktop\chromedriver.exe"
        driver  =  webdriver.Chrome(chrome_path)
        driver.get("https://automotivedigest.com/events/")
        posts = driver.find_elements_by_class_name("person")
        event_post.clear()
        for post in posts:
            print(post.text)
            event_post.append(post.text)
        return render_template('technology.html', posts= event_post)
        

@app.route('/translation', methods=['GET','POST'])
def translation():
    if request.method == 'GET':
        return render_template('translation.html')


@app.route('/translate', methods=['GET','POST'])
def translate():
    translator = Translator()
    if request.method == 'POST':
        file = request.files['translate_file']
        content = file.read()
        content = content.decode('utf-16')
        file.save(secure_filename(file.filename))
        lang = request.form.get('language')
        file1 = open("./translated_doc/file.txt","w", encoding = "utf-8")
        if lang == "English":
            result = translator.translate(content, dest='en')
        elif lang == "Chinese":
            result = translator.translate(content, dest='zh-cn')
        elif lang == "Japanese":
            result = translator.translate(content, dest='ja')
        elif lang == "German":
            result = translator.translate(content, dest='de')
        elif lang == "Hindi":
            result = translator.translate(content, dest='hi')
        file1.writelines(result.text)
        print(file1)

        return render_template('translation.html', lang = str(lang))
    else:
        return render_template('translation.html')

@app.route('/analysis', methods=['GET','POST'])
def analysis():
    if request.method == 'GET':
        return render_template('analysis.html')

@app.route('/analyze', methods=['GET','POST'])
def analyze():
    if request.method == 'POST':
        file = request.files['analysis_file']
        content = file.read()
        content = content.decode('utf-16')
        methods = request.form.get('method')
        models = request.form.get('model')
        if models == " train":
            if methods == "linearReg":
                runpy.run_module(mod_name='trial_visualization')
                images = os.listdir(os.path.join('./static/', "SensorsPlots"))
                return render_template('analysis.html', images=images)
        else:
            return render_template('analysis.html')



#----------------------------------------------------visualization-------------------------------------------------------------------

@app.route('/portfolio')
def portfolio():
    runpy.run_module(mod_name='trial_visualization')
    images = os.listdir(os.path.join('./static/', "SensorsPlots"))
    return render_template('trial_visualize.html', images=images)
'''


@app.route('/portfolio')
def portfolio():
    image_list = []
    runpy.run_module(mod_name='trial_visualization')
    for filename in glob.glob('/home/isuzu/mysite/SensorsPlots/*'):
        im=Image.open(filename)
        image_list.append(im)
    return render_template('trial_visualize.html', images=image_list)
'''
if __name__ == '__main__':
   app.run()