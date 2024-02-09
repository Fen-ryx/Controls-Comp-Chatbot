from flask import Flask, request, render_template_string, Markup, session, redirect, url_for
from flask_session import Session  # Requires Flask-Session extension
import os
import json
import once_interact

app = Flask(__name__)

# Configure the Flask app for session use
# app.config["SECRET_KEY"] = "your_secret_key_here"  # Change this to a random secret key
# app.config["SESSION_PERMANENT"] = False
# app.config["SESSION_TYPE"] = "filesystem"
# Session(app)


# HTML template with updated color scheme
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Chat Interface</title>
    <script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
    <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
    <style>
        body, html {
            height: 100%;
            margin: 0;
            display: flex;
            flex-direction: column;
            font-family: Arial, sans-serif;
            background-color: #1C192A; /* Dark grey background */
            color: #1C192A; /* White text color for better contrast */
        }
        .chat-history {
            flex-grow: 1; /* this is the line deviding the chat history and the input bar at the bottom  */
            overflow-y: auto;
            padding: 10px;
            border-bottom: 2px solid #444444; /* Slightly lighter grey for the input divider */
            display:flex;
            flex-direction:column;
        }
        .chat-input {
            margin-top: auto; /* this is backgroud area of the bottom input area */ 
            padding: 10px;
            background-color: #2C2C2C; /* Very dark grey for input area */
            display: flex;
        }
        .chat-input input[type="text"], .chat-input input[type="submit"] {
            padding: 10px; /* this section for the bottom input bar */
            border-radius: 10px;
            border: 1px solid #555555; /* Grey border */
            margin-right: 8px;
            background-color: #444444; /* Dark grey background for inputs */
            color: #FFFFFF; /* White text */
        }
        .chat-input input[type="submit"] {
            background-color: #007AFF; /* Blue color for the send button */
            cursor: pointer;
        }
        .message {
            margin-bottom: 12px;
            min-width: 60 px;
            max-width: 60%;
            
        }
        .user-msg { place-self: flex-end; justify-content: flex-end;} /* Blue background for user messages */
        .bot-msg { place-self: flex-start; justify-content: flex-start;} /* Light gray for bot messages */
        .user-msg .message-content{
            padding: 10px 15px;
            background-color: #E6DFF6;
            border-radius: 10px;
        }
        .bot-msg .message-content{ 
            padding: 10px 15px;
            background-color: #CAC3DA; 
            border-radius: 10px;
        }
        .like-dislike-button
        {
            margin-top:8px;
            height:20px;
            display:flex;
            padding-left:4px;
        }
        .like-dislike-button button{
            background:none;
            border:none;
            height:100%;
            color:white;
        }
        .selected{
            color:#0b8fed !important;
        }
        .mybtn{
            cursor:pointer
        }
        .spinner {
            border: 4px solid rgba(0, 0, 0, 0.1);
            width: 36px;
            height: 36px;
            border-radius: 50%;
            border-left-color: #09f;
            animation: spin 1s infinite linear;
            position: absolute; /* Center the spinner */
            top: 50%;
            left: 50%;
            margin: -18px 0 0 -18px; /* Offset for spinner size to center it */
            display: none; /* Hide by default */
        }

        @keyframes spin {
            0% {
                transform: rotate(0deg);
            }
            100% {
                transform: rotate(360deg);
            }
        }

    </style>
