import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';

function ScentCertificateModal({ isOpen, onClose, theme }) {
  const [isPlaying, setIsPlaying] = React.useState(false);
  const palaceName = theme?.name || '광화문';
  const rawAccent = theme?.accentHex || '#ea580c';
  
  // Create TTS
  const playTTS = (text) => {
    if (!window.speechSynthesis) return;
    if (isPlaying) {
      window.speechSynthesis.cancel();
      setIsPlaying(false);
      return;
    }
    setIsPlaying(true);
    
    window.speechSynthesis.cancel();
    setTimeout(() => {
      const utterance = new SpeechSynthesisUtterance(text);
      utterance.lang = 'ko-KR';
      utterance.onend = () => setIsPlaying(false);
      utterance.onerror = () => setIsPlaying(false);
      window.speechSynthesis.speak(utterance);
    }, 50);
  };

  const certText = "이름 모를 무고한 이들의 한을 기리는 낭독... 귀하의 목소리가 잊힌 이들의 마음을 따뜻하게 위로합니다.";

  return (
    <AnimatePresence>
      {isOpen && (
        <div className="fixed inset-0 z-[110] flex items-center justify-center p-4">
          <motion.div 
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={onClose}
            className="absolute inset-0 bg-black/60 backdrop-blur-sm"
          />
          <motion.div 
            initial={{ opacity: 0, scale: 0.95, y: 20 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.95, y: 20 }}
            className="relative w-full max-w-md bg-white/85 backdrop-blur-2xl border border-white/60 rounded-[2rem] shadow-2xl overflow-hidden"
          >
            {/* Wave Background */}
            <div className="absolute inset-0 z-0 opacity-60 pointer-events-none" style={{ backgroundImage: `url('${import.meta.env.BASE_URL}bg_waves.png')`, backgroundSize: 'cover', backgroundPosition: 'center' }}></div>
            {/* Top decorative wave */}
            <div className="w-full h-32 relative flex items-center justify-center overflow-hidden">
                <div className="absolute inset-0 opacity-10" style={{ backgroundImage: 'radial-gradient(circle at 2px 2px, black 1px, transparent 0)', backgroundSize: '24px 24px' }}></div>
                <div className="absolute bottom-0 w-[150%] h-24 bg-white/30 backdrop-blur-sm rounded-t-[50%] translate-y-12 shadow-sm"></div>
                
                {/* Wax seal (Logo) */}
                <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-16 h-16 rounded-full border border-dashed border-slate-300 flex items-center justify-center shadow-md bg-white p-0.5 z-10 overflow-hidden">
                    <img src={`${import.meta.env.BASE_URL}logo_circle.png`} alt="당목담글 로고" className="w-full h-full object-cover rounded-full" />
                </div>
            </div>

            <div className="px-8 pb-10 pt-4 text-center relative z-10">
              <span className="text-[10px] uppercase tracking-[0.3em] font-bold mb-3 block" style={{ color: rawAccent }}>
                Voice Scent Certificate
              </span>
              <h2 className="serif text-3xl font-extrabold text-slate-800 mb-8">당신의 조향 증명서</h2>
              
              <div className="w-12 h-1 bg-slate-200 mx-auto mb-6 rounded-full"></div>
              
              <p className="text-lg text-slate-700 serif mb-2 font-bold">{palaceName} 전시관</p>
              <p className="text-xs tracking-widest font-bold mb-6 uppercase" style={{ color: rawAccent }}>
                목소리 색채: 분석 완료
              </p>
              
              <div className="serif text-sm text-slate-600 font-medium leading-loose bg-slate-50 p-6 rounded-2xl border border-slate-100 mb-8 shadow-inner italic">
                  "{certText}"
              </div>
              
              <p className="text-[10px] text-slate-400 mb-8 font-medium leading-relaxed px-2">
                  * 생성된 엽서 및 낭독 기록은 귀하의 브라우저 로컬 환경에만 보관됩니다.
              </p>
              
              <div className="flex flex-col space-y-3">
                  <button 
                    onClick={() => playTTS(certText)} 
                    className="w-full py-4 bg-slate-50 hover:bg-slate-100 border border-slate-200 text-slate-700 text-sm rounded-xl transition flex items-center justify-center space-x-2 font-bold shadow-sm"
                  >
                      <span>{isPlaying ? '🔊 증서 낭독 중...' : '🔊 증서 목소리로 듣기'}</span>
                  </button>
                  <button 
                    onClick={onClose} 
                    className="w-full py-4 text-white text-sm rounded-xl transition font-bold shadow-md"
                    style={{ backgroundColor: rawAccent }}
                  >
                      마음속에 간직하기
                  </button>
              </div>
            </div>
          </motion.div>
        </div>
      )}
    </AnimatePresence>
  );
}

export default ScentCertificateModal;
