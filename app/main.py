import os
from flask import Flask, request
from google import genai

app = Flask(__name__)

# Lấy API Key từ biến môi trường
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

# Khởi tạo Client (SDK Mới)
if GOOGLE_API_KEY:
    client = genai.Client(api_key=GOOGLE_API_KEY)
else:
    client = None

@app.route('/')
def home():
    if not client:
        return "Lỗi: Chưa cấu hình GOOGLE_API_KEY trong Kubernetes!"
    
    query = request.args.get('q', 'Xin chào Gemini')
    
    try:
        # Gọi Gemini 2.5 Flash
        response = client.models.generate_content(
            model="gemini-2.5-flash", 
            contents=query
        )
        
        # Giao diện Chatbot đẹp mắt
        return f"""
        
        
        
            
            Gemini AI Chat
            
                body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f4f6f9; margin: 0; padding: 20px; display: flex; justify-content: center; }}
                .chat-container {{ background: white; width: 100%; max-width: 800px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); overflow: hidden; display: flex; flex-direction: column; height: 90vh; }}
                .header {{ background: #0ea5e9; color: white; padding: 20px; text-align: center; }}
                .header h1 {{ margin: 0; font-size: 1.5rem; }}
                .content {{ flex: 1; padding: 20px; overflow-y: auto; display: flex; flex-direction: column; gap: 15px; }}
                .message {{ padding: 15px; border-radius: 8px; max-width: 80%; line-height: 1.5; }}
                .user-msg {{ background: #e0f2fe; align-self: flex-end; border-bottom-right-radius: 0; }}
                .ai-msg {{ background: #f3f4f6; align-self: flex-start; border-bottom-left-radius: 0; }}
                .input-area {{ border-top: 1px solid #eee; padding: 20px; background: white; }}
                form {{ display: flex; gap: 10px; }}
                input {{ flex: 1; padding: 12px; border: 1px solid #ddd; border-radius: 6px; outline: none; }}
                input:focus {{ border-color: #0ea5e9; }}
                button {{ padding: 12px 24px; background: #0ea5e9; color: white; border: none; border-radius: 6px; font-weight: bold; cursor: pointer; transition: background 0.2s; }}
                button:hover {{ background: #0284c7; }}
            
        
        
            
                
                    🤖 Trợ Lý AI Gemini 2.5
                
                
                    Bạn: {query}
                    Gemini: {response.text}
                
                
                    
                        
                        Gửi
                    
                
            
        
        
        """
    except Exception as e:
        return f"Lỗi gọi API: {str(e)}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
