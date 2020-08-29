

from starlette.applications import Starlette
from starlette.responses import Response
from starlette.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.authentication import requires
from .auth.backend import SisterAuthenticationBackend
from .auth.routes import login, logout


@requires(['staff'], redirect='login')
def dashboard(request):
    print(request.user.__dict__)
    return Response('Dashboard')


middlewares = [
    Middleware(SessionMiddleware, secret_key='my_secret_key'),
    Middleware(AuthenticationMiddleware, backend=SisterAuthenticationBackend())
]


def get_application():
    app = Starlette(middleware=middlewares)
    app.add_route('/', dashboard, methods=['GET', 'POST'], name='homepage')
    app.add_route('/login', login, methods=['GET', 'POST'], name='login')
    app.add_route('/logout', logout, methods=['GET', 'POST'])
    return app


app = get_application()
