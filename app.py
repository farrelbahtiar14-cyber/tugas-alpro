from flask import Flask, jsonify, render_template, request
import math

app = Flask(__name__)

def positive_number(data, key):
    """Ambil angka positif dari payload JSON dan validasi inputnya."""
    try:
        value = float(data[key])
    except (KeyError, TypeError, ValueError):
        raise ValueError(f"Nilai {key} harus berupa angka.")
    if not math.isfinite(value) or value <= 0:
        raise ValueError(f"Nilai {key} harus lebih besar dari nol.")
    return value

@app.get("/")
def index():
    return render_template("index.html")

@app.post("/api/simulate")
def simulate():
    """Menghitung rangkaian resistor DC seri atau paralel di Python."""
    data = request.get_json(silent=True) or {}
    try:
        voltage = positive_number(data, "voltage")
        r1 = positive_number(data, "r1")
        r2 = positive_number(data, "r2")
        mode = data.get("mode", "seri")
        if mode == "seri":
            req = r1 + r2
            v1 = voltage * r1 / req
            v2 = voltage * r2 / req
        elif mode == "paralel":
            req = (r1 * r2) / (r1 + r2)
            v1 = voltage
            v2 = voltage
        else:
            return jsonify({"error": "Mode harus 'seri' atau 'paralel'."}), 400
        current = voltage / req
        power = voltage * current
        return jsonify({
            "Req": round(req, 6),
            "I": round(current, 6),
            "V1": round(v1, 6),
            "V2": round(v2, 6),
            "power": round(power, 6),
        })
    except ValueError as error:
        return jsonify({"error": str(error)}), 400

@app.post("/api/ohm")
def ohm():
    """Hitung satu besaran dari Hukum Ohm, berdasarkan dua nilai yang diisi."""
    data = request.get_json(silent=True) or {}
    present = [key for key in ("voltage", "current", "resistance")
               if data.get(key) not in (None, "")]
    if len(present) != 2:
        return jsonify({"error": "Isi tepat dua nilai: tegangan, arus, atau resistansi."}), 400
    try:
        values = {}
        for key in present:
            value = float(data[key])
            if not math.isfinite(value) or value < 0:
                raise ValueError("Nilai harus angka nol atau positif.")
            values[key] = value
        if "voltage" not in values:
            result = values["current"] * values["resistance"]
            return jsonify({"field": "voltage", "value": result, "formula": "V = I × R"})
        if "current" not in values:
            if values["resistance"] == 0:
                raise ValueError("Resistansi tidak boleh 0 Ω untuk menghitung arus.")
            result = values["voltage"] / values["resistance"]
            return jsonify({"field": "current", "value": result, "formula": "I = V / R"})
        if values["current"] == 0:
            raise ValueError("Arus tidak boleh 0 A untuk menghitung resistansi.")
        result = values["voltage"] / values["current"]
        return jsonify({"field": "resistance", "value": result, "formula": "R = V / I"})
    except (ValueError, TypeError) as error:
        return jsonify({"error": str(error)}), 400

if __name__ == "__main__":
    app.run(debug=True)
