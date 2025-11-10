const API_URL = '/api/todos';

async function loadTodos() {
    try {
        const response = await fetch(API_URL);
        const todos = await response.json();
        renderTodos(todos);
    } catch (error) {
        console.error('Error loading todos:', error);
    }
}

function renderTodos(todos) {
    const todoList = document.getElementById('todoList');
    
    if (todos.length === 0) {
        todoList.innerHTML = '<div class="empty-state">No tasks yet. Add one above!</div>';
        return;
    }
    
    todoList.innerHTML = todos.map(todo => `
        <div class="todo-item ${todo.completed ? 'completed' : ''}">
            <input type="checkbox" ${todo.completed ? 'checked' : ''} 
                   onchange="toggleTodo(${todo.id})">
            <span class="todo-task">${escapeHtml(todo.task)}</span>
            <div class="todo-actions">
                <button class="btn-toggle" onclick="toggleTodo(${todo.id})">
                    ${todo.completed ? 'Undo' : 'Complete'}
                </button>
                <button class="btn-delete" onclick="deleteTodo(${todo.id})">Delete</button>
            </div>
        </div>
    `).join('');
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

async function addTodo() {
    const input = document.getElementById('taskInput');
    const task = input.value.trim();
    
    if (!task) {
        alert('Please enter a task');
        return;
    }
    
    try {
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ task })
        });
        
        if (response.ok) {
            input.value = '';
            loadTodos();
        } else {
            alert('Error adding todo');
        }
    } catch (error) {
        console.error('Error adding todo:', error);
        alert('Error adding todo');
    }
}

async function toggleTodo(id) {
    try {
        const response = await fetch(`${API_URL}/${id}`, {
            method: 'PUT'
        });
        
        if (response.ok) {
            loadTodos();
        }
    } catch (error) {
        console.error('Error toggling todo:', error);
    }
}

async function deleteTodo(id) {
    if (!confirm('Are you sure you want to delete this task?')) {
        return;
    }
    
    try {
        const response = await fetch(`${API_URL}/${id}`, {
            method: 'DELETE'
        });
        
        if (response.ok) {
            loadTodos();
        }
    } catch (error) {
        console.error('Error deleting todo:', error);
    }
}

document.getElementById('taskInput').addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        addTodo();
    }
});

loadTodos();

