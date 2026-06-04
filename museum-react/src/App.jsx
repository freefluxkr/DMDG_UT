import React, { useState, useEffect } from 'react';
import { Routes, Route } from 'react-router-dom';
import { AnimatePresence } from 'framer-motion';
import Lobby from './pages/Lobby';
import Chamber from './pages/Chamber';
import MediaGallery from './pages/MediaGallery';
import SplashIntro from './components/SplashIntro';

import PaperCutBackground from './components/PaperCutBackground';

function App() {
  const [showIntro, setShowIntro] = useState(true);

  useEffect(() => {
    // Hide intro after 5.5 seconds (allowing animations to finish)
    const timer = setTimeout(() => {
      setShowIntro(false);
    }, 5500);
    return () => clearTimeout(timer);
  }, []);

  return (
    <div className="w-full min-h-screen relative text-slate-800">
      <AnimatePresence>
        {showIntro && <SplashIntro />}
      </AnimatePresence>

      <PaperCutBackground />
      
      <Routes>
        <Route path="/" element={<Lobby />} />
        <Route path="/chamber/:palaceId" element={<Chamber />} />
        <Route path="/gallery/:palaceId" element={<MediaGallery />} />
      </Routes>
    </div>
  );
}

export default App;
