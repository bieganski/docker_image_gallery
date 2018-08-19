from  flask import Flask, render_template,request,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_json import FlaskJSON, JsonError, json_response, as_json


app = Flask(__name__)
FlaskJSON(app)


app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:example@postgres_db:5432/images'

db = SQLAlchemy(app)

class Photo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(700))
    votes = db.Column(db.Integer)
    desc = db.Column(db.String(200))

    def __init__(self,url,votes,desc):
        self.url = url
        self.votes = votes
        self.desc = desc
   
    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id' : self.id,
            'url': self.url,
            'votes': self.votes,
            'desc': self.desc
        }

    def __repr__(self):
        return 'Url: %r' % self.url

db.create_all()

# photo = Photo("fajny_url1",1,"no elo1")
# db.session.add(photo)
#
# photo = Photo("fajny_url2",2,"no elo2")
# db.session.add(photo)
#
# photo = Photo("fajny_url3",3,"no elo3")
# db.session.add(photo)
#
# photo = Photo("fajny_url4",4,"no elo4")
# db.session.add(photo)
#
# db.session.commit()

@app.route('/')
def index():
    return "<h1> No siema </h1>"


@app.route('/post_data', methods=['POST'])
def processjson():
    data = request.get_json()
    url=data['url']
    votes=data['votes']
    desc=data['desc']
    photo = Photo(url,votes,desc )
    db.session.add(photo)
    db.session.commit()
    return json_response(success=True)

@app.route('/photos_human_readable')
def photos_human_readable():
    photos = Photo.query.all()
    return render_template('index.html', photos = photos)
    
@app.route('/photos')
def photos():
    photos = Photo.query.all()
    return jsonify(json_list=[i.serialize for i in photos ] )

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
