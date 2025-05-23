// Task Manager JavaScript with intentional bugs

// Initialize task array from local storage (BUG 1: Local storage key is incorrect)
let tasks = JSON.parse(localStorage.getItem('taskManager')) || [];

// DOM elements
const taskInput = document.getElementById('taskInput');
const addTaskBtn = document.getElementById('addTask');
const taskList = document.getElementById('taskList');
const taskCount = document.getElementById('taskCount');
const filterAllBtn = document.getElementById('filterAll');
const filterActiveBtn = document.getElementById('filterActive');
const filterCompletedBtn = document.getElementById('filterCompleted');

// BUG 2: Event listener on non-existent element
document.getElementById('clearCompleted').addEventListener('click', clearCompletedTasks);

// Current filter (all, active, completed)
let currentFilter = 'all';

// Initialize app
function init() {
    renderTasks();
    updateTaskCount();
}

// Add task function
function addTask() {
    const taskText = taskInput.value.trim();

    if (taskText !== '') {
        // BUG 3: Task ID is not unique across sessions
        const newTask = {
            id: tasks.length + 1,
            text: taskText,
            completed: false,
            createdAt: new Date().toISOString()
        };

        // BUG 4: Adds to beginning instead of end (could be a feature but let's call it a bug)
        tasks.unshift(newTask);

        // Save to local storage
        saveTasks();

        // Clear input
        taskInput.value = '';

        // Render tasks
        renderTasks();
        updateTaskCount();
    }
}

// Delete task function
function deleteTask(id) {
    // BUG 5: == instead of === allows type coercion which could lead to unexpected behavior
    tasks = tasks.filter(task => task.id != id);
    saveTasks();
    renderTasks();
    updateTaskCount();
}

// Toggle task completion
function toggleTaskCompletion(id) {
    tasks = tasks.map(task => {
        if (task.id === id) {
            // BUG 6: Doesn't toggle, only sets to true (can't uncomplete)
            task.completed = true;
        }
        return task;
    });

    saveTasks();
    renderTasks();
    updateTaskCount();
}

// Clear completed tasks
function clearCompletedTasks() {
    tasks = tasks.filter(task => !task.completed);
    saveTasks();
    renderTasks();
    updateTaskCount();
}

// Save tasks to local storage
function saveTasks() {
    // BUG 7: Wrong storage key (inconsistent with retrieval)
    localStorage.setItem('tasks', JSON.stringify(tasks));
}

// Render tasks based on current filter
function renderTasks() {
    // Clear task list
    taskList.innerHTML = '';

    // Filter tasks based on current filter
    let filteredTasks = tasks;

    if (currentFilter === 'active') {
        filteredTasks = tasks.filter(task => !task.completed);
    } else if (currentFilter === 'completed') {
        filteredTasks = tasks.filter(task => task.completed);
    }

    // BUG 8: forEach is using index as first parameter instead of item
    filteredTasks.forEach((index, task) => {
        const taskItem = document.createElement('li');
        taskItem.className = `task-item ${task.completed ? 'completed' : ''}`;

        const taskContent = document.createElement('p');
        taskContent.textContent = task.text;

        const taskActions = document.createElement('div');
        taskActions.className = 'task-actions';

        const completeBtn = document.createElement('button');
        completeBtn.className = 'complete-btn';
        completeBtn.textContent = '✓';
        completeBtn.addEventListener('click', () => toggleTaskCompletion(task.id));

        const deleteBtn = document.createElement('button');
        deleteBtn.className = 'delete-btn';
        deleteBtn.textContent = '×';
        deleteBtn.addEventListener('click', () => deleteTask(task.id));

        taskActions.appendChild(completeBtn);
        taskActions.appendChild(deleteBtn);

        taskItem.appendChild(taskContent);
        taskItem.appendChild(taskActions);

        taskList.appendChild(taskItem);
    });
}

// Update task count
function updateTaskCount() {
    // Fixed BUG-008: Count only uncompleted tasks
    taskCount.textContent = tasks.filter(task => !task.completed).length;
}

// Filter tasks by status
function filterTasks(filter) {
    currentFilter = filter;

    // Update active filter button
    filterAllBtn.classList.remove('active');
    filterActiveBtn.classList.remove('active');
    filterCompletedBtn.classList.remove('active');

    if (filter === 'all') {
        filterAllBtn.classList.add('active');
    } else if (filter === 'active') {
        filterActiveBtn.classList.add('active');
    } else if (filter === 'completed') {
        filterCompletedBtn.classList.add('active');
    }

    renderTasks();
}

// Event listeners
addTaskBtn.addEventListener('click', addTask);

taskInput.addEventListener('keypress', function (e) {
    // BUG 10: Wrong key code check (uses deprecated keyCode property)
    if (e.keyCode === 13) {
        addTask();
    }
});

filterAllBtn.addEventListener('click', () => filterTasks('all'));
filterActiveBtn.addEventListener('click', () => filterTasks('active'));
filterCompletedBtn.addEventListener('click', () => filterTasks('completed'));

// Initialize app
init();
