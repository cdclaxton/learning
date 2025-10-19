import express from 'express';
import cors from 'cors';
import { nanoid } from 'nanoid';
const app = express();
const port = 3000;
// Parse JSON using middleware
app.use(express.json());
// Allow CORS
app.use(cors());
;
const items = [
    {
        id: nanoid(),
        title: 'Wash the car',
        completed: true,
    },
    {
        id: nanoid(),
        title: 'Floss the cat',
        completed: false,
    },
    {
        id: nanoid(),
        title: 'Weekly shopping',
        completed: false,
    },
    {
        id: nanoid(),
        title: 'Learn Redux',
        completed: true,
    },
    {
        id: nanoid(),
        title: 'Pay car tax',
        completed: false,
    },
];
// GET all of the todos
app.get('/todos', (req, res) => {
    console.log(`${req.url} -- Todos requested`);
    res.send(items);
});
// POST a new todo
app.post('/todos', (req, res) => {
    const todo = {
        id: nanoid(),
        title: req.body.title,
        completed: false,
    };
    console.log(`${req.url} Adding a new todo: ${JSON.stringify(todo)}`);
    items.push(todo);
    return res.send(items);
});
// PATCH an existing todo by changing the completed status
app.patch('/todo/:id', (req, res) => {
    const id = req.params.id;
    console.log(`${req.url} Updating todo with ID: ${id}`);
    const index = items.findIndex((todo) => todo.id === id);
    const completed = Boolean(req.body.completed);
    if ((index > -1) && (items[index])) {
        items[index].completed = completed;
    }
    return res.send(items);
});
// DELETE an existing todo
app.delete('/todo/:id', (req, res) => {
    const id = req.params.id;
    console.log(`${req.url} Deleting todo with ID: ${id}`);
    const index = items.findIndex((todo) => todo.id === id);
    if (index > -1) {
        items.splice(index, 1);
    }
    res.send(items);
});
app.listen(port, () => {
    console.log(`Server running on ${port}`);
});
//# sourceMappingURL=server.js.map