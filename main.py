import json
import os

import uvicorn
from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette.responses import FileResponse
from utils import load_static, load_files, search

app = FastAPI()
bookmarks, comments, data = load_files()
templates = Jinja2Templates(directory="templates")


@app.get('/favicon.ico')
async def favicon():
    return FileResponse("favicon.ico")


@app.get("/index.html")
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
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
async def add_bookmarks(request: Request, postid:int):

    with open("data/bookmarks.json", "w", encoding="utf-8") as file:
        bookmarks.append(search(data=data, by='pk', value=postid).pop())
        json.dump(bookmarks, file, indent=4, ensure_ascii=False)
    return RedirectResponse("/")


@app.get("/bookmarks/", response_class=HTMLResponse)
@app.get("/bookmarks/{tagname}", response_class=HTMLResponse)
async def bookmark(request: Request, tagname: str = '*'):
    with open("data/bookmarks.json","r",encoding="utf-8") as file:
        data = json.load(file)
    return templates.TemplateResponse("/bookmarks.html", {"request": request,
                                                          "data": data})


if __name__ == '__main__':
    app = load_static(app)
    uvicorn.run(app=app,
                host=os.getenv("HOST", "0.0.0.0"),
                port=int(os.getenv("PORT", 8080)))
