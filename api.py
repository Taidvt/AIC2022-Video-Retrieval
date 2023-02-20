import json
import faiss
import Levenshtein
import numpy as np
import pickle
import torch
import open_clip
from open_clip import tokenizer
from flask import Flask, request, jsonify
from flask_cors import CORS

# from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

app = Flask(__name__)
CORS(app)
def setup_app(app):
    # All your initialization code
    print('Initialize Server')

    #For CLIP
    with open( '/mmlabworkspace/Students/AIC/ALL_3batch_CLIPFeatures.pkl', "rb") as f:
      image_features = pickle.load(f)
      
    model, _, preprocess = open_clip.create_model_and_transforms('ViT-B-16', pretrained='openai')
    model.eval()

    # Load translate model
    # model_name = "VietAI/envit5-translation"
    # tokenizer_vn = AutoTokenizer.from_pretrained(model_name)
    # translate_model = AutoModelForSeq2SeqLM.from_pretrained(model_name).cuda()


    #context_length = model.context_length
    #vocab_size = model.vocab_size
    
    feature_shape = 512
    res = faiss.StandardGpuResources()
    flat_config = faiss.GpuIndexFlatConfig()
    flat_config.device = 0
    #index = faiss.IndexFlatL2(512)
    index = faiss.GpuIndexFlatL2(res, feature_shape, flat_config)
    index.add(image_features)
    k = 100
    #k=20
    
    #For OCR
    f = open("/mmlabworkspace/Students/AIC/ALL_3batch_OCR_Metadata.json")
    data_ocr = json.load(f)
    f.close()


    f = open("/mmlabworkspace/Students/AIC/ALL_3batch_metadata.json")
    data_vbs = json.load(f)
    f.close()

    f = open('/mmlabworkspace/Students/AIC/Data_Batch3/keyframe_p_batch3/keyframe_p/result_batch1_2_3.json', 'r')
    frame_id_mapping = json.load(f)
    f.close()

    return model, index, data_ocr,data_vbs, k, frame_id_mapping #tokenizer_vn, translate_model
    
# model, index, data_ocr, k, tokenizer_vn, translate_model = setup_app(app)
model, index, data_ocr, data_vbs, k, frame_id_mapping = setup_app(app)


def load_video(id,mode):
  # assume id is string (int) type
    id = str(int(id) + 1)
 
    #   keyframe_name = data_vbs[id]["keyframe_name"]
    video_name = data_vbs[id]["video_id"]
  #   image_name = data_vbs[id]["image_name"]
    try:
      f = open('/mmlabworkspace/Students/AIC/metadata/'+  "Metadata_"+video_name[0:7]+"/" + video_name+".json")
      data = json.load(f)
      url = data["watch_url"]
    except:
      url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    return url


    # if mode == "caption":
    #     id = str(int(id) + 1)
    # #   keyframe_name = data_vbs[id]["keyframe_name"]
    #     video_name = data_vbs[id]["video_id"]
    # #   image_name = data_vbs[id]["image_name"]
    #     prefix, postfix = video_name.split('_')
    #     if int(postfix[1:]) < 100:
    #         video_path = "/mmlabworkspace/Students/AIC/Data_Batch1/Video/" + \
    #             "Video" + prefix + "_V00/" + video_name + ".mp4"
    #     elif int(postfix[1:])>=100 and int(postfix[1:])<=199:
    #         video_path = "/mmlabworkspace/Students/AIC/Data_Batch2/Video/" + \
    #             "Video" + prefix + "_V01/" + video_name + ".mp4"
    #     else:
    #         video_path = "/mmlabworkspace/Students/AIC/Data_Batch3/Video" + \
    #             video_name[:-2] + "/" + video_name+ ".mp4"
        


