from  flask import Flask, render_template,request,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_json import FlaskJSON, JsonError, json_response, as_json
import time


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

no_conn=True
while no_conn:
    try:
        db.session.execute('SELECT 1')
        no_conn=False
    except:
        print( "Im waiting for connection with database")
        time.sleep(1)

db.create_all()


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
    
@app.route('/photos')
def photos():
    photos = Photo.query.all()
    return jsonify(json_list=[i.serialize for i in photos ] )

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
