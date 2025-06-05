import requests
import firebase_admin
from firebase_admin import credentials, db
from datetime import datetime
import os
import json

# Validasi FIREBASE_CREDENTIALS
firebase_credentials = os.getenv("FIREBASE_CREDENTIALS")
if not firebase_credentials:
    raise ValueError("FIREBASE_CREDENTIALS environment variable is not set or empty")

try:
    cred_dict = json.loads(firebase_credentials)
except json.JSONDecodeError as e:
    raise ValueError(f"Failed to parse FIREBASE_CREDENTIALS as JSON: {e}")

# Inisialisasi Firebase
cred = credentials.Certificate(cred_dict)
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://ambildata-749c7-default-rtdb.asia-southeast1.firebasedatabase.app'
})

# Ambil data dari API BMKG
url = "https://api.bmkg.go.id/publik/prakiraan-cuaca?adm4=33.21.02.2001"
try:
    response = requests.get(url)
    response.raise_for_status()  # Akan error jika request gagal
    weather_data = response.json()
except requests.RequestException as e:
    raise Exception(f"Failed to fetch data from BMKG API: {e}")

# Simpan ke Firebase Realtime Database
ref = db.reference(f'weather_data/{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}')
ref.set({
    'timestamp': datetime.now().isoformat(),
    'weather': weather_data
})
print("Data successfully saved to Firebase")
