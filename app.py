from flask import Flask, render_template, request
import urllib.parse
import requests

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def directions():
    if request.method == 'POST':
        main_api = "https://www.mapquestapi.com/directions/v2/route?"
        key = "tlA9ZQblr79C1PntWAKMXS8FU5VTYDZb"
        
        orig = request.form.get("orig")
        dest = request.form.get("dest")

        url = main_api + urllib.parse.urlencode({"key": key, "from": orig, "to": dest})
        json_data = requests.get(url).json()
        json_status = json_data["info"]["statuscode"]

        result = {}
        result["url"] = url
        result["api_status"] = json_status

        if json_status == 0:
            result["directions"] = []
            result["formatted_time"] = json_data["route"]["formattedTime"]
            result["distance_miles"] = json_data["route"]["distance"]
            result["distance_km"] = "{:.2f}".format(result["distance_miles"] * 1.61)

            for each in json_data["route"]["legs"][0]["maneuvers"]:
                narrative = each["narrative"]
                distance = each["distance"]
                distance_km = "{:.2f}".format(distance * 1.61)
                formatted_maneuver = f"{narrative} ({distance_km} km)"
                result["directions"].append(formatted_maneuver)

        return render_template('index.html', result=result)

    return render_template('index.html')

if __name__ == '__main__':
    app.run()
