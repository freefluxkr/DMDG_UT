import React, { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import Chart from 'chart.js/auto';

const gates = [
  {
    id: 'gwanghwa',
    title: '광화문 (정궁)',
    desc: '따뜻한 봄날, 단종과 정조 등 조선 왕실 정사',
    tag: '@dmdg-free',
    tagClass: 'text-orange-600 bg-orange-100',
    titleClass: 'text-blue-950',
    bgImage: 'gwanghwa_spring.png',
    doorClass: 'palace-wood door-gwanghwa border-orange-500/30',
    knobBg: 'from-orange-100 to-white',
    knobBorder: 'border-orange-200',
    knobDot: 'bg-orange-500',
    btnColor: 'bg-orange-500 hover:bg-orange-600 text-white shadow-[0_10px_20px_rgba(234,88,12,0.3)]'
  },
  {
    id: 'deoksu',
    title: '덕수궁 (근대의 아픔)',
    desc: '간도와 관동 학살 등 아픈 역사의 현장',
    tag: '@koreans-culture',
    tagClass: 'text-teal-600 bg-teal-50',
    titleClass: 'text-blue-950',
    bgImage: 'deoksu_autumn.png',
    doorClass: 'palace-wood door-deoksu border-teal-500/30',
    knobBg: 'from-teal-100 to-white',
    knobBorder: 'border-teal-200',
    knobDot: 'bg-teal-500',
    btnColor: 'bg-teal-600 hover:bg-teal-700 text-white shadow-[0_10px_20px_rgba(13,148,136,0.3)]'
  },
  {
    id: 'changgyeong',
    title: '창경궁 (비극의 전각)',
    desc: '하얀 눈, 사도세자 등 전각의 슬픈 비사',
    tag: '@dmdg-sad',
    tagClass: 'text-blue-700 bg-blue-100',
    titleClass: 'text-blue-950',
    bgImage: 'changgyeong_winter.png',
    doorClass: 'palace-wood door-changgyeong border-blue-500/30',
    knobBg: 'from-blue-100 to-white',
    knobBorder: 'border-blue-200',
    knobDot: 'bg-blue-600',
    btnColor: 'bg-blue-800 hover:bg-blue-900 text-white shadow-[0_10px_20px_rgba(30,58,138,0.3)]'
  }
];

function Lobby() {
  const [currentIndex, setCurrentIndex] = useState(0);
  const [opening, setOpening] = useState(false);
  const navigate = useNavigate();

  const handleOpen = (id) => {
    setOpening(true);
    setTimeout(() => {
      navigate(`/chamber/${id}`);
    }, 2000);
  };

  const nextGate = () => !opening && setCurrentIndex((prev) => (prev + 1) % gates.length);
  const prevGate = () => !opening && setCurrentIndex((prev) => (prev - 1 + gates.length) % gates.length);

  const currentGate = gates[currentIndex];
  const chartRef = useRef(null);
  const chartInstance = useRef(null);

  useEffect(() => {
    if (chartRef.current) {
      if (chartInstance.current) {
        chartInstance.current.destroy();
      }
      const ctx = chartRef.current.getContext('2d');
      const chartColors = [
        'rgba(234, 88, 12,', // orange
        'rgba(13, 148, 136,', // teal
        'rgba(30, 58, 138,' // blue
      ][currentIndex];
      
      chartInstance.current = new Chart(ctx, {
        type: 'radar',
        data: {
          labels: ['엄숙함', '정통성', '서사성', '기록성', '기부 활성도'],
          datasets: [{
            data: [95, 85, 70, 80, 90],
            backgroundColor: `${chartColors} 0.2)`,
            borderColor: `${chartColors} 0.8)`,
            borderWidth: 2,
            pointBackgroundColor: `${chartColors} 1)`,
            pointBorderColor: '#fff',
            pointRadius: 4,
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            r: {
              angleLines: { color: 'rgba(0, 0, 0, 0.1)' },
              grid: { color: 'rgba(0, 0, 0, 0.1)' },
              pointLabels: { color: 'rgba(30, 41, 59, 0.7)', font: { size: 10, family: "'Noto Sans KR', sans-serif" } },
              ticks: { display: false }
            }
          },
          plugins: { legend: { display: false } }
        }
      });
    }
    return () => {
      if (chartInstance.current) chartInstance.current.destroy();
    };
  }, [currentIndex]);

  return (
    <div className="w-full h-[100dvh] relative overflow-hidden flex items-center justify-center bg-transparent">
      
      {/* Top Navigation */}
      <nav className="fixed top-0 left-0 w-full z-50 p-6 flex justify-between items-center bg-gradient-to-b from-white/90 to-transparent">
        <div className="serif text-2xl font-bold tracking-wider text-blue-950 drop-shadow-sm">The Gates</div>
        <div className="flex items-center space-x-4">
          <div className="hidden sm:flex space-x-6 text-xs font-bold tracking-widest uppercase text-slate-500">
            {gates.map((g, idx) => (
              <button 
                key={g.id} 
                onClick={() => setCurrentIndex(idx)}
                className={`hover:text-orange-500 transition ${currentIndex === idx ? 'text-orange-600' : ''}`}
              >
                {g.id}
              </button>
            ))}
          </div>
          <button 
            onClick={() => alert('설정 기능은 다음 업데이트에 제공됩니다.')}
            className="flex items-center space-x-1 sm:space-x-2 bg-white/20 hover:bg-white/30 px-3 sm:px-4 py-1.5 sm:py-2 rounded-full backdrop-blur-md transition text-xs sm:text-sm font-bold text-white shadow-lg border border-white/30"
          >
            <span>⚙️</span> <span className="hidden md:inline">설정</span>
          </button>
        </div>
      </nav>

      {/* Navigation Helpers */}
      <div className="fixed inset-y-0 left-4 z-40 flex items-center pointer-events-none">
        <button onClick={prevGate} className="pointer-events-auto p-4 rounded-full bg-white/80 backdrop-blur shadow-lg text-blue-900 hover:text-orange-500 transition border border-slate-200 z-50">
          <b className="text-xl">←</b>
        </button>
      </div>
      <div className="fixed inset-y-0 right-4 z-40 flex items-center pointer-events-none">
        <button onClick={nextGate} className="pointer-events-auto p-4 rounded-full bg-white/80 backdrop-blur shadow-lg text-blue-900 hover:text-orange-500 transition border border-slate-200 z-50">
          <b className="text-xl">→</b>
        </button>
      </div>

      {/* Carousel Container */}
      <div className="relative w-full h-full flex items-center justify-center gate-slider">
        <AnimatePresence mode="wait">
          <motion.div
            key={currentIndex}
            initial={{ opacity: 0, x: 100 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: -100 }}
            transition={{ duration: 0.8, ease: [0.16, 1, 0.3, 1] }}
            className={`gate-frame relative w-full max-w-lg aspect-[4/5] flex items-center justify-center ${opening ? 'gate-open' : ''}`}
          >
            <div className="absolute inset-0 flex overflow-hidden rounded-2xl shadow-[0_20px_50px_rgba(0,0,0,0.3)] bg-[#090d16]" style={{ perspective: 1200 }}>
              
              {/* Background Image (Portal) */}
              <div className={`absolute inset-0 portal-bg transition-transform duration-[2s] ease-out ${opening ? 'scale-110 opacity-100' : 'scale-100 opacity-60'}`}>
                <div 
                  className="w-full h-full bg-cover bg-center"
                  style={{ backgroundImage: `url(${import.meta.env.BASE_URL}${currentGate.bgImage})` }}
                />
              </div>

              {/* Left Door */}
              <div className={`door door-left absolute left-0 top-0 w-1/2 h-full ${currentGate.doorClass} border-r shadow-2xl origin-left flex items-center justify-end pr-4 z-10`}>
                <div className="stud-grid">
                  {[...Array(15)].map((_, i) => <div key={i} className="stud"></div>)}
                </div>
                <div className={`w-12 h-12 rounded-full border-2 ${currentGate.knobBorder} bg-radial ${currentGate.knobBg} flex items-center justify-center shadow-lg relative z-20`}>
                  <div className={`w-4 h-4 rounded-full ${currentGate.knobDot} shadow-inner flex items-center justify-center`}>
                    <div className="w-8 h-8 rounded-full border border-yellow-500/20 absolute -right-2 top-4"></div>
                  </div>
                </div>
              </div>

              {/* Right Door */}
              <div className={`door door-right absolute right-0 top-0 w-1/2 h-full ${currentGate.doorClass} border-l shadow-2xl origin-right flex items-center justify-start pl-4 z-10`}>
                <div className="stud-grid">
                  {[...Array(15)].map((_, i) => <div key={i} className="stud"></div>)}
                </div>
                <div className={`w-12 h-12 rounded-full border-2 ${currentGate.knobBorder} bg-radial ${currentGate.knobBg} flex items-center justify-center shadow-lg relative z-20`}>
                  <div className={`w-4 h-4 rounded-full ${currentGate.knobDot} shadow-inner flex items-center justify-center`}>
                    <div className="w-8 h-8 rounded-full border border-yellow-500/20 absolute -left-2 top-4"></div>
                  </div>
                </div>
              </div>
            </div>
            
            {/* UI Layer */}
            <div className="ui-layer relative z-20 w-full p-8 text-center transition-all duration-700">
              <div className="glass-card p-6 rounded-3xl mt-12 mx-auto shadow-xl inline-block max-w-[90%]">
                <span className={`${currentGate.tagClass} text-xs tracking-[0.3em] font-extrabold px-3 py-1 rounded-full`}>{currentGate.tag}</span>
                <h2 className={`serif text-3xl sm:text-4xl mt-5 mb-2 font-bold ${currentGate.titleClass}`}>{currentGate.title}</h2>
                <p className="text-slate-600 font-medium text-sm mb-6">{currentGate.desc}</p>
                
                <div className="relative w-full max-w-[450px] mx-auto h-[180px] sm:h-[260px] mb-6">
                  <canvas ref={chartRef}></canvas>
                </div>

                <button 
                  onClick={() => handleOpen(currentGate.id)}
                  className={`px-10 py-3.5 rounded-full text-sm font-bold tracking-widest uppercase transition-all ${currentGate.btnColor}`}
                >
                  문의 안쪽으로 입장하기
                </button>
              </div>
            </div>
          </motion.div>
        </AnimatePresence>
      </div>

      {/* Bottom Status Bar */}
      <footer className="fixed bottom-0 left-0 w-full p-6 flex justify-between items-end z-40 pointer-events-none">
        <div className="pointer-events-auto glass-card px-4 py-2 rounded-full">
          <div className="flex items-center space-x-2">
            <span className="w-2 h-2 rounded-full bg-teal-500 animate-pulse"></span>
            <span className="text-[10px] font-bold text-slate-700 tracking-widest uppercase">{currentGate.title.split(' ')[0]} 게이트 동기화 완료</span>
          </div>
        </div>
      </footer>

    </div>
  );
}

export default Lobby;
