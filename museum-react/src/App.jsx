import { Routes, Route } from 'react-router-dom';
import Lobby from './pages/Lobby';
import Chamber from './pages/Chamber';

function App() {
  return (
    <div className="w-full h-screen bg-[#090d16] text-white overflow-hidden relative">
      {/* Background Mist Animation */}
      <div className="mist-container">
        <div className="mist" />
      </div>
      
      <Routes>
        <Route path="/" element={<Lobby />} />
        <Route path="/chamber/:palaceId" element={<Chamber />} />
      </Routes>
    </div>
  );
}

export default App;
