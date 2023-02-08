import json
import faiss
import Levenshtein
import numpy as np
import pickle
import torch
import open_clip
from open_clip import tokenizer
from flask import Flask, request, jsonify
# from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

app = Flask(__name__)

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
    k = 1000
    #k=20
    
    #For OCR
    f = open("/mmlabworkspace/Students/AIC/ALL_3batch_OCR_Metadata.json")
    data_ocr = json.load(f)
    f.close()
    return model, index, data_ocr, k, #tokenizer_vn, translate_model
    
# model, index, data_ocr, k, tokenizer_vn, translate_model = setup_app(app)
model, index, data_ocr, k, = setup_app(app)

# def translateVi2En(input_sentence):
#   return tokenizer_vn.batch_decode(translate_model.generate(tokenizer_vn(input_sentence, return_tensors="pt", padding=True).input_ids.cuda(), max_length=128), skip_special_tokens=True)[0][3:]
  
@app.route("/process", methods = ["POST","GET"])
def result():
  # query_input = request.data  # OCR input
  query = request.json["query"]
  # query = translateVi2En(query)
  print(query)

  mode = request.json["mode"]
  mode_ocr = "visual"
  score = 0.85
  
  if mode == "ocr":
    indeces = []
    query = query.split('&')
    for i in data_ocr:
      true_q = 0
      for j in data_ocr[i]['words']:    
          for num_q in query:
              #if this is visual mode, we have to check whether the query is greater than score or not
              if mode_ocr == "visual":
                  if num_q[0] == '"':
                      num_q = num_q[1:-1]
                      #if (Levenshtein.ratio(num_q, j)) == 1:
                      if num_q == j: 
                          true_q += 1
                  else:
                      if ((Levenshtein.ratio(num_q, j)) >= score) or ( num_q in j):
                          true_q += 1
              
              # if this is textual mode, we just check whether query is in description or not
              # elif mode_ocr == "textual":
              #     if num_q in j:
              #         true_q += 1
      
      # In the visual mode case, if true_q == len(query) => it's the index of keyframe that we seek
      # In the textual mode case, if true_q >= len(query), it means that the query in the description equal or more than len(query) times
      if true_q >= len(query):    
          indeces.append(i)
          
    return json.dumps(indeces)
  
  elif mode == "caption":
    text_tokens = tokenizer.tokenize([query])
    with torch.no_grad():
      text_features = model.encode_text(text_tokens).float()
      text_features /= text_features.norm(dim=-1, keepdim = True)
      text_features = text_features.cpu().numpy()
      
    D,I = index.search(text_features, k)
    
    I = I.tolist()
    I = I[0]
    print("I", I)
    return json.dumps(I)


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
    app.run(host="0.0.0.0", debug=False, port=2021,threaded=True)
    # print("here")
