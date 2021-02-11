# Build a web service that visualise data in a map

In this blog, I am going to explain how I visualise a couple of coordinates of locations and show them in a map with my browser.

I divide this exercise into two parts:

1. Demonstrate how coordinates can be visualised as a map with Python package folium.
2. Create a restful API with Flask, a python web framework that return a html file or content once a request is made from browser.

We need to install the necessary packages using the pip command:

```bash
# python 2
pip install folium
pip install flask
# python 3
pip3 install folium
pip3 install flask
```

## Generate a map

Before to get the hands dirty, some coordinates related to hospitals in Hong Kong are collected and saved in a csv file as shown below. We need latitude and longitude to generate a map.

![Build%20a%20web%20service%20that%20visualise%20data%20in%20a%20map%204480bf53ec31415c957e30e2763370d1/Untitled.png](Build%20a%20web%20service%20that%20visualise%20data%20in%20a%20map%204480bf53ec31415c957e30e2763370d1/Untitled.png)

Let’s start by writing main.py:

```python
import folium
import pandas as pd

def generate_map():
    df = pd.read_csv("coordinates.csv")

    my_map = folium.Map(
        # center: Hong Kong Space Museum
        location=[22.295403586726987, 114.17205382336623],
        tiles='cartodbpositron',
        zoom_start=13
    )
    df.apply(lambda row:folium.Marker(location=[row["Latitude"], row["Longitude"]], popup=row["Location"], icon=folium.Icon(color='red', prefix='fa fa-circle-o')).add_to(my_map), axis=1)
    my_map.save("mymap.html")
    

if __name__=="__main__":
    generate_map()
    print("Map is generated")
```

First of all, importing pandas to load the data from the file coordinates.csv. After that, creating a map with variable my_map and assign a coordinate of Hong Kong Space Museum to the argument location which is used to identify the center of the map. Argument zoom_start is to determine the area to be shown. The greater the number is, the smaller area will be or the more detailed will be.  Lastly, applying all coordinates to the object my_map with function Marker and save the object as a html file.

Okay. Let's try to run the script. Open a terminal , navigate to the current working directory and run it.

![Build%20a%20web%20service%20that%20visualise%20data%20in%20a%20map%204480bf53ec31415c957e30e2763370d1/Untitled%201.png](Build%20a%20web%20service%20that%20visualise%20data%20in%20a%20map%204480bf53ec31415c957e30e2763370d1/Untitled%201.png)

Now you should see a file name "mymap.html" is generated in your current directory. If you open it with your browser, you are expected to see the same effect as the following picture.

![Build%20a%20web%20service%20that%20visualise%20data%20in%20a%20map%204480bf53ec31415c957e30e2763370d1/Untitled%202.png](Build%20a%20web%20service%20that%20visualise%20data%20in%20a%20map%204480bf53ec31415c957e30e2763370d1/Untitled%202.png)

Great. We have already gone through the process of generating a map. 

## Create a web service

Now we should consider how to build a web service which could give the browser the html file. We will use the function render_template from Flask to render the html file to the browser.

```python
from flask import Flask, render_template
app = Flask(__name__)
```

We will create two endpoints, one is for checking the status, making sure my service is running. Another one is for render the file.

```python
@app.route("/", methods=["GET"])
def status():
    print("/")
    return "Status: OK"

@app.route("/map", methods=["GET"])
def map():
    print("/map")
    return render_template("mymap.html")
```

Note that as the function render_template will look for the filename from the folder templates, we need to modify the previous code on directory of saving the html file by changing

```python
my_map.save("mymap.html")
```

to

```python
my_map.save("templates/mymap.html")
```

And remember to create a folder named "templates" in your current directory.

Finally, we need to host the service with the following snippet of code.

```python
if __name__=="__main__":
    generate_map()
    print("Map is generated")

    app.run(host="0.0.0.0", port=4000, debug=True)
```

It is time to test it out again. 

![Build%20a%20web%20service%20that%20visualise%20data%20in%20a%20map%204480bf53ec31415c957e30e2763370d1/Untitled%203.png](Build%20a%20web%20service%20that%20visualise%20data%20in%20a%20map%204480bf53ec31415c957e30e2763370d1/Untitled%203.png)

I specify the service to be run at port 4000. Now go to browser search bar and type "localhost:4000/", you should see "Status: OK" is shown, this indicates the service is running successfully. After that, try "localhost:4000/map"Yeah!! You are successful to create a simple web app that visualise coordinates in a map.

![Build%20a%20web%20service%20that%20visualise%20data%20in%20a%20map%204480bf53ec31415c957e30e2763370d1/Untitled%204.png](Build%20a%20web%20service%20that%20visualise%20data%20in%20a%20map%204480bf53ec31415c957e30e2763370d1/Untitled%204.png)

Yead!! You are successful to create a simple web app that visualise a list of coordinates in a map.

If you want to stop your service, just press Control + C to quit.

Additionally, if you don't want to save the html file, you can transform the map object to a string and directly return it. And the benefit is no I/O is performed.

```python
return(my_map.get_root().render())
```# web-service-for-data-visualization