def load_image(id, mode):
    # assume id is string (int) type
    if mode == "caption":
        id = str(int(id) + 1)
        # keyframe_name = data_vbs[id]["keyframe_name"]
        # video_name = data_vbs[id]["video_id"]
        # image_name = data_vbs[id]["image_name"]
        # if int(id) - 1 < 226636:
        if len(data_vbs[id])==3:
            image_path = '/3Batch_KeyFrames/'+data_vbs[id]['keyframe_id']+'/'+ data_vbs[id]['video_id'] +'/'+ data_vbs[id]['image_name']
        else:
        # except:
            image_path = '/Data_Batch3/KeyFrame_extractByCV/' + data_vbs[id]['video_id'] +'/' + data_vbs[id]['image_name']
    elif mode == "ocr":
        video_name = data_ocr[id]["video_name"]
        image_name = data_ocr[id]["image_name"]
        # image_path = "/mmlabworkspace/Students/AIC/3Batch_KeyFrames/" + video_name[:6] + "/" + video_name
        image_path = "/Data_Batch3/KeyFrame_extractByCV/" + video_name + "/"+ image_name
    return image_path
    

    # image_folder = '/home/tuanld/AIC/Data_Batch1/KeyFrame/' + \
    #     keyframe_name+'/' + video_name
    # image_path = ('/home/tuanld/AIC/Data_Batch1/KeyFrame/' +
    #               data_vbs[id]['keyframe_name']+'/' + data_vbs[id]['video_id'] + '/' + data_vbs[id]['image_name'])
   

def get_timecode(frame_id, fps):
    timecode = (int(frame_id) / fps)
    return int(timecode)




@app.route("/process", methods = ["POST","GET"])
def result():
  # query_input = request.data  # OCR input
  res = json.loads(request.data.decode("utf-8"))
  query = res.get("query")
  # query = translateVi2En(query)
  print(query)

  mode = res.get("mode")
  mode_ocr = "visual"
  score = 0.85
  
  if mode == "ocr":
    indeces = []
    query = query.split('&')
    print('after split: ',query)
    for i in data_ocr:
      true_q = 0
      for j in data_ocr[i]['words']:    
          for num_q in query:
              #if this is visual mode, we have to check whether the query is greater than score or not
              if mode_ocr == "visual":
                  #print("visual")
                  if num_q[0] == '"':
                      num_q = num_q[1:-1]
                      #if (Levenshtein.ratio(num_q, j)) == 1:
                      if num_q == j.lower(): 
                          true_q += 1
                  else:
                      #print("not 100%")
                      if ((Levenshtein.ratio(num_q, j.lower())) >= score) or ( num_q in j.lower()):
                          true_q += 1
                          #print("added")
              #break
          #break
    
              
              # if this is textual mode, we just check whether query is in description or not
              # elif mode_ocr == "textual":
              #     if num_q in j:
              #         true_q += 1
      
      # In the visual mode case, if true_q == len(query) => it's the index of keyframe that we seek
      # In the textual mode case, if true_q >= len(query), it means that the query in the description equal or more than len(query) times
      if true_q >= len(query):    
          indeces.append(i)
      #break
    
          
    # return json.dumps(indeces)
    payload=[]
    for ind in indeces:
      image_path = load_image(ind, mode)
      url = load_video(ind,mode)
      id_video = url.split('=')[1]
      payload.append({"image_path":image_path,
                      "id_video":id_video})
  
  elif mode == "caption":
    text_tokens = tokenizer.tokenize([query])
    with torch.no_grad():
      text_features = model.encode_text(text_tokens).float()
      text_features /= text_features.norm(dim=-1, keepdim = True)
      text_features = text_features.cpu().numpy()
      
    D,I = index.search(text_features, k)
    
    I = I.tolist()
    I = I[0]
    # print("I", I)

    payload=[]
    for ind in I:
      image_path = load_image(ind, mode)
      url = load_video(ind,mode)
      id_video = url.split('=')[1]
      payload.append({"image_path":image_path,
                      "id_video":id_video})

  # res = json.dumps(payload)
  # print(jsonify(res))
  
  return jsonify(payload)


# @app.route("/process_FAISS", methods = ["POST","GET"])
# def result():
#     query = request.json["query"]
#     print(query)
    
#     data = {"id": "1", "title": "2"}
#     resp = jsonify(data)
#     resp.status_code = 200
#     print(resp)
#     return resp 

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, port=2021,threaded=True)
    # print("here")
