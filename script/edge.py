import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import argparse
#import json

def mdsPlot(fcsv,result):
	mdsDf= pd.read_csv(fcsv)
	print(mdsDf)
	fig = px.scatter(mdsDf, x="V1", y="V2", color="group", text="Row.names")
	fig.update_traces(marker_size=8,
		mode="markers+text",
		textposition="top center")
	#print(type(fig.data[0]))
	#print(fig.data[0])
	print(fig.__dict__.keys())
	jsonFig=str(fig.to_json())
	#fig.show()
	
	"""
	f = open(result+"mds.json", "w")
	f.write(jsonFig)
	f.close()
	"""
	
	f = open(result+"mdsata.js", "w")
	f.write("var jsdata= '"+jsonFig+"'")
	f.close()
	
	print("\n\n")
	print(fig.__dict__["_data"][0].keys())
	print(fig.__dict__["_data"][0]["text"])
	"""
"""
	scatter = fig.data[0]
	colors = ['#a3a7e4'] * 100
	scatter.marker.color = colors
	scatter.marker.size = [10] * 100
	fig.layout.hovermode = 'closest'
	
	def update_point(trace, points, selector):
		c = list(scatter.marker.color)
		s = list(scatter.marker.size)
		for i in points.point_inds:
			c[i] = '#bae2be'
			s[i] = 20
			with f.batch_update():
				scatter.marker.color = c
				scatter.marker.size = s

	scatter.on_click(update_point)
"""	
	#fig.show()
	
	
def amdsPlot(fcsv):
	mdsDf= pd.read_csv(fcsv)
	print(mdsDf)
	fig = go.Figure(data=go.Scatter(x=mdsDf["V1"],
			y=mdsDf["V2"],
			mode='markers'))
	print(fig.data)
	

if __name__ == '__main__':

	parser = argparse.ArgumentParser(
	description="")
	parser.add_argument('-m', '--mds', dest="mds", default=False, help="")
	parser.add_argument('-o', '--output', dest="repResult", default=False, help="")
	parser.add_argument('-p', '--processor', dest="cpu", default=False, help="")
	args=parser.parse_args()
	
	if args.mds:
		mdsPlot(args.mds, args.repResult)
		#amdsPlot(args.mds)
"""
