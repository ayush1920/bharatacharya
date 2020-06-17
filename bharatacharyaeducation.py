# downloader
import urllib.request
import urllib.error as error
import os
import multithread as mt
import sys

global failed_list, trigger,count
# thread limit
thread_limit = 20

def download(cnt,url,var,inp):
    global failed_list, trigger, count
    if var==0:
        loc = "download/"+inp+"/audio/"
    elif var==1:
        loc = "download/"+inp+"/video/"
    else:
        print("Var error")
        sys.exit()
        
    try:
        url = url.replace("seg_id",str(cnt))
        urllib.request.urlretrieve(url,loc+"part"+str(cnt)+".m4s")
        print(cnt,end=",")
    except error.HTTPError as err:
        if err.code == 403:
            print("Finished downloading parts.")
            trigger = False
            if cnt<count:
                count = cnt
            sys.exit()
        else:
            print("Some error occured.")
            failed_list.append(cnt)
            sys.exit()
    except:
            print("Some error occured.")
            failed_list.append(cnt)
            sys.exit()

def start(inp,ql=str(3)):
    print('''
    =============================================================
                    Downloading - '''+str(inp)+'''
    =============================================================
''')
    global count
    global trigger
    global failed_list
    inp=str(inp)
    audio_lang="en"    
    # video - quality
    '''
    1 - 240p
    2 - 360p
    3 - 480p
    4 - 540p
    '''
    count = 9999
    failed_list = []
    trigger = True
    if not os.path.isdir("download"):
        os.mkdir("download")
    if not os.path.isdir("download/"+inp):
        os.mkdir("download/"+inp)
    if not os.path.isdir("download/"+inp+"/audio"):
        os.mkdir("download/"+inp+"/audio")
    if not os.path.isdir("download/"+inp+"/video"):
        os.mkdir("download/"+inp+"/video")


    mt.setlimit(thread_limit)            
    # var 0 for audio
    # var 1 for video

    # download audio
    # download init_file
    opener = urllib.request.build_opener()
    opener.addheaders = [("User-Agent" , "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246")]
    urllib.request.install_opener(opener)
    
    try:
        urllib.request.urlretrieve("https://bae.sgp1.digitaloceanspaces.com/videos/"+inp+"/dash/audio/"+audio_lang+"/mp4a/init.mp4","download/"+inp+"/audio/init.mp4")
    except error.HTTPError as err:
        if err.code == 403:
            print("changing language")
            audio_lang="und"
            urllib.request.urlretrieve("https://bae.sgp1.digitaloceanspaces.com/videos/"+inp+"/dash/audio/"+audio_lang+"/mp4a/init.mp4","download/"+inp+"/audio/init.mp4")
    url_audio= ("https://bae.sgp1.digitaloceanspaces.com/videos/video_id/dash/audio/"+audio_lang+"/mp4a/seg-seg_id.m4s").replace("video_id",inp)
    
    cnt = 1
    while trigger:
        mt.init(download,[cnt,url_audio,0,inp])
        cnt=cnt+1  
    mt.checkfinished()
    " Log for errors"
    file  = open("download/"+inp+"/audio/audio_file_error.log","w+")
    file.write(str(failed_list))
    file.close()
    print("Error List - Audio\n",failed_list)
    failed_list = []

    # download video
    # download init_file
    try:
        urllib.request.urlretrieve("https://bae.sgp1.digitaloceanspaces.com/videos/"+inp+"/dash/video/avc1/"+ql+"/init.mp4","download/"+inp+"/video/init.mp4")
    except error.HTTPError as err:
        if err.code == 403:
            ql=str(2)
            urllib.request.urlretrieve("https://bae.sgp1.digitaloceanspaces.com/videos/"+inp+"/dash/video/avc1/"+ql+"/init.mp4","download/"+inp+"/video/init.mp4")
    url_video= ("https://bae.sgp1.digitaloceanspaces.com/videos/video_id/dash/video/avc1/quality/seg-seg_id.m4s".replace("quality",ql)).replace("video_id",inp)        
    cnt = 1
    trigger = True
    while trigger:
        mt.init(download,[cnt,url_video,1,inp])
        cnt=cnt+1
    mt.checkfinished()
    " Log for errors"
    file  = open("download/"+inp+"/video/video_file_error.log","w+")
    file.write(str(failed_list))
    file.close()

    count = count-1
    print("Total no of parts -",count)
    print("Error List - Video\n",failed_list)

    import subprocess
    import time

    print("\n-- MERGING AUDIO --")
    if(os.path.isfile("download/"+inp+"/audio/source.mp4")):
        os.remove("download/"+inp+"/audio/source.mp4")
    in_file = open("download/"+inp+"/audio/init.mp4", "rb")
    data = in_file.read()   
    in_file.close()
    out_file = open("download/"+inp+"/audio/source.mp4", "ab+")
    out_file.write(data)
    out_file.close()
    for i in range(1,count+1):
        in_file = open("download/"+inp+"/audio/part"+str(i)+".m4s", "rb")
        data = in_file.read()   
        in_file.close()
        out_file = open("download/"+inp+"/audio/source.mp4", "ab+")
        out_file.write(data)
        out_file.close()
        print(i,end=",")

    print("\n-- MERGING VIDEO --")
    if(os.path.isfile("download/"+inp+"/video/source.mp4")):
        os.remove("download/"+inp+"/video/source.mp4")
    in_file = open("download/"+inp+"/video/init.mp4", "rb")
    data = in_file.read()   
    in_file.close()
    out_file = open("download/"+inp+"/video/source.mp4", "ab+")
    out_file.write(data)
    out_file.close()
    for i in range(1,count+1):
        in_file = open("download/"+inp+"/video/part"+str(i)+".m4s", "rb")
        data = in_file.read()   
        in_file.close()
        out_file = open("download/"+inp+"/video/source.mp4", "ab+")
        out_file.write(data)
        out_file.close()
        print(i,end=",")

        
    print("\n-- MERGING AUDIO AND VIDEO --")
    if (os.path.isfile('download/'+inp+'.mp4')):
        os.remove('download/'+inp+'.mp4')
    cmd = 'ffmpeg -i '+"download/"+inp+"/video/source.mp4"+" -i "+"download/"+inp+"/audio/source.mp4"+' -c copy '+'download/'+inp+'.mp4'
    subprocess.call(cmd, shell=True)# "Muxing Done
    print('Muxing Done')
    print('Deleting part files directory') 
    import shutil
    shutil.rmtree('download/'+inp)
for i in [44, 45, 46, 47, 48, 49, 50, 51, 52]:
    start(i)
# --------------------- EXCEPTIONS ----------------------------
#   1. language en and und
#   2. Some videos are available in 320p only 2
#   3. download - Last part error


"""
865
https://bae.sgp1.digitaloceanspaces.com/videos/31/dash/video/avc1/3/init.mp4
https://bae.sgp1.digitaloceanspaces.com/videos/31/dash/audio/"+audio_lang+"/mp4a/init.mp4

https://bae.sgp1.digitaloceanspaces.com/videos/31/dash/audio/"+audio_lang+"/mp4a/seg-8.m4s
https://bae.sgp1.digitaloceanspaces.com/videos/31/dash/video/avc1/1/seg-7.m4s

avc -1
https://bae.sgp1.digitaloceanspaces.com/videos/146/dash/video/avc1/1/seg-7.m4s 
avc-4
https://bae.sgp1.digitaloceanspaces.com/videos/31/dash/video/avc1/4/seg-7.m4s

"""
