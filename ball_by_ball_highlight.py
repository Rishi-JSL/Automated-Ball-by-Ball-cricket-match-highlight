from ast import pattern
import cv2
import subprocess as sp
# import required libraries
from vidgear.gears import CamGear
import cv2
import re
import pytesseract
import time
import csv 
from csv import writer


def current_time_mile_sec():
    return str(round(time.time() * 1000))

# testing match link
url1 = "https://www.youtube.com/watch?v=cNmCmyBE4dY"
url2 = "https://www.youtube.com/watch?v=qGYDnaCUNT4"
chirag_stream = "https://www.youtube.com/watch?v=ttNCGKit2No"
tnca_match = "https://www.youtube.com/watch?v=FzpOmY5cl_A"

# global variable

# set desired quality as 720p
options = {"STREAM_RESOLUTION": "720p"}


width = 1280
height = 720
fps = 60
seq = 0
current_over = 0.0
match_id = 3456664
time_now = current_time_mile_sec()
hl_name = 'vid_M_id-{}_{}_{}.mp4'.format(match_id, seq, current_over) # vid_{timeInMileSecond}_M_id-{matchId}_{sequence}_{current_over}


stream = CamGear(
    source='https://www.youtube.com/watch?v=3cWJ_7nhEnY',
    stream_mode=True,
    # y_tube =True,
    # time_delay=1,
    logging=True,
    **options
).start()



def updating_file():
    # match_id / current innings / current over / filename
    highlight_data = [match_id,1,current_over,hl_name]
    # List 
    print(type(highlight_data))
    # Open our existing CSV file in append mode 
    # Create a file object for this file
    with open('{}.csv'.format(match_id), 'a') as f_object:
  
        # Pass this file object to csv.writer()
        # and get a writer object
        writer_object = writer(f_object)
  
        # Pass the list as an argument into
        # the writerow()
        writer_object.writerow(highlight_data)
  
        #Close the file object
        f_object.close()

def compress_video(file_name):
    updating_file()
    trim_command = ['ffmpeg', 
			        '-i', file_name, 
			        '-vcodec', 'libx264', 
			    'hl\{}'.format(file_name)
			]
    trim_process = sp.Popen(trim_command)


def extract_text_from_image(img, co):
    text = pytesseract.image_to_string(img)
    # txt = "B /3 (6.5 ov)"
    pattern = r'(\d*[.,]\d?)'
    x = re.findall(pattern, text)
    print(text)
    # return co
    # print("test : ",text.split()[1][1:])
    try:
        print(x[0], co)
        # split on space and return the value the over value
        return float(x[0])
    except:
        print("extracted over is not float : ", text, x)
        return co
    # return float(text.split()[0][1:]) # split on space and return the value the over value

# global variable 
fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
video = cv2.VideoWriter(hl_name, fourcc, fps, (width, height))

# test = stream.read()
# test_r = test[640:690, 280:420, 0:3]  # for 720p stream
# cv2.imshow('full', test)
# cv2.imshow('croped', test_r)
# cv2.waitKey(0)
# print(test.shape)
# current_over = extract_text_from_image(test, 0)

current_over = 0.0
# print(current_over)

i = 0
j = 0

# loop over
while True:
    # read frames from stream
    frame = stream.read()

    # check for frame if Nonetype
    if frame is None:
        break

    # {do something with the frame here}

    # crop = frame[625:675, 345:520, 0:3] # mobile theam
    # crop = frame[625:675, 360:450, 0:3] # tnca match
    crop = frame[640:690, 280:420, 0:3] # glass theam
    # crop = cv2.resize(crop, (0,0), fx=3, fy=3)

    if (j % fps == 0):
        over = extract_text_from_image(crop, current_over)
        if over != current_over and over > current_over: # for extracting wrong data
            video.write(frame)
            video.release()
            compress_video(hl_name)
            # creating new hl video 
            current_over = over
            hl_name = 'vid_M_id-{}_{}_{}.mp4'.format(match_id, seq, current_over)
            seq = seq + 1

            video = cv2.VideoWriter(hl_name, fourcc, fps, (width, height))
            print("video saved", over)
            continue
        # print("value added successully", frame[10][10])

    video.write(frame)
    j = j + 1
    # print(j)

    # Show output window
    # cv2.imshow("Output", frame)
    cv2.imshow("Output", crop)

    # check for 'q' key if pressed
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

# close output window
cv2.destroyAllWindows()
# exit()
print(i)
video.release()
compress_video(hl_name)
# safely close video stream
stream.stop()




