# images.py
import io
import logging
import requests
from enum import Enum

from PIL import Image
import cv2
import pilgram
from fastapi import Form, File, UploadFile, APIRouter
from fastapi.responses import FileResponse
from pydantic import BaseModel, HttpUrl

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


@router.get("/sqy-filter-by-url")
async def apply_sqy_filter_by_url(image_url: str, select_filter: LutFilter):
    """
    Provide an image from the image_url and then specify the filter specified
    using the filter argument and this endpoint then returns the edited image
    file.
    """
    response = requests.get(image_url)
    image_bytes = response.content
    image_path = apply_lut(image_bytes, select_filter)
    return FileResponse(image_path, media_type="image/jpg")

@router.post("/sqy-filter-by-file")
async def apply_sqy_filter_on_file(image_file: UploadFile=File(...), select_filter: LutFilter=Form(...)):
    """
    Takes the file from the request and applies from the 8 SquareYards filter specified by the
    user and then returns the edited image file.
    """
    image_bytes = await image_file.read()
    image_path = apply_lut(image_bytes, select_filter)
    return FileResponse(image_path, media_type="image/jpg")

def apply_filter(image_bytes: bytes, filter: Filter):
    """
    Abstracted function that takes an file as bytes and applies the filter.
    """
    log.info(f"Applying {filter} filter")
    image_file = io.BytesIO(image_bytes)
    im = Image.open(image_file)
    image_path = "edited_image.jpg"
    filter_method = getattr(pilgram, filter)
    new_im = filter_method(im)
    new_im.save(image_path)
    return image_path

def apply_lut(image_bytes: bytes, lut_filter: LutFilter):
    """
    Apply the lut to the image
    """
    image_file = io.BytesIO(image_bytes)
    im = Image.open(image_file)
    image_path = "edited_image.jpg"
    process_image(im, image_path, lut_filter)
    return image_path
