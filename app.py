from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import sqlite3
import os
from datetime import datetime

app = Flask(__name__, static_folder='static')
CORS(app)

# Use environment variable for DB path, default to local path for development
DB_PATH = os.getenv('DB_PATH', 'todo.db')

def init_db():
    """Initialize the SQLite database"""
    db_dir = os.path.dirname(DB_PATH)
    if db_dir:  # Only create directory if path contains a directory
        os.makedirs(db_dir, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS todos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT NOT NULL,
            completed INTEGER DEFAULT 0,
            created_at TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    """Serve the frontend"""
    return send_from_directory('static', 'index.html')

@app.route('/api/todos', methods=['GET'])
def get_todos():
    """Get all todos"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM todos ORDER BY created_at DESC')
    todos = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return jsonify(todos)

@app.route('/api/todos', methods=['POST'])
def create_todo():
    """Create a new todo"""
    data = request.get_json()
    task = data.get('task', '').strip()
    
    if not task:
        return jsonify({'error': 'Task cannot be empty'}), 400
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO todos (task, completed, created_at) VALUES (?, ?, ?)',
        (task, 0, datetime.now().isoformat())
    )
    conn.commit()
    todo_id = cursor.lastrowid
    conn.close()
    
    return jsonify({'id': todo_id, 'task': task, 'completed': 0}), 201

@app.route('/api/todos/<int:todo_id>', methods=['PUT'])
def update_todo(todo_id):
    """Update a todo (toggle completion)"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM todos WHERE id = ?', (todo_id,))
    todo = cursor.fetchone()
    
    if not todo:
        conn.close()
        return jsonify({'error': 'Todo not found'}), 404
    
    new_completed = 1 if todo[2] == 0 else 0
    cursor.execute('UPDATE todos SET completed = ? WHERE id = ?', (new_completed, todo_id))
    conn.commit()
    conn.close()
    
    return jsonify({'id': todo_id, 'completed': new_completed}), 200

@app.route('/api/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    """Delete a todo"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM todos WHERE id = ?', (todo_id,))
    conn.commit()
    deleted = cursor.rowcount > 0
    conn.close()
    
    if not deleted:
        return jsonify({'error': 'Todo not found'}), 404
    
    return jsonify({'message': 'Todo deleted'}), 200

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5001, debug=False)

