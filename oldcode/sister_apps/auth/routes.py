import httpx
from starlette.responses import RedirectResponse
from starlette.authentication import AuthenticationError

from ..templates import render


async def api_login(username, password):
    # login
    query = """
        mutation getToken($username: String!, $password: String!){
            tokenAuth(username: $username, password: $password) {
                payload
                refreshExpiresIn
                token
            }
        }
    """
    variables = """
        {
            "username": "%s",
            "password": "%s"
        }
    """ % (username, password)
    client = httpx.AsyncClient(base_url='http://localhost:8000/api/v1/')
    result = await client.post('', json={
        'query': query, 'variables': variables
    })
    json_data = result.json()['data']
    return json_data['tokenAuth']


async def login(request):
    # if user logged in redirect to dashboard
    if request.user.is_authenticated:
        return RedirectResponse(request.url_for('homepage'))
    context = {
        'request': request
    }
    if request.method == 'POST':
        try:
            form_data = await request.form()
            auth_token = await api_login(**form_data)
            if not auth_token:
                raise AuthenticationError('Username dan password salah')
            request.session['username'] = auth_token
            return RedirectResponse(request.url_for('homepage'))
        except Exception as err:
            context.update({
                'errors': err
            })
    return render('login.html', context)


def logout(request):
    if request.user.is_authenticated:
        request.session.clear()
    return RedirectResponse('login')
