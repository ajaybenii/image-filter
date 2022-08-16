# images.py
import io
import logging
from typing import Optional
import requests
from enum import Enum

from PIL import Image
import cv2
import pilgram
from fastapi import Form, File, UploadFile, APIRouter
from fastapi.responses import FileResponse
from pydantic import BaseModel, HttpUrl
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



# class Filter(str, Enum):
#     _1977 = '_1977'
#     aden = 'aden'
#     brannan = 'brannan'
#     brooklyn = 'brooklyn'
#     clarendon = 'clarendon'
#     earlybird = 'earlybird'
#     gingham = 'gingham'
#     hudson = 'hudson'
#     inkwell = 'inkwell'
#     kelvin = 'kelvin'
#     lark = 'lark'
#     lofi = 'lofi'
#     maven = 'maven'
#     mayfair = 'mayfair'
#     moon = 'moon'
#     nashville = 'nashville'
#     perpetua = 'perpetua'
#     reyes = 'reyes'
#     rise = 'rise'
#     slumber = 'slumber'
#     stinson = 'stinson'
#     toaster = 'toaster'
#     valencia = 'valencia'
#     walden = 'walden'
#     willow = 'willow'
#     xpro2 = 'xpro2'


# @router.get("/filter-by-url")
# async def apply_filter_by_url(image_url: str, filter: Filter):
#     """
#     Provide an image from the image_url and then specify the filter specified
#     using the filter argument and this endpoint then returns the edited image
#     file.
#     """
#     response = requests.get(image_url)
#     image_bytes = response.content
#     image_path = apply_filter(image_bytes, filter)
#     return FileResponse(image_path, media_type="image/jpg")


@router.get("/filter-by-url")
async def apply_filter_by_url(image_url: str,  Select_filter: str = Query("Normal", enum=['Brighter','Blue','Grey','Orange','Shadow','Coolwhite','Gold','Yellowtowhite'])):
    """
    Provide an image from the image_url and then specify the filter specified
    using the filter argument and this endpoint then returns the edited image
    file.
    """
    # if Select_filter == LutFilters.No_filter:
    #     return FileResponse(image_path, media_type="image/jpg")
    if Select_filter == 'Normal':
        response = requests.get(image_url)
        image_file = io.BytesIO(image_bytes)
        im = Image.open(image_file) 

        im.save("edited_image.jpg")
        image_path = "edited_image.jpg"
        return FileResponse(image_path, media_type="image/jpg")

    if Select_filter == 'Blue':
        Select_filter =LutFilter.bluesky
        response = requests.get(image_url)
        image_bytes = response.content
        image_path = apply_lut(image_bytes, Select_filter)
        return FileResponse(image_path, media_type="image/jpg")

    if Select_filter == 'Brighter':
        Select_filter =LutFilter.brighterwhite
        response = requests.get(image_url)
        image_bytes = response.content
        image_path = apply_lut(image_bytes, Select_filter)
        return FileResponse(image_path, media_type="image/jpg")
    
    if Select_filter == 'Grey':
        Select_filter =LutFilter.bluetogrey
        response = requests.get(image_url)
        image_bytes = response.content
        image_path = apply_lut(image_bytes, Select_filter)
        return FileResponse(image_path, media_type="image/jpg")

    if Select_filter == 'Orange':
        Select_filter =LutFilter.bluetoorange
        response = requests.get(image_url)
        image_bytes = response.content
        image_path = apply_lut(image_bytes, Select_filter)
        return FileResponse(image_path, media_type="image/jpg")
    
    if Select_filter == 'Shadow':
        Select_filter =LutFilter.coolshadow
        response = requests.get(image_url)
        image_bytes = response.content
        image_path = apply_lut(image_bytes, Select_filter)
        return FileResponse(image_path, media_type="image/jpg")
    
    if Select_filter == 'Coolwhite':
        Select_filter =LutFilter.coolwhite
        response = requests.get(image_url)
        image_bytes = response.content
        image_path = apply_lut(image_bytes, Select_filter)
        return FileResponse(image_path, media_type="image/jpg")
    
    if Select_filter == 'Gold':
        Select_filter =LutFilter.vibrantsunset
        response = requests.get(image_url)
        image_bytes = response.content
        image_path = apply_lut(image_bytes, Select_filter)
        return FileResponse(image_path, media_type="image/jpg")

    if Select_filter == 'Yellowtowhite':
        Select_filter =LutFilter.yellowtowhite
        response = requests.get(image_url)
        image_bytes = response.content
        image_path = apply_lut(image_bytes, Select_filter)
        return FileResponse(image_path, media_type="image/jpg")
        


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
    

# @router.post("/filter-by-file")
# async def apply_filter_on_file(image_file: UploadFile=File(...), filter: Filter=Form(...)):
#     """
#     Takes the file from the request and applies the filter specified by the
#     user and then returns the edited image file.
#     """
#     image_bytes = await image_file.read()
#     image_path = apply_filter(image_bytes, filter)
#     return FileResponse(image_path, media_type="image/jpg")


# def apply_filter(image_bytes: bytes, filter: Filter):
#     """
#     Abstracted function that takes an file as bytes and applies the filter.
#     """
#     log.info(f"Applying {filter} filter")
#     image_file = io.BytesIO(image_bytes)
#     im = Image.open(image_file)
#     image_path = "edited_image.jpg"
#     filter_method = getattr(pilgram, filter)
#     new_im = filter_method(im)
#     new_im.save(image_path)
#     return image_path


def apply_lut(image_bytes: bytes, Select_filter: LutFilter):
    """
    Apply the lut to the image
    """
    image_file = io.BytesIO(image_bytes)
    im = Image.open(image_file)
    image_path = "edited_image.jpg"
    process_image(im, image_path, Select_filter)
    return image_path
