import ChatBot from './components/chatbot/Main';

const isProd = process.env.NODE_ENV === 'production';
const appStyle = {
  width: isProd ? '500px' : '100vw',
  height: isProd ? '500px' : '100vh',
  backgroundColor: 'rgb(32, 31, 31)',
  color: 'white'
};

function App() {
  return (
    <div className="App" style={appStyle}>
      <ChatBot/>
    </div>
  );
}

export default App;
