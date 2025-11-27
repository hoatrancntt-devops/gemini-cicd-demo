import os
from flask import Flask, request
import google.generativeai as genai

app = Flask(__name__)
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

if GOOGLE_API_KEY:
    genai.configure(api_key=GOOGLE_API_KEY)
else:
    print("Warning: Missing API Key")

def get_model():
    # Thử lần lượt các model có trong danh sách hỗ trợ của bạn
    candidates = [
        'gemini-2.0-flash', 
        'gemini-2.5-flash', 
        'gemini-1.5-flash'
    ]
    for model_name in candidates:
        try:
            return genai.GenerativeModel(model_name)
        except:
            continue
    return genai.GenerativeModel('gemini-2.0-flash')

model = get_model()

@app.route('/')
def home():
    if not GOOGLE_API_KEY: return "Lỗi: Thiếu API Key!"
    
    query = request.args.get('q', 'Cấu hình OSPF area 0 cho interface Gi0/0 IP 10.0.0.1/30')
    
    try:
        # Prompt đóng vai kỹ sư mạng
        prompt = f"Bạn là kỹ sư mạng Cisco. Viết lệnh CLI cho yêu cầu: '{query}'. Chỉ hiện lệnh."
        response = model.generate_content(prompt)
        
        return f"""
        body{{background:#1e1e1e;color:#d4d4d4;font-family:monospace;padding:20px}} 
               pre{{background:black;padding:15px;border-left:4px solid #0ea5e9;color:#00ff00}}
        🤖 AI Network Config Generator
        Generate
        Command Output:
        {response.text}
        """
    except Exception as e:
        return f"Lỗi API: {str(e)}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
