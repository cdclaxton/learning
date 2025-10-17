import React from 'react';
import TodoItem from './TodoItem';
import { useAppSelector, useAppDispatch } from '../hooks';
import{ getTodosAsync } from '../store/todoSlice';

const TodoList = () => {
    const dispatch = useAppDispatch();
    const todos = useAppSelector( (state) => state.todos);

    React.useEffect(() => {
        dispatch(getTodosAsync())
    }, [dispatch])

    return(
        <ul className='list-group'>
            {todos.map((todo) => (
                <TodoItem key={todo.id} id={todo.id} title={todo.title} completed={todo.completed} />
            ))}
        </ul>
    )
}

export default TodoList;
