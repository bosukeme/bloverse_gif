"""
Resource file to parse out bloverse_gif script
"""
from flask import request
from flask_restful import Resource
import bloverse_gif



class BloverseGif(Resource):   

    def get(self):
        youtube_link = request.form['youtube_link']
        
        result=bloverse_gif.run_all(youtube_link)

        

        return {
            'Response': "Gif generated"
            }


