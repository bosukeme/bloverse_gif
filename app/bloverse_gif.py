from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import cv2
import random
from moviepy.editor import VideoFileClip
from pydub import AudioSegment
from pydub.playback import play
from pytube import YouTube
import os, re, glob
import generate_trimaps
import demo 
from datetime import datetime 
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

    gif_name = 'test_video' # name that you want to assign to the gif
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

def edit_youtube_video(video_path):
    """
    This function :
    - get youtube video
    - takes the first seven seconds of the video
    - get audio from video
    - append audio and video into a folder
    """

    print("---now cropping the video---")
    # The full video that you are trying to generate a subclip of ** - don't forget to change this!!
    full_video_path = video_path
    # The output path for the subclip - ** don't forget to change this!!
    subclip_video_path = home_dir +'/content/video/crop_video.mp4'
    subclip_audio_path = home_dir + '/content/test_audio.mp3'

    # The start and end times of the sub clip (in seconds), this can be a float
    start_time = 3
    end_time = 10
    clip = VideoFileClip(video_path)

    # clip = clip.resize((1080, 1080)) ## This is if you need to resize the video
    subclip = clip.subclip(start_time, end_time)
    subclip.to_videofile(subclip_video_path, audio_codec='aac')
    """
    Get subclip audio
    """
    temp = VideoFileClip(subclip_video_path)
    temp.audio.write_audiofile(subclip_audio_path)


def getFrame(sec, target_height, target_width, vidcap):
    fr_lst = []
    vidcap.set(cv2.CAP_PROP_POS_MSEC,sec*1000)
    hasFrames,image = vidcap.read()
    if hasFrames:
        image = cv2.cvtColor(np.uint8(image), cv2.COLOR_BGR2RGB)
        fr_lst.append(cv2.resize(image, (target_width, target_height)))

    return hasFrames, fr_lst
 
    
## Build a function that takes a video path, ingests that video, converts it to frames and then returns the frames to you
def convert_vid_to_frames(video_path, FPS, target_height, target_width):
    vidcap = cv2.VideoCapture(video_path)
    sec = 0 #start location of where we want to start 
    frameRate = 1/FPS #//it will capture image in each 0.5 second
    count=1
    frame_list = []
    success, fr_lst = getFrame(sec, target_height, target_width, vidcap)
    while success:
        count = count + 1
        sec = sec + frameRate
        sec = round(sec, 2)
        success, fr_lst = getFrame(sec, target_height, target_width, vidcap)
        try:
            frame_list.append(fr_lst[0])
        except:
            pass
        if len(frame_list) > 360:
            print('Too many frames')
            break
    return frame_list.copy()
 
def video_size(path):
    vidcap = cv2.VideoCapture(path)
    width = int(vidcap.get(3))
    height = int(vidcap.get(4))
    fps = vidcap.get(5)
    print("the width, height and fps are:", width, height, fps )
    
    return width, height, fps



def convert_frames_to_png(frame_list):
    """
    This function convert frames to image
    """
    count = 0
    for frame in frame_list:
        img = Image.fromarray(frame, 'RGB')
        
        newpath = home_dir + '/content/images/img' 
        if not os.path.exists(newpath):
            os.makedirs(newpath)
        
        img.save(newpath + "%d.png" % count)
        count += 1
    
    return None


def change_backgound():
    """
    This function generates trimaps and append the image and teh trimaps.
    Note: Edit the demo.py code (i.e from green_bg[:, :, 1] = 255 to green_bg[:, :, :] = 255) -- line 31
    """
    print("Now changing the background. Would take a long time")
    generate_trimaps.main("content/images", "person", 0.5)
    
    print("now on demo")
    os.system("python3 demo.py --image_dir content/images --trimap_dir content/images/trimaps --output_dir content/matting-output/")
    return None

def get_swapped_bg_files():
    data_files = sorted(glob.glob("content/matting-output/*_swapped_bg.png"))
    
    return data_files


def sort_alphanumeric(data_files):
    """
    This function sorts items in a list
    """
    convert = lambda text: float(text) if text.isdigit() else text
    alphanum = lambda key: [convert(c) for c in re.split('([-+]?[0-9]*\.?[0-9]*)', key)]
    data_files.sort(key=alphanum)
    
    return data_files

def convert_png_to_frames(data_files):
    """
    This function converts images back to frames
    """

    nframes = []
    for image in data_files:
        img = np.asarray(Image.open(image))
        nframes.append(img)
    return nframes





def get_swapped_bg_files():
    data_files = sorted(glob.glob("content/matting-output/*_swapped_bg.png"))
    
    return data_files

def sort_alphanumeric(data_files):
    """
    This function sorts items in a list
    """
    convert = lambda text: float(text) if text.isdigit() else text
    alphanum = lambda key: [convert(c) for c in re.split('([-+]?[0-9]*\.?[0-9]*)', key)]
    data_files.sort(key=alphanum)
    
    return data_files

def convert_png_to_frames(images):
    """
    This function converts images back to frames
    """

    nframes = []
    for image in images:
        img = np.asarray(Image.open(image))
        nframes.append(img)
    return nframes

def generate_video(frames,output_path):
    """
    This function takes in a list of frames and an output path
    and return an mp4 video
    """

    height, width, layers = np.array(frames[0]).shape
    size = (width,height)   
    video = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'DIVX'), 30, size)

    #draw stuff that goes on every frame here
    for i in frames:
    # draw frame specific stuff here.
        video.write(cv2.cvtColor(np.array(i), cv2.COLOR_RGB2BGR))
    video.release()


def extract_mp3_audio_from_mp4_file(video_path, output_audio_path):
    """
    This function takes in an input 
    """
    
    audio = AudioSegment.from_file(video_path, format="mp4")
    audio.export(output_audio_path, format="mp3")

    return None


def append_image_and_audio(video_path, audio_path, output_path):
    """
    This function takes in takes in a video, an audio and append both
    """
    final_output = os.system("ffmpeg -i " + video_path+" -i "+audio_path+" -c:v copy -c:a aac "+output_path)
    return final_output



def run_all(youtube_link):

    start= datetime.now()
    print("Starting at: ", start)
    get_youtube_video(youtube_link)

    vid= "content/video/test_video.mp4"
    edit_youtube_video(vid)

    cropped_vid= "content/video/crop_video.mp4"

    width, height, fps = video_size(cropped_vid)
    width= width/2
    height= height/2
    
    frame_list = convert_vid_to_frames(cropped_vid, round(fps), round(height), round(width))
    print("---now getting frames---")

    convert_frames_to_png(frame_list)

    change_backgound()


    data_files = get_swapped_bg_files()
    
    data_files = sort_alphanumeric(data_files)
    
    nframes = convert_png_to_frames(data_files)
    
    final_output=generate_video(nframes, "content/output.mp4" )
    

    #extract_mp3_audio_from_mp4_file(cropped_vid, "content/audio.mp3")
    
    #final_output=append_image_and_audio("content/output.mp4", "content/audio.mp3", "content/complete.mp4")
    

    #os.system("sudo rm -r content/images/trimaps")
    #os.system("sudo rm -r content/images")
    #os.system("sudo rm -r content/matting-output")
    
    end= datetime.now()
    print("The process took: ", end-start)
    return final_output


#run_all()
