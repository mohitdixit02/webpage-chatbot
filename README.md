# WebPage Chatbot
A Chrome extension chatbot that answers user queries based on the content of the currently open webpage. The project features a chatbot UI as a Chrome extension, integrated with a Retrieval-Augmented Generation (RAG) backend built using FastAPI. It uses Hugging Face models and Wikipedia retrieval to provide contextual responses.

### Key Features
- `Contextual Responses:` Provides answers based on the content of the webpage you are viewing.
- `External Search:` When enabled by the user, Backend uses Wikipedia to fetch additional information based on the user query before responding.
- `Automatic Fallback:` If webpage content is insufficient, the chatbot automatically performs external searches even if it is not enabled.
- `Model Behavior:` Can Explain, Summarize or give one-line answers based on user selection.
- `In-built Context based Filtering:` Filters out irrelevant information to provide accurate responses. It involves optimizations at database as well as retriver level.
- `Efficient Resource Management:` Caches and manages webpage content to maintain performance and limit database size.
- `Additional Attribution:` The chatbot informs users when answers are based on external sources, especially if external search was performed automatically or fallback was triggered. Same thing applied if external search fails but was requested by user. This ensures transparency about the source of information.

## Installation
### Prerequisites
Make sure you have following installed in your system:
1. Node.js (21.7 used in this project)
2. Conda (25.9 used in this project) (Recommended) or Python 3.11+
3. Hugging Face API Key (You can create one by signing up at Hugging face website)

### Setup
1. Clone the repository:
   ```bash
    git clone git@github.com:mohitdixit02/webpage-chatbot.git
    cd webpage-chatbot
    ```

2. Backend Setup:
    - Enter into the backend directory:
        ```bash
        cd backend
        ```
    - If you have conda installed, create a conda environment:
        ```bash
        conda env create -f environment.yml
        conda activate webpage-chatbot
        ```
    - If you don't have conda, create a virtual environment using venv. For windows:
        ```bash
        python -m venv venv
        .\venv\Scripts\activate
        pip install -r requirements.txt
        ```
    - Create a env file by referencing the `env.example` and add your Hugging Face API key in `HF_TOKEN`. 
        - For `FRONTEND_URL`, you can use the default one in `env.example`.
        - For `BACKEND_EXTENSION_AUTH_ID`, you can generate a random value on your own. Make sure its the same in both frontend and backend env files.
        - For `HF_CACHE_DIR`, provide a valid path in your system where you want to store the Hugging Face models cache. Currently, Embedding Model run locally based on the `transformers` module.

    - Make sure you are in the activated environment and run the backend server:
        ```bash
        uvicorn app:app --host 127.0.0.1 --port 8000
        ``` 

3. Frontend Setup:
    - Open a new terminal and navigate to the frontend directory:
        ```bash
        cd ../webchatbot
        ```
    - Install the dependencies:
        ```bash
        npm install
        ```
    - Create a env file by referencing the `env.example` and add your `BACKEND_EXTENSION_AUTH_ID` in it. Make sure its the same in both frontend and backend env files. For `REACT_APP_NODE_ENV`, use `production` before building the extension. For `REACT_APP_SERVER_URL`, use the backend server url.

    - Build the extension:
        ```bash
        npm run build
        ```
    - Load the extension in Chrome:
        - Open Chrome and go to `chrome://extensions/`
        - Enable "Developer mode" using the toggle on the top right.
        - Click on "Load unpacked" and select the `build` folder inside the `webchatbot` directory.

    Note: Use `development` in `REACT_APP_NODE_ENV` only if you want to run it for testing. Make sure to change it to `production` before building the extension for actual use.


## Project Architecture
![Chatbot Architecture](images/chatbot_architecture.png)

## Challenges and Optimizations


## Modules and Libraries Used

## References


     