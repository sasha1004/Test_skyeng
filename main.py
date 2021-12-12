import json
import os

import uvicorn
from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette.responses import FileResponse
from utils import load_static, load_files, search

app = FastAPI()
app = load_static(app)
bookmarks, comments, data = load_files()
templates = Jinja2Templates(directory="templates")

origins = [
    "http://localhost",
    "http://localhost:8080",
    "https://test-skyeng.herokuapp.com/"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/favicon.ico')
async def favicon():
    return FileResponse("favicon.ico")


@app.get("/index.html")
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    global bookmarks
    return templates.TemplateResponse("/index.html", {"request": request,
                                                      "data": data,
                                                      "bookmarks": bookmarks})


@app.get("/posts/{post_id}", response_class=HTMLResponse)
async def posts(request: Request, post_id: int):
    return templates.TemplateResponse("/post.html", {"request": request,
                                                     "post_id": post_id,
                                                     "data": search(data, by='pk', value=post_id).pop(),
                                                     "comments": [comment for comment in comments if
                                                                  comment['post_id'] == post_id]})


@app.get("/search", response_class=HTMLResponse)
@app.get("/search/s", response_class=HTMLResponse)
@app.get("/search/s=", response_class=HTMLResponse)
@app.get("/search/s={find}", response_class=HTMLResponse)
async def searchs(request: Request, find: str = '*'):
    return templates.TemplateResponse("/search.html", {"request": request,
                                                       "data": search(data, by='content', value=find)})


@app.get("/users/", response_class=HTMLResponse)
@app.get("/users/{username}", response_class=HTMLResponse)
async def users(request: Request, username: str = "*"):
    return templates.TemplateResponse("/user-feed.html", {"request": request,
                                                          "username": username,
                                                          "data": search(data, by='poster_name', value=username)})


@app.get("/tag/", response_class=HTMLResponse)
@app.get("/tag/{tagname}", response_class=HTMLResponse)
async def tag(request: Request, tagname: str = '*'):
    return templates.TemplateResponse("/tag.html", {"request": request,
                                                    "data": search(data, by='tags', value=tagname)})


@app.get("/bookmarks/add/{postid}", response_class=HTMLResponse)
async def add_bookmarks(request: Request, postid: int):
    global bookmarks
    for item in bookmarks:
        if item.get("pk") == postid:
            return RedirectResponse("/")

    item = search(data=data, by='pk', value=postid).pop()
    item['active'] = True
    bookmarks.append(item)

    return RedirectResponse("/")


@app.get("/bookmarks/delete/{postid}", response_class=HTMLResponse)
async def add_bookmarks(request: Request, postid: int):
    global bookmarks
    for index, item in enumerate(bookmarks):
        if item.get("pk") == postid:
            bookmarks.pop(index)
            break

    return templates.TemplateResponse("/bookmarks.html", {"request": request,
                                                          "data": bookmarks})


@app.get("/bookmarks/", response_class=HTMLResponse)
async def bookmark(request: Request):
    global bookmarks
    return templates.TemplateResponse("/bookmarks.html", {"request": request,
                                                          "data": bookmarks})


@app.on_event("shutdown")
def shutdown_event():
    with open("data/bookmarks.json", mode="w", encoding="utf-8") as file:
        json.dump(bookmarks, file, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    uvicorn.run(app=app,
                host=os.getenv("HOST", "0.0.0.0"),
                port=int(os.getenv("PORT", 5000)))
