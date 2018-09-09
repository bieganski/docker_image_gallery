from minio import Minio
from minio.error import ResponseError
from datetime import timedelta
import time,socket,sys,json,urllib,os,urllib, urllib2
from flask import Flask, flash, request, redirect, url_for,render_template,send_from_directory, jsonify
import requests

def add_photo_to_db(photo):
    try:
        url = minioClient.presigned_get_object('animals', photo, expires=timedelta(days=2))
        data = {}
        data['url'] = url
        data['votes'] = 0
        data['desc'] = 'default_animal'
        req = urllib2.Request('http://flask_db:5000/post_data')
        req.add_header('Content-Type', 'application/json')
        response = urllib2.urlopen(req, json.dumps(data))
        print(str(photo) + " added to db!")
    except:
        print("Could not add " + str(photo) + " to db..." )


address="notyet"
while address == "notyet":
    try:
        address = socket.gethostbyname('minio')
        print( "Minio ip address is:" + address)
    except socket.gaierror:
        print("Waiting for minio")
        time.sleep(1)


minioClient = Minio('{}:9000'.format(address),
                  access_key='ADMIN',
                  secret_key='EXAMPLEPASSWORD', secure=False)



def check_db_empty():
    r = requests.get('http://flask_db:5000/empty', auth=('user', 'pass'))
    return r.json()['empty']


def populate_db():
    try:
        if check_db_empty():
            bucket_photos = minioClient.list_objects('animals')
            print(bucket_photos)
            [add_photo_to_db(photo.object_name.encode('utf-8')) for photo in bucket_photos]
    except:
        print('Could not populate database!')


app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

image_counter = 0
@app.route('/',methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        populate_db()

    if request.method == 'POST':

        target = os.path.join(APP_ROOT, 'images/')
        print(target)

        if not os.path.isdir(target):
            os.mkdir(target)

        for file in request.files.getlist("file"):
            global image_counter
            image_counter = image_counter + 1
            filename = file.filename
            filename = 'picture_nr{}.jpg'.format(image_counter)
            destination = "/".join([target, filename])
            file.save(destination)

            try:
                print(minioClient.fput_object('animals', filename, destination))
                add_photo_to_db(filename)
            except ResponseError as err:
                print(err)

            # #This is option2 for the above - it should works
            # with open('images/{}'.format(filename), 'rb') as file_data:
            #     file_stat = os.stat('images/{}'.format(filename))
            #     print(minioClient.put_object('animals', filename,
            #                                  file_data, file_stat.st_size))


    url = "http://flask_db:5000/photos"
    response = urllib.urlopen(url)
    data = json.loads(response.read())

    def cmp(x):
        return x['votes']

    photos = sorted(data['json_list'], key=cmp, reverse=True)
    return render_template('index.html', photos=photos)


@app.route('/vote/<id>')
def vote(id):
    r = requests.get('http://flask_db:5000/vote/{}'.format(int(id)), auth=('user', 'pass'))
    if r.status_code == 200:
        return jsonify(success=True)
    return jsonify(success=False)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0',port=5151)