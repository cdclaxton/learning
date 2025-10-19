import type { Item } from '../model/types';
import { useItemStore } from '../store/store';

const TodoItem = ({item}: {item: Item}) => {

    const deleteItem = useItemStore((state) => state.deleteItem);
    const toggleCompleted = useItemStore((state) => state.toggleCompleted);

    const handleCompletedClick = () => {
        toggleCompleted(item.id);
    }

    const handleDeleteClick = () => {
        deleteItem(item.id);
    }

    return (
        <li className={`list-group-item ${item.completed && 'list-group-item-success'}`}>
            <div className='d-flex justify-content-between'>
                <span className='d-flex align-items-center'>
                    <input type='checkbox' className='mr-3'
                        onChange={handleCompletedClick}
                        checked={item.completed} />
                    {item.title}
                </span>
                <button className='btn btn-danger'
                    onClick={handleDeleteClick}>Delete</button>
            </div>
        </li>
    )
}

export default TodoItem;