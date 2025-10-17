import { useAppSelector } from '../hooks';

const TotalCompleteItems = () => {
    const completedTodos = useAppSelector(
        (state) => state.todos.filter((todo) => todo.completed)
    );

    return (
        <h4 className='mt-3'>Total complete items: {completedTodos.length}</h4>
    )
}

export default TotalCompleteItems;