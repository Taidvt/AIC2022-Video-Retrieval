import pickle
import open_clip
from open_clip import tokenizer
import numpy as np
import os
from PIL import Image
import numpy as np
import torch
import json
from tqdm import tqdm
import pandas as pd
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True
from PIL import UnidentifiedImageError
# import faiss
import time

def transform_Images_to_FeatureVector(model, images):
  image_input = torch.tensor(np.stack(images)).cuda()
  with torch.no_grad():
    image_features = model.encode_image(image_input).float()
  image_features /= image_features.norm(dim=-1, keepdim=True)
  print(image_features.shape)
  print(type(image_features))
  return image_features

def processing(model, preprocess):
    '''
    this function is used to extract image features from keyframes cut by ourselves
    '''
    images_transform = []
    dict_ = {}

    dir_path = '/mmlabworkspace/Students/AIC/Flickr8k/images/Images'
    img_list = os.listdir(dir_path)
    img_list.sort()
    print(len(img_list))
    for j in range(8):
      print("lan thu: {}".format(j+1))
      if j == 7:
            sub_img_list = img_list[j*1000:]
      else:
        sub_img_list = img_list[j * 1000:(j+1)*1000]
      print("lan thu: {} voi do dai cua img_list: {}".format(j, len(sub_img_list)))
      for i in tqdm(range(len(sub_img_list))):
        # print("iter {}".format((j*1000)+i))
        # dict_[(j*1000) + i] = img_list[j*1000+i]
        path = os.path.join(dir_path,img_list[j*25+i])
        try:
          image = Image.open(path).convert("RGB")
          images_transform.append(preprocess(image))
          del image 
          del path
        except UnidentifiedImageError:
          print('image error')
          images_transform.append(torch.zeros([3, 224, 224]))
      print(len(images_transform))                                
      image_features = transform_Images_to_FeatureVector(model, images_transform)
      numpy_host = image_features.cpu().numpy()               
      print('transform_Images_to_FeatureVector.....done!')                                
      del images_transform
      images_transform = []             
    
      save_name = '/mmlabworkspace/Students/AIC/Flickr8k_npy/clip_R_101/flickr8k_image_fetures_{}.npy'.format(j+1)                          
      with open(save_name, "wb") as fOut:
          np.save(fOut, numpy_host)
      del image_features
    # dict_save_name = '/mmlabworkspace/Students/AIC/flickr8k_idx2img.json'
    # with open(dict_save_name, 'w') as fOut_:
      # json.dump(dict_, fOut_, indent=4)
  
def concat():
  '''
  this function is used to concatenate image features files.
  '''
  folder_path = "/mmlabworkspace/Students/AIC/Flickr8k_npy/clip_R_101"
  file_list = os.listdir(folder_path)
  file_list.sort()
  for i in range(8):
    file_name = f"flickr8k_image_fetures_{i+1}.npy"
    file_path = os.path.join(folder_path, file_name)
    print(file_path, i)
    if i == 0:
        feature = np.load(file_path)
    else:
        feature_ = np.load(file_path)
        feature = np.concatenate((feature, feature_), axis = 0)
  print(feature.shape)
  np.save(os.path.join(folder_path, 'flickr8k_R101.npy'), feature)


def eval_on_flickr8k(a2b_sims, return_ranks=True):
    """
    Args:
        a2b_sims: Result of computing similarity between two sets of embeddings (emb1 @ emb2.T)
            with shape (num_datapoints, num_datapoints).

    Returns:
        Retrieval metrics for that similarity.
    """
    npts = a2b_sims.shape[0]
    ranks = np.zeros(npts)
    top1 = np.zeros(npts)
    # loop source embedding indices
    for index in range(npts):
        gt = index//5
        # print(gt)
        # get order of similarities to target embeddings
        inds = np.argsort(a2b_sims[index])[::-1]
        # print(inds.shape)
        # find where the correct embedding is ranked
        where = np.where(inds == gt)
        # print('hello: ',where[0])
        rank = where[0][0]
        # print('hi: ',rank)
        ranks[index] = rank
        # save the top1 result as well
        top1[index] = inds[0]

    # Compute metrics
    r1 = 100.0 * len(np.where(ranks < 1)[0]) / len(ranks)
    r5 = 100.0 * len(np.where(ranks < 5)[0]) / len(ranks)
    r10 = 100.0 * len(np.where(ranks < 10)[0]) / len(ranks)
    r50 = 100.0 * len(np.where(ranks < 50)[0]) / len(ranks)
    medr = np.floor(np.median(ranks)) + 1
    meanr = ranks.mean() + 1

    report_dict = {"r1": r1, "r5": r5, "r10": r10, "r50": r50, "medr": medr, "meanr": meanr, "sum": r1 + r5 + r10}

    if return_ranks:
        return report_dict, (ranks, top1)
    else:
        return report_dict

def read_groundtruth():
  file_path = "/mmlabworkspace/Students/AIC/Flickr8k/captions.txt"
  captions = pd.read_csv(file_path)
  with open("/mmlabworkspace/Students/AIC/flickr8k_img2idx.json", "r") as fIn:
    img2idx = json.load(fIn)
  ground_truth_indices = [int(img2idx[i]) for i in list(captions['image'])] 
  return ground_truth_indices, (list(captions['caption']))

  
def _eval(model):
    image_features = np.load('/mmlabworkspace/Students/AIC/Flickr8k_npy/clip_R_101/flickr8k_R101.npy')
    ground_truth, text = read_groundtruth() 
    # start = time.time()
    for i in tqdm(range(0,len(text), 5)):
      sub_text = text[i:i+5]
      #encode text
      text_token = tokenizer.tokenize(sub_text).cuda()
      with torch.no_grad():
          sub_text_features = model.encode_text(text_token).float()
          sub_text_features /= sub_text_features.norm(dim = -1, keepdim = True)
          sub_text_features = sub_text_features.cpu().numpy()
      if i == 0:
        text_features = sub_text_features
      else:
        text_features = np.concatenate((text_features, sub_text_features), axis = 0)
    # calculate the similarity
    sim = text_features@image_features.T
    print(sim.shape)
    report_dict, result = eval_on_flickr8k(a2b_sims=sim, return_ranks=True)
    print(report_dict)
    print(result)
    with open("/mmlabworkspace/Students/AIC/result_R_101_flickr8k.json", "w") as fOut:
      json.dump(report_dict, fOut, indent = 4)
if __name__ == "__main__":
  model, _, preprocess = open_clip.create_model_and_transforms('ViT-B-16', pretrained='openai')
  model.cuda().eval()
  processing(model, preprocess)
  concat() # concatenate the 8 image features file.
  _eval(model)
  
  # with open("/mmlabworkspace/Students/AIC/flickr8k_idx2img.json", "r") as fIn:
  #   idx2img = json.load(fIn)  
  # img2idx = {v: k for k,v in idx2img.items()}
  # with open("/mmlabworkspace/Students/AIC/flickr8k_img2idx.json", "w") as fOut:
  #   json.dump(img2idx, fOut, indent = 4)