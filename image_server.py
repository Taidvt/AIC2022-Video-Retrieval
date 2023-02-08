from sys import prefix
from flask import Flask, send_file, request
import os
import random
import csv
import time
import json
import cv2
import requests

app = Flask(__name__)

root = '/storageStudents/Dataset/VBS'


def setup_app(app):
    f = open("/mmlabworkspace/Students/AIC/ALL_3batch_metadata.json")
    data_vbs = json.load(f)
    f.close()
    f = open("/mmlabworkspace/Students/AIC/ALL_3batch_OCR_Metadata.json")
    data_ocr = json.load(f)
    f.close()
    return data_vbs, data_ocr


data_vbs, data_ocr = setup_app(app)


def load_image(id, mode):
    # assume id is string (int) type
    if mode == "caption":
        id = str(int(id) + 1)
        # keyframe_name = data_vbs[id]["keyframe_name"]
        # video_name = data_vbs[id]["video_id"]
        # image_name = data_vbs[id]["image_name"]
        # if int(id) - 1 < 226636:
        if len(data_vbs[id])==3:
            image_path = '/mmlabworkspace/Students/AIC/3Batch_KeyFrames/'+data_vbs[id]['keyframe_id']+'/'+ data_vbs[id]['video_id'] +'/'+ data_vbs[id]['image_name']
        else:
        # except:
            image_path = '/mmlabworkspace/Students/AIC/Data_Batch3/KeyFrame_extractByCV/' + data_vbs[id]['video_id'] +'/' + data_vbs[id]['image_name']
    elif mode == "ocr":
        video_name = data_ocr[id]["video_name"]
        image_name = data_ocr[id]["image_name"]
        # image_path = "/mmlabworkspace/Students/AIC/3Batch_KeyFrames/" + video_name[:6] + "/" + video_name
        image_path = "/mmlabworkspace/Students/AIC/Data_Batch3/KeyFrame_extractByCV/" + video_name + "/"+ image_name
    return image_path
    

    # image_folder = '/home/tuanld/AIC/Data_Batch1/KeyFrame/' + \
    #     keyframe_name+'/' + video_name
    # image_path = ('/home/tuanld/AIC/Data_Batch1/KeyFrame/' +
    #               data_vbs[id]['keyframe_name']+'/' + data_vbs[id]['video_id'] + '/' + data_vbs[id]['image_name'])
   

def get_timecode(frame_id, fps):
    timecode = (int(frame_id) / fps)
    return int(timecode)

@app.route("/getClipID2")
def get_clip_id_vbs2():
    id = request.args.get("id")
    mode = request.args.get("mode")
    new_frame_id = request.args.get("new_frame_id")
    if mode == "caption":
        id = str(int(id) + 1)
    #   keyframe_name = data_vbs[id]["keyframe_name"]
        video_name = data_vbs[id]["video_id"]
    #   image_name = data_vbs[id]["image_name"]
        prefix, postfix = video_name.split('_')
        if int(postfix[1:]) < 100:
            video_path = "/mmlabworkspace/Students/AIC/Data_Batch1/Video/" + \
                "Video" + prefix + "_V00/" + video_name + ".mp4"
        elif int(postfix[1:])>=100 and int(postfix[1:])<=199:
            video_path = "/mmlabworkspace/Students/AIC/Data_Batch2/Video/" + \
                "Video" + prefix + "_V01/" + video_name + ".mp4"
        else:
            video_path = "/mmlabworkspace/Students/AIC/Data_Batch3/Video" + \
                video_name[:-2] + "/" + video_name+ ".mp4"
        
    elif mode == "ocr":

        id = str(int(id) + 1)
        video_name = data_ocr[id]["video_name"]
        # image_name = data_ocr[id]["image_name"]
        prefix, postfix = video_name.split('_')
        if int(postfix[1:]) < 100:
            video_path = "/mmlabworkspace/Students/AIC/Data_Batch1/Video/" + \
                "Video" + prefix + "_V00/" + video_name + ".mp4"
        elif int(postfix[1:])>=100 and int(postfix[1:])<=199:
            video_path = "/mmlabworkspace/Students/AIC/Data_Batch2/Video/" + \
                "Video" + prefix + "_V01/" + video_name + ".mp4"
        else:
            video_path = "/mmlabworkspace/Students/AIC/Data_Batch3/Video" + \
                video_name[:-2] + "/" + video_name+ ".mp4"
    video = cv2.VideoCapture(video_path)
    fps = video.get(cv2.CAP_PROP_FPS)

#    clip_id = image_folder.split('/')[1]
#    timecode, frame_idx, shot= get_timecode(image_folder, image_name)

#    return json.dumps({"clip_id": clip_id,"image_folder" : image_folder,  "timecode": timecode, "frame_idx": frame_idx, "shot":shot})
    
    return json.dumps({"clip_id": video_name, "video_path": video_path, "timecode": get_timecode(new_frame_id,fps=fps)})


@app.route("/getImage")
def login():
    # mode = 1 là caption
    # mode = 2 là ocr
    id = request.args.get("id")
    mode = request.args.get("mode")
    image = load_image(id, mode)
    return send_file(image, mimetype='image/png')

@app.route("/getVideo")
def playVideo():
    video_name = request.args.get("video_name")
    print(video_name)
    prefix, postfix = video_name.split('_')
    if int(postfix[1:]) < 100:
        video_path = "/mmlabworkspace/Students/AIC/Data_Batch1/Video/" + \
            "Video" + prefix + "_V00/" + video_name + ".mp4"
    elif int(postfix[1:])>=100 and int(postfix[1:])<=199:
        video_path = "/mmlabworkspace/Students/AIC/Data_Batch2/Video/" + \
            "Video" + prefix + "_V01/" + video_name + ".mp4"
    else:
        video_path = "/mmlabworkspace/Students/AIC/Data_Batch3/" + \
            + prefix + "_"+ postfix[:3] +video_name+ ".mp4"
    print(video_path)
    return send_file(video_path, mimetype='image/mp4')

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, port=2023,threaded=True)
