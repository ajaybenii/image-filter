import io
import os
from re import U
import aiohttp
import cv2
from io import BytesIO
import logging
from typing import Optional
import requests
from enum import Enum
import numpy as np

from PIL import Image
import cv2
import pilgram
from fastapi import Form, File, UploadFile, APIRouter
from fastapi.responses import FileResponse , StreamingResponse
from pydantic import BaseModel, HttpUrl
from urllib.parse import urlparse
from pydantic import BaseModel
from fastapi import FastAPI,HTTPException
from fastapi.param_functions import Query

from snapmoon.pylut import process_image


router = APIRouter()
log = logging.getLogger("uvicorn")


class LutFilter(str, Enum):
    bluesky = 'bluesky'
    bluetogrey = 'bluetogrey'
    bluetoorange = 'bluetoorange'
    brighterwhite = 'brighterwhite'
    coolshadow = 'coolshadow'
    coolwhite = 'coolwhite'
    vibrantsunset = 'vibrantsunset'
    yellowtowhite = 'yellowtowhite'

class LutFilters(str, Enum):
    No_filter = "No_filter"

class URL(BaseModel):
    url_: str
 
def extract_filename(URL):
    parsed = urlparse(URL)
    return os.path.basename(parsed.path)

@router.get("/filter-by-url")
async def apply_filter_by_url(image_url: str,  Select_filter: str = Query("Normal", enum=['Brighter','Blue','Grey','Orange','Shadow','Coolwhite','Gold','Yellowtowhite'])):
    """
    Provide an image from the image_url and then specify the filter specified
    using the filter argument and this endpoint then returns the edited image
    file.
    """
    parsed = urlparse(image_url)
    filename = (os.path.basename(parsed.path))

    if Select_filter == 'Normal':

        response = requests.get(image_url)
        image_bytes = response.content
        image_file = io.BytesIO(image_bytes)
        im = Image.open(image_file) 
        
        img_format = im.format.lower()
        im.save("edited_image.jpg")
        image_path = "edited_image.jpg"
        return FileResponse(image_path, headers={'Content-Disposition': 'inline; filename="%s"' %(filename,)})

    if Select_filter == 'Blue':
        Select_filter =LutFilter.bluesky
        
        response = requests.get(image_url)
        image_bytes = response.content
        image_path = apply_lut(image_bytes, Select_filter)

        return FileResponse(image_path,headers={'Content-Disposition': 'inline; filename="%s"' %(filename,)})

    if Select_filter == 'Brighter':
        Select_filter =LutFilter.brighterwhite
        response = requests.get(image_url)
        image_bytes = response.content
        image_path = apply_lut(image_bytes, Select_filter)
        return FileResponse(image_path,headers={'Content-Disposition': 'inline; filename="%s"' %(filename,)})
    
    if Select_filter == 'Grey':
        Select_filter =LutFilter.bluetogrey
        response = requests.get(image_url)
        image_bytes = response.content
        image_path = apply_lut(image_bytes, Select_filter)
        return FileResponse(image_path,headers={'Content-Disposition': 'inline; filename="%s"' %(filename,)})

    if Select_filter == 'Orange':
        Select_filter =LutFilter.bluetoorange
        response = requests.get(image_url)
        image_bytes = response.content
        image_path = apply_lut(image_bytes, Select_filter)
        return FileResponse(image_path,headers={'Content-Disposition': 'inline; filename="%s"' %(filename,)})
    
    if Select_filter == 'Shadow':
        Select_filter =LutFilter.coolshadow
        response = requests.get(image_url)
        image_bytes = response.content
        image_path = apply_lut(image_bytes, Select_filter)
        return FileResponse(image_path,headers={'Content-Disposition': 'inline; filename="%s"' %(filename,)})
    
    if Select_filter == 'Coolwhite':
        Select_filter =LutFilter.coolwhite
        response = requests.get(image_url)
        image_bytes = response.content
        image_path = apply_lut(image_bytes, Select_filter)
        return FileResponse(image_path,headers={'Content-Disposition': 'inline; filename="%s"' %(filename,)})
    
    if Select_filter == 'Gold':
        Select_filter =LutFilter.vibrantsunset
        response = requests.get(image_url)
        image_bytes = response.content
        image_path = apply_lut(image_bytes, Select_filter)
        return FileResponse(image_path,headers={'Content-Disposition': 'inline; filename="%s"' %(filename,)})

    if Select_filter == 'Yellowtowhite':
        Select_filter =LutFilter.yellowtowhite
        response = requests.get(image_url)
        image_bytes = response.content
        image_path = apply_lut(image_bytes, Select_filter)
        return FileResponse(image_path,headers={'Content-Disposition': 'inline; filename="%s"' %(filename,)})
        


