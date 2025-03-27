from pprint import pprint
from urllib.parse import urlencode

import httpx
from fastapi import APIRouter, Request, HTTPException

from app.api.schemas.allinfo import AllInfo
from app.api.schemas.followers import FollowersCount
from app.api.schemas.user import UserNameStatus
from app.api.schemas.video import Videos
from app.api.schemas.wall import WallPostCount

router = APIRouter()

VERSION_VK_API = '5.199'
PROFILE_INFO_GET_URL = 'https://api.vk.com/method/account.getProfileInfo'
VIDEO_GET_URL = 'https://api.vk.com/method/video.get'
WALL_GET_URL = 'https://api.vk.com/method/wall.get'
USERS_GET_FOLLOWERS_URL = 'https://api.vk.com/method/users.getFollowers'


@router.get('/profile')
async def get_profile_info(request: Request):
    async with httpx.AsyncClient() as client:
        data = {
            'access_token': request.cookies.get('access_token'),
            'v': VERSION_VK_API,
        }
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        response = await client.post(
            PROFILE_INFO_GET_URL, data=urlencode(data), headers=headers
        )
    response_data = response.json()
    pprint(response_data)
    if 'error' in response_data:
        raise HTTPException(status_code=400, detail=response_data)
    return response_data


@router.get('/name-status', response_model=UserNameStatus)
async def get_user_name_status(request: Request):
    async with httpx.AsyncClient() as client:
        data = {
            'access_token': request.cookies.get('access_token'),
            'v': VERSION_VK_API,
        }
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        response = await client.post(
            PROFILE_INFO_GET_URL, data=urlencode(data), headers=headers
        )
    response_data = response.json()
    pprint(response_data)
    if 'error' in response_data:
        raise HTTPException(status_code=400, detail=response_data)
    return response_data.get('response')


@router.get('/get-video', response_model=Videos)
async def get_videos(request: Request):
    async with httpx.AsyncClient() as client:
        data = {
            'access_token': request.cookies.get('access_token'),
            'v': VERSION_VK_API,
        }
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        response = await client.post(
            VIDEO_GET_URL, data=urlencode(data), headers=headers
        )
    response_data = response.json()
    if 'error' in response_data:
        raise HTTPException(status_code=400, detail=response_data)
    return response_data.get('response')


@router.get('/get-followers-count', response_model=FollowersCount)
async def get_followers_count(request: Request):
    async with httpx.AsyncClient() as client:
        data = {
            'access_token': request.cookies.get('access_token'),
            'v': VERSION_VK_API,
        }
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        response = await client.post(
            USERS_GET_FOLLOWERS_URL, data=urlencode(data), headers=headers
        )
    response_data = response.json()
    if 'error' in response_data:
        raise HTTPException(status_code=400, detail=response_data)
    return response_data.get('response')


@router.get('/get-wall-post-count', response_model=WallPostCount)
async def get_wall_post_count(request: Request):
    async with httpx.AsyncClient() as client:
        data = {
            'access_token': request.cookies.get('access_token'),
            'v': VERSION_VK_API,
        }
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        response = await client.post(
            WALL_GET_URL, data=urlencode(data), headers=headers
        )
    response_data = response.json()
    if 'error' in response_data:
        raise HTTPException(status_code=400, detail=response_data)
    return response_data.get('response')


@router.get('/get-all-info', response_model=AllInfo)
async def get_all_info(request: Request):
    return {
        'user': await get_user_name_status(request),
        'posts': await get_wall_post_count(request),
        'followers': await get_followers_count(request),
        'videos': await get_videos(request)
    }
