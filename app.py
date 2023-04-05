from flask import Flask, render_template, request,Response
import geopandas as gpd
import io
import contextily
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

app = Flask(__name__)
df = gpd.read_file('/workspace/Fontanelle/ds964_nil_wm.zip')
fonta=gpd.read_file("/workspace/Fontanelle/Fontanelle.zip")
@app.route('/')
def home():
  lista=df.NIL.to_list()
  lista.sort()
  return render_template('html.html',list=lista)

@app.route('/search', methods = ['GET'])
def search():
  comune=request.args["comu"]
  sel=df[df.NIL==comune]
  return render_template('mapp.html',comune=comune)

@app.route('/map', methods = ['GET'])
def map():
  comune=request.args["comune"]
  sel=df[df.NIL==comune]
  fon=fonta[fonta.intersects(sel.geometry.item())]

  fig, ax = plt.subplots(figsize = (12,8))
  sel.to_crs(epsg=3857).plot(ax=ax, alpha=0.5)
  fon.to_crs(3857).plot(ax=ax,color="Blue")
  contextily.add_basemap(ax=ax)
  output = io.BytesIO()
  FigureCanvas(fig).print_png(output)
  return Response(output.getvalue(), mimetype='image/png')

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3245, debug=True)