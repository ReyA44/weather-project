"""
Flask application - Weather Forecast API server.
"""
import os
import uuid
import logging
from functools import wraps
from flask import Flask, request, jsonify, g
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
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

# --- Rate Limiting (Security: prevents API abuse) ---
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["60 per minute"]
)
# --- Monitoring: API usage counter + alert threshold ---
api_stats = {"total_requests": 0, "forecast_calls": 0, "errors": 0}
ALERT_THRESHOLD = 100

# --- Basic Auth credentials from env vars (Bonus 9b) ---
AUTH_USERNAME = os.environ.get("APP_USERNAME", "admin")
AUTH_PASSWORD = os.environ.get("APP_PASSWORD", "1234")


def require_auth(f):
    """Decorator that enforces HTTP Basic Authentication."""
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or auth.username != AUTH_USERNAME \
                or auth.password != AUTH_PASSWORD:
            logger.warning("Unauthorized access attempt")
            return jsonify({"error": "Unauthorized"}), 401
        return f(*args, **kwargs)
    return decorated


# --- Request Tracing: unique ID per request ---
@app.before_request
def before_request():
    g.request_id = str(uuid.uuid4())[:8]
    api_stats["total_requests"] += 1
    logger.info("[%s] %s %s", g.request_id, request.method, request.path)


@app.after_request
def after_request(response):
    response.headers["X-Request-ID"] = g.request_id
    return response


# --- Routes ---
@app.route("/api/forecast")
@require_auth
@limiter.limit("30 per minute")
def forecast_route():
    city = request.args.get("city", "")
    try:
        data = get_forecast(city)
        api_stats["forecast_calls"] += 1
        if api_stats["forecast_calls"] >= ALERT_THRESHOLD:
            logger.warning(
                "ALERT: forecast API usage high (%d calls)",
                api_stats["forecast_calls"]
            )
        return jsonify(data)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        api_stats["errors"] += 1
        logger.error("Forecast error: %s", str(e))
        return jsonify({"error": "Failed to fetch weather"}), 500


@app.route("/api/addresses", methods=["GET", "POST", "DELETE"])
@require_auth
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


@app.route("/api/stats")
@require_auth
def stats_route():
    """Monitoring endpoint: shows API usage statistics."""
    return jsonify(api_stats)


if __name__ == "__main__":
    host = os.environ.get("HOST", "127.0.0.1")
    port = int(os.environ.get("PORT", 5001))
    app.run(host=host, port=port)
    