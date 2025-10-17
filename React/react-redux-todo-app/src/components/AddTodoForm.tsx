import React from 'react';
import { useAppDispatch } from '../hooks';
import { addTodoAsync } from '../store/todoSlice';

const AddTodoForm = () => {
    const [value, setValue] = React.useState('');
    const dispatch = useAppDispatch();

    const onSubmit = (event: any) => {
        event.preventDefault();
        dispatch(addTodoAsync({
            title: value
        }))
    }

    return(
        <form onSubmit={onSubmit} className='form-inline mt-3 mb-3'>
            <label className='sr-only'>Name</label>
            <input type='text' className='form-control mb-2 mr-sm-2'
                placeholder='Add todo...' value={value}
                onChange={(event) => setValue(event.target.value)} />
            <button type='submit' className='btn btn-primary mb-2'>
                Submit
            </button>
        </form>
    )
}

export default AddTodoForm;