@router.post("/filter-by-file")
async def apply_filter_on_file(image_file: UploadFile=File(...), Select_filter: str = Query("Normal", enum=['Brighter','Blue','Grey','Orange','Shadow','Coolwhite','Gold','Yellowtowhite'])):
    """
    Takes the file from the request and applies from the 8 SquareYards filter specified by the
    user and then returns the edited image file.
    """
    if Select_filter == 'Normal':
        image_bytes = await image_file.read()
        image_file = io.BytesIO(image_bytes)
        im = Image.open(image_file) 

        im.save("edited_image.jpg")
        image_path = "edited_image.jpg"
        return FileResponse(image_path, media_type="image/jpg")
    
    if Select_filter == 'Blue':
        Select_filter =LutFilter.bluesky 
        image_bytes = await image_file.read()
        image_path = apply_lut(image_bytes, Select_filter)
        return FileResponse(image_path, media_type="image/jpg")

    if Select_filter == 'Brighter':
        Select_filter =LutFilter.brighterwhite 
        image_bytes = await image_file.read()
        image_path = apply_lut(image_bytes, Select_filter)
        return FileResponse(image_path, media_type="image/jpg")
    
    if Select_filter == 'Grey':
        Select_filter =LutFilter.bluetogrey 
        image_bytes = await image_file.read()
        image_path = apply_lut(image_bytes, Select_filter)
        return FileResponse(image_path, media_type="image/jpg")
    
    if Select_filter == 'Orange':
        Select_filter =LutFilter.bluetoorange
        image_bytes = await image_file.read()
        image_path = apply_lut(image_bytes, Select_filter)
        return FileResponse(image_path, media_type="image/jpg")
    
    if Select_filter == 'Shadow':
        Select_filter =LutFilter.coolshadow
        image_bytes = await image_file.read()
        image_path = apply_lut(image_bytes, Select_filter)
        return FileResponse(image_path, media_type="image/jpg")
    
    if Select_filter == 'Coolwhite':
        Select_filter =LutFilter.coolwhite
        image_bytes = await image_file.read()
        image_path = apply_lut(image_bytes, Select_filter)
        return FileResponse(image_path, media_type="image/jpg")
    
    if Select_filter == 'Gold':
        Select_filter = LutFilter.vibrantsunset
        image_bytes = await image_file.read()
        image_path = apply_lut(image_bytes, Select_filter)
        return FileResponse(image_path, media_type="image/jpg")
    
    if Select_filter == 'Yellowtowhite':
        Select_filter =LutFilter.yellowtowhite 
        image_bytes = await image_file.read()
        image_path = apply_lut(image_bytes, Select_filter)
        return FileResponse(image_path, media_type="image/jpg")
    

def apply_lut(image_bytes: bytes, Select_filter: LutFilter):
    """
    Apply the lut to the image
    """
    image_file = io.BytesIO(image_bytes)
    im = Image.open(image_file)
    img_format = im.format.lower()
    image_path = "edited_image.jpg"
    process_image(im, image_path, Select_filter)
    return image_path

