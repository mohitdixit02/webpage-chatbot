import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_SERVER_URL + "/api";
const EXTENSION_AUTH_ID = process.env.REACT_APP_EXTENSION_AUTH_ID;
console.log(BACKEND_URL);

const reqApi = async (url, method = 'GET', body = null) =>{
    try{
        const res = await axios({
            url: `${BACKEND_URL}${url}`,
            method,
            data: body,
            headers:{
                'X-EXTENSION-AUTH-ID': EXTENSION_AUTH_ID
            }
        });
        return res.data;
    }
    catch (error){
        console.error('API Error:', error);
        return {
            "res_status" : false,
            "res_message" : "Some error has occured! Please try again later"
        };
    }
}

const send_web_url = async (url) => {
    return await reqApi('/load_script/', 'POST', {"url":url});
};

const send_query = async(body) => {
    return await reqApi('/query/', 'POST', body);
}

export {
    send_web_url,
    send_query
};