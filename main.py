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
    return {"mesaj": "Sistem Aktif!"}

@app.get("/kesintiler")
def get_kesintiler():
    # UEDAŞ'ın gerçek veri ucu
    url = "https://www.uedas.com.tr/api/GetOutages"
    
    # Kuryeye taktığımız 'insan' maskesi (Headers)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Content-Type": "application/json",
        "Referer": "https://www.uedas.com.tr/tr/planli-kesintiler"
    }
    
    # Bursa (16) için örnek payload
    payload = {"cityId": 16}
    
    try:
        # İsteği maskeli bir şekilde gönderiyoruz
        response = requests.post(url, json=payload, headers=headers, timeout=15)
        
        if response.status_code == 200:
            return response.json()
        else:
            return {"hata": f"UEDAŞ hata kodu verdi: {response.status_code}"}
            
    except Exception as e:
        return {"hata": f"Bağlantı sırasında bir sorun oluştu: {str(e)}"}
