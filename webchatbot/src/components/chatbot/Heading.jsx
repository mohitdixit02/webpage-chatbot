import React from 'react'
import { useState } from 'react';
import styles from "./index.module.css";
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import Select from '@mui/material/Select';
import Checkbox from '@mui/material/Checkbox';
import ExploreOutlinedIcon from '@mui/icons-material/ExploreOutlined';
import ExploreOffOutlinedIcon from '@mui/icons-material/ExploreOffOutlined';
import { styled } from '@mui/material/styles';
import Tooltip, {tooltipClasses } from '@mui/material/Tooltip';

export default function Heading() {
        const behaviourOptions = [
            {
                value: "Explain",
                header: "Explain",
                description: "Reply with detailed explanation of the topic."
            },
            {
                value: "Summary",
                header: "Summary",
                description: "Provide a concise summary of the topic."
            },
            {
                value: "One-Line",
                header: "One-Line",
                description: "Quick One line answer to the query."
            }
        ];
        const [behaviour, setBehaviour] = useState('Summary');
        const label = { slotProps: { input: { 'aria-label': 'External Search' } } };
        const HtmlTooltip = styled(({ className, ...props }) => (
        <Tooltip {...props} classes={{ popper: className }} />
            ))(({ theme }) => ({
            [`& .${tooltipClasses.tooltip}`]: {
                backgroundColor: '#272727',
                maxWidth: 180,
                fontSize: theme.typography.pxToRem(12),
            },
        }));
  return (
    <div className={styles['chatbot_heading_section']}>            
        <div className={styles['chatbot_heading']}>
            Web<span>Chat</span>
        </div>
        <div className={styles['chatbot_heading_options']}>
            <HtmlTooltip 
                title={
                    <React.Fragment>
                        <h3>External Search</h3>
                        <p>Enable this option to allow the chatbot to perform external searches for more accurate and up-to-date information.</p>
                    </React.Fragment>
                }
                arrow
                placement="top-end"
                >
                <Checkbox
                    className={styles["model_explore_checkbox"]}
                    color='warning'
                    {...label}
                    icon={<ExploreOffOutlinedIcon 
                        sx={{color: 'white',
                            fontSize: '16px',
                    }} />}
                    checkedIcon={<ExploreOutlinedIcon
                        sx={{
                            fontSize: '16px'
                        }}
                        />}
                        />
            </HtmlTooltip>
            <FormControl className={styles["model_behaviour_select"]}>
                <InputLabel id="behaviour-select-label" color='warning' sx={{color:"white"}}>Model Behaviour</InputLabel>
                <Select
                    labelId="behaviour-select-label"
                    id="behaviour-select"
                    value={behaviour}
                    label="Model Behaviour"
                    onChange={(e)=>setBehaviour(e.target.value)}
                    color='warning'
                    sx={{color:"white",
                        border: '0px',
                        borderBottom: '0.5px solid rgb(192, 142, 42)',
                        fontSize: '12px',
                    }}
                    renderValue={(selected) => {
                        const option = behaviourOptions.find(opt => opt.value === selected);
                        return option ? option.header : selected;
                    }}
                    >
                    {behaviourOptions.map(opt => (
                        <MenuItem value={opt.value} key={opt.value}>
                        <div>
                            <div className={styles['menu_item_header']}>{opt.header}</div>
                            <div className={styles['menu_item_description']}>{opt.description}</div>
                        </div>
                        </MenuItem>
                    ))}
                </Select>
            </FormControl>
        </div>
    </div>
  )
}
