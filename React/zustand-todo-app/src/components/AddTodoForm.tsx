import React from 'react';
import { useItemStore } from '../store/store';

const AddTodoForm = () => {
    const [value, setValue] = React.useState('');
    const addItem = useItemStore((state) => state.addItem)

    const onSubmit = (event) => {
        event.preventDefault();
        addItem(value);
    }

    return (
        <form onSubmit={onSubmit} className='form-inline mt-3 mb-3'>
            <label className='sr-only'>Name</label>
            <input type='text' className="form-control mb-2 mr-sm-2" 
                placeholder="Add todo ..." value={value}
                onChange={(event) => setValue(event.target.value)} />
            <button type='submit' className='btn btn-primary mb-2'>Submit</button>
        </form>
    )
}

export default AddTodoForm;