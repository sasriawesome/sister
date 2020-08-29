import httpx
from httpx import Auth

from starlette.authentication import (
    BaseUser,
    AuthenticationBackend,
    AuthCredentials,
)

from ..cache import cache


class SisterUser(BaseUser):

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    @property
    def is_authenticated(self):
        return True


class JWTAuth(Auth):
    def __init__(self, token):
        self._token = self._build_token(token)

    def auth_flow(self, request):
        request.headers["Authorization"] = self._token
        yield request

    def _build_token(self, token):
        return "jwt %s" % token


async def get_profile(auth_token):
    query = """
        query{
            account{
                id
                username
                email
                isSuperuser
                isStaff
                isActive
                profile {
                    id
                    fullName
                }
            }
        }
    """
    client = httpx.AsyncClient(base_url='http://localhost:8000/api/v1/')
    headers = {'Authorization': "jwt %s" % auth_token['token']}
    result = await client.post('', json={'query': query}, headers=headers)
    return result


class SisterAuthenticationBackend(AuthenticationBackend):

    async def authenticate(self, request):
        # check in session
        auth_token = request.session.get('username', None)
        print(auth_token)
        if auth_token:
            # get from user_object from cache
            cache_key = auth_token['payload']['username']
            cached_user = await cache.get(cache_key)
            scopes = ['staff']
            if cached_user:
                user_data = cached_user
            else:
                # get user data from graphql API
                try:
                    profile = await get_profile(auth_token)
                    user_data = profile.json()['data']['account']
                    await cache.set(cache_key, user_data)
                except Exception as err:
                    return
            return (
                AuthCredentials(scopes),
                SisterUser(**user_data)
            )
        else:
            return


class SisterAuthCredentials(AuthCredentials):
    pass
