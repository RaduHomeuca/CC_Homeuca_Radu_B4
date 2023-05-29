
# [START gae_python38_render_template]
# [START gae_python3_render_template]
import datetime
import requests
import json
import os
import google.oauth2.id_token
import google.auth.transport.requests
import subprocess
from flask import Flask, render_template,request

app = Flask(__name__)


from google.cloud import storage
from google.cloud import datastore
from google.cloud import translate_v2 as translate


datastore_client = datastore.Client(project='cc-project-382319')
storage_client = storage.Client(project='cc-project-382319')
translate_client = translate.Client()

def put_sellers():
    entity = datastore.Entity(key=datastore_client.key('Seller'))

    entity.update({
        'nume': 'Seller4',
        'adresa': 'Strada Anastasie Panu nr. 46, Iași 700019'
    })
    datastore_client.put(entity)
def put_shoes():
    entity = datastore.Entity(key=datastore_client.key('Object'))

    entity.update({
        'owner': 'Seller5',
        'descriere': 'Jordan 1 High - Sneaker înalt',
        'site': 'https://www.aboutyou.ro/p/jordan/sneaker-inalt-9432021'
    })
    datastore_client.put(entity)

def translate(shoe):
    target='en'
    list=[]
    for i in range(0,6):
        text=shoe[i]['descriere']

        translation = translate_client.translate(text, target_language=target)
        new={'owner': shoe[i]['owner'],'descriere': translation['translatedText']}
        #print(translation['translatedText'])
        list.append(new)
    print(list)
    return list
# def store_time(dt):
#     entity = datastore.Entity(key=datastore_client.key('visit'))
#     entity.update({
#         'timestamp': dt
#     })
#
#     datastore_client.put(entity)
#
#
# def fetch_times(limit):
#     query = datastore_client.query(kind='visit')
#     query.order = ['-timestamp']
#
#     times = query.fetch(limit=limit)
#
#     return times





# def functions():
#     #response = requests.get('https://us-central1-cc-project-382319.cloudfunctions.net/function-1')
#     #print(response.text)
#     payload = {'key1': 'value1', 'key2': 'value2'}
#     headers = {'Content-type': 'application/json'}
#
#     response = requests.post('https://europe-west2-cc-project-382319.cloudfunctions.net/function-2', data=json.dumps(payload), headers=headers)
#     print(response.text)


def cloud_get_sellers():
    payload = {'key1': 'value1', 'key2': 'value2'}
    headers = {'Content-type': 'application/json'}

    response = requests.post('https://europe-west2-cc-project-382319.cloudfunctions.net/get_sellers', data=json.dumps(payload), headers=headers)
    print(response)
    return response


def bucket():
    bucket_name = "cc-project-382319.appspot.com"
    #bucket = storage_client.get_bucket(bucket_name)
    bucket = storage_client.bucket(bucket_name)
    blobs = bucket.list_blobs()
    blob_list=[]
    for blob in blobs:
        print(blob.name)
        #print(bucket.blob(blob.name).public_url)
        blob_list.append(bucket.blob(blob.name))
    return blob_list




def get_sellers():
    query = datastore_client.query(kind='Seller')
    query.order = ['-nume']
    sellers = query.fetch(limit=5)
    sellers_list=[]
    for seller in sellers:
        dict={'nume':seller['nume'], 'adresa':seller['adresa']}
        sellers_list.append(dict)
    return sellers_list
def get_shoe_info():
    payload = {'key1': 'value1', 'key2': 'value2'}
    # os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = './my-service-account.json'
    # request = google.auth.transport.requests.Request()
    # audience = 'https://mylocation-myprojectname.cloudfunctions.net/MyFunctionName'
    # TOKEN = google.oauth2.id_token.fetch_id_token(request, audience)
    headers = {
                'Content-type': 'application/json'}
    #'Authorization': 'bearer ' + subprocess.check_output(['C:\\Users\\Radu\\AppData\\Local\\Google\\Cloud SDK\\google-cloud-sdk\\bin', 'auth', 'print-identity-token']).decode('utf-8').strip(),



    response = requests.post('https://europe-west2-cc-project-382319.cloudfunctions.net/get_shoe_info', headers=headers)
    print(response.content)
    regular_string = response.content.decode('utf-8')
    my_dict = json.loads(regular_string)
    print(my_dict[2]['owner'])
    return my_dict

