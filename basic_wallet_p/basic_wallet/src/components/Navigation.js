import React from 'react';
import { Link } from 'react-router-dom';

const Navigation = (props) => {
    const { user } = props
    return (
        <nav className="navbar">
            <Link to='/'><h1>Coin Wallet</h1></Link>
            <h1>{user? user+"'s Account" : null}</h1>
        </nav>
    );
};

export default Navigation;
