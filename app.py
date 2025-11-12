from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import sqlite3
import os
import logging
from datetime import datetime
from contextlib import closing

app = Flask(__name__, static_folder='static')
CORS(app)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Use environment variables for configuration, with defaults for local development
DB_PATH = os.getenv('DB_PATH', 'todo.db')
APP_PORT = int(os.getenv('APP_PORT', '5001'))
APP_ENV = os.getenv('APP_ENV', 'development')

def init_db():
    """Initialize the SQLite database"""
    try:
        db_dir = os.path.dirname(DB_PATH)
        if db_dir:  # Only create directory if path contains a directory
            os.makedirs(db_dir, exist_ok=True)
        
        with closing(sqlite3.connect(DB_PATH)) as conn:
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
            logger.info(f'Database initialized at {DB_PATH}')
    except Exception as e:
        logger.error(f'Error initializing database: {e}')
        raise

@app.route('/')
def index():
    """Serve the frontend"""
    return send_from_directory('static', 'index.html')

@app.route('/api/todos', methods=['GET'])
def get_todos():
    """Get all todos"""
    try:
        with closing(sqlite3.connect(DB_PATH)) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM todos ORDER BY created_at DESC')
            todos = [dict(row) for row in cursor.fetchall()]
            logger.info(f'Retrieved {len(todos)} todos from database')
            return jsonify(todos)
    except Exception as e:
        logger.error(f'Error retrieving todos: {e}')
        return jsonify({'error': 'Failed to retrieve todos'}), 500

@app.route('/api/todos', methods=['POST'])
def create_todo():
    """Create a new todo"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        task = data.get('task', '').strip()
        
        if not task:
            return jsonify({'error': 'Task cannot be empty'}), 400
        
        with closing(sqlite3.connect(DB_PATH)) as conn:
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO todos (task, completed, created_at) VALUES (?, ?, ?)',
                (task, 0, datetime.now().isoformat())
            )
            conn.commit()
            todo_id = cursor.lastrowid
            logger.info(f'Created todo with ID {todo_id}: {task}')
            return jsonify({'id': todo_id, 'task': task, 'completed': 0}), 201
    except Exception as e:
        logger.error(f'Error creating todo: {e}')
        return jsonify({'error': 'Failed to create todo'}), 500

@app.route('/api/todos/<int:todo_id>', methods=['PUT'])
def update_todo(todo_id):
    """Update a todo (toggle completion)"""
    try:
        with closing(sqlite3.connect(DB_PATH)) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM todos WHERE id = ?', (todo_id,))
            todo = cursor.fetchone()
            
            if not todo:
                return jsonify({'error': 'Todo not found'}), 404
            
            new_completed = 1 if todo[2] == 0 else 0
            cursor.execute('UPDATE todos SET completed = ? WHERE id = ?', (new_completed, todo_id))
            conn.commit()
            logger.info(f'Updated todo {todo_id} to completed={new_completed}')
            return jsonify({'id': todo_id, 'completed': new_completed}), 200
    except Exception as e:
        logger.error(f'Error updating todo: {e}')
        return jsonify({'error': 'Failed to update todo'}), 500

@app.route('/api/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    """Delete a todo"""
    try:
        with closing(sqlite3.connect(DB_PATH)) as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM todos WHERE id = ?', (todo_id,))
            conn.commit()
            deleted = cursor.rowcount > 0
            
            if not deleted:
                return jsonify({'error': 'Todo not found'}), 404
            
            logger.info(f'Deleted todo {todo_id}')
            return jsonify({'message': 'Todo deleted'}), 200
    except Exception as e:
        logger.error(f'Error deleting todo: {e}')
        return jsonify({'error': 'Failed to delete todo'}), 500

@app.route('/health', methods=['GET'])
@app.route('/health/', methods=['GET'])  # Also handle trailing slash
def health():
    """Health check endpoint for monitoring"""
    return jsonify({
        'status': 'healthy',
        'environment': APP_ENV
    }), 200

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=APP_PORT, debug=(APP_ENV == 'development'))

