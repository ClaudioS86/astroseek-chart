from flask import Flask, request, send_file
import subprocess

app = Flask(__name__)

@app.route("/generate-chart", methods=["POST"])
def generate_chart():
    data = request.json
    date = data["date"]
    time_str = data["time"]
    lat = data["lat"]
    lon = data["lon"]
    location = data["location"]
    output_path = "chart.png"

    subprocess.run([
        "python3", "astroseek_screenshot.py",
        date, time_str, str(lat), str(lon), location, output_path
    ], check=True)

    return send_file(output_path, mimetype="image/png")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
