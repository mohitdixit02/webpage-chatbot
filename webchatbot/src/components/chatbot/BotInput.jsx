import React from 'react'
import { useState } from 'react';
import TextField from '@mui/material/TextField';
import SendIcon from '@mui/icons-material/Send';
import styles from "./index.module.css";

import IconButton from '@mui/material/IconButton';
import CircularProgress from '@mui/material/CircularProgress';

export default function BotInput({messages, addNewMessage, setNewQuery, loading, actvURL}) {
    const [userInput, setUserInput] = useState("");
    const addUserMessage = (e) => {
        console.log(e);
        if(e.type === 'keydown' && e.key !== 'Enter') return;
        if (userInput.trim() === "") return;
        addNewMessage('user', userInput);
        setNewQuery(userInput);
        setUserInput("");
    }

  return (
    <div className={styles['chatbot_input_section']}>
        <div className={styles["message_input_field_holder"]}>
            <TextField 
                className={styles["message_input_field"]} 
                fullWidth 
                label="Ask your Question" 
                variant="filled"
                color='warning'
                disabled={(actvURL === null || loading)}
                slotProps={{
                    inputLabel: {
                        style: { color: 'rgb(168, 168, 168)',
                            fontSize: '14px',
                         }
                    },
                    input: {
                        style: { color: 'white',
                            borderBottom: '0.5px solid rgb(192, 142, 42)',
                            borderRadius: '4px',
                            fontSize: '12px',
                         }
                    }
                }}
                onKeyDown={addUserMessage}
                value={userInput}
                onChange={(e) => setUserInput(e.target.value)}
                />
            <IconButton onClick={addUserMessage} variant="contained" className={styles["message_send_button"]}>
                {loading ? (
                    <div style={{display: 'flex', alignItems: 'center', justifyContent: 'center', padding: '10px'}}>
                        <CircularProgress size={18} color='warning' />
                    </div>
                ) : (
                    <SendIcon disabled={(actvURL === null)} color='warning' sx={{ fontSize: '18px', padding: '10px' }} />
                )}
            </IconButton>
        </div>
    </div>
  )
}
