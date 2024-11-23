import pytesseract
import numpy as np
def getFields(imsrc:str,a:int,b:int)->list:
    data:dict = pytesseract.image_to_data(imsrc, output_type="dict")
    text = data['text']
    symbs = [",",":","?","."]
    x = list(np.array(data["left"]) + np.array(data["width"])+a/100)
    y = list(np.array(data["top"]) + np.array(data["height"])-2*(b/100))
    field_data = dict()
    text1:list[str] = []
    field = ""
    for i in range(len(text)):
        field += " "+ text[i]
        field = field.lower()
        if((len(text[i])==0) and (len(field)!=0) or any(char in text[i] for char in symbs)): 
            gg=1
            if(":" in text[i]):
                gg = 0
            text1.append(field.replace(":","")) 
            if(field not in field_data):
                field_data[field] = {"x":data["left"][i]+data["width"][i],"y":data["top"][i]+data["height"][i]}
            else:
                field_data[field+"1"] = {"x":data["left"][i]+data["width"][i],"y":data["top"][i]+data["height"][i]}
            field=""
    text1 = [i for i in text1 if len(i)>3]
    return [text1,field_data]