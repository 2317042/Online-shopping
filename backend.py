from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Enable frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Online Shopping Bill Calculator Backend running!"}

@app.post("/calculate")
def calculate(price: float, quantity: int, tax_percent: float = 5.0, tip: float = 0.0):
    subtotal = price * quantity
    tax = subtotal * tax_percent / 100
    total = subtotal + tax + tip
    return {
        "subtotal": subtotal,
        "tax": tax,
        "tip": tip,
        "total": total
    }
