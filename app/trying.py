from pytube import YouTube
import os, re
home_dir=os.getcwd()



def get_youtube_video(youtube_url):
    """
    This function:
    - create a folder
    - rename the video
    - get youtube video
    """

    """
    Initialise video input paths
    """
    youtube_video_path = home_dir=os.getcwd()+ '/content/video' # path to store video downloaded from youtube

    gif_name = 'test_video_again' # name that you want to assign to the gif
    input_video_path = '%s/%s.mp4' % (youtube_video_path, gif_name) # input video path (based on location of youtube video)
    
    """
    Download youtube video
    """

    youtube_video_url = youtube_url
    yt = YouTube(youtube_video_url)
    #ys = yt.streams.get_highest_resolution() # Get the highest resolution version of the video
    ys = yt.streams.first()
    ys.download(youtube_video_path) # Download video
    temp_filename = '%s/%s' % (youtube_video_path, ys.default_filename)
    os.rename(temp_filename, input_video_path)

get_youtube_video("https://youtu.be/rXRAjWOrH9A")