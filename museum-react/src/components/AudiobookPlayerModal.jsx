import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';

let audiobookUtterance = null;

function AudiobookPlayerModal({ isOpen, onClose, theme, email }) {
  const [isPlaying, setIsPlaying] = useState(false);
  const [progress, setProgress] = useState(0);

  const rawAccent = theme?.accentHex || '#ea580c';

  useEffect(() => {
    if (!isOpen) {
      window.speechSynthesis.cancel();
      setIsPlaying(false);
      setProgress(0);
    }
  }, [isOpen]);

  const togglePlay = () => {
    if (isPlaying) {
      window.speechSynthesis.pause();
      setIsPlaying(false);
    } else {
      if (window.speechSynthesis.paused && audiobookUtterance) {
        window.speechSynthesis.resume();
        setIsPlaying(true);
      } else {
        startAudiobook();
      }
    }
  };

  const startAudiobook = () => {
    window.speechSynthesis.cancel();

    const spiritScript = theme.name === '광화문' ? '단종' : theme.name === '창경궁' ? '사도세자' : '고종 황제';
    const script = `${theme.name}의 깊은 밤. ${email.split('@')[0]} 님께서 남겨주신 발자취를 따라 이야기가 시작됩니다. 
    수백 년 전, 닫힌 문틈 사이로 흘러나오던 ${spiritScript}의 슬픈 한숨은, 
    오늘 당신이 남겨준 따뜻한 위로의 향기와 만나 비로소 평안을 얻습니다. 
    비는 대지를 적시고, 당신의 목소리는 시공을 넘어 영혼의 마음에 가닿아 한 편의 아름다운 시가 되었습니다.`;

    const utterance = new SpeechSynthesisUtterance(script);
    utterance.lang = 'ko-KR';
    utterance.rate = 0.85;
    utterance.pitch = 0.8;

    audiobookUtterance = utterance;

    utterance.onstart = () => setIsPlaying(true);
    utterance.onend = () => {
      setIsPlaying(false);
      audiobookUtterance = null;
      setProgress(0);
    };
    utterance.onerror = (e) => {
      console.error('TTS Error', e);
      setIsPlaying(false);
      audiobookUtterance = null;
    };
    
    setProgress(0);
    window.speechSynthesis.speak(utterance);
    
    if (window.speechSynthesis.paused) {
      window.speechSynthesis.resume();
    }
  };

  useEffect(() => {
    let interval;
    if (isPlaying) {
      interval = setInterval(() => {
        setProgress(p => (p >= 100 ? 100 : p + 0.25));
      }, 100);
    }
    return () => clearInterval(interval);
  }, [isPlaying]);

  if (!isOpen) return null;

  return (
    <AnimatePresence>
      <motion.div 
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        exit={{ opacity: 0 }}
        className="fixed inset-0 z-[100] flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm"
      >
        <motion.div 
          initial={{ y: 20, scale: 0.95, opacity: 0 }}
          animate={{ y: 0, scale: 1, opacity: 1 }}
          exit={{ y: 20, scale: 0.95, opacity: 0 }}
          className="bg-white/80 backdrop-blur-2xl border border-white/60 rounded-[2rem] w-full max-w-sm overflow-hidden shadow-2xl relative"
        >
          {/* Wave Background */}
          <div className="absolute inset-0 z-0 opacity-70 pointer-events-none" style={{ backgroundImage: `url('${import.meta.env.BASE_URL}bg_waves.png')`, backgroundSize: 'cover', backgroundPosition: 'center' }}></div>
          {/* Header */}
          <div className="p-5 border-b border-white/40 flex justify-between items-center bg-white/40 backdrop-blur-sm relative z-10">
            <h3 className="text-xs font-bold text-slate-700 tracking-widest uppercase">당목담글 특별판 오디오북</h3>
            <button onClick={onClose} className="text-slate-500 hover:text-orange-500 p-1 font-bold transition">
              ✕
            </button>
          </div>

          {/* Record Player UI */}
          <div className="p-8 pb-10 flex flex-col items-center justify-center relative">
            <div className="absolute inset-0 opacity-10" style={{ backgroundImage: 'radial-gradient(circle at 2px 2px, black 1px, transparent 0)', backgroundSize: '24px 24px' }}></div>
            
            <div className="relative w-48 h-48 mb-8 z-10">
              {/* Outer Glow */}
              <div 
                className={`absolute inset-0 rounded-full transition-all duration-1000 ${isPlaying ? 'opacity-30 scale-110' : 'opacity-0 scale-100'}`}
                style={{ backgroundColor: rawAccent, filter: 'blur(20px)' }}
              />
              {/* Light Vinyl / CD Element */}
              <motion.div 
                animate={{ rotate: isPlaying ? 360 : 0 }}
                transition={{ duration: 4, repeat: Infinity, ease: "linear" }}
                className="absolute inset-0 rounded-full bg-slate-50 border-[4px] border-white shadow-xl flex items-center justify-center overflow-hidden"
              >
                {/* Grooves */}
                <div className="absolute inset-3 rounded-full border border-slate-200/80" />
                <div className="absolute inset-7 rounded-full border border-slate-100/80" />
                <div className="absolute inset-11 rounded-full border border-slate-200/80" />
                <div className="absolute inset-14 rounded-full border border-slate-100/80" />
                {/* Center Label (Logo) */}
                <div className="w-[5.5rem] h-[5.5rem] rounded-full flex items-center justify-center shadow-inner relative z-20 overflow-hidden bg-white p-0.5 border border-slate-200">
                  <img src={`${import.meta.env.BASE_URL}logo_circle.png`} alt="당목담글 로고" className="w-full h-full object-cover rounded-full" />
                </div>
              </motion.div>
            </div>

            <h2 className="serif text-2xl text-blue-950 font-extrabold mb-2 text-center relative z-10">{theme?.name || '광화문'}의 목소리 수필</h2>
            <p className="text-xs text-slate-500 mb-8 text-center italic relative z-10">받는 이: {email}</p>

            {/* Progress Bar */}
            <div className="w-full h-1.5 bg-slate-100 rounded-full mb-8 overflow-hidden relative z-10 shadow-inner">
              <div 
                className="absolute top-0 left-0 h-full transition-all duration-200" 
                style={{ width: `${progress}%`, backgroundColor: rawAccent }}
              />
            </div>

            {/* Controls */}
            <button 
              onClick={togglePlay}
              className="w-16 h-16 rounded-full flex items-center justify-center transition-all hover:scale-105 shadow-lg relative z-10 text-white"
              style={{ backgroundColor: rawAccent }}
            >
              {isPlaying ? (
                <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 24 24"><path d="M6 19h4V5H6v14zm8-14v14h4V5h-4z"/></svg>
              ) : (
                <svg className="w-6 h-6 ml-1" fill="currentColor" viewBox="0 0 24 24"><path d="M8 5v14l11-7z"/></svg>
              )}
            </button>
            <p className="mt-4 text-[10px] font-bold text-slate-400 relative z-10">
                {isPlaying ? '재생 중입니다...' : '버튼을 눌러 재생하세요'}
            </p>
          </div>
        </motion.div>
      </motion.div>
    </AnimatePresence>
  );
}

export default AudiobookPlayerModal;