</head>
<body>
    {% if request.endpoint == 'home' %}
        <form action="/chat" method="get">
            <input type="text" name="session_id" placeholder="Enter a unique session ID">
            <input type="submit" value="Start Session">
        </form>
    {% else %}
        <div class="chat-history">
            {% for entry in chat_histories.get(session_id, []) %}
                <div class="message {{entry['class']}}">
                    <div class="message-content">{{ entry['message'] }}</div>
                    {% if entry.class =="bot-msg" %}
                        <div class="like-dislike-button">
                            <!--like button -->
                            <button class="like-button mybtn" id="like-btn-{{loop.index}}">
                                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" style="height:100%">
                                <path stroke-linecap="round" stroke-linejoin="round" d="M6.633 10.25c.806 0 1.533-.446 2.031-1.08a9.041 9.041 0 0 1 2.861-2.4c.723-.384 1.35-.956 1.653-1.715a4.498 4.498 0 0 0 .322-1.672V2.75a.75.75 0 0 1 .75-.75 2.25 2.25 0 0 1 2.25 2.25c0 1.152-.26 2.243-.723 3.218-.266.558.107 1.282.725 1.282m0 0h3.126c1.026 0 1.945.694 2.054 1.715.045.422.068.85.068 1.285a11.95 11.95 0 0 1-2.649 7.521c-.388.482-.987.729-1.605.729H13.48c-.483 0-.964-.078-1.423-.23l-3.114-1.04a4.501 4.501 0 0 0-1.423-.23H5.904m10.598-9.75H14.25M5.904 18.5c.083.205.173.405.27.602.197.4-.078.898-.523.898h-.908c-.889 0-1.713-.518-1.972-1.368a12 12 0 0 1-.521-3.507c0-1.553.295-3.036.831-4.398C3.387 9.953 4.167 9.5 5 9.5h1.053c.472 0 .745.556.5.96a8.958 8.958 0 0 0-1.302 4.665c0 1.194.232 2.333.654 3.375Z" />
                                </svg> 
                                <!-- <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" style="height:100%">
                                <path d="M7.493 18.5c-.425 0-.82-.236-.975-.632A7.48 7.48 0 0 1 6 15.125c0-1.75.599-3.358 1.602-4.634.151-.192.373-.309.6-.397.473-.183.89-.514 1.212-.924a9.042 9.042 0 0 1 2.861-2.4c.723-.384 1.35-.956 1.653-1.715a4.498 4.498 0 0 0 .322-1.672V2.75A.75.75 0 0 1 15 2a2.25 2.25 0 0 1 2.25 2.25c0 1.152-.26 2.243-.723 3.218-.266.558.107 1.282.725 1.282h3.126c1.026 0 1.945.694 2.054 1.715.045.422.068.85.068 1.285a11.95 11.95 0 0 1-2.649 7.521c-.388.482-.987.729-1.605.729H14.23c-.483 0-.964-.078-1.423-.23l-3.114-1.04a4.501 4.501 0 0 0-1.423-.23h-.777ZM2.331 10.727a11.969 11.969 0 0 0-.831 4.398 12 12 0 0 0 .52 3.507C2.28 19.482 3.105 20 3.994 20H4.9c.445 0 .72-.498.523-.898a8.963 8.963 0 0 1-.924-3.977c0-1.708.476-3.305 1.302-4.666.245-.403-.028-.959-.5-.959H4.25c-.832 0-1.612.453-1.918 1.227Z" />
                                </svg> -->
                            </button>

                            <!--Dislike button -->
                            <button class="dislike-button mybtn" id="dislike-btn-{{loop.index}}" >
                                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" style="height:100%">
                                    <path stroke-linecap="round" stroke-linejoin="round" d="M7.498 15.25H4.372c-1.026 0-1.945-.694-2.054-1.715a12.137 12.137 0 0 1-.068-1.285c0-2.848.992-5.464 2.649-7.521C5.287 4.247 5.886 4 6.504 4h4.016a4.5 4.5 0 0 1 1.423.23l3.114 1.04a4.5 4.5 0 0 0 1.423.23h1.294M7.498 15.25c.618 0 .991.724.725 1.282A7.471 7.471 0 0 0 7.5 19.75 2.25 2.25 0 0 0 9.75 22a.75.75 0 0 0 .75-.75v-.633c0-.573.11-1.14.322-1.672.304-.76.93-1.33 1.653-1.715a9.04 9.04 0 0 0 2.86-2.4c.498-.634 1.226-1.08 2.032-1.08h.384m-10.253 1.5H9.7m8.075-9.75c.01.05.027.1.05.148.593 1.2.925 2.55.925 3.977 0 1.487-.36 2.89-.999 4.125m.023-8.25c-.076-.365.183-.75.575-.75h.908c.889 0 1.713.518 1.972 1.368.339 1.11.521 2.287.521 3.507 0 1.553-.295 3.036-.831 4.398-.306.774-1.086 1.227-1.918 1.227h-1.053c-.472 0-.745-.556-.5-.96a8.95 8.95 0 0 0 .303-.54" />
                                </svg>
                            </button>
                        </div>
                    {% endif %}
                </div>
            {% endfor %}
        </div>
        <div class="chat-input">
            <form method="post" action="/chat?session_id={{ session_id }}">
                <input type="text" name="user_input" placeholder="Type your message here..." autocomplete="off">
                <input type="submit" value="Send">
            </form>
        </div>
    {% endif %}
    <div id="loading" class="spinner"></div>
    <script>
        // Scroll to the bottom of the chat history every time the page loads
        var chatHistory = document.querySelector('.chat-history');
        chatHistory.scrollTop = chatHistory.scrollHeight;

        // adding click event listener on like-dislike buttons
        var buttons = document.getElementsByClassName("mybtn") ;
        Array.from(buttons).forEach(elem => elem.addEventListener("click", toggleselection));

        function  toggleselection(  ){
            var chosen_btn=document.getElementById(this.id);
            chosen_btn.classList.toggle("selected");
        }
        document.addEventListener("DOMContentLoaded", function() {
            var form = document.querySelector(".chat-input form");
            form.onsubmit = function() {
                document.getElementById("loading").style.display = "block"; // Show the spinner
            };
        });
    </script>
</body>
</html>
'''

# Dictionary to store chat histories keyed by session ID
chat_histories = {}

@app.route('/', methods=['GET'])
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/chat', methods=['GET', 'POST'])
def chat():
    session_id = request.args.get('session_id')  # Get the session ID from the URL parameter

    if not session_id:
        # If no session ID is provided, redirect to the home page
        return redirect(url_for('home'))

    if request.method == 'POST':
        user_input = request.form['user_input']

        save_file = os.path.join(os.getcwd(), "Task_Theory_Part_1_DB.json")
        with open(save_file, 'r') as f:
            contexts = json.load(f)
        instruction = "Please include at least one relevant example in your response. Additionally, please structure your response in the following format: a) Theory \nb)Mathematical Example. Also, please try and keep your responses short."# \n c) Code (if applicable)"
        
        #response = once_interact.interactions(user_input,contexts,instruction)
        response = process_input(user_input)
        response_html = Markup(response.replace("\n", "<br>"))
        chat_histories.setdefault(session_id, []).append({"message": user_input, "class": "user-msg"})
        chat_histories[session_id].append({"message": response_html, "class": "bot-msg"})
    # print(chat_histories)
    return render_template_string(HTML_TEMPLATE, chat_histories=chat_histories, session_id=session_id, request=request)

def process_input(input_string):
    # Your existing process_input function
    input_string = ""

    return f"e-Chat: {input_string}"

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=8007, debug=True)