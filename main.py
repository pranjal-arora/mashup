import urllib.request  #The urllib.request module defines functions and classes which help in opening URLs (mostly HTTP) - authentication, redirections, cookies and more.
import re #provides reguslar expression support
from pytube import YouTube #downloading YouTube Videos. Create the object of the YouTube module by passing the link as the parameter. Then, get the appropriate extension and resolution of the video. After that, download the file using the download function which has one parameter which is the location where to download the file.

import os #OS module in Python helps interact with underlying os. provides functions for creating and removing a directory (folder), fetching its contents, changing and identifying the current directory, etc. 
import imageio #Imageio is a Python library that provides an easy interface to read and write a wide range of image data, including animated images, video, volumetric data, and scientific formats. 
imageio.plugins.ffmpeg.download() #Read/Write video frames using FFMPEG(external software to process multimedia files) thorugh pipes. The ffmpeg format provides reading and writing for a wide range of movie formats such as .avi, .mpeg, .mp4, etc. as well as the ability to read streams from webcams and USB cameras. It is based on moviepy.
#FFMPEG:- FFMPEG stands for Fast Forward Moving Picture Experts Group. It is a free and open source software project that offers many tools for video and audio processing. It's designed to run on a command line interface, and has many different libraries and programs to manipulate and handle video files
from moviepy.editor import *  #MoviePy (full documentation) is a Python library for video editing: cutting, concatenations, title insertions, video compositing (a.k.a. non-linear editing), video processing, and creation of custom effects. 
import sys #provides various functions and variables that are used to manipulate different parts of the Python runtime environment.
import streamlit as st #Streamlit is an open source app framework in Python language. It helps us create web apps for data science and machine learning in a short time. With Streamlit, no callbacks are needed since widgets are treated as variables. Data caching simplifies and speeds up computation pipelines. Streamlit watches for changes on updates of the linked Git repository and the application will be deployed automatically in the shared link.
import zipfile #manipulates zip file,  It supports decryption of encrypted files in ZIP archives,
import email, smtplib, ssl
#the 'email' package to read, write, and send simple email messages, as well as more complex MIME(Multipurpose Internet Mail Extension(extension of the original Simple Mail Transport Protocol (SMTP) email protocol.)) messages.
#smtplib - for the actual sending function. SMTP client session object that can be used to send mail to any internet machine with an SMTP listener daemon
#ssl- secure socket layer encryption and peer authentication for network sockets both on client-side and server-side. It uses cryptography and message digests to secure data and detect alteration attempts in the network.
from email import encoders # provides encoders used by MIMEAudio and MIMEImage class to provide default encodings. These extract the payload, encode the message and reset the paylaod to this newly encoded value
from email.mime.base import MIMEBase #This is the base class for all the MIME-specific subclasses of Message
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

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

        if instance.length/60 < 7.00:  #.length() gives length of video in seconds
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






#FUNCTION TO CONVERT THE DOWNLOADED VIDEOS TO THEIR CORRESPONDING AUDIO FILES, ONE BY ONE
def videoToAudioConversion():
   
    #get file names in directory
    videodirectorypath = os.getcwd()+"\\videos\\"
    # print(videodirectorypath)

    filenames = []
    for filename in os.listdir(videodirectorypath):
            filenames.append(filename)
    print("LIST OF FILES CURRENTLY PRESENT IN THE DIRECTORY ARE:-")
    print(filenames)

    audiodirectorypath = os.getcwd()+"\\audios\\" #define path
    if not os.path.exists(audiodirectorypath): 
        os.makedirs(audiodirectorypath)

    count=1
    for filename in filenames:
        print("\nCURRENTLY CONVERTING THIS FILE:- ", filename)
        video = VideoFileClip(videodirectorypath+filename).subclip(0, int(durationOfFirstCut)) #clipping the video to the cut duration
        video.audio.write_audiofile(audiodirectorypath + str(count) + ".mp3")#converting the video to audio file, saving it with .mp3 extension
        video.close()
        os.remove(videodirectorypath+filename) #remove the video after use
        count += 1





#FUNCTION TO COMBINE THE AUDIOS TOGETHER AUDIOS 
def combineTogetherAllAudioFiles():
    audiodirectorypath = os.getcwd()+"\\audios\\"
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






#FUCNTION TO ZIP THE COMBINED AUDIO CLIP
def zipCombinedAudioClip():
    audiodirectorypath = os.getcwd()+"\\audios\\"
    audioFile =audiodirectorypath + outputName

    zipAudioFile = audioFile + ".zip" #adding the extension

    with zipfile.ZipFile(zipAudioFile, 'w') as finalZipFile:
        finalZipFile.write(audioFile)





    
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
        

