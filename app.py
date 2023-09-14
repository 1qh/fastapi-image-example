import io

from fastapi import FastAPI, UploadFile
from fastapi.responses import FileResponse
from PIL import Image

app = FastAPI()


@app.post('/grayscale')
async def grayscale(file: UploadFile):
    if file.filename.split('.')[-1].lower() in {'jpg', 'jpeg', 'png'}:
        out = 'grayscale.png'
        Image.open(io.BytesIO(await file.read())).convert('L').save(out)
        return FileResponse(
            out,
            headers={'Content-Disposition': f'attachment; filename={out}'},
        )
