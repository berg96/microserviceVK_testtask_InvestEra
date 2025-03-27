import base64
import hashlib
import secrets
from urllib.parse import urlencode

import httpx
from fastapi import APIRouter, HTTPException, Request
from starlette.responses import RedirectResponse, JSONResponse

from app.core.config import settings

router = APIRouter()

CODE_VERIFIERS = {}

REDIRECT_URI = 'http://localhost/auth/callback'
AUTH_URL = 'https://id.vk.com/authorize'
TOKEN_URL = 'https://id.vk.com/oauth2/auth'
REVOKE_URL = 'https://id.vk.com/oauth2/revoke'
LOGOUT_URL = 'https://id.vk.com/oauth2/logout'


def generate_code_verifier() -> str:
    """Генерирует случайную строку code_verifier длиной ~64 символа."""
    return secrets.token_urlsafe(48)


def generate_code_challenge(code_verifier: str) -> str:
    """Преобразует code_verifier в code_challenge по стандарту PKCE (S256)."""
    digest = hashlib.sha256(code_verifier.encode('ascii')).digest()
    return base64.urlsafe_b64encode(digest).rstrip(b'=').decode('ascii')


def generate_state() -> str:
    """Генерирует случайную строку состояния (state) не менее 32 символов."""
    return secrets.token_urlsafe(32)


@router.get("/login")
async def auth_login():
    """Перенаправляет пользователя на авторизацию в VK"""
    state = generate_state()
    code_verifier = generate_code_verifier()
    CODE_VERIFIERS[state] = code_verifier
    params = {
        'response_type': 'code',
        'client_id': settings.client_id,
        'redirect_uri': REDIRECT_URI,
        'state': state,
        'code_challenge': generate_code_challenge(code_verifier),
        'code_challenge_method': 'S256',
        'scope': '%20'.join(['status', 'wall', 'friends', 'video', 'email']),
    }
    return RedirectResponse(
        url=f'https://id.vk.com/authorize?{urlencode(params, safe="%20")}'
    )


@router.get("/callback")
async def auth_callback(code: str, state: str, device_id: str):
    """
    Обрабатывает редирект с VK после авторизации, получает токены,
    сохраняет их и перенаправляет пользователя на /profile.
    """
    if state not in CODE_VERIFIERS:
        raise HTTPException(status_code=400, detail='Неверный state')
    code_verifier = CODE_VERIFIERS.pop(state)
    new_state = generate_state()
    async with httpx.AsyncClient() as client:
        data = {
            'grant_type': 'authorization_code',
            'code_verifier': code_verifier,
            'redirect_uri': REDIRECT_URI,
            'code': code,
            'client_id': settings.client_id,
            'device_id': device_id,
            'state': new_state,
        }
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        token_response = await client.post(
            TOKEN_URL, data=urlencode(data), headers=headers
        )
    token_data = token_response.json()
    if 'error' in token_data:
        raise HTTPException(status_code=400, detail=token_data)
    if token_data.get('state') != new_state:
        raise HTTPException(status_code=400, detail='Неверный state')
    redirect_response = RedirectResponse(url='/users/profile')
    redirect_response.set_cookie(
        key='access_token',
        value=token_data.get('access_token'),
        httponly=True
    )
    redirect_response.set_cookie(
        key='refresh_token',
        value=token_data.get('refresh_token'),
        httponly=True
    )
    redirect_response.set_cookie(
        key='device_id',
        value=device_id,
        httponly=True
    )
    return redirect_response


@router.get('/refresh')
async def refresh_token(request: Request):
    state = generate_state()
    async with httpx.AsyncClient() as client:
        data = {
            'grant_type': 'refresh_token',
            'refresh_token': request.cookies.get('refresh_token'),
            'client_id': settings.client_id,
            'device_id': request.cookies.get('device_id'),
            'state': state,
        }
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        token_response = await client.post(
            TOKEN_URL, data=urlencode(data), headers=headers
        )
    token_data = token_response.json()
    if 'error' in token_data:
        raise HTTPException(status_code=400, detail=token_data)
    if token_data.get('state') != state:
        raise HTTPException(status_code=400, detail='Неверный state')
    response = JSONResponse(
        content={'message': 'Cookies успешно обновлены'})
    response.set_cookie(
        key='access_token',
        value=token_data.get('access_token'),
        httponly=True
    )
    response.set_cookie(
        key='refresh_token',
        value=token_data.get('refresh_token'),
        httponly=True
    )
    return response


@router.get('/revoke')
async def revoke_tokens(request: Request):
    async with httpx.AsyncClient() as client:
        data = {
            'client_id': settings.client_id,
            'access_token': request.cookies.get('access_token'),
        }
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        response = await client.post(
            REVOKE_URL, data=urlencode(data), headers=headers
        )
    response_data = response.json()
    if 'error' in response_data:
        raise HTTPException(status_code=400, detail=response_data)
    if response_data.get('response') == 1:
        return {'message': 'Разрешения доступов пользователя успешно отозваны'}
    else:
        raise HTTPException(status_code=400, detail='Что-то пошло не так')


@router.get('/logout')
async def logout(request: Request):
    try:
        await revoke_tokens(request)
    except Exception as error:
        raise HTTPException (status_code=400, detail=str(error))
    async with httpx.AsyncClient() as client:
        data = {
            'client_id': settings.client_id,
            'access_token': request.cookies.get('access_token'),
        }
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        response = await client.post(
            LOGOUT_URL, data=urlencode(data), headers=headers
        )
    response_data = response.json()
    if 'error' in response_data:
        raise HTTPException(
            status_code=400,
            detail=response_data
        )
    if response_data.get('response') == 1:
        return {'message': 'Сессия пользователя успешно завершена'}
    else:
        raise HTTPException(status_code=400, detail='Что-то пошло не так')
