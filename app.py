import os
import sqlite3
from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_cors import CORS
from openai import OpenAI
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app)

# Initialize OpenAI API
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),  # This is the default and can be omitted
)

def init_db():
    conn = sqlite3.connect('notes.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY,
            title TEXT,
            content TEXT,
            category TEXT,
            date TEXT,
            sentiment TEXT,
            summary TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    conn = sqlite3.connect('notes.db')
    c = conn.cursor()
    c.execute("SELECT * FROM notes")
    notes = c.fetchall()
    conn.close()
    return render_template('index.html', notes=notes)

@app.route('/add_note', methods=['POST'])
def add_note():
    title = request.form['title']
    content = request.form['content']
    category = request.form['category']
    # Use the current date and time
    date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    sentiment = request.form.get('sentiment', '')
    summary = request.form.get('summary', '')
    conn = sqlite3.connect('notes.db')
    c = conn.cursor()
    c.execute("INSERT INTO notes (title, content, category, date, sentiment, summary) VALUES (?, ?, ?, ?, ?, ?)",
              (title, content, category, date, sentiment, summary))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/edit_note/<int:note_id>', methods=['GET', 'POST'])
def edit_note(note_id):
    conn = sqlite3.connect('notes.db')
    c = conn.cursor()
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        category = request.form['category']
        date = request.form['date']  # Retain the original date
        sentiment = request.form.get('sentiment', '')
        summary = request.form.get('summary', '')
        c.execute("UPDATE notes SET title = ?, content = ?, category = ?, date = ?, sentiment = ?, summary = ? WHERE id = ?",
                  (title, content, category, date, sentiment, summary, note_id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    else:
        c.execute("SELECT * FROM notes WHERE id = ?", (note_id,))
        note = c.fetchone()
        conn.close()
        return render_template('edit_note.html', note=note)

@app.route('/delete_note/<int:note_id>')
def delete_note(note_id):
    conn = sqlite3.connect('notes.db')
    c = conn.cursor()
    c.execute("DELETE FROM notes WHERE id = ?", (note_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/summarize', methods=['POST'])
def summarize_note():
    data = request.get_json()
    content = data.get('content', '')
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes notes."},
                {"role": "user", "content": f"Generate a concise summary for: {content}"}
            ]
        )
        summary = response.choices[0].message.content.strip()
        return jsonify({'summary': summary})
    except Exception as e:
        return jsonify({'error': 'Failed to summarize note'}), 500

@app.route('/categorize', methods=['POST'])
def categorize_note():
    data = request.get_json()
    content = data.get('content', '')
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that categorizes notes in a single word category."},
                {"role": "user", "content": f"Categorize this note: {content}"}
            ]
        )
        category = response.choices[0].message.content.strip()
        return jsonify({'category': category})
    except Exception as e:
        return jsonify({'error': 'Failed to categorize note'}), 500
    
@app.route('/sentiment', methods=['POST'])
def analyze_sentiment():
    data = request.get_json()
    content = data.get('content', '')
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that analyzes the sentiment of notes in a single word (e.g., Positive, Neutral, Negative)."},
                {"role": "user", "content": f"Detect and display the sentiment of this note: {content}"}
            ]
        )
        sentiment = response.choices[0].message.content.strip()
        return jsonify({'sentiment': sentiment})
    except Exception as e:
        return jsonify({'error': 'Failed to analyze sentiment'}), 500
    


@app.route('/view_note/<int:note_id>')
def view_note(note_id):
    conn = sqlite3.connect('notes.db')
    c = conn.cursor()
    c.execute("SELECT * FROM notes WHERE id = ?", (note_id,))
    note = c.fetchone()
    conn.close()
    return render_template('view_note.html', note=note)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
