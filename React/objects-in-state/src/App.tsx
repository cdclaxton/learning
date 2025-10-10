import React from 'react';

function SetNameUsingState() {
  const [person, setPerson] = React.useState({
    name: "Bob",
  })

  return(
    <div className="approach">
      <p>Set name using state:</p>
      <div>
        <label>
          Name:
          <input value={person.name} 
            onChange={e => setPerson({name: e.target.value})} />
        </label>
      </div>
    </div>
  )
}

class Person {
  name: string

  constructor(name: string) {
    this.name = name;
  }

  updateName(newName: string) {
    this.name = newName;
  }
}

function SetNameUsingMutableClass() {
  const [state, setState] = React.useState({
    person: new Person('Robert')
  })

  return(
    <div className="approach">
      <p>Set name using a mutable class:</p>
      <div>
        <label>
          Name:
          <input value={state.person.name} 
            onChange={e => {
              state.person.updateName(e.target.value);
              setState({person: state.person})
            }} />
        </label>
      </div>
    </div>
  )
}

class PersonAge {
  name: string
  age: number

  constructor(name: string, age: number) {
    this.name = name;
    this.age = age;
  }

  updateName(newName: string) {
    this.name = newName;
  }

  updateAge(newAge: number) {
    this.age = newAge;
  }
}

interface State {
  person: PersonAge
}

function AgeComponent({state, setState}: {state: State, 
  setState: React.Dispatch<React.SetStateAction<State>>}) {
  return (
    <label>
      Age:
      <input value={state.person.age}
        onChange={e => {
          state.person.updateAge(Number(e.target.value));
          setState({person: state.person});
        }}
      />
    </label>
  )
}

function SetNameAndAgeUsingMutableClass() {
  const [state, setState] = React.useState<State>({
    person: new PersonAge('Robert', 42)
  })

  return(
    <div className="approach">
      <p>Set name using a mutable class with a child component:</p>
      <div>
        <label>
          Name:
          <input value={state.person.name} 
            onChange={e => {
              state.person.updateName(e.target.value);
              setState({person: state.person})
            }} />
        </label>
        <AgeComponent state={state} setState={setState} />
      </div>
    </div>
  )
}

interface NameAction {
  type: string
  newName: string
}

function nameReducer(name: string, action: NameAction) {
  switch (action.type) {
    case 'changed': {
      return action.newName
    }
    default: {
      throw Error(`Unknown action: ${action}`)
    }
  }
}

function SetNameUsingReducer() {
  const [name, dispatch] = React.useReducer(nameReducer, "David");

  function handleChange(name: string) {
    dispatch({
      type: 'changed',
      newName: name,
    })
  }

  return (
    <div className="approach">
      <p>Set name using a reducer:</p>
      <div>
        <label>
          Name:
          <input value={name} 
            onChange={e => handleChange(e.target.value)} />
        </label>
      </div>      
    </div>
  )
}

function personReducer(person: Person, action: NameAction) {
  switch (action.type) {
    case 'changed': {
      person.updateName(action.newName);
      return person;
    }
    default: {
      throw Error(`Unknown action: ${action}`)
    }
  }
}

function SetNameUsingReducerWithClass() {
  const initial = new Person('Sally');
  const [person, dispatch] = React.useReducer(personReducer, initial);

  function handleChange(name: string) {
    dispatch({
      type: 'changed',
      newName: name,
    })
  }

  return (
    <div className="approach">
      <p>Set name using a reducer on a class (doesn't work because the object is mutating):</p>
      <div>
        <label>
          Name:
          <input value={person.name} 
            onChange={e => handleChange(e.target.value)} />
        </label>
      </div>      
    </div>
  )
}

function App() {
  return (
    <>
      <SetNameUsingState />
      <SetNameUsingMutableClass />
      <SetNameAndAgeUsingMutableClass />
      <SetNameUsingReducer />
      <SetNameUsingReducerWithClass />
    </>
  );
}

export default App;
