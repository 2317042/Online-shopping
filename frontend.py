from flask import Flask, render_template_string, request
import requests
import os

app = Flask(__name__)

BACKEND_URL = os.environ.get("BACKEND_URL", "http://127.0.0.1:8000")

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Online Shopping Bill Calculator</title>
</head>
<body>
    <h2>Online Shopping Bill Calculator</h2>
    <form method="post" action="/calculate">
        <input type="number" step="0.01" name="price" placeholder="Price per item" required>
        <input type="number" name="quantity" placeholder="Quantity" required>
        <input type="number" step="0.01" name="tax" placeholder="Tax %" value="5.0">
        <input type="number" step="0.01" name="tip" placeholder="Tip" value="0">
        <button type="submit">Calculate</button>
    </form>

    {% if result %}
        <h3>Bill Details:</h3>
        <ul>
            <li>Subtotal: {{ result.subtotal }}</li>
            <li>Tax: {{ result.tax }}</li>
            <li>Tip: {{ result.tip }}</li>
            <li><strong>Total: {{ result.total }}</strong></li>
        </ul>
    {% endif %}
</body>
</html>
"""

@app.route("/", methods=["GET"])
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route("/calculate", methods=["POST"])
def calculate():
    try:
        price = float(request.form.get("price"))
        quantity = int(request.form.get("quantity"))
        tax = float(request.form.get("tax", 5.0))
        tip = float(request.form.get("tip", 0))
        response = requests.post(f"{BACKEND_URL}/calculate", params={
            "price": price,
            "quantity": quantity,
            "tax_percent": tax,
            "tip": tip
        })
        return render_template_string(HTML_TEMPLATE, result=response.json())
    except Exception as e:
        return render_template_string(HTML_TEMPLATE, result={"error": str(e)})
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
