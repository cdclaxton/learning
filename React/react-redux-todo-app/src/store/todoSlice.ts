import { createAsyncThunk, createSlice, nanoid, PayloadAction } from '@reduxjs/toolkit';

export interface Item {
    id: string, // Unique ID for the item
    title: string, // Title of the todo, i.e. what to do
    completed: boolean, // Whether the todo has been completed
}

const initialState: Item[] = [];

interface AllTodos {
    todos: Item[]
}

interface SingleTodo {
    todo: Item
}

interface IdCompleted {
    id: string,
    completed: boolean
}

interface TitleOnly {
    title: string
}

export const getTodosAsync = createAsyncThunk(
    'todos/fetchAll',
    async (): Promise<AllTodos> => {
        const res = await fetch('http://localhost:7000/todos')
        const todos = await res.json()
        return { todos };
    }
)

export const addTodoAsync = createAsyncThunk(
    'todos/addTodoAsync',
    async (payload: TitleOnly): Promise<SingleTodo | undefined> => {
        const res = await fetch('http://localhost:7000/todos', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                title: payload.title
            })
        })

        if (res.ok) {
            const todo = await res.json();
            return { todo };
        }
    }
)

export const toggleCompleteAsync = createAsyncThunk(
    'todos/toggleTodoAsync',
    async (payload: IdCompleted): Promise<IdCompleted | undefined> => {
        const res = await fetch(`http://localhost:7000/todos/${payload.id}`, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                completed: payload.completed
            })
        })

        if (res.ok) {
            const todo = await res.json();
            return { id: todo.id, completed: todo.completed };
        }
    }
)

interface IdOnly {
    id: string
}

export const deleteTodoAsync = createAsyncThunk(
    'todos/deleteTodo',
    async (payload: IdOnly): Promise<AllTodos | undefined> => {
        const res = await fetch(`http://localhost:7000/todos/${payload.id}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
            }
        })
        
        if (res.ok) {
            const todos = await res.json()
            return { todos };
        }
    }
)

const todoSlice = createSlice({
    name: "todos",
    initialState,
    // Note that these three reducers aren't used as the async ones are now
    // used with the backend
    reducers: {
        addTodo: (state, action: PayloadAction<Item>) => {
            const newTodo = {
                id: nanoid(),
                title: action.payload.title,
                completed: false,
            };
            state.push(newTodo);
        },
        toggleComplete: (state, action: PayloadAction<Item>) => {
            const index = state.findIndex((todo) => todo.id === action.payload.id);
            state[index].completed = action.payload.completed;
        },
        deleteTodo: (state, action: PayloadAction<Item>) => {
            return state.filter((todo) => todo.id !== action.payload.id);
        }
    },
    extraReducers: (builder) => {
        builder.addCase(getTodosAsync.fulfilled, (_, action: PayloadAction<AllTodos>) => {
            return action.payload.todos;
        }),
        builder.addCase(addTodoAsync.fulfilled, (state, action: PayloadAction<SingleTodo | undefined>) => {
            if (action.payload) {   
                state.push(action.payload.todo);
            }
        }),
        builder.addCase(toggleCompleteAsync.fulfilled, (state, action: PayloadAction<IdCompleted | undefined>) => {
            if (action.payload) {
                const id = action.payload.id;
                const index = state.findIndex((todo) => todo.id === id);
                state[index].completed = action.payload.completed;
            }
        }),
        builder.addCase(deleteTodoAsync.fulfilled, (_, action: PayloadAction<AllTodos | undefined>) => {
            if (action.payload) {
                return action.payload.todos;
            }
        })        
    }
})

export const { addTodo, toggleComplete, deleteTodo } = todoSlice.actions;

export default todoSlice.reducer;