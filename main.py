import folium
import pandas as pd
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/", methods=["GET"])
def status():
    print("/")
    return "Status: OK"

@app.route("/map", methods=["GET"])
def map():
    print("/map")
    return render_template("mymap.html")
    # return(my_map.get_root().render())

def generate_map():
    df = pd.read_csv("coordinates.csv")

    my_map = folium.Map(
        # center: Hong Kong Space Museum
        location=[22.295403586726987, 114.17205382336623],
        tiles='cartodbpositron',
        zoom_start=13
    )
    df.apply(lambda row:folium.Marker(location=[row["Latitude"], row["Longitude"]], popup=row["Location"], icon=folium.Icon(color='red', prefix='fa fa-circle-o')).add_to(my_map), axis=1)
    my_map.save("templates/mymap.html")


if __name__=="__main__":
    generate_map()
    print("Map is generated")

    app.run(host="0.0.0.0", port=4000, debug=True)