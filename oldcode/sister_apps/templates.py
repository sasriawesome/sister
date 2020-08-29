from starlette.templating import Jinja2Templates

templates = Jinja2Templates(directory='sister_app/templates')
render = templates.TemplateResponse
