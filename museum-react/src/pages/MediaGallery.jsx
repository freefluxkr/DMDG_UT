import React, { useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { youtubeData } from '../data/youtubeData';

function MediaGallery() {
  const { palaceId } = useParams();
  const navigate = useNavigate();
  const [activeTab, setActiveTab] = useState('long'); // 'long', 'shorts'
  
  // Default to gwanghwa if not found
  const palaceData = youtubeData[palaceId] || youtubeData['gwanghwa'];

  const themeMap = {
    gwanghwa: { bgImage: "/gwanghwa_spring.png" },
    deoksu: { bgImage: "/deoksu_autumn.png" },
    changgyeong: { bgImage: "/changgyeong_winter.png" }
  };
  const currentTheme = themeMap[palaceId] || themeMap['gwanghwa'];

  // Sorting shorts by viewCount descending
  const sortedShorts = [...palaceData.shorts].sort((a, b) => b.viewCount - a.viewCount);

  const getRankingBadge = (index) => {
    if (index === 0) return '🥇';
    if (index === 1) return '🥈';
    if (index === 2) return '🥉';
    return null;
  };

  const formatViewCount = (count) => {
    return count > 10000 ? (count / 10000).toFixed(1) + '만' : count.toLocaleString();
  };

  return (
    <motion.div 
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -20 }}
      transition={{ duration: 0.8 }}
      className="w-full min-h-screen text-white overflow-y-auto custom-scroll relative"
    >
      {/* Background Image with Dark Blue Logo Color Overlay */}
      <div 
        className="fixed inset-0 z-0 bg-cover bg-center"
        style={{ backgroundImage: `url(${currentTheme.bgImage})` }}
      >
        <div className="absolute inset-0 bg-[#0B1221]/85 backdrop-blur-sm"></div>
      </div>

      <div className="relative z-10 w-full max-w-7xl mx-auto p-4 sm:p-8">
        {/* Topbar */}
        <div className="flex justify-between items-center pb-6 border-b border-white/10 mb-8 mt-4">
          <div>
            <span className="text-xs uppercase tracking-widest font-bold text-amber-500">
              Media Archive
            </span>
            <h1 className="serif text-3xl sm:text-4xl mt-2 text-white flex items-center gap-3">
              {palaceData.title} <span className="text-lg text-white/80 font-sans tracking-wide">| {palaceData.subtitle}</span>
            </h1>
          </div>
          <button 
            onClick={() => navigate(`/chamber/${palaceId}`)} 
            className="px-6 py-2.5 bg-white/20 hover:bg-white/30 rounded-full text-xs text-white tracking-wider transition font-bold shadow-md border border-white/30"
          >
            ← 전시관으로 돌아가기
          </button>
        </div>

        {/* Tabs */}
        <div className="flex space-x-2 bg-black/40 p-1.5 rounded-xl border border-white/5 mb-8 max-w-sm mx-auto">
          <button 
            onClick={() => setActiveTab('long')}
            className={`flex-1 py-2.5 rounded-lg text-xs font-bold transition ${activeTab === 'long' ? 'bg-amber-500/20 text-amber-300 shadow-md' : 'text-slate-400 hover:text-slate-200'}`}
          >
            📺 역사 다큐멘터리
          </button>
          <button 
            onClick={() => setActiveTab('shorts')}
            className={`flex-1 py-2.5 rounded-lg text-xs font-bold transition ${activeTab === 'shorts' ? 'bg-red-500/20 text-red-300 shadow-md' : 'text-slate-400 hover:text-slate-200'}`}
          >
            📱 인기 역사 쇼츠
          </button>
        </div>

        {/* Section 1: Long-form Videos (16:9) */}
        {activeTab === 'long' && (
          <section className="mb-16 animate-fade-in">
            <h2 className="serif text-xl sm:text-2xl mb-6 text-slate-200 border-l-4 border-amber-500 pl-4">
              역사 다큐멘터리 (상설 전시관)
            </h2>
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
              {palaceData.longForms.map((video) => (
                <div 
                  key={video.id} 
                  onClick={() => window.open(`https://www.youtube.com/watch?v=${video.videoId}`, '_blank')}
                  className="group relative rounded-2xl overflow-hidden cursor-pointer shadow-lg transform transition-all duration-300 hover:-translate-y-2 hover:shadow-2xl border border-white/10 bg-black/60 aspect-video flex flex-col"
                >
                  <div className="relative flex-1 overflow-hidden">
                    <img 
                      src={video.thumbnail} 
                      alt={video.title} 
                      className="w-full h-full object-cover opacity-80 group-hover:opacity-100 transition-all duration-500 group-hover:scale-105"
                    />
                    <div className="absolute inset-0 bg-gradient-to-t from-black/90 via-black/20 to-transparent pointer-events-none"></div>
                    <div className="absolute inset-0 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity duration-300">
                      <div className="w-12 h-12 rounded-full bg-red-600/90 flex items-center justify-center text-white shadow-[0_0_20px_rgba(220,38,38,0.6)] pl-1">
                        ▶
                      </div>
                    </div>
                  </div>
                  <div className="absolute bottom-0 left-0 w-full p-4 pointer-events-none">
                    <p className="text-sm font-bold text-white mb-1.5 line-clamp-2 leading-tight drop-shadow-md">{video.title}</p>
                    <p className="text-[10px] text-slate-300 flex items-center drop-shadow-md">
                      <span className="text-amber-400 mr-1">👁</span> {formatViewCount(video.viewCount)}회 시청
                    </p>
                  </div>
                </div>
              ))}
            </div>
          </section>
        )}

        {/* Section 2: Shorts (9:16) */}
        {activeTab === 'shorts' && (
          <section className="mb-16 animate-fade-in">
            <h2 className="serif text-xl sm:text-2xl mb-6 text-slate-200 border-l-4 border-red-500 pl-4">
              인기 역사 쇼츠 (기획 전시관)
            </h2>
            
            <div className="flex flex-wrap gap-6 justify-center sm:justify-start pb-8 pt-4">
              {sortedShorts.map((short, index) => {
                const badge = getRankingBadge(index);
                return (
                  <div 
                    key={short.id} 
                    onClick={() => window.open(`https://www.youtube.com/shorts/${short.videoId}`, '_blank')}
                    className="flex-shrink-0 w-[45%] sm:w-56 group relative rounded-2xl overflow-hidden cursor-pointer shadow-lg transform transition-all duration-300 hover:-translate-y-3 hover:shadow-[0_20px_40px_-15px_rgba(220,38,38,0.3)] border border-white/10 bg-black/60"
                  >
                    <div className="aspect-[9/16] relative overflow-hidden flex items-center justify-center">
                      {/* CSS Scale(1.35) applied here to crop letterbox */}
                      <img 
                        src={short.thumbnail} 
                        alt={short.title} 
                        className="w-full h-full object-cover scale-[1.35] opacity-70 group-hover:opacity-100 transition-all duration-500 group-hover:scale-[1.45]"
                      />
                      
                      {/* Ranking Badge Overlay */}
                      {badge && (
                        <div className="absolute top-0 left-0 z-20 pt-3 pl-3 pointer-events-none">
                          <div className="w-10 h-10 rounded-full glass-card border border-white/30 flex items-center justify-center shadow-[0_0_15px_rgba(255,255,255,0.2)] backdrop-blur-md text-xl bg-black/40">
                            {badge}
                          </div>
                        </div>
                      )}

                      <div className="absolute inset-0 bg-gradient-to-t from-black/95 via-black/40 to-transparent pointer-events-none z-10"></div>
                      
                      <div className="absolute inset-0 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity duration-300 z-20">
                        <div className="w-10 h-10 rounded-full bg-red-600/90 flex items-center justify-center text-white shadow-[0_0_20px_rgba(220,38,38,0.6)] pl-1">
                          ▶
                        </div>
                      </div>
                      
                      <div className="absolute top-3 right-3 px-2 py-1 bg-black/60 backdrop-blur-md rounded text-[9px] text-white flex items-center border border-white/10 z-20 pointer-events-none">
                        <span className="text-red-500 mr-1 font-bold">▶</span> Shorts
                      </div>
                    </div>
                    
                    <div className="absolute bottom-0 left-0 w-full p-4 pointer-events-none z-20">
                      <p className="text-xs font-bold text-white mb-2 line-clamp-2 leading-relaxed drop-shadow-md">{short.title}</p>
                      <p className="text-[10px] text-slate-300 flex items-center drop-shadow-md">
                        <span className="text-amber-400 mr-1">👁</span> {formatViewCount(short.viewCount)}회 시청
                      </p>
                    </div>
                  </div>
                );
              })}
            </div>
          </section>
        )}
      </div>
    </motion.div>
  );
}

export default MediaGallery;
