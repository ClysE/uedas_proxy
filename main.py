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
    return {"durum": "Kurye Hazır, Figma'yı Bekliyor!"}

@app.get("/kesintiler")
def get_kesintiler():
    url = "https://edrimsapi.uedas.com.tr/api/DoimGeneral/KesintiGetirByKesintiTur"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Content-Type": "application/json"
    }
    
    payload = {"KesintiTur": 1, "IlId": 16, "IlceId": 0, "MahalleId": 0}
    
    try:
        # UEDAŞ'a soruyoruz
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception("UEDAŞ Engeli")
            
    except Exception:
        # UEDAŞ kapıyı kapattıysa Figma boş dönmesin diye bunları gönderiyoruz:
        return [
            {
                "IlceAd": "NİLÜFER",
                "BaslangicTarihi": "07.05.2026 09:00",
                "BitisTarihi": "07.05.2026 17:00",
                "KesintiNedeni": "Şebeke Bakım Çalışması",
                "EtkilenenYer": "ÖZLÜCE, ERTUĞRUL MAHALLELERİ"
            },
            {
                "IlceAd": "OSMANGAZİ",
                "BaslangicTarihi": "07.05.2026 10:00",
                "BitisTarihi": "07.05.2026 14:00",
                "KesintiNedeni": "Yatırım Çalışması",
                "EtkilenenYer": "HÜRRİYET, ADALET MAHALLELERİ"
            },
            {
                "IlceAd": "YILDIRIM",
                "BaslangicTarihi": "07.05.2026 13:00",
                "BitisTarihi": "07.05.2026 16:00",
                "KesintiNedeni": "Arıza Onarım",
                "EtkilenenYer": "MİLLET MAHALLESİ, 11. SOKAK"
            }
        ]
