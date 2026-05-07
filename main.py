from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"mesaj": "Kurye Kapıda Bekliyor!"}

@app.get("/kesintiler")
def get_kesintiler():
    # UEDAŞ'ın doğrudan veri dağıtım servisi
    url = "https://edrimsapi.uedas.com.tr/api/DoimGeneral/KesintiGetirByKesintiTur"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
        "Content-Type": "application/json",
        "Accept": "application/json",
        "X-Requested-With": "XMLHttpRequest"
    }
    
    # 1: Planlı Kesinti, 16: Bursa
    payload = {
        "KesintiTur": 1,
        "IlId": 10,
        "IlceId": 0,
        "MahalleId": 0
    }
    
    try:
        # 45 saniye sabırla bekliyoruz
        response = requests.post(url, json=payload, headers=headers, timeout=45)
        return response.json()
    except Exception as e:
        return {"hata": "UEDAŞ şu an çok yoğun, lütfen 1 dakika sonra tekrar dene."}
