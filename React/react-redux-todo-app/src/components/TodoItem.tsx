import { useAppDispatch  } from '../hooks';
import { Item, toggleCompleteAsync, deleteTodoAsync } from '../store/todoSlice';

const TodoItem = ({id, title, completed}: Item) => {

    const dispatch = useAppDispatch();

    const handleCompleteClick = () => {
        dispatch(toggleCompleteAsync({
            id: id,
            completed: !completed,
        }))
    }

    const handleDeleteClick = () => {
        dispatch(deleteTodoAsync({
            id: id
        }))
    }

    return (
        <li className={`list-group-item ${completed && 'list-group-item-success'}`} >
            <div className='d-flex justify-content-between'>
                <span className='d-flex align-items-center'>
                    <input type='checkbox' className='mr-3' 
                        onChange={() => handleCompleteClick()}
                        checked={completed} />
                    {title}
                </span>
                <button className='btn btn-danger'
                    onClick={() => handleDeleteClick()}>Delete</button>
            </div>
        </li>
    )
}

export default TodoItem;