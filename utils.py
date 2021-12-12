import re
import json
import copy
from typing import Any

from fastapi.staticfiles import StaticFiles


def load_static(app):
    app.mount("/css", StaticFiles(directory="static/css"), name="css")
    app.mount("/img", StaticFiles(directory="static/img"), name="img")
    app.mount("/posts/img", StaticFiles(directory="static/img"), name="posts_img")
    app.mount("/posts/css", StaticFiles(directory="static/css"), name="posts_css")
    app.mount("/search/img", StaticFiles(directory="static/img"), name="search_img")
    app.mount("/search/css", StaticFiles(directory="static/css"), name="search_css")
    app.mount("/users/img", StaticFiles(directory="static/img"), name="search_img")
    app.mount("/users/css", StaticFiles(directory="static/css"), name="search_css")
    app.mount("/tag/img", StaticFiles(directory="static/img"), name="search_img")
    app.mount("/tag/css", StaticFiles(directory="static/css"), name="search_css")
    app.mount("/bookmarks/img", StaticFiles(directory="static/img"), name="search_img")
    app.mount("/bookmarks/css", StaticFiles(directory="static/css"), name="search_css")
    app.mount("/bookmarks/delete/img", StaticFiles(directory="static/img"), name="search_img")
    app.mount("/bookmarks/delete/css", StaticFiles(directory="static/css"), name="search_css")
    app.mount("/bookmarks/add/img", StaticFiles(directory="static/img"), name="search_img")
    app.mount("/bookmarks/add/css", StaticFiles(directory="static/css"), name="search_css")
    return app


def load_files():
    with open("data/bookmarks.json", "r", encoding='utf-8') as file:
        try:
            bookmarks = json.load(file)
        except Exception:
            bookmarks = []

    with open("data/comments.json", "r", encoding='utf-8') as file:
        comments = json.load(file)

    with open("data/data.json", "r", encoding='utf-8') as file:
        data = json.load(file)

    for item in data:
        item.update(copy.deepcopy({
            "count_comments": sum(
                [1 if comment.get('post_id', None) == item.get('pk', None) else 0 for comment in comments])
        }))
        item["count_comments"] = f'Кол-во комментариев: {item["count_comments"]}' if item[
            "count_comments"] else "Нет комментариев"

        item.update(copy.deepcopy({
            "tags": search_tag(item['content'])
        }))

    return bookmarks, comments, data


def search(data: list, by: Any, value: Any):
    if by != 'content' and by != 'tags':
        return [item for item in data if str(item[f'{by}']) == str(value)]
    else:
        value = '' if value == '*' else value
        return [item for item in data if str(value).lower() in str(item[f'{by}']).lower() ]


def search_tag(input_line:str):
    return re.findall(r'(?i)(?<=\#)\w+', input_line)