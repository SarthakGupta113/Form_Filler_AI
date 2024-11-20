from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

def fillDetails(lines_data,rect_data,text_data,imgsrc):
    img = Image.open(imgsrc)
    f_size =20
    text_data  = fillRectData(rect_data,text_data,img,f_size)
    fillLinesData(lines_data,text_data,img,f_size)
    img.show()

def fillLinesData(lines_data,text_data,img,f_size):
    for i,j in zip(list(text_data.keys()),list(text_data.values())):
        for k in list(lines_data.values()):
            if(abs(j["x"]-k["x"])<30 and abs(j["y"]-k["y"])<15):
                # print(f"{i} has coods {k["x"]},{k["y"]}")
                userinput = input(f"Enter the {i}")
                i1 = ImageDraw.Draw(img)
                myFont = ImageFont.truetype("arial.ttf", size= f_size)
                i1.text((k["x"]+5, k["y"]-f_size-3), userinput, font=myFont, fill =(0, 0, 0))

def fillRectData(rect_data,text_data,img,f_size):
    for i,j in zip(list(text_data.keys()),list(text_data.values())):
        for k in list(rect_data):
            if(abs(j["x"]-k["top_left"][0])<150 and abs(j["y"]-k["top_left"][1])<50):
                # print(f"{i} has coods {k["x"]},{k["y"]}")
                userinput = input(f"Enter the {i}")
                i1 = ImageDraw.Draw(img)
                myFont = ImageFont.truetype("arial.ttf", size= f_size)
                i1.text((k["top_left"][0]+20, k["top_left"][1]+k["height"]/10), userinput, font=myFont, fill =(0, 0, 0))
                del text_data[i]
    return text_data