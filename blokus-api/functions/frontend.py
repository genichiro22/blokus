from jinja2 import Environment, FileSystemLoader
from fastapi.responses import HTMLResponse

# def get(current_user):
def get(p):
    env = Environment(loader=FileSystemLoader('./templates/', encoding='utf8'))
    tmpl = env.get_template('render.j2')
    # c = tmpl.render(player_name=current_user.name)
    c = tmpl.render(player_name=p)
    return HTMLResponse(content=c)