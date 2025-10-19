import { create } from 'zustand';
import type { Item } from '../model/types';
import { nanoid } from 'nanoid';

type ItemStore = {
    items: Item[];
    addItem: (title: string) => void;
    deleteItem: (id: string) => void;
    toggleCompleted: (id: string) => void;
}

// Create a new item given the item's title.
const newItem = (title: string): Item => {
    return {
        id: nanoid(),
        title: title,
        completed: false,
    }
}

const updateCompletedStatus = (state: ItemStore, id: string) => {
    const items = [...state.items];
    const index = items.findIndex((item) => item.id === id);
    items[index].completed = !items[index].completed;
    return items;
}

// custom hook
export const useItemStore = create<ItemStore>((set) => ({
    items: [
        {
            id: "A1",
            title: "Wash car",
            completed: false,
        },
        {
            id: "A2",
            title: "Floss the cat",
            completed: true,
        },
    ],
    addItem: (title: string) => set((state) => ({items: [...state.items, newItem(title)]})),
    deleteItem: (id: string) => set((state) => ({items: state.items.filter((item) => item.id !== id)})),
    toggleCompleted: (id: string) => set((state) => ({items: updateCompletedStatus(state, id)})),
}));