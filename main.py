from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests

app = FastAPI()

# Figma'nın erişebilmesi için güvenlik kilidini (CORS) açan bölüm
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Her yerden gelen isteğe izin ver
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def baslangic():
    return {"mesaj": "Sistem Aktif! Kesintiler için /kesintiler adresine gidin."}

@app.get("/kesintiler")
def verileri_getir():
    # Burası UEDAŞ'ın gerçek veri gönderdiği gizli adres (Network sekmesinden bulduğun)
    url = "https://www.uedas.com.tr/api/GetOutages" 
    
    # Hangi il/ilçeyi istediğini buraya yazıyoruz
    payload = {"cityId": 16} # Örnek: Bursa (16)
    
    try:
        r = requests.post(url, json=payload, timeout=10)
        return r.json() # Veriyi temiz bir liste olarak Figma'ya fırlatır
    except:
        return {"hata": "UEDAŞ sitesine ulaşılamadı!"}