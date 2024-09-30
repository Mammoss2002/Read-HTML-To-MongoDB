import gspread
from oauth2client.service_account import ServiceAccountCredentials
import requests

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
client = gspread.authorize(creds)

sheet = client.open('Copy of Google_Debug Bone pile 2024 (30SEP)').sheet1

cell_list = sheet.col_values(1)[1:]

for index, serial_number in enumerate(cell_list, start=2):
    url = f"https://cthmes44.asia.ad.celestica.com/des/ELM/Check.asp?SN={serial_number}"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.text

            sheet.update_cell(index, 35, data)
            print(f"อัพเดทข้อมูลที่แถว {index} สำเร็จ")

        else:
            print(f"ไม่สามารถดึงข้อมูลจาก {url} ได้ (สถานะ: {response.status_code})")

    except Exception as e:
        print(f"เกิดข้อผิดพลาด: {e}")
