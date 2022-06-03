# # images.py
# import io
# import logging
# import requests
# from enum import Enum

# from PIL import Image
# import cv2
# import pilgram
# from fastapi import Form, File, UploadFile, APIRouter
# from fastapi.responses import FileResponse,StreamingResponse
# from pydantic import BaseModel, HttpUrl

# from snapmoon.pylut import process_image

# router = APIRouter()
# log = logging.getLogger("uvicorn")

# class LutFilter(str, Enum):
#     bluesky = 'bluesky'
#     bluetogrey = 'bluetogrey'
#     bluetoorange = 'bluetoorange'
#     brighterwhite = 'brighterwhite'
#     coolshadow = 'coolshadow'
#     coolwhite = 'coolwhite'
#     vibrantsunset = 'vibrantsunset'
#     yellowtowhite = 'yellowtowhite'

# @router.get("/bluesky-filter")
# async def apply_bluesky_filter_by_url(image_url: str):
#     """
#     Provide an image from the image_url and then specify the filter specified
#     using the filter argument and this endpoint then returns the edited image
#     file.
#     """
#     LutFilter = 'bluesky'
#     response = requests.get(image_url)
#     image_bytes = response.content
#     image_path = apply_lut(image_bytes,LutFilter)
#     return FileResponse(image_path, media_type="image/jpg")

# @router.get("/bluetogrey-filter")
# async def apply_bluetogrey_filter_by_url(image_url: str):
#     """
#     Provide an image from the image_url and then specify the filter specified
#     using the filter argument and this endpoint then returns the edited image
#     file.
#     """
#     LutFilter = 'bluetogrey'
#     response = requests.get(image_url)
#     image_bytes = response.content
#     image_path = apply_lut(image_bytes,LutFilter)
#     return FileResponse(image_path, media_type="image/jpg")

# @router.get("/bluetoorange-filter")
# async def apply_bluetoorange_filter_by_url(image_url: str):
#     """
#     Provide an image from the image_url and then specify the filter specified
#     using the filter argument and this endpoint then returns the edited image
#     file.
#     """
#     LutFilter = 'bluetoorange'
#     response = requests.get(image_url)
#     image_bytes = response.content
#     image_path = apply_lut(image_bytes,LutFilter)
#     return FileResponse(image_path, media_type="image/jpg")

# @router.get("/brighterwhite-filter")
# async def apply_brighterwhite_filter_by_url(image_url: str):
#     """
#     Provide an image from the image_url and then specify the filter specified
#     using the filter argument and this endpoint then returns the edited image
#     file.
#     """
#     LutFilter = 'brighterwhite'
#     response = requests.get(image_url)
#     image_bytes = response.content
#     image_path = apply_lut(image_bytes,LutFilter)
#     return FileResponse(image_path, media_type="image/jpg")

# @router.get("/coolshadow-filter")
# async def apply_coolshadow_filter_by_url(image_url: str):
#     """
#     Provide an image from the image_url and then specify the filter specified
#     using the filter argument and this endpoint then returns the edited image
#     file.
#     """
#     LutFilter = 'coolshadow'
#     response = requests.get(image_url)
#     image_bytes = response.content
#     image_path = apply_lut(image_bytes,LutFilter)
#     return FileResponse(image_path, media_type="image/jpg")

# @router.get("/coolwhite-filter")
# async def apply_coolwhite_filter_by_url(image_url: str):
#     """
#     Provide an image from the image_url and then specify the filter specified
#     using the filter argument and this endpoint then returns the edited image
#     file.
#     """
#     LutFilter = 'coolwhite'
#     response = requests.get(image_url)
#     image_bytes = response.content
#     image_path = apply_lut(image_bytes,LutFilter)
#     return FileResponse(image_path, media_type="image/jpg")

# @router.get("/vibrantsunset-filter")
# async def apply_vibrantsunset_filter_by_url(image_url: str):
#     """
#     Provide an image from the image_url and then specify the filter specified
#     using the filter argument and this endpoint then returns the edited image
#     file.
#     """
#     LutFilter = 'vibrantsunset'
#     response = requests.get(image_url)
#     image_bytes = response.content
#     image_path = apply_lut(image_bytes,LutFilter)
#     return FileResponse(image_path, media_type="image/jpg")

# @router.get("/yellowtowhite-filter")
# async def apply_yellowtowhite_filter_by_url(image_url: str):
#     """
#     Provide an image from the image_url and then specify the filter specified
#     using the filter argument and this endpoint then returns the edited image
#     file.
#     """
#     LutFilter = 'yellowtowhite'
#     response = requests.get(image_url)
#     image_bytes = response.content
#     image_path = apply_lut(image_bytes,LutFilter)
#     return FileResponse(image_path, media_type="image/jpg")

# def apply_lut(image_bytes: bytes, lut_filter: LutFilter):
#     """
#     Apply the lut to the image
#     """
#     image_file = io.BytesIO(image_bytes)
#     im = Image.open(image_file)
#     image_path = "edited_image.jpg"
#     process_image(im, image_path, lut_filter)
#     return image_path
# images.py
from fileinput import filename
import io
import os
import logging
from numpy import quantile
import requests
from enum import Enum

from PIL import Image
import cv2
import pilgram
from io import BytesIO
from urllib.parse import urlparse
from fastapi import Form, File, UploadFile, APIRouter
from fastapi.responses import FileResponse,StreamingResponse
from pydantic import BaseModel, HttpUrl

from snapmoon.pylut import process_image

router = APIRouter()
log = logging.getLogger("uvicorn")

class Select_Filter(str, Enum):
    bluesky = 'bluesky'
    bluetogrey = 'bluetogrey'
    bluetoorange = 'bluetoorange'
    brighterwhite = 'brighterwhite'
    coolshadow = 'coolshadow'
    coolwhite = 'coolwhite'
    vibrantsunset = 'vibrantsunset'
    yellowtowhite = 'yellowtowhite'

class Filter(str, Enum):
    _1977 = '_1977'
    aden = 'aden'
    brannan = 'brannan'
    brooklyn = 'brooklyn'
    clarendon = 'clarendon'
    earlybird = 'earlybird'
    gingham = 'gingham'
    hudson = 'hudson'
    inkwell = 'inkwell'
    kelvin = 'kelvin'
    lark = 'lark'
    lofi = 'lofi'
    maven = 'maven'
    mayfair = 'mayfair'
    moon = 'moon'
    nashville = 'nashville'
    perpetua = 'perpetua'
    reyes = 'reyes'
    rise = 'rise'
    slumber = 'slumber'
    stinson = 'stinson'
    toaster = 'toaster'
    valencia = 'valencia'
    walden = 'walden'
    willow = 'willow'
    xpro2 = 'xpro2'

@router.get("/bluesky-filter")
async def apply_blueksy_filter_by_url(image_url: str,Select_Filter = 'bluesky'):
    """
    Provide an image from the image_url and then specify the filter specified
    using the filter argument and this endpoint then returns the edited image
    file.
    """
    parsed = urlparse(image_url)
    filename = (os.path.basename(parsed.path))

    response = requests.get(image_url,allow_redirects=True)
    image_bytes = response.content
    image_path = apply_lut(image_bytes,Select_Filter)

    return FileResponse(image_path,headers={'Content-Disposition': 'inline; filename="%s"' %(filename,)})

def apply_lut(image_bytes: bytes, lut_filter: Select_Filter):
    """
    Apply the lut to the image
    """
    image_file = io.BytesIO(image_bytes)
    im = Image.open(image_file)
    image_path = "filterd_image.jpg"
    process_image(im, image_path, lut_filter)
    
    return image_path
