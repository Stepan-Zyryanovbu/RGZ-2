from flask import Flask, request, jsonify
from flask_caching import Cache
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from data import DATA

app = Flask(__name__)

# Кэш в памяти, TTL = 1 час
app.config["CACHE_TYPE"] = "SimpleCache"
cache = Cache(app)
TTL = 60 * 60

# Лимит: 10 запросов в час с одного IP
limiter = Limiter(get_remote_address, app=app, storage_uri="memory://")


@app.get("/weather/")
@limiter.limit("10 per hour")
def weather():
    city = (request.args.get("city") or "").strip().lower()
    if not city:
        return jsonify({"error": "city is required"}), 400

    key = f"w:{city}"

    cached = cache.get(key)
    if cached is not None:
        return jsonify({"source": "cache", "data": cached})

    data = DATA.get(city)
    if data is None:
        return jsonify({"error": "city not found"}), 404

    cache.set(key, data, timeout=TTL)
    return jsonify({"source": "data", "data": data})


@app.errorhandler(429)
def too_many(_e):
    # Flask-Limiter обычно сам ставит Retry-After (секунды)
    return jsonify({"error": "too many requests", "message": "try later"}), 429


if __name__ == "__main__":
    app.run(port=5000)
