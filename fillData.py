from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import pandas as pd

def testIt(lines_data,rect_data,text_data):
    # if(len(lines_data.values())+len(rect_data)-len(text_data.values())>3):
    #     return False
    return True

def fillDetails(lines_data,rect_data,text_data,imgsrc):
    img = Image.open(imgsrc)
    a, b = img.size
    f_size =a/100+b/100
    tot = 0
    if(testIt(lines_data,rect_data,text_data)):
        fillRectData(rect_data,text_data,img,f_size)
        fillLinesData(lines_data,text_data,img,f_size)
        if(tot>2):
            img.show("Template Not Supported")
        else:
            print("Template Not Supported")
    else:
        print("Template Not Supported")

def fillLinesData(lines_data,text_data,img,f_size):
    for i,j in zip(list(text_data.keys()),list(text_data.values())):
        for k in list(lines_data.values()):
            if(abs(j["x"]-k["x"])<30 and abs(j["y"]-k["y"])<15):
                # print(f"{i} has coods {k["x"]},{k["y"]}")
                userinput = input(f"Enter the {i}")
                i1 = ImageDraw.Draw(img)
                myFont = ImageFont.truetype("arial.ttf", size= f_size)
                i1.text((k["x"]+5, k["y"]-f_size-3), userinput, font=myFont, fill =(0, 0, 0))
                tot+=1

def fillRectData(rect_data,text_data,img,f_size):
    l1  =[]
    for i,j in zip(list(text_data.keys()),list(text_data.values())):
        for k in list(rect_data):
            if(abs(j["x"]-k["top_left"][0])<400 and abs(j["y"]-k["top_left"][1])<50 and i not in l1):
                # print(f"{i} has coods {k["x"]},{k["y"]}")
                userinput = input(f"Enter the {i}")
                i1 = ImageDraw.Draw(img)
                myFont = ImageFont.truetype("arial.ttf", size= f_size)
                i1.text((k["top_left"][0]+f_size, k["top_left"][1]+k["height"]/(f_size*0.5)), userinput, font=myFont, fill =(0, 0, 0))
                text_data[i] == None
                l1.append(i)
                tot+=1
    return text_data