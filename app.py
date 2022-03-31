from cmath import e
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
import shutil
from typing import List
import os

app = FastAPI()


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


@app.get("/list_files")
async def list_all_files():
    files = [f for f in os.listdir(
        './upload') if os.path.isfile(os.path.join('./upload', f))]

    file_list = []
    for f in files:
        file_list.append(f)

    return {
        "files": file_list
    }


@app.get("/getfile/{name_file}")
async def get_file(name_file):
    file_path = os.getcwd() + "/upload/" + name_file

    if os.path.exists(file_path):
        return FileResponse(path=file_path, status_code=204)

    return {
        "error": "file not found"
    }


@app.delete("/delete/file/{name_file}")
async def delete_file(name_file: str):
    file_path = os.getcwd() + "/upload/" + name_file
    try:
        os.remove(file_path)
        return JSONResponse(content={
            "removed": True
        }, status_code=200)

    except FileNotFoundError:
        return JSONResponse(content={
            "removed": False,
            "error_message": "File not found"
        }, status_code=404)


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
