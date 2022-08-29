from jinja2 import Environment, FileSystemLoader

TEMPLATE_ENV = Environment(loader=FileSystemLoader('./templates/', encoding='utf8'))
