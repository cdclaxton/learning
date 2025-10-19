import { useItemStore } from "../store/store";
import TodoItem from "./TodoItem";

const TodoList = () => {
    const todos = useItemStore((state) => state.items);

    return (
        <ul className="list-group">
            {todos.map((todo) => (
                <TodoItem key={todo.id} item={todo} />
            ))}
        </ul>
    )
}

export default TodoList;