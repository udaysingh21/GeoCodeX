from flask import Flask, render_template, request, send_file
from werkzeug.utils import secure_filename
import pandas
from geopy.geocoders import Nominatim

app=Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/success/', methods=["POST"])
def success():
    global filename
    if request.method=="POST":
        file=request.files["file"]
        try:
            df=pandas.read_csv(file)
            locator=Nominatim(user_agent="my_geocoder")
            df["Locations"]=df["Address"].apply(locator.geocode)
            df["Latitude"]=df["Locations"].apply(lambda x: x.latitude if x is not None else None)
            df["Longitude"]=df["Locations"].apply(lambda x: x.longitude if x is not None else None)
            df=df.drop("Locations",axis=1)
            filename="uploads/Co-ordinates "+file.filename
            df.to_csv(filename,index=None)
            return render_template("index.html", text=df.to_html(), btn="download.html")
        except Exception as exe:
            return render_template("index.html", text="Please make sure you have an Address column in your csv file")

@app.route('/download')
def download():
    return send_file(filename , download_name="your_file.csv", as_attachment=True)

if __name__=="__main__":
    app.run(debug=True)
