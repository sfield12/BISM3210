# import packages
from flask import Flask, render_template
from main import survivalRatePerSex
from bokeh.embed import components


app = Flask(__name__)
plot = survivalRatePerSex()
script1, div1 = components(plot)
@app.route("/")
def hello():
    return render_template('index.html', plot_div='plot', div1=div1, script1=script1)

@app.route("/test")
def hello1():
    return render_template('index.html', plot_div='plot', div1=div1, script1=script1)




