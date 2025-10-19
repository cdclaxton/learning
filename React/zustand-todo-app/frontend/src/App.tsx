import react from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import AddTodoForm from './components/AddTodoForm';
import TodoList from './components/TodoList';
import TotalCompleteItems from './components/TotalCompleteItems';
import { useItemStore } from "./store/store";

function App() {

  // Populate the item store on component load
  const fetch = useItemStore(s => s.fetch);
  react.useEffect(() => {
    console.log("App loaded");
    fetch();
  }, []);

  return (
    <div className='container bg-white p-4 mt-5'>
      <h1>My Todo List</h1>
      <AddTodoForm />
      <TodoList />
      <TotalCompleteItems />
    </div>
  )
}

export default App
