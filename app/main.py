import os
from flask import Flask, request, jsonify
import google.generativeai as genai

app = Flask(__name__)

# Lấy API Key từ biến môi trường (Được inject từ Helm Chart)
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

if GOOGLE_API_KEY:
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    model = None

@app.route('/')
def home():
    if not model:
        return "Lỗi: Chưa cấu hình GOOGLE_API_KEY trong Kubernetes!"
    
    # Lấy câu hỏi từ URL ?q=...
    query = request.args.get('q', 'Giới thiệu ngắn gọn về DevOps?')
    
    try:
        response = model.generate_content(query)
        return f"""
        Demo Gemini AI trên Kubernetes
        
            
            Hỏi Gemini
        
        
        Câu trả lời:
        {response.text}
        """
    except Exception as e:
        return f"Lỗi gọi API: {str(e)}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
