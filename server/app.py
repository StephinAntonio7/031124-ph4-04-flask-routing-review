#!/usr/bin/env python3

from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS

from models import db, Meme

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)

migrate = Migrate(app, db)

db.init_app(app)

@app.get('/api')
def index():
    return "Hello world"

@app.get ('/api/memes')
def get_memes():  
    return[meme.to_dict() for meme in Meme.query.all() ]

@app.post('/api/memes')
def post_meme():
    new_meme=Meme(
        img_url=request.json['img_url'],
        caption=request.json['caption'],
        likes=request.json.get('likes')
    )
    
    db.session.add(new_meme)
    db.session.commit()
    
    return new_meme.to_dict(), 201

    return new_meme, 201

@app.patch('/api/memes/<int:id>')
def meme(id):
    
    meme_to_update=Meme.query.where(Meme.id == id).first()
    
    if meme_to_update:
        for key in request.json.keys(): 
            if not key =='id':
                setattr(meme_to_update, key, request.json[key])
        db.session.add( meme_to_update )
        db.session.commit() 
        
        return meme_to_update.to_dict(), 202
    else:
        return { 'error': 'Not found' }, 404  
    
@app.delete ('/api/memes/<int:id>')
def delete_meme(id:int):
    
    meme_to_delete = Meme.query.where(Meme.id ==id).first()
    
    if meme_to_delete:
        db.session.delete(meme_to_delete)
        db.session.commit()
        return {}, 204
    else:
        return { "error": "Not found" }, 404
    
# write your routes here!

if __name__ == '__main__':
    app.run(port=5555, debug=True)
