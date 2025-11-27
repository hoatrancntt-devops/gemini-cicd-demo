import os
from flask import Flask, request
import google.generativeai as genai

app = Flask(__name__)
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

if GOOGLE_API_KEY:
    genai.configure(api_key=GOOGLE_API_KEY)
else:
    print("Warning: GOOGLE_API_KEY missing")

def get_model():
    # Thử danh sách model mới nhất
    for model_name in ['gemini-1.5-flash', 'gemini-1.5-pro', 'gemini-pro']:
        try:
            return genai.GenerativeModel(model_name)
        except:
            continue
    return genai.GenerativeModel('gemini-1.5-flash') # Default fallback

model = get_model()

@app.route('/')
def home():
    if not GOOGLE_API_KEY:
        return "Lỗi: Chưa cấu hình GOOGLE_API_KEY trong Kubernetes!"
    
    query = request.args.get('q', 'Giới thiệu DevOps là gì?')
    
    try:
        response = model.generate_content(query)
        return f"""
        Gemini AI Demo
        Ask
        {response.text}
        """
    except Exception as e:
        # Debug: Liệt kê model khả dụng nếu lỗi
        try:
            models = [m.name for m in genai.list_models()]
            debug_msg = f"Available Models: {models}"
        except:
            debug_msg = "Cannot list models."
        return f"Lỗi API: {str(e)}{debug_msg}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
