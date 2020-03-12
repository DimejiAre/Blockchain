import React, { useState } from 'react';
import './App.css';
import { Route } from 'react-router-dom';
import Transactions from './components/Transactions';
import Navigation from './components/Navigation';
import UserForm from './components/UserForm';
import './styles.scss'

function App() {
  const [user, setUser] = useState("")

  const search = (formValue, actions) => {
    const user = formValue.name
    setUser(user)
  }

  return (
    <div className="App">
      <Route path='/' render={props => <Navigation {...props} user={user}/>} />
      <Route path='/' render={props => <UserForm {...props} search={search} />} />
      <Route path='/' render={props => <Transactions {...props} user={user} />} />
    </div>
  );
}

export default App;
