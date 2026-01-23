#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

class TodoApp {
  constructor() {
    this.todos = [];
    this.nextId = 1;
    this.dataFile = path.join(process.cwd(), 'todos.json');
    this.loadTodos();
  }

  loadTodos() {
    try {
      if (fs.existsSync(this.dataFile)) {
        const data = JSON.parse(fs.readFileSync(this.dataFile, 'utf8'));
        this.todos = data.todos || [];
        this.nextId = data.nextId || 1;
      } else {
        this.todos = [];
        this.nextId = 1;
      }
    } catch (error) {
      console.error('Error loading todos:', error.message);
      this.todos = [];
      this.nextId = 1;
    }
  }

  saveTodos() {
    try {
      const data = {
        todos: this.todos,
        nextId: this.nextId
      };
      fs.writeFileSync(this.dataFile, JSON.stringify(data, null, 2));
    } catch (error) {
      throw new Error(`Failed to save todos: ${error.message}`);
    }
  }

  add(description) {
    if (!description || description.trim() === '') {
      throw new Error('Error: Todo description cannot be empty');
    }

    const newTodo = {
      id: this.nextId++,
      description: description.trim(),
      completed: false,
      createdAt: new Date().toISOString()
    };

    this.todos.push(newTodo);
    this.saveTodos();

    return `Added todo with ID ${newTodo.id}: ${newTodo.description}`;
  }

  list() {
    if (this.todos.length === 0) {
      return 'No todos found.';
    }

    let output = 'Todo List:\n';
    output += this.todos.map(todo =>
      `${todo.id}. [${todo.completed ? 'x' : ' '}] ${todo.description}`
    ).join('\n');

    return output;
  }

  update(id, newDescription) {
    const todoIndex = this.todos.findIndex(todo => todo.id === parseInt(id));

    if (todoIndex === -1) {
      throw new Error(`Error: Todo item with ID ${id} not found`);
    }

    if (!newDescription || newDescription.trim() === '') {
      throw new Error('Error: Todo description cannot be empty');
    }

    this.todos[todoIndex].description = newDescription.trim();
    this.saveTodos();

    return `Updated todo ${id}: ${newDescription}`;
  }

  delete(id) {
    const initialLength = this.todos.length;
    this.todos = this.todos.filter(todo => todo.id !== parseInt(id));

    if (this.todos.length === initialLength) {
      throw new Error(`Error: Todo item with ID ${id} not found`);
    }

    this.saveTodos();
    return `Deleted todo with ID ${id}`;
  }

  mark(id, status) {
    const todo = this.todos.find(todo => todo.id === parseInt(id));

    if (!todo) {
      throw new Error(`Error: Todo item with ID ${id} not found`);
    }

    if (status !== 'complete' && status !== 'incomplete') {
      throw new Error("Error: Status must be 'complete' or 'incomplete'");
    }

    todo.completed = (status === 'complete');
    this.saveTodos();

    return `Marked todo ${id} as ${status}`;
  }

  help() {
    return `
Todo Console Application Help

Available Commands:
  add <description>           - Add a new todo item
  list                       - List all todo items
  update <id> <description>  - Update a todo item's description
  delete <id>               - Delete a todo item
  mark <id> <complete|incomplete> - Mark a todo as complete/incomplete
  help                      - Show this help message
  quit/exit                 - Exit the application
    `.trim();
  }
}

function main() {
  const app = new TodoApp();
  const args = process.argv.slice(2);

  if (args.length === 0) {
    // Interactive mode
    console.log('Todo Console Application');
    console.log('Type "help" for available commands or "quit" to exit.\n');

    const readline = require('readline');
    const rl = readline.createInterface({
      input: process.stdin,
      output: process.stdout
    });

    function prompt() {
      rl.question('> ', (input) => {
        const command = input.trim();

        if (command.toLowerCase() === 'quit' || command.toLowerCase() === 'exit') {
          console.log('Goodbye!');
          rl.close();
          return;
        }

        try {
          const result = processCommand(app, command);
          console.log(result);
        } catch (error) {
          console.log(error.message);
        }

        prompt();
      });
    }

    prompt();
  } else {
    // Command mode
    try {
      const result = processCommand(app, args.join(' '));
      console.log(result);
    } catch (error) {
      console.log(error.message);
      process.exit(1);
    }
  }
}

function processCommand(app, commandLine) {
  const parts = commandLine.split(' ');
  const cmd = parts[0].toLowerCase();
  const params = parts.slice(1);

  switch (cmd) {
    case 'add':
      if (params.length === 0) {
        throw new Error('Error: Missing description for add command');
      }
      return app.add(params.join(' '));

    case 'list':
      return app.list();

    case 'update':
      if (params.length < 2) {
        throw new Error('Error: Missing ID or new description for update command');
      }
      return app.update(params[0], params.slice(1).join(' '));

    case 'delete':
      if (params.length < 1) {
        throw new Error('Error: Missing ID for delete command');
      }
      return app.delete(params[0]);

    case 'mark':
      if (params.length < 2) {
        throw new Error('Error: Missing ID or status for mark command');
      }
      return app.mark(params[0], params[1].toLowerCase());

    case 'help':
      return app.help();

    case 'quit':
    case 'exit':
      console.log('Goodbye!');
      process.exit(0);

    default:
      throw new Error(`Error: Unknown command '${cmd}'. Type 'help' for available commands.`);
  }
}

if (require.main === module) {
  main();
}

module.exports = TodoApp;