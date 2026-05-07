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
    return {"mesaj": "Kurye Hazır!"}

@app.get("/kesintiler")
def get_kesintiler():
    # Bu sefer doğrudan ana web sitesi üzerinden şansımızı deniyoruz
    url = "https://edrimsapi.uedas.com.tr/api/DoimGeneral/KesintiGetirByKesintiTur"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/json",
        "Origin": "https://www.uedas.com.tr",
        "Referer": "https://www.uedas.com.tr/tr/planli-kesintiler"
    }
    
    # Bursa (16) için veri paketi
    payload = {"cityId": 16}
    
    try:
        # Timeout süresini 30 saniyeye çıkardık
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        
        if response.status_code == 200:
            return response.json()
        else:
            return {"hata": f"UEDAŞ cevap vermedi. Durum kodu: {response.status_code}"}
            
    except requests.exceptions.Timeout:
        return {"hata": "UEDAŞ çok yavaş, bağlantı zaman aşımına uğradı."}
    except Exception as e:
        return {"hata": f"Beklenmedik bir sorun oluştu: {str(e)}"}
