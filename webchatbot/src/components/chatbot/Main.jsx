import styles from "./index.module.css";
import Container from '@mui/material/Container';
import Heading from "./Heading";
import BotInput from './BotInput';
import MessageSection from './MessageSection';
import { useEffect, useState } from 'react';
import { send_web_url } from "../api";

export default function ChatBot() {
    const [loading, setLoading] = useState(false);
    const [actvURL, setActvURL] = useState(null);
    const [messages, setMessages] = useState([]);
    const [behaviour, setBehaviour] = useState('Summary');
    const [isExternalSearchEnabled, setIsExternalSearchEnabled] = useState(false);

    const addNewMessage = (msgType, msgContent) => {
        setMessages(prevMessages => [
            ...prevMessages,
            {
                'type': msgType,
                'message': msgContent
            }
        ]);
    };

    useEffect(() => {
        // Wait for 3 seconds and then send request to backend
        setTimeout(() => {
            setLoading(true);
            loadWebScripts();
        }, 3000);
    }, []);

    const loadWebScripts = async() => {
        if(window.chrome && window.chrome.tabs){
            window.chrome.tabs.query({active: true, currentWindow: true}, async (tabs) => {
                const currentTabUrl = tabs[0].url;
                let res = await send_web_url(currentTabUrl);
                if(res.res_status === 'success'){
                    setActvURL(currentTabUrl);
                    addNewMessage('bot', 'Hello! How can I assist you today?');
                }
                else{
                    setActvURL(null);
                    addNewMessage('bot', 'Hello! Unfortunately, I could not load the webpage content. Sorry for the inconvenience.');
                }
                setLoading(false);
            });
        }
        else{
            console.log("Chrome tabs API not available.");
            addNewMessage('bot', 'Hello! Unfortunately, I am not supported in this environment.');
            setLoading(false);
        }
    }

    const [newQuery, setNewQuery] = useState(null);

    return (
        <Container maxWidth="" className={styles['chatbot_main']}>
            <Heading
                behaviour={behaviour}
                setBehaviour={setBehaviour}
                isExternalSearchEnabled={isExternalSearchEnabled}
                setIsExternalSearchEnabled={setIsExternalSearchEnabled}
            />
            <MessageSection 
                messages={messages} 
                addNewMessage={addNewMessage} 
                newQuery={newQuery}
                setNewQuery={setNewQuery}
                loading={loading}
                setLoading={setLoading}
                actvURL={actvURL}
                behaviour={behaviour}
                isExternalSearchEnabled={isExternalSearchEnabled}
            />
            <BotInput 
                messages={messages} 
                addNewMessage={addNewMessage} 
                setNewQuery={setNewQuery}
                loading={loading}
                actvURL={actvURL}
            />
        </Container>
        )
}
