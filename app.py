from flask import Flask,render_template, request
import requests

app = Flask(__name__)

weather_API_Key="4aa1150b6dbd4a9994440819250603"

@app.route("/")
def home():
    return render_template("index.html")
@app.route("/get_weather", methods=["GET", "POST"])
def get_weather():
    if request.method == "POST":
        city = request.form["city"]
        url = f"http://api.weatherapi.com/v1/current.json?key={weather_API_Key}&q={city}"
        
        response = requests.get(url)
        data = response.json()

        if response.status_code == 200:
            temperature = data["current"]["temp_c"]
            latitude = data["location"]["lat"]
            longitude = data["location"]["lon"]
            country = data["location"]["country"]
            condition = data["current"]["condition"]["text"]
            icon = data["current"]["condition"]["icon"]
            localtime = data["location"]["localtime"]  # Get local time from JSON

            return render_template("index.html", 
                                   city=city.capitalize(), 
                                   temperature=temperature, 
                                   latitude=latitude, 
                                   longitude=longitude, 
                                   country=country, 
                                   condition=condition,
                                   icon=icon,
                                   localtime=localtime)  # Pass localtime to template
        else:
            return render_template("index.html", error="Invalid city name or API error!")

    return render_template("index.html")

if __name__ == "__main__":
    app.run()