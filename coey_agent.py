
import os
from flask import Flask, request, render_template_string
import anthropic

app = Flask(__name__)

CLAUDE_API_KEY = os.getenv('CLAUDE_API_KEY', 'your-claude-api-key-here')
client = anthropic.Anthropic(api_key=CLAUDE_API_KEY)

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Coey Bot Backoffice</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        textarea { width: 100%; height: 100px; }
        .response { margin-top: 20px; padding: 10px; background: #f0f0f0; border-radius: 5px; }
    </style>
</head>
<body>
    <h1>Coey Bot Backoffice</h1>
    <form method="post" action="/ask">
        <label for="prompt">Enter your order for Claude:</label><br>
        <textarea id="prompt" name="prompt"></textarea><br><br>
        <button type="submit">Send to Claude</button>
    </form>
    {% if response %}
    <div class="response">
        <strong>Claude's Response:</strong><br>
        {{ response }}
    </div>
    {% endif %}
</body>
</html>
'''

@app.route('/', methods=['GET'])
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/ask', methods=['POST'])
def ask_claude():
    prompt = request.form.get('prompt', '')
    if not prompt:
        return render_template_string(HTML_TEMPLATE, response="Please enter a prompt.")
    try:
        response = client.beta.messages.create(
            model="claude-sonnet-4-5",  # Update model as needed
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt}
                    ]
                }
            ],
            betas=["files-api-2025-04-14"],
        )
        ai_response = response.content[0].text if hasattr(response, 'content') and response.content else 'No response from Claude.'
    except Exception as e:
        ai_response = f"Error: {e}"
    return render_template_string(HTML_TEMPLATE, response=ai_response)

if __name__ == '__main__':
    app.run(debug=True)
