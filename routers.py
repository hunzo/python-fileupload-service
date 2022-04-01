from fastapi import APIRouter
from fastapi.responses import FileResponse, JSONResponse

import os

route = APIRouter()


@route.get("/list_files")
async def list_all_files():
    files = [f for f in os.listdir(
        './upload') if os.path.isfile(os.path.join('./upload', f))]

    file_list = []
    for f in files:
        file_list.append(f)

    return {
        "files": file_list
    }


@route.get("/getfile/{name_file}")
async def get_file(name_file: str):
    file_path = os.getcwd() + "/upload/" + name_file

    if os.path.exists(file_path):
        return FileResponse(path=file_path)

    return {
        "error": "file not found"
    }


@route.get("/download/file/{name_file}")
async def download_file(name_file: str):
    file_path = os.getcwd() + "/upload/" + name_file

    if os.path.exists(file_path):
        return FileResponse(path=file_path, media_type='application/octet-stream', filename=name_file)

    return {
        "error": "file not found"
    }


@route.delete("/delete/file/{name_file}")
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
