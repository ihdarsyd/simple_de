from flask import Blueprint, render_template, json
import os

home_blueprint = Blueprint('home', __name__, template_folder='templates')


def load_json():
    SITE_ROOT = os.path.realpath(os.getcwd())
    json_url = os.path.join(SITE_ROOT,"app/data","homedepo.json")
    data = json.load(open(json_url, encoding="utf8"))
    return data

ROW_PER_PAGE = 41
@home_blueprint.route('/nextpage/<page>')
def next_page(page):
   data = load_json()
   new_page = int(page) + ROW_PER_PAGE
   return render_template("index.html", data=data[int(page):new_page])

@home_blueprint.route('/prevpage/<page>')
def prev_page(page):
   data = load_json()
   new_page = int(page) + ROW_PER_PAGE 
   return render_template("index.html", data=data[int(page):new_page])

@home_blueprint.route('/')
def index():
   data = load_json()
   return render_template("index.html", data=data[:41])

@home_blueprint.route('/show/<int:id>')
def show(id):
   data = load_json()
   return render_template("show.html", data=data[id])
