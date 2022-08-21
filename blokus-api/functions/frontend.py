from jinja2 import Environment, FileSystemLoader
from fastapi.responses import HTMLResponse

def get():
    env = Environment(loader=FileSystemLoader('./templates/', encoding='utf8'))
    tmpl = env.get_template('render.j2')
    c = tmpl.render()
    return HTMLResponse(content=c)