@router.get("/sqy_image")
async def image_quality_checker(URL1): 

    '''This function get image from your system or
       take input as original image
    '''
    try:
        filename = extract_filename(URL1)
        filename = filename.strip()
    
    except Exception:
        ##logger.info("Error: HTTPException(status_code=406, detail=Not a valid URL)")
        raise HTTPException(status_code=406, detail="Not a valid URL")
    
    if URL1.lower().endswith((".jpg", ".png", ".jpeg", ".gif", ".webp",".jfif")) == False:
        ##logger.info("Error: HTTPException(status_code=406, detail=Not a valid URL)")
        raise HTTPException(status_code=406, detail="Not a valid URL")

    async with aiohttp.ClientSession() as session:
        async with session.get(URL1) as resp:
            contents = await resp.read()
  
    async with aiohttp.ClientSession() as session:
        async with session.get(URL1) as resp:
            contents = await resp.read()

    if contents == None:
        raise HTTPException(status_code=406, detail="No image found.")

    image = Image.open(BytesIO(contents))

    #this function get the format type of input image
    def get_format(filename):
        
        format_ = filename.split(".")[-1]
        if format_.lower() == "jpg":
            format_ = "jpeg"
        elif format_.lower() == "webp":
            format_ = "WebP"
    
        return format_
    
    format_ = get_format(filename) #here format_ store the type of image by filename

    def calculate_brightness(image):
        greyscale_image = image.convert('L')
        histogram = greyscale_image.histogram()
        pixels = sum(histogram)
        brightness = scale = len(histogram)

        for index in range(0, scale):
            ratio = histogram[index] / pixels
            brightness += ratio * (-scale + index)

        return 1 if brightness == 255 else brightness / scale
    bright1 = calculate_brightness(image)
    print("b_bright",calculate_brightness(image))

    def calculate_sharpness(image): #here calculate the sharpness 
        image = Image.open(BytesIO(contents))
        image.save("original_img."+format_)

        try:
            img = cv2.imread("original_img."+format_, cv2.IMREAD_GRAYSCALE)
            laplacian_var = cv2.Laplacian(img, cv2.CV_64F).var()
            print("laplacian try = ", laplacian_var)

            img_c = cv2.imread("original_img."+format_)
            Y = cv2.cvtColor(img_c, cv2.COLOR_BGR2YUV)[:,:,0]
            # compute min and max of Y
            min = np.min(Y)
            max = np.max(Y)

            # compute contrast
            contrast = (max-min)/(max+min)
            # print("try min=",min)

            img_s = cv2.imread("original_img."+format_)
            img_hsv = cv2.cvtColor(img_s, cv2.COLOR_BGR2HSV)
            saturation = img_hsv[:, :, 1].mean()
            # print("saturation try",saturation)

        except:
            img_s = cv2.imread("original_img."+format_)
            img_hsv = cv2.cvtColor(img_s, cv2.COLOR_BGR2HSV)
            saturation = img_hsv[:, :, 1].mean()
            # print("saturation",saturation)

            img = cv2.imread("original_img."+format_, cv2.IMREAD_GRAYSCALE)
            laplacian_var = cv2.Laplacian(img, cv2.CV_64F).var()
            # print("lap except", laplacian_var)
        
        
        wid,hgt = image.size
        print(wid,hgt)
        if laplacian_var > 500:
            result = 10

        if laplacian_var > 290 and laplacian_var < 500:
            result = 9

        if laplacian_var > 135 and laplacian_var < 290:
            result = 8

        if laplacian_var > 105 and laplacian_var < 135:
            result = 7

        if laplacian_var > 80 and laplacian_var < 105:
            result = 6

        if laplacian_var > 70  and laplacian_var < 80:
            result = 5

        if laplacian_var > 60 and laplacian_var < 70:
            result = 4

        if laplacian_var > 50 and laplacian_var < 60:
            result = 3

        if laplacian_var > 45 and laplacian_var < 50:
            result = 2

        if laplacian_var > 1 and  laplacian_var < 45:
            result = 1  

        if min < 9 and laplacian_var < 100 and laplacian_var >40:
            result = 8

        if min >3 and laplacian_var >250:
            result = 8

        if saturation > 115 and laplacian_var >400:
            result = 9

        if saturation > 130 and laplacian_var >300:
            result = 8

        if saturation < 85 and laplacian_var < 50:
            result = 3

        if saturation < 103 and saturation > 85 and laplacian_var < 60 and laplacian_var >40:
            result = 6

        if min < 5 and laplacian_var < 30:
            result = 4

        if saturation > 147 and saturation <165:
            result = 7

        if saturation > 175:
            result = 3

        if saturation < 85 and laplacian_var < 50 and min > 1:
            result=3
            
        if min < 1  and laplacian_var < 40:
            result = 5

        if bright1 > 0.63 and laplacian_var < 40 and saturation < 40:
            result = 7

        if laplacian_var < 50 and min < 1 and saturation <50:
            result = 7

        if bright1 < 0.3:
            result = 3

        # if (str(wid) + "x" + str(hgt)) < (str(400) + "x" + str(400)):
        #     print(str(wid) + "x" + str(hgt),"<",(str(400) + "x" + str(400)))
        #     result = 300

        print("rank =",result)
 
        return result
    
    result_check1 = calculate_sharpness(image)
    wid,hgt = image.size

    if (str(wid)) < (str(380)):
        print(wid, hgt)
        result_check1 = 3

    buffer = BytesIO()
    image.save(buffer, format=format_)
    buffer.seek(0)

    return ({"quality":result_check1/10})
