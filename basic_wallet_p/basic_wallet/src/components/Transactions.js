import React, { useState, useEffect } from 'react';
import axios from 'axios';

function Transactions(props) {
    const { user } = props
    const [chain, setChain] = useState([])

    useEffect(() => {
        axios.get('http://localhost:5000/chain')
            .then(response => {
                setChain(response.data.chain)
            })
    }, [])

    const userTransactions = chain.map(block => {
        return block.transactions.filter(trans => {
            return trans.length !== 0 && (trans.recipient === user || trans.sender === user)
        })
    })

    const transactions = userTransactions.filter(trans => trans.length !== 0)
    let balance = 0

    for (let i = 0; i < transactions.length; i++) {
        for (let j = 0; j < transactions[i].length; j++) {
            if (transactions[i][j].recipient === user) {
                balance += Number(transactions[i][j].amount)
            }
            if (transactions[i][j].sender === user) {
                balance -= Number(transactions[i][j].amount)
            }
        }
    }

    return (
        <div class='transactions'>
            <div class="balance">Current Balance: {balance} Coins</div>
            {transactions.map(trans => (
                trans.map(t => (
                    <div class='transaction'>
                        <div>Recipient: {t.recipient}</div>
                        <div>Sender: {t.sender}</div>
                        <div>Amount: {t.amount}</div>
                    </div>
                ))
            ))}
        </div>
    );
}

export default Transactions