import pandas as pd
from PIL import Image
import numpy as np
from fillDetails import getData,fillAll,fillMultiple
from get_fields import getFields
from line_detect import lineDetect
from rect_detect import detectRectangles
from util import createJson
def getFieldsandLines(imsrc:str):
    img = Image.open(imsrc)
    a, b = img.size
    text,field_data = getFields(imsrc,a,b)
    lines = lineDetect(imsrc)
    rects = detectRectangles(imsrc)
    createJson("lines_data",lines)
    createJson("field_data",field_data)
    createJson("rect_data",rects)
    return getData(lines,rects,field_data,imsrc)


# fillDetails(lines,rects,field_data,imsrc)