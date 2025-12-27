import React, { useState, useEffect } from 'react';

const App = () => {
  const [tasks, setTasks] = useState([]);
  const [newTask, setNewTask] = useState('');
  const apiUrl = process.env.REACT_APP_API_URL;

  useEffect(() => {
    fetch(apiUrl+'/tasks')
      .then(response => response.json())
      .then(data => setTasks(data));
  }, [apiUrl]);

  const addTask = () => {
    fetch(apiUrl+'/tasks', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ task: newTask })
    })
      .then(response => response.json())
      .then(data => {
        setTasks([...tasks, { task: newTask }]);
        setNewTask('');
      });
  };

  const deleteTask = (taskToDelete) => {
    fetch(apiUrl+'/tasks', {
      method: 'DELETE',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ task: taskToDelete })
    })
      .then(response => response.json())
      .then(data => {
        setTasks(tasks.filter(task => task.task !== taskToDelete));
      });
  };

  return (
    <div>
      <h1>Task Manager</h1>
      <input
        type="text"
        value={newTask}
        onChange={(e) => setNewTask(e.target.value)}
        placeholder="New task"
      />
      <button onClick={addTask}>Add Task</button>
      <ul>
        {tasks.map((task, index) => (
          <li key={index}>
            {task.task}
            <button onClick={() => deleteTask(task.task)}>Delete</button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default App;
