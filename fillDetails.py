from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import pandas as pd

def testIt(lines_data,rect_data,text_data):
    if(len(lines_data.values())+len(rect_data)-len(text_data.values())>3):
        return False
    return True

def getData(lines_data,rect_data,text_data,imgsrc):
    dict1 = {}
    img = Image.open(imgsrc)
    a, b = img.size
    f_size =a/100+b/100
    tot=0
    tot+= getRectData(rect_data,text_data,img,f_size,dict1)
    tot+= getLinesData(lines_data,text_data,img,f_size,dict1)
    if(tot<2):
        dict1 ={"Error":True}
    print(tot)
    return dict1

def fillMultiple(imgsrc,df,dict1):
    inputs = df.to_dict(orient='records')
    images = []
    print(inputs)
    for user_inputs in inputs:
        data = {}
        # for user_input in user_inputs.:
        #     for field in dict1.keys():             
        for key in user_inputs.keys():
            data[user_inputs[key]] = dict1[key]
        images.append(fillAll(imgsrc,data))
    return images

def fillAll(imgsrc,data):
    img = Image.open(imgsrc)
    a, b = img.size
    f_size =a/100+b/100
    for i in data.keys():
        i1 = ImageDraw.Draw(img)
        myFont = ImageFont.truetype("arial.ttf", size= f_size)
        i1.text((data[i]["x"], data[i]["y"]), i, font=myFont, fill =(0, 0, 0))
    return img

def getLinesData(lines_data,text_data,img,f_size,dict1):
    tot = 0
    for i,j in zip(list(text_data.keys()),list(text_data.values())):
        for k in list(lines_data.values()):
            if(abs(j["x"]-k["x"])<30 and abs(j["y"]-k["y"])<15):
                dict1[i] = {"x":k["x"]+5,"y":k["y"]-f_size-3}
                tot+=1
    return tot

def getRectData(rect_data,text_data,img,f_size,dict1):
    tot = 0
    l1  =[]
    for i,j in zip(list(text_data.keys()),list(text_data.values())):
        for k in list(rect_data):
            if(abs(j["x"]-k["top_left"][0])<400 and abs(j["y"]-k["top_left"][1])<50 and i not in l1):
                dict1[i] = {"x":k["top_left"][0]+f_size,"y":k["top_left"][1]+k["height"]/(f_size*0.5)}
                l1.append(i)
                tot+=1
    return tot