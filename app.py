import os
import logging
from flask import Flask, request, jsonify
from weather_service import get_forecast
from address_manager import AddressManager

# Logging setup (Requirement 8: log to file + console)
logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
mgr = AddressManager()

@app.route("/api/forecast")
def forecast_route():
    city = request.args.get("city", "")
    try:
        data = get_forecast(city)
        return jsonify(data)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        logger.error("Forecast error: %s", str(e))
        return jsonify({"error": "Failed to fetch weather"}), 500

@app.route("/api/addresses", methods=["GET", "POST", "DELETE"])
def addresses_route():
    if request.method == "GET":
        return jsonify({"addresses": mgr.get_all()})
    
    data = request.get_json(silent=True) or {}
    city = data.get("city", "")
    
    if request.method == "POST":
        try:
            return jsonify({"addresses": mgr.add(city)}), 201
        except ValueError as e:
            return jsonify({"error": str(e)}), 400

    if request.method == "DELETE":
        if mgr.delete(city):
            return jsonify({"message": f"Deleted {city}"})
        return jsonify({"error": "City not found"}), 404

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    app.run(host="0.0.0.0", port=port)