from minio import Minio
from minio.error import ResponseError
from datetime import timedelta
import time,socket,sys,json,urllib,os
from flask import Flask, flash, request, redirect, url_for,render_template,send_from_directory
from werkzeug.utils import secure_filename

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


sys.stdout.write("no" )
address="notyet"
ktory=0
while address == "notyet":
    ktory = ktory + 1
    try:
        address = socket.gethostbyname('minio')
    except socket.gaierror:
        time.sleep(1)

minioClient = Minio('{}:9000'.format(address),
                  access_key='ADMIN',
                  secret_key='EXAMPLEPASSWORD', secure=False)

time.sleep(5)

bucket_photos = minioClient.list_objects('animals')
[add_photo_to_db(photo.object_name.encode('utf-8')) for photo in bucket_photos ]

app = Flask(__name__)

# APP_ROOT = os.path.dirname(os.path.abspath(__file__))
# UPLOAD_FOLDER = '/home/michal/proba_flask/src'
# ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# def allowed_file(filename):
#     return '.' in filename and \
#            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/',methods=['GET', 'POST'])
def index():
    # if request.method == 'POST':
    #
    #     # target = os.path.join(APP_ROOT, 'images/')
    #     # print(target)
    #     #
    #     # if not os.path.isdir(target):
    #     #     os.mkdir(target)
    #
    #     for file in request.files.getlist("file"):
    #         print(minioClient.put_object('animals', 'moj_obiekt',
    #                                      file, file.st_size))
    #
    #         # filename = file.filename
    #         # filename = "filemon"
    #         # destination = "/".join([target, filename])
    #         # print(destination)
    #         # file.save(destination)

    url = "http://localhost:5000/photos"
    response = urllib.urlopen(url)
    data = json.loads(response.read())


    return render_template('index.html',photos= data['json_list'])

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0',port=5151)


# file = open("testfile.txt","w")
# file.write(giraffe_url)
# file.close()

#file2 = open("resp","w") 
#file2.write(response)
#file2.close()

# time.sleep(232344324)


# buckets=minioClient.list_buckets()
#
# for b in buckets:
#     print(b)