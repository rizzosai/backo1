import os
import requests

from flask import Blueprint, request, render_template, session, redirect, url_for, send_file, flash

claude_bp = Blueprint('claude', __name__)

ANTHROPIC_API_KEY = os.environ.get('CLAUDE_API_KEY', 'sk-REPLACE_ME')
CLAUDE_API_URL = 'https://api.anthropic.com/v1/messages'


@claude_bp.route('/claude', methods=['POST'])
def claude():
    if 'user' not in session:
        return redirect(url_for('login'))
    prompt = request.form.get('prompt')
    response = None
    # Initialize memory if not present
    if 'claude_history' not in session:
        session['claude_history'] = []
    # Add user message to history
    if prompt:
        session['claude_history'].append({"role": "user", "content": prompt})
        # Only keep the last 10 messages for context (adjust as needed)
        session['claude_history'] = session['claude_history'][-5000:]
        headers = {
            'x-api-key': ANTHROPIC_API_KEY,
            'content-type': 'application/json',
            'anthropic-version': '2023-06-01'
        }
        data = {
            'model': 'claude-3-opus-20240229',
            'max_tokens': 2048,
            'messages': session['claude_history']
        }
        try:
            r = requests.post(CLAUDE_API_URL, headers=headers, json=data)
            r.raise_for_status()
            result = r.json()
            # Add Claude's response to history
            ai_content = result.get('content', '')
            session['claude_history'].append({"role": "assistant", "content": ai_content})
            session['claude_history'] = session['claude_history'][-5000:]
            response = ai_content
        except Exception as e:
            response = f"Error: {e}"
    return render_template('dashboard.html', response=response)

# Route to let Claude generate app/website code and return as a downloadable file (placeholder)
@claude_bp.route('/claude/generate', methods=['POST'])
def claude_generate():
    if 'user' not in session:
        return redirect(url_for('login'))
    task = request.form.get('task')
    if not task:
        flash('No task provided')
        return redirect(url_for('dashboard'))
    # Here, you would send a prompt to Claude to generate code for the requested app/website
    # and save the result to a file, then return it as a download.
    # This is a placeholder for the actual implementation.
    flash('Claude code generation feature coming soon!')
    return redirect(url_for('dashboard'))
