from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.params import Security
from fastapi.security import APIKeyHeader
from fastapi.exceptions import HTTPException
from dotenv import load_dotenv
from routers import route
from starlette import status
from typing import List

import os
import shutil

load_dotenv()
API_KEY = os.getenv('API_KEY')
API_KEY_NAME = "x-api-key"

app = FastAPI()

api_key_header_auth = APIKeyHeader(name=API_KEY_NAME, auto_error=True)


def check_token(api_key_header: str = Security(api_key_header_auth)):

    # print(os.getenv('X_API_KEY'))
    if api_key_header != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid KEY"
        )


app.include_router(
    route,
    prefix="/api",
    dependencies=[Security(check_token)]
)


@app.get("/")
async def example_files_service():
    content = """
    <body>
    <H1>Single File</H1>
    <form action="/upload_singlefile/" enctype="multipart/form-data" method="post">
    <input name="files" type="file" required>
    <input type="submit">

    </form>
    <H1>Multiple Files</H1>
    <form action="/upload_multiplefiles/" enctype="multipart/form-data" method="post">
    <input name="files" type="file" multiple required>
    <input type="submit">
    </form>
    </body>
    """
    return HTMLResponse(content=content)


@app.post("/upload_singlefile")
async def upload_single_file(files: UploadFile = File(...)):
    fileUpload = f'./upload/{files.filename}'

    with open(fileUpload, "wb") as buffer:
        shutil.copyfileobj(files.file, buffer)

    f = open(fileUpload)
    f.seek(0, os.SEEK_END)

    return {
        "filename": files.filename,
        "sizeInMegaBytes": (os.stat(fileUpload).st_size / (1024 * 1024)),
        "sizeInBytes": f.tell()
    }


@app.post("/upload_multiplefiles")
async def upload_multiple_files(files: List[UploadFile] = File(...)):
    for file in files:
        with open(f'./upload/{file.filename}', "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

    return {
        "uploadfile": [[f.filename, f] for f in files]
    }
