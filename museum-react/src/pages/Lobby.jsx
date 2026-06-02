import React, { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';

const gates = [
  {
    id: 'gwanghwa',
    title: '광화문 (정궁)',
    desc: '따뜻한 봄날, 단종과 정조 등 묵직한 조선 왕실 정사',
    tag: '@dmdg-free',
    tagColor: 'text-amber-500',
    doorLeftColor: 'from-slate-900 to-slate-800',
    doorRightColor: 'from-slate-900 to-slate-800',
    btnColor: 'bg-amber-500/10 hover:bg-amber-500/20 border-amber-500/30 text-amber-300',
    bgImage: '/gwanghwa_spring.png'
  },
  {
    id: 'deoksu',
    title: '덕수궁 (근대의 아픔)',
    desc: '하늘이 높은 가을, 간도와 관동 학살 등 아픈 역사',
    tag: '@anti-korea',
    tagColor: 'text-red-500',
    doorLeftColor: 'from-red-950/40 to-slate-900',
    doorRightColor: 'from-red-950/40 to-slate-900',
    btnColor: 'bg-red-500/10 hover:bg-red-500/20 border-red-500/30 text-red-300',
    bgImage: '/deoksu_autumn.png'
  },
  {
    id: 'changgyeong',
    title: '창경궁 (비극의 전각)',
    desc: '하얀 눈이 쌓이는 겨울, 사도세자 등 전각의 슬픈 비사',
    tag: '@dmdg-sad',
    tagColor: 'text-indigo-400',
    doorLeftColor: 'from-indigo-950/30 to-slate-900',
    doorRightColor: 'from-indigo-950/30 to-slate-900',
    btnColor: 'bg-indigo-500/10 hover:bg-indigo-500/20 border-indigo-500/30 text-indigo-300',
    bgImage: '/changgyeong_winter.png',
    chartData: [85, 95, 75, 90, 80] // 예시 데이터
  }
];

import Chart from 'chart.js/auto';

function Lobby() {
  const [currentIndex, setCurrentIndex] = useState(0);
  const [opening, setOpening] = useState(false);
  const navigate = useNavigate();

  const handleOpen = (id) => {
    setOpening(true);
    setTimeout(() => {
      navigate(`/chamber/${id}`);
    }, 1200); // 2000ms -> 1200ms로 단축하여 빠른 전환
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
      chartInstance.current = new Chart(ctx, {
        type: 'radar',
        data: {
          labels: ['엄숙함', '정통성', '서사성', '기록성', '기부 활성도'],
          datasets: [{
            data: [95, 85, 70, 80, 90], // 현재 인덱스에 맞춰 데이터 변경 가능
            backgroundColor: 'rgba(212, 175, 55, 0.2)',
            borderColor: 'rgba(212, 175, 55, 0.8)',
            borderWidth: 2,
            pointBackgroundColor: 'rgba(212, 175, 55, 1)',
            pointBorderColor: '#fff',
            pointRadius: 4,
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            r: {
              angleLines: { color: 'rgba(255, 255, 255, 0.1)' },
              grid: { color: 'rgba(255, 255, 255, 0.1)' },
              pointLabels: { color: 'rgba(255, 255, 255, 0.6)', font: { size: 10, family: "'Noto Sans KR', sans-serif" } },
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
    <div className="w-full h-full relative overflow-hidden flex items-center justify-center">
      {/* Top Navigation */}
      <nav className="fixed top-0 left-0 w-full z-50 p-6 flex justify-between items-center bg-gradient-to-b from-black/80 to-transparent">
        <div className="serif text-xl font-bold tracking-wider text-slate-200">The Gates</div>
        <div className="flex items-center space-x-6 text-xs tracking-widest uppercase text-slate-400 hidden sm:flex">
          {gates.map((g, idx) => (
            <button 
              key={g.id} 
              onClick={() => setCurrentIndex(idx)}
              className={`hover:text-amber-500 transition ${currentIndex === idx ? 'text-amber-400' : ''}`}
            >
              {g.id}
            </button>
          ))}
        </div>
      </nav>

      {/* Navigation Arrows */}
      <div className="fixed inset-y-0 left-4 z-40 flex items-center pointer-events-none">
        <button onClick={prevGate} className="pointer-events-auto p-3 rounded-full glass-card hover:text-amber-400 transition z-50">
          ←
        </button>
      </div>
      <div className="fixed inset-y-0 right-4 z-40 flex items-center pointer-events-none">
        <button onClick={nextGate} className="pointer-events-auto p-3 rounded-full glass-card hover:text-amber-400 transition z-50">
          →
        </button>
      </div>

      {/* Carousel Container */}
      <div className="relative w-full h-full flex items-center justify-center perspective-[1200px]">
        <AnimatePresence mode="wait">
          <motion.div
            key={currentIndex}
            initial={{ opacity: 0, x: 100 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: -100 }}
            transition={{ duration: 0.8, ease: [0.16, 1, 0.3, 1] }}
            className="w-full max-w-lg aspect-[4/5] relative flex items-center justify-center gate-frame"
          >
            <div className="absolute inset-0 flex overflow-hidden rounded-2xl" style={{ perspective: 1200 }}>
              {/* Background Image (Portal) */}
              <div className={`absolute inset-0 transition-transform duration-[2s] ease-out ${opening ? 'scale-110 opacity-100' : 'scale-100 opacity-60'}`}>
                <div 
                  className="w-full h-full bg-cover bg-center"
                  style={{ backgroundImage: `url(${currentGate.bgImage})` }}
                />
              </div>

              {/* Left Door */}
              <motion.div 
                animate={{ rotateY: opening ? -110 : 0 }}
                transition={{ duration: 3.8, ease: [0.25, 1, 0.5, 1] }}
                className={`absolute left-0 top-0 w-1/2 h-full bg-gradient-to-br ${currentGate.doorLeftColor} border-r border-white/10 shadow-2xl origin-left flex items-center justify-end pr-4 z-10`}
              >
                <div className="w-10 h-10 rounded-full border-2 border-white/20 flex items-center justify-center shadow-inner">
                  <div className="w-3 h-3 rounded-full bg-amber-500/50"></div>
                </div>
              </motion.div>

              {/* Right Door */}
              <motion.div 
                animate={{ rotateY: opening ? 110 : 0 }}
                transition={{ duration: 3.8, ease: [0.25, 1, 0.5, 1] }}
                className={`absolute right-0 top-0 w-1/2 h-full bg-gradient-to-bl ${currentGate.doorRightColor} border-l border-white/10 shadow-2xl origin-right flex items-center justify-start pl-4 z-10`}
              >
                <div className="w-10 h-10 rounded-full border-2 border-white/20 flex items-center justify-center shadow-inner">
                  <div className="w-3 h-3 rounded-full bg-amber-500/50"></div>
                </div>
              </motion.div>
            </div>

            {/* UI Overlay */}
            <motion.div 
              animate={{ opacity: opening ? 0 : 1, scale: opening ? 0.95 : 1 }}
              transition={{ duration: 0.5 }}
              className="relative z-20 w-full p-8 text-center pointer-events-auto"
            >
              <span className={`text-xs tracking-[0.3em] font-bold ${currentGate.tagColor}`}>{currentGate.tag}</span>
              <h2 className="serif text-3xl sm:text-4xl mt-4 mb-2 text-white">{currentGate.title}</h2>
              <p className="text-slate-300 font-light text-sm mb-6 drop-shadow-md">{currentGate.desc}</p>
              
              <div className="relative w-full max-w-[280px] mx-auto h-[200px] mb-8">
                <canvas ref={chartRef}></canvas>
              </div>

              <button 
                onClick={() => handleOpen(currentGate.id)}
                className={`px-10 py-3 rounded-full border text-xs tracking-widest uppercase transition-all backdrop-blur-md shadow-lg ${currentGate.btnColor}`}
              >
                문의 안쪽으로 입장하기
              </button>
            </motion.div>

          </motion.div>
        </AnimatePresence>
      </div>

      {/* Bottom Status Bar */}
      <footer className="fixed bottom-0 left-0 w-full p-6 flex justify-between items-end z-40 pointer-events-none">
        <div className="pointer-events-auto">
          <p className="text-[10px] text-slate-500 uppercase tracking-widest mb-1">Current Portal Status</p>
          <div className="flex items-center space-x-2">
            <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
            <span className="text-xs font-light text-slate-300 tracking-tighter">{currentGate.title.split(' ')[0]} 게이트 동기화 완료</span>
          </div>
        </div>
        <div className="pointer-events-auto text-right hidden md:block">
          <p className="serif text-sm opacity-50 italic leading-relaxed">"역사는 문 뒤에 숨어 있지 않다, <br/>우리가 열기를 기다릴 뿐이다."</p>
        </div>
      </footer>

      {/* White Flash Transition Overlay */}
      <AnimatePresence>
        {opening && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 1.0, delay: 0.2 }}
            className="fixed inset-0 z-[100] bg-white pointer-events-none"
          />
        )}
      </AnimatePresence>
    </div>
  );
}

export default Lobby;
