import json

import requests
from fastapi import APIRouter
from fastapi.params import Depends
from starlette.requests import Request
from starlette.responses import Response

from config import x_api_key
from models import FavoriteFilm, User
from schemas import KinopoiskID
from utils import get_current_user

movies_router = APIRouter()


@movies_router.get('/search')
async def search(request: Request, user: User = Depends(get_current_user)):
    kino_name = request.query_params.get('query')
    page = request.query_params.get('page')

    if kino_name is not None:
        url = f"https://kinopoiskapiunofficial.tech/api/v2.1/films/search-by-keyword?keyword={kino_name}"
        if page is not None:
            url = f"https://kinopoiskapiunofficial.tech/api/v2.1/films/search-by-keyword?keyword={kino_name}?page={page}"
        headers = {
            "X-API-KEY": x_api_key,
        }

        response = requests.get(url, headers=headers)
        if response.status_code == 404:
            return Response('неверный kino_name', status_code=404)
        items = json.loads(response.text)
        return items['films']


@movies_router.get('/film/{kinopoisk_id}')
async def get_by_kinopoisk_id(kinopoisk_id: int, user: User = Depends(get_current_user)):
    if kinopoisk_id is not None:
        url = f"https://kinopoiskapiunofficial.tech/api/v2.2/films/{kinopoisk_id}"
        headers = {
            "X-API-KEY": x_api_key,
        }

        response = requests.get(url, headers=headers)
        if response.status_code == 404:
            return Response('неверный Kinopoisk ID', status_code=404)

        items = json.loads(response.text)

        return items


@movies_router.post('/favorites')
async def add_favorite_film(form: KinopoiskID, request: Request, user: User = Depends(get_current_user)):
    kinopoisk_id = form.kinopoisk_id
    if kinopoisk_id is not None:
        url = f"https://kinopoiskapiunofficial.tech/api/v2.2/films/{kinopoisk_id}"
        headers = {
            "X-API-KEY": x_api_key,
        }

        response = requests.get(url, headers=headers)
        if response.status_code == 404:
            return Response('неверный Kinopoisk ID', status_code=404)

        items = json.loads(response.text)

        film = await FavoriteFilm.create(user_id=user.id, kinopoisk_id=kinopoisk_id, information=items)
        if film is None:
            return Response('Фильм с таким ID уже существует.')
        return film


@movies_router.post('/favorites/{kinopoisk_id}')
async def delete_favorite_film(kinopoisk_id: int, request: Request, user: User = Depends(get_current_user)):
    return await FavoriteFilm.delete(kinopoisk_id, user.id)


@movies_router.get('/favorites')
async def get_favorite_films(request: Request, user: User = Depends(get_current_user)):
    return await FavoriteFilm.get(user.id)
