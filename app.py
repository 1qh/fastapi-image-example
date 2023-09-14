import io
from shutil import copyfileobj

import cv2
from fastapi import FastAPI, UploadFile
from fastapi.responses import FileResponse
from PIL import Image

app = FastAPI()


def validate_image(file: UploadFile):
    if file.filename.split('.')[-1].lower() not in {'jpg', 'jpeg', 'png'}:
        raise ValueError('File must be an image')


@app.post('/grayscale_PIL')
async def grayscale_PIL(file: UploadFile):
    validate_image(file)
    out = 'grayscale.png'
    Image.open(io.BytesIO(await file.read())).convert('L').save(out)
    return FileResponse(out)


@app.post('/grayscale_cv2')
async def grayscale_cv2(file: UploadFile):
    validate_image(file)
    fn = file.filename
    with open(fn, 'wb') as f:
        copyfileobj(file.file, f)
    out = 'grayscale.png'
    cv2.imwrite(out, cv2.cvtColor(cv2.imread(fn), cv2.COLOR_BGR2GRAY))
    return FileResponse(out)
