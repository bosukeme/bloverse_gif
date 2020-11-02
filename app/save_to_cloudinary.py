import cloudinary
from cloudinary.uploader import upload
import os

cloud_name="bosukeme"  #os.environ.get("CLOUD_NAME")
api_key= 989783835596593   ##int(os.environ.get("API_KEY"))
api_secret= "EwqVFRlXKRIW_Eq6E-CAoF9vw74"     ##os.environ.get("API_SECRET")

cloudinary.config(
    cloud_name=cloud_name,
    api_key=api_key,
    api_secret=api_secret,
)


def upload_video(video_output_path):
    upload_response = upload(
        video_output_path,
        resource_type="video",
        folder="videos/test-article-videos/",
    )
    video_url_payload = upload_response["secure_url"]
    del video_output_path, upload_response  
    return video_url_payload

# if __name__ == '__main__':
#     upload_video("cut.mp4")