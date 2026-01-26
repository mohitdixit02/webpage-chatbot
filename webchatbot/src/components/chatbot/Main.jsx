import styles from "./index.module.css";
import Container from '@mui/material/Container';
import Heading from "./Heading";
import BotInput from './BotInput';
import MessageSection from './MessageSection';
import { useEffect, useState } from 'react';

export default function ChatBot() {
    const [loading, setLoading] = useState(false);
    const [messages, setMessages] = useState([
        {
        'type': 'bot',
        'message': 'Hello! How can I assist you today?'
        },
    ]);

    const [newQuery, setNewQuery] = useState(null);

    return (
        <Container maxWidth="" className={styles['chatbot_main']}>
            <Heading />
            <MessageSection 
                messages={messages} 
                setMessages={setMessages} 
                newQuery={newQuery} 
                setNewQuery={setNewQuery}
                loading={loading}
                setLoading={setLoading}
            />
            <BotInput 
                messages={messages} 
                setMessages={setMessages} 
                setNewQuery={setNewQuery}
                loading={loading}
            />
        </Container>
        )
}
