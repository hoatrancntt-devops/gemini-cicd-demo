import os
from flask import Flask, request, render_template_string
from google import genai
from google.genai import types

app = Flask(__name__)

# Lấy API Key
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

# Khởi tạo Client (Sử dụng SDK google-genai mới nhất)
client = None
if GOOGLE_API_KEY:
    try:
        client = genai.Client(api_key=GOOGLE_API_KEY)
    except Exception as e:
        print(f"Lỗi khởi tạo Client: {e}")

# HTML Template (Giao diện Chat đẹp - Đã nhúng vào Python để gọn nhẹ 1 file)
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0">
    <title>Gemini 2.5 Flash Chat</title>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
    <style>
        :root { --primary: #0ea5e9; --bg: #f0f2f5; --white: #fff; --user-msg: #e3f2fd; }
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: var(--bg); margin: 0; height: 100vh; display: flex; justify-content: center; }
        .app-container { width: 100%; max-width: 600px; background: var(--white); display: flex; flex-direction: column; height: 100%; box-shadow: 0 0 20px rgba(0,0,0,0.05); }
        
        /* Header */
        .header { background: var(--primary); color: white; padding: 15px; text-align: center; font-weight: bold; font-size: 1.1rem; box-shadow: 0 2px 5px rgba(0,0,0,0.1); z-index: 10; display: flex; align-items: center; justify-content: center; gap: 10px; }
        
        /* Chat List */
        .chat-list { flex: 1; overflow-y: auto; padding: 20px; display: flex; flex-direction: column; gap: 15px; scroll-behavior: smooth; }
        .msg { max-width: 85%; padding: 12px 16px; border-radius: 15px; line-height: 1.5; font-size: 0.95rem; word-wrap: break-word; position: relative; animation: fadeIn 0.3s ease; }
        .msg.user { align-self: flex-end; background: var(--primary); color: white; border-bottom-right-radius: 4px; }
        .msg.ai { align-self: flex-start; background: #f3f4f6; color: #333; border-bottom-left-radius: 4px; }
        .msg strong { display: block; font-size: 0.75rem; margin-bottom: 4px; opacity: 0.8; }
        
        @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }

        /* Input Area */
        .input-area { padding: 15px; border-top: 1px solid #eee; background: white; display: flex; gap: 10px; align-items: center; }
        input { flex: 1; padding: 12px 15px; border: 1px solid #ddd; border-radius: 25px; outline: none; font-size: 1rem; transition: border 0.3s; }
        input:focus { border-color: var(--primary); }
        button { background: var(--primary); color: white; border: none; width: 45px; height: 45px; border-radius: 50%; cursor: pointer; transition: transform 0.2s; display: flex; align-items: center; justify-content: center; font-size: 1.1rem; }
        button:hover { transform: scale(1.1); }
        button:disabled { background: #ccc; cursor: not-allowed; }

        /* Loading */
        .typing { font-style: italic; color: #888; font-size: 0.8rem; margin-left: 10px; display: none; }
    </style>
</head>
<body>
    <div class="app-container">
        <div class="header"><i class="fa-solid fa-bolt"></i> Gemini 2.5 Flash</div>
        
        <div class="chat-list" id="chatList">
            {% if response_text %}
                <div class="msg user"><strong>Bạn</strong> {{ query }}</div>
                <div class="msg ai"><strong>Gemini</strong> {{ response_text | safe }}</div>
            {% else %}
                <div class="msg ai">Xin chào! Tôi là AI được hỗ trợ bởi Gemini 2.5 Flash (Google). Hãy hỏi tôi bất cứ điều gì!</div>
            {% endif %}
        </div>
        
        <div class="typing" id="typingIndicator">Gemini đang trả lời...</div>

        <div class="input-area">
            <form action="/" method="get" style="display:flex; width:100%; gap:10px" onsubmit="showLoading()">
                <input type="text" name="q" placeholder="Nhập tin nhắn..." required autocomplete="off" autofocus>
                <button type="submit"><i class="fa-solid fa-paper-plane"></i></button>
            </form>
        </div>
    </div>

    <script>
        // Auto scroll to bottom
        const chatList = document.getElementById('chatList');
        chatList.scrollTop = chatList.scrollHeight;

        function showLoading() {
            document.getElementById('typingIndicator').style.display = 'block';
            // Disable button to prevent double submit
            document.querySelector('button').disabled = true;
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    query = request.args.get('q')
    
    if not query:
        return render_template_string(HTML_TEMPLATE, query=None, response_text=None)
    
    if not client:
        return render_template_string(HTML_TEMPLATE, query=query, response_text="Lỗi: Chưa cấu hình API Key trên Server!")

    try:
        # Gọi model Gemini 2.5 Flash
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=query
        )
        # Chuyển đổi xuống dòng thành thẻ <br> để hiển thị đẹp trên HTML
        formatted_text = response.text.replace('\n', '<br>')
        return render_template_string(HTML_TEMPLATE, query=query, response_text=formatted_text)
        
    except Exception as e:
        error_msg = f"Lỗi API: {str(e)} <br><br> (Hãy kiểm tra lại API Key hoặc Model Name)"
        return render_template_string(HTML_TEMPLATE, query=query, response_text=error_msg)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
