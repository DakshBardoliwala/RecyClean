from app import app
from ..secondary import *

@app.route('/')
def home():
    return render_template('index.html', context = {"clicked": False})

@app.route('/describe')
def describe():
    return render_template('index.html', context = {"clicked": True, "category": main()})