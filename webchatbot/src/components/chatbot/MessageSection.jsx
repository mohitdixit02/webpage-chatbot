import React from 'react'
import { useEffect, useState, useRef } from 'react';
import Box from '@mui/material/Box';
import Avatar from '@mui/material/Avatar';
import SupportAgentIcon from '@mui/icons-material/SupportAgent';
import PersonIcon from '@mui/icons-material/Person';
import styles from "./index.module.css";
import CircularProgress from '@mui/material/CircularProgress';

export default function MessageSection({messages, setMessages, newQuery, setNewQuery, loading, setLoading}) {
  const messagesEndRef = useRef(null);
  const addBotMessage = (botMessage) => {
    setMessages(prevMessages => [
      ...prevMessages,
      {
        'type': 'bot',
        'message': botMessage
      }
    ]);
  };

  useEffect(() => {
    if (!newQuery) return;
    console.log("New Query Detected in MessageSection:", newQuery);
    setLoading(true);
    setTimeout(() => {
      addBotMessage(`This is a placeholder response to your query: "${newQuery}".`);
      setLoading(false);
    }, 2000);
    setNewQuery(null);
  }, [newQuery]);

  useEffect(() => {
    if (messagesEndRef.current) {
      messagesEndRef.current.scrollTop = messagesEndRef.current.scrollHeight;
    }
  }, [messages]);
  return (
    <Box component="section" className={styles['chatbot_messages_section']}>
      <Box className={styles['chatbot_messages_section_wrapper']} ref={messagesEndRef}>
        {messages.map((msg, index) => (
          <Box className={`${styles['chatbot_message_container']} ${msg.type === 'bot' ? styles['bot_message'] : styles['user_message']}`} key={`msg-${index}`}>
            <Avatar sx={ msg.type === 'bot' ? {'bgcolor':'rgb(29, 69, 92)'} : {'bgcolor':'rgb(125, 75, 29)'} }>
              {msg.type === 'bot' ? <SupportAgentIcon /> : <PersonIcon />}
            </Avatar>
            <Box
              className={`${styles['chatbot_message']}`}
            >
              {msg.message}
            </Box>
          </Box>
        ))}
        {loading ? 
          <Box className={`${styles['chatbot_message_container']} ${styles['bot_message']}`}>
            <Avatar sx={{'bgcolor':'rgb(41, 78, 100)'}}>
              <SupportAgentIcon />
            </Avatar>
            <div style={{"display":"flex", "alignItems":"center", "paddingLeft":"5px"}}>
              <CircularProgress size={"25px"} enableTrackSlot />
            </div>
          </Box>
        : ""}
      </Box>
    </Box>
  )
}