def put_faves(nume, fave):
    entity = datastore.Entity(key=datastore_client.key('Faves'))

    entity.update({
        'nume': nume,
        'fave': fave
    })
    datastore_client.put(entity)
def delete_faves(fave):

    query = datastore_client.query(kind='Faves')
    query.add_filter('fave', '=', fave)
    entities = list(query.fetch())
    for entity in entities:
        datastore_client.delete(entity.key)
def get_faves(nume):
    query = datastore_client.query(kind='Faves')
    query.add_filter('nume', '=', nume)
    #query.order = ['-nume']
    faves = query.fetch()
    faves_list=[]
    for fave in faves:
        dict={'fave':fave['fave']}
        faves_list.append(dict)
    return faves_list
@app.route('/')
def root():
    # Store the current access time in Datastore.
    #store_time(datetime.datetime.now(tz=datetime.timezone.utc))
    #put_sellers()
    #put_shoes()
    # Fetch the most recent 10 access times from Datastore.
    #times = fetch_times(10)
    sellers=get_sellers()
    #put_faves()
    #sellers=cloud_get_sellers()
    print(sellers[4]['nume'])
    # for sell in sellers:
    #     print(sell['nume'])
    blob = bucket()
    shoe = get_shoe_info()
    translated=translate(shoe)
    #image = 'https://storage.googleapis.com/cc-project-382319.appspot.com/'+blob.name
    #image = blob[1].public_url
    #print(image)
    return render_template(
        'index.html', image=blob,sellers=sellers,shoe=shoe,translated=translated)

@app.route('/info')
def info():
    img = request.args.get('img')
    nume = request.args.get('nume')
    print("asdadda",img)
    print("asdadda", nume)
    shoe = get_shoe_info()
    sellers = get_sellers()
    return render_template('info.html',image=img, nume=nume,shoe=shoe,sellers=sellers)

@app.route('/page2')
def page2():

    sellers=get_sellers()
    #print(sellers[4]['nume'])
    blob = bucket()
    shoe = get_shoe_info()
    translated=translate(shoe)
    return render_template(
        'page2.html', image=blob,sellers=sellers,shoe=shoe,translated=translated)
@app.route('/favorites')
def favorites():

    sellers=get_sellers()
    #print(sellers[4]['nume'])
    blob = bucket()
    shoe = get_shoe_info()
    translated=translate(shoe)
    return render_template(
        'favorites.html', image=blob,sellers=sellers,shoe=shoe,translated=translated)

@app.route('/put', methods=['POST'])
def put():
    data = request.json
    fave = data.get('fave')
    nume = data.get('nume')
    print(fave)
    print(nume)
    put_faves(nume,fave)
    #delete_faves('d1')

    return fave
@app.route('/del', methods=['POST'])
def delete():
    data = request.json
    fave = data.get('fave')
    #nume = data.get('nume')
    print(fave)
    #print(nume)
    #put_faves(nume,fave)
    delete_faves(fave)
    return fave
@app.route('/get', methods=['POST'])
def get():
    data = request.json
    nume = data.get('nume')

    print(nume)
    #print(nume)
    #put_faves(nume,fave)
    #delete_faves(fave)
    lista = get_faves(nume)
    return lista
if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    # Flask's development server will automatically serve static files in
    # the "static" directory. See:
    # http://flask.pocoo.org/docs/1.0/quickstart/#static-files. Once deployed,
    # App Engine itself will serve those files as configured in app.yaml.
    #functions()
    #bucket()
    app.run(host='127.0.0.1', port=8000, debug=True)

# [END gae_python3_render_template]
# [END gae_python38_render_template]
