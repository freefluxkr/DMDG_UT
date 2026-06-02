import React, { useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';

function Chamber() {
  const { palaceId } = useParams();
  const navigate = useNavigate();

  const [activeMode, setActiveMode] = useState('docent'); // 'docent' or 'mirror'
  const [activeTab, setActiveTab] = useState('reading'); // 'reading', 'letter', 'lantern'

  const themeMap = {
    gwanghwa: { 
      name: "광화문 (정궁)", season: "봄", spirit: "단종", 
      bgImage: "/gwanghwa_spring.png",
      accent: "text-amber-400"
    },
    deoksu: { 
      name: "덕수궁 (근대의 아픔)", season: "가을", spirit: "고종 황제", 
      bgImage: "/deoksu_autumn.png",
      accent: "text-red-400"
    },
    changgyeong: { 
      name: "창경궁 (비극의 전각)", season: "겨울", spirit: "사도세자", 
      bgImage: "/changgyeong_winter.png",
      accent: "text-indigo-400"
    }
  };

  const currentTheme = themeMap[palaceId] || themeMap['gwanghwa'];

  return (
    <motion.div 
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      transition={{ duration: 1.5 }}
      className="w-full min-h-screen relative overflow-y-auto"
    >
      {/* Background Image */}
      <div 
        className="fixed inset-0 z-0 bg-cover bg-center"
        style={{ backgroundImage: `url(${currentTheme.bgImage})` }}
      >
        {/* Dark overlay for readability */}
        <div className="absolute inset-0 bg-black/60 backdrop-blur-sm"></div>
      </div>

      <div className="relative z-10 w-full max-w-7xl mx-auto p-4 sm:p-8 flex flex-col min-h-screen">
        {/* Topbar */}
        <div className="flex justify-between items-center pb-6 border-b border-white/10 mt-4">
          <div>
            <span className={`text-xs uppercase tracking-widest font-bold ${currentTheme.accent}`}>
              {currentTheme.name} 전시관
            </span>
            <h1 className="serif text-2xl sm:text-3xl mt-1 text-slate-100 flex items-center gap-3">
              {activeMode === 'docent' ? '도슨트 제이의 기록' : `영령의 거울 : ${currentTheme.spirit}`}
            </h1>
          </div>
          <button 
            onClick={() => navigate('/')} 
            className="px-6 py-2.5 glass-card hover:bg-white/10 rounded-full text-xs text-slate-300 tracking-wider transition font-bold"
          >
            ← 대문으로 돌아가기
          </button>
        </div>

        {/* Immersive Split Screen (Grid) */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mt-8 flex-1">
          
          {/* Left Column: Rituals */}
          <div className="flex flex-col space-y-6">
            <div className="flex space-x-1 bg-black/40 p-1 rounded-xl border border-white/5">
              <button 
                onClick={() => setActiveTab('reading')}
                className={`flex-1 py-2 rounded-lg text-xs font-medium transition ${activeTab === 'reading' ? 'bg-white/20 text-white' : 'text-slate-400 hover:text-slate-200'}`}
              >
                📖 목소리 낭독 의례
              </button>
              <button 
                onClick={() => setActiveTab('letter')}
                className={`flex-1 py-2 rounded-lg text-xs font-medium transition ${activeTab === 'letter' ? 'bg-white/20 text-white' : 'text-slate-400 hover:text-slate-200'}`}
              >
                ✉️ 시공의 우체통
              </button>
            </div>

            <div className="glass-card p-6 rounded-2xl flex-1 flex flex-col justify-between min-h-[400px]">
              {activeTab === 'reading' && (
                <div className="flex flex-col h-full animate-fade-in">
                  <div className="flex justify-between items-center mb-4">
                    <h3 className="serif text-lg text-slate-200">오늘의 마중물</h3>
                    <button className="px-3 py-1.5 bg-white/10 hover:bg-white/20 text-white border border-white/30 rounded-full text-[11px] transition">
                      🔊 낭독 듣기
                    </button>
                  </div>
                  <div className="serif text-base sm:text-lg text-slate-300 leading-loose tracking-wide flex-1 overflow-y-auto italic pr-2">
                    "비는 대지를 적시고, 내 목소리는 누군가의 마음에 가닿아 따뜻한 위로가 됩니다. {currentTheme.name}의 깊은 전각에서 과거의 숨결을 목소리로 되살립니다."
                  </div>
                  <div className="mt-6 pt-6 border-t border-white/10 flex justify-between items-center">
                    <div>
                      <h4 className="text-xs text-slate-300 font-medium">목소리 기부하기</h4>
                      <p className="text-[10px] text-slate-500 mt-1">마이크 대기 중</p>
                    </div>
                    <button className="w-12 h-12 rounded-full bg-red-500/20 hover:bg-red-500/40 border border-red-500/50 flex items-center justify-center text-lg transition shadow-[0_0_15px_rgba(239,68,68,0.3)]">
                      🎙️
                    </button>
                  </div>
                </div>
              )}

              {activeTab === 'letter' && (
                <div className="flex flex-col h-full animate-fade-in">
                  <h3 className="serif text-lg text-slate-200 mb-2">시공의 우체통</h3>
                  <p className="text-xs text-slate-400 leading-relaxed mb-4">
                    {currentTheme.spirit}에게 따뜻한 위로의 편지를 남겨 보세요. Gemini가 역사적 사실을 바탕으로 화답 편지를 적어내려 갑니다.
                  </p>
                  <textarea 
                    rows="5" 
                    placeholder="마음을 담아 편지를 작성해주세요..." 
                    className="w-full p-4 bg-black/40 border border-white/10 rounded-2xl text-xs text-white focus:outline-none focus:border-white/40 resize-none mb-4"
                  />
                  <button className="w-full py-3 bg-white/10 hover:bg-white/20 border border-white/20 rounded-2xl text-xs text-white transition font-bold mt-auto">
                    ✉️ 시공간 너머로 편지 보내기
                  </button>
                </div>
              )}
            </div>
          </div>

          {/* Right Column: AI Chat */}
          <div className="flex flex-col space-y-6">
            <div className="glass-card p-6 rounded-2xl flex-1 flex flex-col justify-between min-h-[500px]">
              <div>
                <div className="flex space-x-1 bg-black/40 p-1 rounded-xl border border-white/5 mb-4">
                  <button 
                    onClick={() => setActiveMode('docent')}
                    className={`flex-1 py-1.5 rounded-lg text-[10px] font-bold transition ${activeMode === 'docent' ? 'bg-amber-500/20 text-amber-300' : 'text-slate-400 hover:text-slate-200'}`}
                  >
                    🧑‍🏫 도슨트 제이와 대화
                  </button>
                  <button 
                    onClick={() => setActiveMode('mirror')}
                    className={`flex-1 py-1.5 rounded-lg text-[10px] font-bold transition ${activeMode === 'mirror' ? 'bg-purple-500/20 text-purple-300' : 'text-slate-400 hover:text-slate-200'}`}
                  >
                    🔮 영령({currentTheme.spirit})의 거울
                  </button>
                </div>
                
                <div className="h-[320px] overflow-y-auto pr-2 space-y-4">
                  {/* Chat Bubbles Placeholder */}
                  <div className="flex space-x-2">
                    <div className="w-8 h-8 rounded-full bg-slate-800 flex items-center justify-center text-xs font-bold shrink-0">
                      {activeMode === 'docent' ? 'J' : '영'}
                    </div>
                    <div className="bg-white/10 p-3.5 rounded-2xl rounded-tl-none max-w-[85%] text-slate-200 text-xs serif leading-relaxed">
                      {activeMode === 'docent' 
                        ? `어서 오세요. 저는 도슨트 제이입니다. ${currentTheme.name}의 역사에 대해 무엇이든 물어보세요.` 
                        : `내 이름은 ${currentTheme.spirit}. 차가운 역사의 뒤안길에서 그대를 기다리고 있었소...`}
                    </div>
                  </div>
                </div>
              </div>
              
              <div className="mt-4 pt-4 border-t border-white/10 flex space-x-2">
                <input 
                  type="text" 
                  placeholder={activeMode === 'docent' ? "제이에게 질문하기..." : "영령에게 말 걸기..."} 
                  className="flex-1 px-4 py-3 bg-black/40 border border-white/10 rounded-2xl text-xs text-white focus:outline-none focus:border-white/30"
                />
                <button className="px-5 py-3 bg-white/10 hover:bg-white/20 border border-white/20 rounded-2xl text-xs text-white font-bold transition">
                  전송
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </motion.div>
  );
}

export default Chamber;
