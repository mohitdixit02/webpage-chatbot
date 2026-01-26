import React from 'react'
import { useEffect, useState, useRef } from 'react';
import Box from '@mui/material/Box';
import Avatar from '@mui/material/Avatar';
import SupportAgentIcon from '@mui/icons-material/SupportAgent';
import PersonIcon from '@mui/icons-material/Person';
import styles from "./index.module.css";
import CircularProgress from '@mui/material/CircularProgress';
import { send_query } from '../api';

export default function MessageSection({messages, addNewMessage, newQuery, setNewQuery, loading, setLoading, actvURL, behaviour, isExternalSearchEnabled}) {
  const messagesEndRef = useRef(null);

  useEffect(() => {
    if (!newQuery) return;
    console.log("New Query Detected in MessageSection");
    queryUser();
  }, [newQuery]);

  const queryUser = async () => {
      setLoading(true);
      const res = await send_query({
        "query": newQuery,
        "url": actvURL,
        "behaviour": behaviour,
        "externalSearch": isExternalSearchEnabled
      })
      
      if(res.res_status === 'success'){
        addNewMessage('bot', res.res_message);
      }
      else{
        addNewMessage('bot', 'Sorry, there was an error processing your request. Please try again later.');
      }
      setLoading(false);
      setNewQuery(null);
  }

  const renderMessageContent = (content) => {
    if (typeof content === "string" || typeof content === "number" || typeof content === "boolean") {
      return <p>{content}</p>;
    }
    if (Array.isArray(content)) {
      return (
        <ul style={{ marginLeft: 16 }}>
          {content.map((item, idx) => (
            <li key={idx}>{renderMessageContent(item)}</li>
          ))}
        </ul>
      );
    }
    if (typeof content === "object" && content !== null) {
      return (
        <div style={{ marginLeft: 8 }}>
          {Object.entries(content).map(([key, value], idx) => (
            <div key={key + idx} style={{ marginBottom: 5 }}>
              <strong>{key.charAt(0).toUpperCase() + key.slice(1)}:</strong>
              {renderMessageContent(value)}
            </div>
          ))}
        </div>
      );
  }
  return null;
}

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
              {msg.type === 'bot' && typeof msg.message === 'object' ?
               renderMessageContent(msg.message) : (
                msg.message
              )}
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
