import os 
import sys 
import streamlit
import request.py as rq
import jamscripted.py as jm


streamlit.header("MASHUP- by Pranjal Arora, 102003402, 3CO-16")
mashupform = streamlit.form(key='mashup_form')


import urllib.request  



sing = mashupform.text_input(label='SINGER NAME:-')

nvid =  mashupform.text_input(label='NUMBER OF VIDEOS OF THE SINGER:-')

em = mashupform.text_input(label='YOUR EMAIL ID:-')

sub = mashupform.form_submit_button(label='SUBMIT')

PASSWORD = streamlit.secrets["PASSWORD"]

import re #provides regular expression support
from pytube import YouTube #for downloading YouTube Videos. 
#Create the object of the YouTube module by passing the link as the parameter. 

#FUNCTION TO RETRIEVE VALID VIDEOS' URLS
def retrieveValidVideos(singer):

    response = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + singer) 
    #urlopen() only reads the HTML doucment bytestream of body
    
    #11 digit id
    idOfVideos = re.findall(r"watch\?v=(\S{11})", response.read().decode()) 
       

    listVideos = ["https://www.youtube.com/watch?v=" + id for id in idOfVideos] #list of video urls


#exception handling 6- only validate those videos that are different.
    listVideos = list(set(listVideos)) 
    

    count = 1
    videos = [] #empty videos list
    for video in listVideos:
        if count > numberOfVideosInt:
            break
        instance = YouTube(video) #Instance contains (title, length, thumbnail-url, description, views, rating, age_restricted, video_id) 
        
        videos.append(video)
        count += 1
    return videos  #return the valid videos url list







#FUNCTION TO DOWNLOAD VIDEO FROM THE VALID VIDEO URL LIST
def downloadVideo(video):
    videodirectorypath = 'videos/' 

    instance = YouTube(video) 
    #youtube uses dash streaming method on http, so it adjusts the video quality based on your network speed.
    instance.streams.first().download(videodirectorypath)
        # .first() returns the highest quality stream
  



import imageio 
imageio.plugins.ffmpeg.download() 
#FFMPEG:- FFMPEG stands for Fast Forward Moving Picture Experts Group. 
from moviepy.editor import * 





#FUNCTION TO CONVERT THE DOWNLOADED VIDEOS TO THEIR CORRESPONDING AUDIO FILES, ONE BY ONE
def videoToAudioConversion():
   
    #get file names in directory
    videodirectorypath = os.getcwd()+"/videos/"
   

    filenames = []
    for filename in os.listdir(videodirectorypath):
            filenames.append(filename)
            if filename=="John Legend - All She Wanna Do (Audio).3gpp":
                os.remove(videodirectorypath + filename)
   
    audiodirectorypath = os.getcwd()+"/audios/" #define path
   
    count=1
    for filename in filenames:
        video = VideoFileClip(videodirectorypath+filename).subclip(0, int(durationOfFirstCut)) #clipping the video to the cut duration
        video.audio.write_audiofile(audiodirectorypath + str(count) + ".mp3") #.mp3 extension
        video.close()
        if filename=="100.mp3":
            os.remove(audiodirectorypath + filename)
        count += 1





#FUNCTION TO COMBINE THE AUDIOS TOGETHER AUDIOS 
def combineTogetherAllAudioFiles():
    audiodirectorypath = os.getcwd()+"/audios/"
    audioFile = audiodirectorypath + outputName
    
    if os.path.exists(audioFile):
        os.remove(audioFile)

    audios = os.listdir(audiodirectorypath)
    combinedAudio = concatenate_audioclips([AudioFileClip(audiodirectorypath+audio) for audio in audios])
    
    combinedAudio.write_audiofile(audioFile)
    
    combinedAudio.close()
    
    print("\nCOMBINED ALL AUDIO FILES TO " + outputName)



import zipfile 

#FUCNTION TO ZIP THE COMBINED AUDIO CLIP
def zipCombinedAudioClip():
    audiodirectorypath = os.getcwd()+"/audios/"
    audioFile =audiodirectorypath + outputName

    zipAudioFile = audioFile + ".zip" #adding the extension

    with zipfile.ZipFile(zipAudioFile, 'w') as finalZipFile:
        finalZipFile.write(audioFile)



import email, smtplib, ssl
#the 'email' package to read, write, and send simple email messages
from email import encoders 
from email.mime.base import MIMEBase 
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

    
def sendEmail(em, result_file) : 
    smtp_server = "smtp.gmail.com"
    sender_email = "parora_be20@thapar.edu"  
    receiver_email = em 

        
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
   
    message["Subject"] = "Mashup assignment - By Pranjal Arora, 102003402, zip audio file attachment "
    
    message.attach(MIMEText("Please find the attached zip audio file. Submission made by Pranjal Arora, 102003402, 3CO-16", "plain"))

    
    zip_file = "audios/" + outputName + ".zip"
    
    part = MIMEBase('application', "octet-stream")
    
    encoders.encode_base64(part)
    
    part.add_header(
        "Content-Disposition",
        f"attachment; filename={outputName+'.zip'}",
    )
    
        

    message.attach(part)
    text = message.as_string()

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, PASSWORD)
        server.sendmail(sender_email, receiver_email, text)
    
        singer = singerName.replace(' ', '+')
        num_of_videos = int(numberOfVideos)
        videos = retrieveValidVideos(singer)
        for video in videos:
           
            downloadVideo(video)
        videoToAudioConversion()
        combineTogetherAllAudioFiles()
        zipCombinedAudioClip()
        sendEmail(email, outputName)
        st.success('WE HAVE SUCCESSFULLY MAILED YOU THE AUDIO ZIP FILE, PLEASE CHECK YOU INBOX :)')
        

