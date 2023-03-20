import os 
import sys 
import streamlit as st 

st.header("MASHUP- by Pranjal Arora, 102003402, 3CO-16")
form = st.form(key='my_form')

singerName = form.text_input(label='SINGER NAME:-')
numberOfVideos =  form.text_input(label='NUMBER OF VIDEOS OF THE SINGER:-')
durationOfFirstCut = form.text_input(label='DURATION:-')
outputName = form.text_input(label='OUTPUT FILENAME:-')
email = form.text_input(label='YOUR EMAIL ID:-')
submit_button = form.form_submit_button(label='SUBMIT')

PASSWORD = st.secrets["PASSWORD"]
# passw="aeiou"

numberOfVideosInt = int(float(numberOfVideos))
singer = singerName.replace(' ', '+')

import urllib.request  

import re #provides regular expression support
from pytube import YouTube #for downloading YouTube Videos. 
#Create the object of the YouTube module by passing the link as the parameter. 


#FUNCTION TO RETRIEVE VALID VIDEOS' URLS
def retrieveValidVideos(singer):

    response = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + singer) #urllib.request() returns an HTTP message in bytes object form
    #urlopen() only reads the bytestream of body, that is the HTML document bytestream


    #for a youtube video url like this :- https://www.youtube.com/watch?v=XeSu9fBJ2sI, length of id is 11.
    idOfVideos = re.findall(r"watch\?v=(\S{11})", response.read().decode()) 
    #read() function- helps in reading an HTML file from a url, thats displayed on console in byte literal format
    #decode() function- convert the bytes object to a string. 
   

    listVideos = ["https://www.youtube.com/watch?v=" + id for id in idOfVideos] #list of video urls

    # print(len(listVideos)) #no. of urls found

#exception handling 6- only validate those videos that are different.
    listVideos = list(set(listVideos)) #set has unique elemnents
    # print(len(listVideos))

    count = 1
    videos = [] #empty videos list
    for video in listVideos:
        if count > numberOfVideosInt:
            break
        instance = YouTube(video) #Instance of the Youtube video object- contains information like (title, length, thumbnail-url, description, views, rating, age_restricted, video_id) 
        # if instance.length/60 < 7.00:  #.length() gives length of video in seconds
        videos.append(video)
        count += 1
    return videos  #return the valid videos url list







#FUNCTION TO DOWNLOAD VIDEO FROM THE VALID VIDEO URL LIST
def downloadVideo(video):
    videodirectorypath = 'videos/' 

    #if path doesn't exist then make the path
    if not os.path.exists(videodirectorypath): 
        os.makedirs(videodirectorypath)

    instance = YouTube(video) 
    #youtube uses dash streaming method on http, so it adjusts the video quality based on your network speed.
    try :
        instance.streams.first().download(videodirectorypath)
        # .first() returns the highest quality stream
    
    except :
        print("UNEXPECTED ERROR WHILE DOWNLOADING THE VIDEO")



import imageio 
imageio.plugins.ffmpeg.download() 
#FFMPEG:- FFMPEG stands for Fast Forward Moving Picture Experts Group. 
from moviepy.editor import * #video editing: cutting, concatenations


#FUNCTION TO CONVERT THE DOWNLOADED VIDEOS TO THEIR CORRESPONDING AUDIO FILES, ONE BY ONE
def videoToAudioConversion():
   
    #get file names in directory
    videodirectorypath = os.getcwd()+"/videos/"
    # print(videodirectorypath)

    filenames = []
    for filename in os.listdir(videodirectorypath):
            filenames.append(filename)
            if filename=="John Legend - All She Wanna Do (Audio).3gpp":
                os.remove(videodirectorypath + filename)
    print("LIST OF FILES CURRENTLY PRESENT IN THE DIRECTORY ARE:-")
    print(filenames)


    audiodirectorypath = os.getcwd()+"/audios/" #define path
    if not os.path.exists(audiodirectorypath): 
        os.makedirs(audiodirectorypath)

    
    count=1
    for filename in filenames:
        print("\nCURRENTLY CONVERTING THIS FILE:- ", filename)
        video = VideoFileClip(videodirectorypath+filename).subclip(0, int(durationOfFirstCut)) #clipping the video to the cut duration
        video.audio.write_audiofile(audiodirectorypath + str(count) + ".mp3")#converting the video to audio file, saving it with .mp3 extension
        video.close()
        # os.remove(videodirectorypath+filename) #remove the video after use
        if filename=="100.mp3":
            os.remove(audiodirectorypath + filename)
        count += 1





#FUNCTION TO COMBINE THE AUDIOS TOGETHER AUDIOS 
def combineTogetherAllAudioFiles():
    audiodirectorypath = os.getcwd()+"/audios/"
    audioFile = audiodirectorypath + outputName
    
    if os.path.exists(audioFile):
        os.remove(audioFile)

    for filename in os.listdir(audiodirectorypath):
        #remove any already present .zip files
        if filename.endswith(".zip"):
            os.remove(audiodirectorypath + filename)

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


    
def sendEmail(email, result_file) : 
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = "parora_be20@thapar.edu"  # Enter your address
    receiver_email = email  # Enter receiver address

        
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = "Mashup assignment - By Pranjal Arora, 102003402, zip audio file attachment "
    message.attach(MIMEText("Please find the attached zip audio file. Submission made by Pranjal Arora, 102003402, 3CO-16", "plain"))

    
    zip_file = "audios/" + outputName + ".zip"
    
    part = MIMEBase('application', "octet-stream")
    part.set_payload( open(zip_file,"rb").read() )
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
    
if submit_button:
    if singerName == '' or numberOfVideos == '' or durationOfFirstCut == '' or outputName == '' or email == '':
        st.warning('ENTER ALL FIELDS PLEASE')
    else:
        st.success('WE PROCESSING YOUR REQUEST..')
        if outputName.count('.') == 0:
            outputName += '.mp3'
        outputName.split('.')[-1] = 'mp3'
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
        

