from flask import Flask, render_template, request, redirect

app = Flask(__name__)

import numpy as np # we will use this later, so import it now
from bokeh.layouts import widgetbox
from bokeh.models.widgets import TextInput
from bokeh.io import output_notebook, show
from bokeh.plotting import figure
import requests
import io
import os
import pandas as pd
from bokeh.embed import components 

@app.route('/')
def index():
	#return 'Hello'
	
	code = request.args.get("code")
	if code == None:
		code = "AAPL"

	'''ticker = TextInput(value="GOOGL", title="Ticker Symbol:")
	show(widgetbox(ticker))
	
	def func(attrname, old, new):
		tick = ticker.value
	    

	ticker.on_change('value', func)'''
	script,div = make_plot(code)

	return render_template('index.html', script=script, div=div)



def make_plot(code):
	url = "https://www.quandl.com/api/v3/datasets/WIKI/"+code+"/data.csv?start_date=2013-02-01&end_date=2013-02-28&api_key=nuEqV7LoZyAD2PBtKLWQ"
	data = requests.get(url)
	df = pd.read_csv(io.StringIO(data.text))   
	df.Date = pd.to_datetime(df.Date)
	p = figure(x_axis_type="datetime", title="Quandl WIKI EOD Stock Prices - Feb 2013", plot_height=600, plot_width=600)

	p.xgrid.grid_line_alpha=0.5
	p.ygrid.grid_line_alpha=0.5
	p.xaxis.axis_label = 'Date'

	p.line(df.Date, df.Close, legend=code)
	#show(p)

	script, div = components(p)
	return script,div

'''@app.route('/about')
def about():
  return render_template('about.html')'''

if __name__ == '__main__':
	port = int(os.environ.get("PORT", 5000))
	app.run(host='0.0.0.0', port=port)
