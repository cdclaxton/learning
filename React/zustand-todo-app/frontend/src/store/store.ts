import { create } from 'zustand';
import type { Item } from '../model/types';

interface ItemStore {
    items: Item[];
    fetch: () => void;
    addItem: (title: string) => void;
    deleteItem: (id: string) => void;
    toggleCompleted: (id: string, completed: boolean) => void;
}

// Fetch items from the backend.
const fetchItems = (): Promise<Item[]> => {
    return fetch('http://localhost:3000/todos', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        }
    }).then(r => r.json())
}

// Add an item to the todo list.
const addItem = (title: string) => {
    return fetch('http://localhost:3000/todos', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            title: title,
        })
    }).then(_ => true).catch(_ => false);
};

// Delete an item from the todo list.
const deleteItem = (id: string) => {
    return fetch(`http://localhost:3000/todo/${id}`, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json',
        }
    }).then(_ => true).catch(_ => false);
};

// Toggle whether a todo item is completed.
const toggleCompleted = (id: string, completed: boolean) => {
    return fetch(`http://localhost:3000/todo/${id}`, {
        method: 'PATCH',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            completed: completed,
        })
    }).then(_ => true).catch(_ => false);    
}

// Custom hook
export const useItemStore = create<ItemStore>((set) => ({
    items: [],
    fetch: async () => {
        const items = await fetchItems();
        set((state) => ({
            items: items,
        }))
    },
    addItem: async (title: string) => {
        const res = await addItem(title);
        const items = await fetchItems();
        set((state) => ({
            items: items,
        }))
    },
    deleteItem: async (id: string) => {
        const res = await deleteItem(id);
        const items = await fetchItems();
        set((state) => ({
            items: items,
        }))
    },
    toggleCompleted: async (id: string, completed: boolean) => {
        const res = await toggleCompleted(id, completed);
        const items = await fetchItems();
        set((state) => ({
            items: items,
        }))
    },
}));
