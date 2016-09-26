/**
 * Created by Jeffrey on 9/20/2016.
 */

import React from "react";
import {observer} from "mobx-react";

export const Chat = observer(({chat_store, allies_store}) => {
    let messages = chat_store.messages.map((message) => {
        return (
            <li key={message.id}>{[message.name, ": ", message.text]}</li>
        )
    });

    return (
    <div>
        <ul id="messages">
            {messages}
        </ul>
        <ChatForm chat_store={chat_store} allies_store={allies_store}/>
    </div>
    );
});

const ChatForm = observer(({chat_store, allies_store}) => {
    function handleSubmit(e) {
        e.preventDefault();
        transport_layer.send_msg(allies_store.me.name, chat_store.outgoing_message);
    }

    function handleChange(e) {
        chat_store.outgoing_message = e.target.value;
    }

    return (
        <form onSubmit={handleSubmit}>
            <input id="chat-input" onChange={handleChange} autoComplete="off"/><button type="submit">Send</button>
        </form>
    );
});