from jinja2 import Environment, FileSystemLoader
from fastapi.responses import HTMLResponse

def get(current_player):
    env = Environment(loader=FileSystemLoader('./templates/', encoding='utf8'))
    tmpl = env.get_template('render.j2')
    c = tmpl.render(player_name=current_player.name)
    return HTMLResponse(content=c)