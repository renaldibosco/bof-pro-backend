import random
from datetime import datetime
from typing import Dict, List, Optional
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="BOF Pro Signal Engine")

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

STOCKS = {
    "nifty50": ["RELIANCE", "HDFCBANK", "TCS", "INFY", "ICICIBANK", "KOTAKBANK", "AXISBANK", "LT", "BAJFINANCE", "TATAMOTORS"],
    "sensex": ["RELIANCE", "HDFCBANK", "TCS", "INFY", "ICICIBANK", "BAJFINANCE", "HINDUNILVR", "ITC", "KOTAKBANK"],
    "watchlist": ["BANKNIFTY", "FINNIFTY", "GOLD", "CRUDEOIL", "ADANIENT", "HCLTECH"],
    "fullscan": ["RELIANCE", "HDFCBANK", "TCS", "INFY", "BANKNIFTY", "FINNIFTY", "GOLD", "CRUDEOIL", "IRFC", "BSE"]
}

BASE_PRICES = {
    "RELIANCE": 1287.45, "HDFCBANK": 1923.30, "TCS": 3456.80, "INFY": 1678.25,
    "ICICIBANK": 1345.60, "KOTAKBANK": 1876.40, "AXISBANK": 1156.75, "LT": 3234.50,
    "BAJFINANCE": 7234.80, "TATAMOTORS": 876.90, "BANKNIFTY": 52345.60,
    "FINNIFTY": 24567.80, "GOLD": 71234.50, "CRUDEOIL": 6789.30, "IRFC": 234.50, "BSE": 3234.60
}

class SignalResponse(BaseModel):
    symbol: str
    score: int
    direction: str
    price: float
    change_pct: float
    entry: float
    stop_loss: float
    target1: float
    target2: float
    risk_reward: float
    factors: Dict[str, bool]
    timestamp: str

def calculate_bof_signal(symbol: str) -> SignalResponse:
    base_price = BASE_PRICES.get(symbol, 1000.0)
    current_price = round(base_price * (1 + random.uniform(-0.015, 0.015)), 2)
    
    score = random.choices([1, 2, 3, 4, 5], weights=[0.45, 0.20, 0.17, 0.10, 0.08])[0]
    direction = random.choice(["SHORT", "LONG"]) if score >= 3 else "NONE"
    
    mult = -1 if direction == "SHORT" else 1
    sl = round(current_price * (1 + mult * -0.008), 2)
    entry = round(current_price * (1 + mult * 0.002), 2)
    t1 = round(current_price * (1 + mult * 0.010), 2)
    t2 = round(current_price * (1 + mult * 0.018), 2)
    
    risk = abs(entry - sl)
    reward = abs(t1 - entry)
    rr = round(reward / risk, 1) if risk > 0 else 1.0

    return SignalResponse(
        symbol=symbol,
        score=score,
        direction=direction,
        price=current_price,
        change_pct=round(random.uniform(-1.5, 1.5), 2),
        entry=entry,
        stop_loss=sl,
        target1=t1,
        target2=t2,
        risk_reward=rr,
        factors={
            "multiTF": score >= 2,
            "weakVol": score >= 3,
            "rsiDiv": score >= 3 and random.random() > 0.25,
            "candle": score >= 4,
            "vwap": score >= 5
        },
        timestamp=datetime.now().strftime("%I:%M:%S %p")
    )

@app.get("/api/signals/{category}")
def get_signals(category: str):
    symbols = STOCKS.get(category.lower(), STOCKS["nifty50"])
    signals = [calculate_bof_signal(sym) for sym in symbols]
    return sorted(signals, key=lambda x: x.score, reverse=True)
