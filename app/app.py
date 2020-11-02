import os
from flask import Flask
from flask_restful import Api
from resources import BloverseGif




app=Flask(__name__)



api=Api(app)


@app.route("/")
def home():
    return "<h1 style='color:blue'>This is the Bloverse Gif  pipeline!</h1>"


api.add_resource(BloverseGif, '/bloversegif')

if __name__=='__main__':
    app.run(debug=True, host='0.0.0.0')
