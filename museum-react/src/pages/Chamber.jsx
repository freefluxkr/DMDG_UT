import React, { useState, useEffect, useRef } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import ScentCertificateModal from '../components/ScentCertificateModal';
import AudiobookPlayerModal from '../components/AudiobookPlayerModal';

const playTTS = (text, rate = 0.85, pitch = 0.9, onEndCallback = null) => {
  if (!window.speechSynthesis) return;
  
  window.speechSynthesis.cancel();
  
  // Use a slight delay to ensure cancel finishes
  setTimeout(() => {
    window.currentUtterance = new SpeechSynthesisUtterance(text);
    window.currentUtterance.lang = 'ko-KR';
    window.currentUtterance.rate = rate;
    window.currentUtterance.pitch = pitch;
    if (onEndCallback) {
      window.currentUtterance.onend = onEndCallback;
      window.currentUtterance.onerror = onEndCallback;
    }
    window.speechSynthesis.speak(window.currentUtterance);
  }, 100);
};

function Chamber() {
  const { palaceId } = useParams();
  const navigate = useNavigate();

  const themeMap = {
    gwanghwa: { 
      name: "광화문", subtitle: "정궁의 메아리", spirit: "단종", season: "따뜻한 봄",
      bgImage: "gwanghwa_spring.png",
      accent: "text-orange-600",
      accentHex: "#ea580c",
      accentRgb: "234, 88, 12",
      bgSoft: "bg-orange-50",
      borderSoft: "border-orange-200",
      bgActive: "bg-orange-100",
      tagCode: "@dmdg-free"
    },
    deoksu: { 
      name: "덕수궁", subtitle: "근대의 아픔", spirit: "고종 황제", season: "하늘이 높은 가을",
      bgImage: "deoksu_autumn.png",
      accent: "text-teal-600",
      accentHex: "#0d9488",
      accentRgb: "13, 148, 136",
      bgSoft: "bg-teal-50",
      borderSoft: "border-teal-200",
      bgActive: "bg-teal-100",
      tagCode: "@Anti-korea"
    },
    changgyeong: { 
      name: "창경궁", subtitle: "비극의 전각", spirit: "사도세자", season: "하얀 눈이 쌓이는 겨울",
      bgImage: "changgyeong_winter.png",
      accent: "text-blue-800",
      accentHex: "#1e40af",
      accentRgb: "30, 64, 175",
      bgSoft: "bg-blue-50",
      borderSoft: "border-blue-200",
      bgActive: "bg-blue-100",
      tagCode: "@dmdg-sad"
    }
  };

  const currentTheme = themeMap[palaceId] || themeMap['gwanghwa'];
  const primerText = `비는 대지를 적시고, 내 목소리는 누군가의 마음에 가닿아 따뜻한 위로가 됩니다. ${currentTheme.name}의 깊은 전각에서 과거의 슬픔을 달래는 나만의 향기를 엮어냅니다.`;

  const [activeMode, setActiveMode] = useState('docent'); // 'docent' or 'mirror'
  const handleTabSwitch = (mode) => {
    setActiveMode(mode);
    setChatHistory([]); // 채팅 기록 초기화
  };
  
  const [activeTab, setActiveTab] = useState('reading'); // 'reading', 'letter', 'lantern'
  const [showScentModal, setShowScentModal] = useState(false);
  
  // New States
  const [isRecording, setIsRecording] = useState(false);
  const [recordingProgress, setRecordingProgress] = useState(0);
  const [isRecordingComplete, setIsRecordingComplete] = useState(false);
  const [audioData, setAudioData] = useState(null);
  const mediaRecorderRef = useRef(null);
  const audioChunksRef = useRef([]);

  // 흔적 기록 시스템
  const [savedRecords, setSavedRecords] = useState([]);
  const addRecord = (type, title, detail, audio = null) => {
    setSavedRecords(prev => [...prev, { type, title, detail, audio, time: new Date().toISOString() }]);
  };
  const [chatMessage, setChatMessage] = useState("");
  const [chatHistory, setChatHistory] = useState([]);
  const [letterText, setLetterText] = useState("");
  const [isLetterSent, setIsLetterSent] = useState(false);
  const [letterReply, setLetterReply] = useState("");
  const [isSending, setIsSending] = useState(false);
  
  // Lantern Tab States
  const [lanternText, setLanternText] = useState("");
  const [sijoReply, setSijoReply] = useState("");
  const [isLanternSending, setIsLanternSending] = useState(false);
  const [lanterns, setLanterns] = useState([]);

  // Subscription States
  const [subscriptionEmail, setSubscriptionEmail] = useState("");
  const [isSubscribing, setIsSubscribing] = useState(false);
  const [subscriptionDone, setSubscriptionDone] = useState(false);
  
  // TTS Playing State
  const [ttsPlayingKey, setTtsPlayingKey] = useState(null);
  const [isFetchingText, setIsFetchingText] = useState(false);
  
  // Audiobook Player Mock States
  const [showAudiobookAlert, setShowAudiobookAlert] = useState(false);
  const [showAudiobookPlayer, setShowAudiobookPlayer] = useState(false);



  const handleSubscribe = async () => {
    if (!subscriptionEmail.trim() || !subscriptionEmail.includes("@")) {
      alert("올바른 이메일 주소를 입력해주세요.");
      return;
    }
    setIsSubscribing(true);
    try {
      if (window.db) {
        await window.db.collection("audiobook_subscriptions").add({
          email: subscriptionEmail.trim(),
          palace: currentTheme.name,
          subscribedAt: new Date().toISOString(),
          channelVerified: false
        });
      }
      
      const subs = JSON.parse(localStorage.getItem("dmdg_subscriptions") || "[]");
      subs.push({ email: subscriptionEmail.trim(), palace: currentTheme.name, date: new Date().toISOString() });
      localStorage.setItem("dmdg_subscriptions", JSON.stringify(subs));
      setSubscriptionDone(true);
      
    } catch (err) {
      console.error("Firebase save error:", err);
      const subs = JSON.parse(localStorage.getItem("dmdg_subscriptions") || "[]");
      subs.push({ email: subscriptionEmail.trim(), palace: currentTheme.name, date: new Date().toISOString() });
      localStorage.setItem("dmdg_subscriptions", JSON.stringify(subs));
      setSubscriptionDone(true);
    } finally {
      setIsSubscribing(false);
      setTimeout(() => {
        setShowAudiobookAlert(true);
      }, 3000);
    }
  };

  const handleLaunchLantern = () => {
    if (!lanternText.trim() || isLanternSending) return;
    setIsLanternSending(true);
    setSijoReply("");

    setTimeout(() => {
      setIsLanternSending(false);
      
      const newLantern = {
        id: Date.now(),
        left: Math.random() * 80 + 10,
        size: Math.random() * 0.5 + 0.8,
        duration: Math.random() * 5 + 8
      };
      setLanterns(prev => [...prev, newLantern]);
      
      setTimeout(() => {
        setLanterns(prev => prev.filter(l => l.id !== newLantern.id));
      }, newLantern.duration * 1000);

      const sijo = currentTheme.name === '광화문' 
        ? "해태상 굽어보는 광화문 밤 깊은데\n서러운 넋의 노래 등불로 타오르니\n두어라 저 밝은 빛에 한을 잊고 가소서"
        : `${currentTheme.name} 밤하늘에 별빛이 아스라한데\n그대의 맑은 마음 등불 되어 오르나니\n아마도 이 슬픈 역사 빛으로 남으리라`;
      setSijoReply(sijo);
      setLanternText("");
    }, 2000);
  };

  const handleMicClick = async () => {
    if (isRecordingComplete) return;
    
    if (isRecording) {
      // 녹음 중지
      if (mediaRecorderRef.current && mediaRecorderRef.current.state === 'recording') {
        mediaRecorderRef.current.stop();
      }
      setIsRecording(false);
      setIsRecordingComplete(true);
      setRecordingProgress(100);
      return;
    }
    
    // 실제 마이크 녹음 시작
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const mediaRecorder = new MediaRecorder(stream);
      mediaRecorderRef.current = mediaRecorder;
      audioChunksRef.current = [];
      
      mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) audioChunksRef.current.push(event.data);
      };
      
      mediaRecorder.onstop = () => {
        const audioBlob = new Blob(audioChunksRef.current, { type: 'audio/webm' });
        const reader = new FileReader();
        reader.onloadend = () => {
          const base64 = reader.result;
          setAudioData(base64);
          addRecord('voice', `${currentTheme.name} 목소리 발자취`, primerText, base64);
        };
        reader.readAsDataURL(audioBlob);
        stream.getTracks().forEach(track => track.stop());
      };
      
      mediaRecorder.start();
      setIsRecording(true);
      setRecordingProgress(0);
      
      const interval = setInterval(() => {
        setRecordingProgress(prev => {
          if (prev >= 99) {
            clearInterval(interval);
            if (mediaRecorderRef.current && mediaRecorderRef.current.state === 'recording') {
              mediaRecorderRef.current.stop();
            }
            setIsRecording(false);
            setIsRecordingComplete(true);
            return 100;
          }
          return prev + 6.6;
        });
      }, 1000);
    } catch (err) {
      console.error('마이크 접근 실패:', err);
      alert('마이크 접근이 거부되었습니다. 브라우저 설정에서 마이크를 허용해 주세요.');
    }
  };

  const handleSendLetter = () => {
    if (!letterText.trim() || isSending) return;
    setIsSending(true);
    setLetterReply("");
    
    setTimeout(() => {
      setIsSending(false);
      setIsLetterSent(true);
      const reply = currentTheme.name === '광화문' 
        ? "나는 일제 치하에서 경복궁의 정문인 이 광화문이 헐리고 총독부 건물이 들어서는 것을 눈물로 지켜보던 이름 없는 수문장이라오. 그대의 다정한 목소리가 시공간을 넘어 이곳의 차가운 돌바닥까지 닿으니, 나라를 잃고 문마저 빼앗겨 무너졌던 가슴에 비로소 따뜻한 봄볕이 드는구려. 언젠가 이 문이 다시 우뚝 서서 후손들의 웃음 소리를 지켜줄 것이라는 그대의 약속을 믿으며, 나는 이제야 맺힌 한을 풀고 평안히 눈을 감을 수 있겠소. 이름 모를 미래의 벗이여. 나의 슬픔을 기억하고 위로해 주어 참으로 고맙소."
        : `${currentTheme.spirit}의 영혼이 그대의 따뜻한 편지에 화답합니다.\n"시공간을 넘어 닿은 그대의 온기에 깊은 감사를 전하오. 잊혀지지 않음이 우리에겐 가장 큰 구원이오..."`;
      setLetterReply(reply);
      setLetterText("");
    }, 2000);
  };

  const handleChatSubmit = (e) => {
    e.preventDefault();
    if (!chatMessage.trim()) return;
    
    const userInput = chatMessage.trim();
    const newUserMsg = { sender: 'user', text: userInput };
    setChatHistory(prev => [...prev, newUserMsg]);
    setChatMessage("");

    setTimeout(() => {
      let aiReply = "";
      
      if (activeMode === 'docent') {
        if (userInput.includes("안녕")) aiReply = "안녕하세요! 저는 역사의 숨겨진 이야기를 들려드리는 당목담글 AI 도슨트입니다. 무엇이 궁금하신가요?";
        else if (userInput.includes("누구") || userInput.includes("이름")) aiReply = "저는 구글 역사 데이터베이스를 기반으로 학습된 당목담글 AI입니다. 이 궁궐의 비하인드 스토리를 알려드릴까요?";
        else if (userInput.includes("대화")) aiReply = "네, 저는 마스터의 질문에 대답할 수 있는 대화형 AI입니다! 어떤 역사적 사실을 깊이 파볼까요?";
        else {
          const defaults = [
            "당목담글 AI입니다. 해당 역사적 사실에 대해 더 깊이 있는 해설을 원하시나요?",
            "관련된 조선왕조실록 기록을 구글 데이터베이스에서 찾아볼까요?",
            "역사의 진실은 때론 우리가 아는 것과 다릅니다. 이 전각에 얽힌 다른 이야기를 들려드릴까요?"
          ];
          aiReply = defaults[Math.floor(Math.random() * defaults.length)];
        }
      } else {
        if (userInput.includes(currentTheme.spirit)) aiReply = `그대의 부름에 이 ${currentTheme.spirit}의 넋이 오랜 잠에서 깨어나는구려...`;
        else if (userInput.includes("안녕")) aiReply = "오랜 세월 기다려온 반가운 인사구려... 이곳까지 찾아와 주어 고맙소.";
        else if (userInput.includes("대화") || userInput.includes("진짜")) aiReply = "이것은 시공간을 초월한 마음의 교감이오. 그대의 진심이 내게 닿아 이렇게 답할 수 있다오.";
        else {
          const defaults = [
            "당신의 따뜻한 향기와 마음에 감사드립니다. 역사는 그렇게 기억될 것입니다.",
            "그대의 온기가 이 차가운 곳까지 닿았소... 잊지 않겠소.",
            "수백 년의 침묵을 깨고 그대와 마주하게 되어 기쁘오.",
            "그대가 전해준 위로 덕분에 비로소 맺힌 한이 조금 풀리는 듯하오."
          ];
          aiReply = defaults[Math.floor(Math.random() * defaults.length)];
        }
      }
      
      setChatHistory(prev => [...prev, { sender: 'ai', text: aiReply }]);
    }, 1000);
  };

  return (
    <motion.div 
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      transition={{ duration: 1.5 }}
      className="fixed inset-0 z-10 overflow-y-auto overflow-x-hidden custom-scroll bg-white/10"
    >

      <AnimatePresence>
        {showAudiobookAlert && (
          <motion.div 
            initial={{ y: -100, opacity: 0 }}
            animate={{ y: 20, opacity: 1 }}
            exit={{ y: -100, opacity: 0 }}
            className="fixed top-0 left-0 right-0 z-50 flex justify-center px-4"
          >
            <div 
              onClick={() => {
                setShowAudiobookAlert(false);
                setShowAudiobookPlayer(true);
              }}
              className="bg-white/95 backdrop-blur-md border border-orange-200 shadow-xl p-4 rounded-2xl flex items-center space-x-3 cursor-pointer hover:bg-slate-50 transition-all max-w-sm w-full"
            >
              <div className="text-3xl">💌</div>
              <div className="flex-1">
                <h4 className="text-xs font-bold text-orange-600 mb-1">[시공의 우체통]</h4>
                <p className="text-sm text-slate-800 font-bold">특별판 오디오북이 도착했습니다!</p>
                <p className="text-[10px] text-slate-500 mt-1 font-medium">탭하여 미리 듣기 ▶</p>
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      <AudiobookPlayerModal 
        isOpen={showAudiobookPlayer} 
        onClose={() => setShowAudiobookPlayer(false)} 
        theme={currentTheme}
        email={subscriptionEmail}
        records={savedRecords}
      />

      {/* Floating Lanterns Layer */}
      {lanterns.map(lantern => (
        <motion.div
          key={lantern.id}
          initial={{ y: '100vh', opacity: 0 }}
          animate={{ 
            y: '-20vh', 
            opacity: [0, 1, 1, 0],
            x: [0, Math.random() * 40 - 20, Math.random() * -40 + 20, 0] 
          }}
          transition={{ duration: lantern.duration, ease: 'easeOut' }}
          className="fixed z-10 pointer-events-none drop-shadow-[0_0_15px_rgba(245,158,11,0.8)]"
          style={{ left: `${lantern.left}%`, fontSize: `${lantern.size * 3}rem` }}
        >
          🏮
        </motion.div>
      ))}

      <div className="max-w-7xl mx-auto flex flex-col min-h-full relative z-10 p-4 sm:p-8">
        
        {/* Chamber Topbar */}
        <div className="flex justify-between items-center pb-6 border-b border-slate-200 mt-4">
          <div 
            onClick={() => navigate('/gallery/' + palaceId)} 
            className="cursor-pointer group"
          >
            <span className={`text-xs uppercase tracking-widest font-extrabold transition mb-1 block group-hover:brightness-110 text-amber-500`}>
              MEDIA ARCHIVE (영상실 입장)
            </span>
            <h1 className="serif text-3xl sm:text-4xl mt-1 font-bold text-white group-hover:text-slate-200 transition">
              {currentTheme.name} 전시관 <span className="text-white/60 font-medium text-lg sm:text-xl ml-2 tracking-normal">| {currentTheme.subtitle} ({currentTheme.tagCode})</span>
            </h1>
          </div>
          <button onClick={() => navigate('/')} className="px-6 py-2.5 bg-white border border-slate-300 hover:border-blue-900 rounded-full text-xs text-blue-950 tracking-wider transition font-bold shadow-sm">
            ← 대문으로 돌아가기
          </button>
        </div>

        {/* Slice Illustration Display */}
        <div className={`relative h-64 md:h-72 w-full overflow-hidden ${currentTheme.bgSoft}`}>
          {/* Decorative Background Pattern */}
          <div className="absolute inset-0 bg-cover bg-center mix-blend-multiply opacity-30" style={{ backgroundImage: `url(${import.meta.env.BASE_URL}${currentTheme.bgImage})` }}></div>
          <div className="absolute inset-0 opacity-10" style={{ backgroundImage: 'radial-gradient(circle at 2px 2px, black 1px, transparent 0)', backgroundSize: '24px 24px' }}></div>
          
          <div className="absolute inset-0 bg-gradient-to-t from-white via-white/50 to-transparent z-10" />
          <div className="absolute bottom-5 left-6 flex items-center space-x-2">
            <span className="text-[11px] uppercase font-bold tracking-widest px-3 py-1.5 rounded-full bg-white/90 text-slate-900 shadow-lg backdrop-blur">
              {currentTheme.season}
            </span>
          </div>
          <div className="absolute inset-0 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity">
             <div className="px-6 py-3 bg-white/20 backdrop-blur-md rounded-full text-white font-bold text-sm shadow-xl flex items-center gap-2 border border-white/30">
                <span className="text-xl">▶</span> {currentTheme.name} 유튜브 아카이브 입장
             </div>
          </div>
        </div>

        {/* Immersive Split Screen (Grid) */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mt-10 flex-1">
          
          {/* Left Column: Voice Donation & Time Mailbox & Lantern Ceremony */}
          <div className="flex flex-col space-y-6">
            
            {/* Mode Selector Tab */}
            <div className="flex space-x-2 bg-slate-100 p-1.5 rounded-2xl border border-slate-200 shadow-inner">
              <button onClick={() => setActiveTab('reading')} className={`flex-1 py-2.5 rounded-xl text-xs font-bold transition shadow-sm ${activeTab === 'reading' ? `bg-white ${currentTheme.accent} border border-slate-200` : 'text-slate-500 hover:text-blue-900'}`}>
                📖 목소리 발자취 남기기
              </button>
              <button onClick={() => setActiveTab('letter')} className={`flex-1 py-2.5 rounded-xl text-xs font-bold transition shadow-sm ${activeTab === 'letter' ? `bg-white ${currentTheme.accent} border border-slate-200` : 'text-slate-500 hover:text-blue-900'}`}>
                ✉️ 시공의 우체통
              </button>
              <button onClick={() => setActiveTab('lantern')} className={`flex-1 py-2.5 rounded-xl text-xs font-bold transition shadow-sm ${activeTab === 'lantern' ? `bg-white ${currentTheme.accent} border border-slate-200` : 'text-slate-500 hover:text-blue-900'}`}>
                🌌 등불 추모 의례
              </button>
            </div>

            {/* Ritual Tab 1: Reading Essay Block */}
            {activeTab === 'reading' && (
              <div className="glass-card-heavy p-8 rounded-3xl relative overflow-hidden flex-1 flex flex-col justify-between min-h-[400px] border border-white shadow-xl animate-fade-in">
                <div>
                  <div className="flex justify-between items-center mb-6">
                    <h3 className="serif text-xl font-bold text-blue-950">오늘의 마중물</h3>
                    <div className="flex items-center space-x-2">
                      <button 
                        onClick={() => {
                          if (ttsPlayingKey === 'reading') return;
                          setTtsPlayingKey('reading');
                          const text = `비는 대지를 적시고, 내 목소리는 누군가의 마음에 가닿아 따뜻한 위로가 됩니다. ${currentTheme.name}의 깊은 전각에서 과거의 슬픔을 달래는 나만의 향기를 엮어냅니다.`;
                          playTTS(text, 0.85, 0.9, () => setTtsPlayingKey(null));
                        }}
                        className={`px-4 py-2 ${currentTheme.bgSoft} hover:${currentTheme.bgActive} ${currentTheme.accent} border ${currentTheme.borderSoft} rounded-full text-[11px] transition flex items-center space-x-1 font-bold shadow-sm`}
                      >
                        <span>{ttsPlayingKey === 'reading' ? '🔊 낭독 중...' : '🔊 낭독 듣기'}</span>
                      </button>
                      <button 
                        onClick={() => {
                          setIsFetchingText(true);
                          setTimeout(() => setIsFetchingText(false), 2500);
                        }}
                        disabled={isFetchingText}
                        className={`px-4 py-2 bg-slate-800 hover:bg-slate-900 text-white border border-slate-700 rounded-full text-[11px] transition flex items-center space-x-1 font-bold shadow-sm disabled:opacity-50`}
                      >
                        <span>✨ 새 글 가져오기 (Gemini)</span>
                      </button>
                    </div>
                  </div>
                  
                  {/* Active Essay Reading Text Block */}
                  <div className="relative h-56">
                    <div className="serif text-lg sm:text-xl text-slate-700 leading-loose tracking-wide h-full overflow-y-auto custom-scroll pr-4 font-medium italic">
                      "비는 대지를 적시고, 내 목소리는 누군가의 마음에 가닿아 따뜻한 위로가 됩니다. {currentTheme.name}의 깊은 전각에서 과거의 슬픔을 달래는 나만의 향기를 엮어냅니다."
                    </div>
                    {isFetchingText && (
                      <div className="absolute inset-0 bg-white/90 backdrop-blur-sm flex flex-col items-center justify-center z-10 rounded-2xl">
                        <div className="w-10 h-10 border-4 border-teal-200 border-t-teal-600 rounded-full animate-spin"></div>
                        <p className="text-sm text-blue-950 mt-4 serif font-bold text-center px-4 leading-relaxed">수필을 지어내는 중...</p>
                      </div>
                    )}
                  </div>
                </div>

                {/* Simulated Recording and Evaluation Ritual */}
                <div className="mt-6 pt-6 border-t border-slate-200">
                  <div className="flex items-center justify-between">
                    <div>
                      <h4 className="text-sm text-blue-950 font-bold">목소리 발자취 남기기</h4>
                      <p className={`text-xs mt-1 font-medium ${isRecording ? 'text-red-500 animate-pulse' : 'text-slate-500'}`} style={isRecordingComplete && !isRecording ? { color: currentTheme.accentHex } : {}}>
                        {isRecording ? `녹음 중... ${recordingProgress.toFixed(0)}%` : isRecordingComplete ? "조향(녹음) 완료 ✨" : "대기 중"}
                      </p>
                    </div>
                    
                    <div className="flex items-center space-x-4">
                      <div className="relative w-14 h-14 flex items-center justify-center">
                        {isRecording && <div className={`absolute inset-0 rounded-full ${currentTheme.bgActive} record-pulse`}></div>}
                        <button 
                          onClick={handleMicClick} 
                          className={`relative z-10 w-12 h-12 rounded-full border-2 hover:scale-105 active:scale-95 shadow-lg flex items-center justify-center text-xl transition ${isRecording ? 'bg-red-50 border-red-500 text-red-500 shadow-[0_0_15px_rgba(239,68,68,0.3)]' : `bg-white hover:${currentTheme.bgSoft} border-slate-300 hover:${currentTheme.borderSoft}`}`}
                          style={isRecordingComplete && !isRecording ? { backgroundColor: currentTheme.accentHex, borderColor: currentTheme.accentHex, color: '#fff' } : {}}
                        >
                          🎙️
                        </button>
                      </div>
                      {isRecordingComplete && (
                        <button 
                          onClick={() => setShowScentModal(true)}
                          className="px-5 py-2.5 rounded-full border text-xs font-bold transition-all flex items-center animate-fade-in shadow-md bg-white hover:bg-slate-50"
                          style={{ borderColor: currentTheme.accentHex, color: currentTheme.accentHex }}
                        >
                          조향 완료 ✨
                        </button>
                      )}
                    </div>
                  </div>
                  {/* Waves Visualizer */}
                  <div className={`w-full h-6 mt-4 flex justify-start items-center space-x-1.5 transition-opacity ${isRecording ? 'opacity-100' : 'opacity-20'}`}>
                    <div className={`w-1.5 rounded-full ${isRecording ? 'h-3 animate-bounce' : 'h-2'}`} style={{backgroundColor: currentTheme.accentHex}}></div>
                    <div className={`w-1.5 rounded-full ${isRecording ? 'h-5 animate-bounce' : 'h-3'}`} style={{backgroundColor: currentTheme.accentHex, animationDelay: '0.1s'}}></div>
                    <div className={`w-1.5 rounded-full ${isRecording ? 'h-4 animate-bounce' : 'h-1.5'}`} style={{backgroundColor: currentTheme.accentHex, animationDelay: '0.2s'}}></div>
                    <div className={`w-1.5 rounded-full ${isRecording ? 'h-2 animate-bounce' : 'h-1'}`} style={{backgroundColor: currentTheme.accentHex, animationDelay: '0.3s'}}></div>
                  </div>
                </div>
              </div>
            )}

            {/* Ritual Tab 2: Time Mailbox Block */}
            {activeTab === 'letter' && (
              <div className="glass-card-heavy p-8 rounded-3xl relative overflow-hidden flex-1 flex flex-col justify-between min-h-[400px] border border-white shadow-xl animate-fade-in">
                <div className="flex-1 flex flex-col justify-between">
                  <div>
                    <h3 className="serif text-xl font-bold text-blue-950 mb-3">시공의 우체통</h3>
                    <p className="text-sm text-slate-600 leading-relaxed mb-5 font-medium">
                      {currentTheme.spirit}에게 따뜻한 위로의 편지를 남겨 보세요. <b>Gemini가 그들의 화답 편지</b>를 적어내려 갑니다.
                    </p>
                    
                    <textarea 
                      rows="4" 
                      value={letterText}
                      onChange={(e) => setLetterText(e.target.value)}
                      placeholder="예: 역사 속 아픔을 겪으신 영혼께 위로의 마음을 전합니다..." 
                      className={`w-full p-4 bg-white border-2 border-slate-200 rounded-2xl text-sm text-slate-800 focus:outline-none focus:${currentTheme.borderSoft} custom-scroll resize-none mb-4 shadow-inner`}
                    ></textarea>
                    
                    <button 
                      onClick={handleSendLetter}
                      disabled={isSending}
                      className="w-full py-3.5 bg-blue-900 hover:bg-blue-950 rounded-2xl text-sm text-white transition font-bold shadow-lg"
                    >
                      {isSending ? "✨ 시공간 너머로 편지 보내는 중... ✨" : "✉️ 시공간 너머로 편지 보내기"}
                    </button>
                  </div>

                  {/* Reply Area */}
                  {letterReply && (
                    <div className="mt-6 pt-6 border-t border-slate-200 animate-fade-in">
                      <div className="flex justify-between items-center mb-3">
                        <h4 className={`serif text-sm font-bold ${currentTheme.accent}`}>{currentTheme.spirit}에게서 온 답장</h4>
                        <button 
                          onClick={() => {
                            if (ttsPlayingKey === 'letter') return;
                            setTtsPlayingKey('letter');
                            playTTS(letterReply, 0.85, 0.8, () => setTtsPlayingKey(null));
                          }}
                          className={`px-3 py-1.5 ${currentTheme.bgSoft} hover:${currentTheme.bgActive} ${currentTheme.accent} border ${currentTheme.borderSoft} rounded-full text-[10px] transition flex items-center space-x-1 font-bold`}
                        >
                          <span>{ttsPlayingKey === 'letter' ? '🔊 낭독 중...' : '🔊 목소리로 듣기'}</span>
                        </button>
                      </div>
                      <div className="serif text-sm text-slate-700 leading-relaxed bg-slate-50 p-5 rounded-2xl border border-slate-200 max-h-32 overflow-y-auto custom-scroll font-medium">
                        {letterReply}
                      </div>
                    </div>
                  )}
                </div>
              </div>
            )}

            {/* Ritual Tab 3: Sky Lantern Memorial Block */}
            {activeTab === 'lantern' && (
              <div className="glass-card-heavy p-8 rounded-3xl relative overflow-hidden flex-1 flex flex-col justify-between min-h-[400px] border border-white shadow-xl animate-fade-in">
                <div className="flex-1 flex flex-col justify-between">
                  <div>
                    <h3 className="serif text-xl font-bold text-blue-950 mb-3">🌌 등불 추모 의례</h3>
                    <p className="text-sm text-slate-600 leading-relaxed mb-5 font-medium">
                      역사 속 영혼들에게 전하는 애틋한 바람을 한 구절 적어 보세요. <b>Gemini가 이를 정통 한국 시조(Sijo)</b>로 승화하여 등불과 함께 올립니다.
                    </p>
                    
                    <textarea 
                      rows="3" 
                      value={lanternText}
                      onChange={(e) => setLanternText(e.target.value)}
                      placeholder="예: 차가운 역사 속에서 눈감은 영혼께 따뜻한 바람이 불기를 소망합니다..." 
                      className={`w-full p-4 bg-white border-2 border-slate-200 rounded-2xl text-sm text-slate-800 focus:outline-none focus:border-teal-500 custom-scroll resize-none mb-4 shadow-inner`}
                    ></textarea>
                    
                    <button 
                      onClick={handleLaunchLantern}
                      disabled={isLanternSending}
                      className="w-full py-3.5 bg-teal-600 hover:bg-teal-700 rounded-2xl text-sm text-white transition font-bold shadow-lg"
                    >
                      {isLanternSending ? "🌌 염원의 등불을 올리는 중..." : "🌌 추모 등불 밝히기"}
                    </button>
                  </div>

                  {/* Generated Sijo Display Area */}
                  {sijoReply && (
                    <div className="mt-6 pt-6 border-t border-slate-200 animate-fade-in">
                      <div className="flex justify-between items-center mb-3">
                        <h4 className="serif text-sm font-bold text-teal-700">헌정 추모 시조</h4>
                        <button 
                          onClick={() => {
                            if (ttsPlayingKey === 'sijo') return;
                            setTtsPlayingKey('sijo');
                            playTTS(sijoReply, 0.8, 1.1, () => setTtsPlayingKey(null));
                          }}
                          className="px-3 py-1.5 bg-teal-50 hover:bg-teal-100 text-teal-700 border border-teal-200 rounded-full text-[10px] transition flex items-center space-x-1 font-bold"
                        >
                          <span>{ttsPlayingKey === 'sijo' ? '🔊 낭독 중...' : '🔊 시조 낭송 듣기'}</span>
                        </button>
                      </div>
                      <div className="serif text-base text-center text-blue-950 leading-loose bg-white p-6 rounded-3xl border border-slate-200 shadow-inner max-h-40 overflow-y-auto custom-scroll tracking-wide font-bold">
                        {sijoReply.split('\n').map((line, i) => <div key={i}>{line}</div>)}
                      </div>
                    </div>
                  )}
                </div>
              </div>
            )}
          </div>

          {/* Right Column: AI Chat */}
          <div className="flex flex-col space-y-6">
            <div className="glass-card-heavy p-8 rounded-3xl flex-1 flex flex-col justify-between min-h-[500px] border border-white shadow-xl">
              <div>
                {/* Toggle Mode */}
                <div className="flex space-x-2 bg-slate-100 p-1.5 rounded-2xl border border-slate-200 shadow-inner mb-6">
                  <button 
                    onClick={() => handleTabSwitch('docent')} 
                    className={`flex-1 py-2 rounded-xl text-[11px] font-bold transition shadow-sm ${activeMode === 'docent' ? 'bg-white text-teal-700 border border-slate-200' : 'text-slate-500 hover:text-teal-700'}`}
                  >
                    🧑‍🏫 당목담글 AI와 대화
                  </button>
                  <button 
                    onClick={() => handleTabSwitch('mirror')} 
                    className={`flex-1 py-2 rounded-xl text-[11px] font-bold transition shadow-sm ${activeMode === 'mirror' ? 'bg-white text-purple-700 border border-slate-200' : 'text-slate-500 hover:text-purple-700'}`}
                  >
                    🔮 역사 속 영령의 거울
                  </button>
                </div>

                <div className="flex items-center justify-between pb-5 border-b border-slate-200 mb-5">
                  <div className="flex items-center space-x-3">
                    <div className={`w-10 h-10 rounded-full ${activeMode === 'docent' ? 'bg-teal-500' : 'bg-purple-600'} flex items-center justify-center text-sm shadow-md font-bold text-white`}>
                      {activeMode === 'docent' ? '당' : '영'}
                    </div>
                    <div>
                      <h4 className="text-sm font-bold text-blue-950">
                        {activeMode === 'docent' ? "당목담글 AI" : `영령의 거울 (${currentTheme.spirit})`}
                      </h4>
                      <p className="text-[10px] text-slate-500 font-bold mt-0.5">
                        {activeMode === 'docent' ? "역사와 마음을 지키는 가이드" : "시간을 뛰어넘은 영혼의 화답"}
                      </p>
                    </div>
                  </div>
                </div>

                {/* Chat Scroll Area */}
                <div className="h-[300px] overflow-y-auto custom-scroll space-y-5 pr-4 text-sm">
                  <div className="flex space-x-3">
                    <div className={`w-8 h-8 rounded-full ${activeMode === 'docent' ? 'bg-teal-600' : 'bg-purple-600'} flex items-center justify-center text-[11px] shrink-0 font-bold text-white shadow-sm`}>
                      {activeMode === 'docent' ? '당' : '영'}
                    </div>
                    <div className="bg-slate-50 p-4 rounded-2xl rounded-tl-none border border-slate-200 max-w-[85%] text-slate-700 leading-relaxed text-sm serif font-medium shadow-sm">
                      {activeMode === 'docent' 
                        ? `어서 오세요. 저는 '당목담글'의 수필 편집자이자 역사적 진실을 전하는 동행자, 당목담글 AI입니다. ${currentTheme.name}에 대해 질문을 던져주시면 따뜻하게 답해 드릴게요.`
                        : `내 이름은 ${currentTheme.spirit}. 차가운 역사의 뒤안길에서 그대를 기다리고 있었소...`}
                    </div>
                  </div>
                  
                  {chatHistory.map((msg, i) => (
                    <div key={i} className={`flex ${msg.sender === 'user' ? 'justify-end' : 'justify-start'} space-x-3 animate-fade-in`}>
                      {msg.sender === 'ai' && (
                        <div className={`w-8 h-8 rounded-full ${activeMode === 'docent' ? 'bg-teal-600' : 'bg-purple-600'} flex items-center justify-center text-[11px] shrink-0 font-bold text-white shadow-sm`}>
                          {activeMode === 'docent' ? '당' : '영'}
                        </div>
                      )}
                      <div 
                        className={`p-4 rounded-2xl max-w-[85%] text-sm serif font-medium shadow-sm leading-relaxed ${msg.sender === 'user' ? 'bg-orange-500 text-white rounded-tr-none' : 'bg-slate-50 text-slate-700 border border-slate-200 rounded-tl-none'}`}
                        style={msg.sender === 'user' ? { backgroundColor: currentTheme.accentHex } : {}}
                      >
                        {msg.text}
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {/* Chat Input Block */}
              <div className="mt-5 pt-5 border-t border-slate-200">
                <form onSubmit={handleChatSubmit} className="flex space-x-2">
                  <input 
                    type="text" 
                    value={chatMessage}
                    onChange={(e) => setChatMessage(e.target.value)}
                    placeholder={activeMode === 'docent' ? "당목담글 AI에게 질문해 보세요..." : "영령에게 말 걸기..."} 
                    className={`flex-1 px-4 py-3.5 bg-white border-2 border-slate-200 rounded-2xl text-sm text-slate-800 focus:outline-none focus:${currentTheme.borderSoft} shadow-inner font-medium`}
                  />
                  <button type="submit" className={`px-6 py-3.5 ${activeMode === 'docent' ? 'bg-teal-600 hover:bg-teal-700' : 'bg-purple-600 hover:bg-purple-700'} rounded-2xl text-sm text-white transition font-bold shrink-0 shadow-md`}>
                    보내기
                  </button>
                </form>
              </div>
            </div>
          </div>
        </div>

        {/* Custom Email Subscription Banner */}
        <div id="audiobook-section" className="glass-card-heavy p-8 rounded-3xl mt-8 border-2 bg-gradient-to-tr from-orange-50 to-white shadow-xl" style={{ borderColor: `rgba(${currentTheme.accentRgb}, 0.2)` }}>
          <div className="flex flex-col md:flex-row justify-between items-center gap-6">
            <div className="text-center md:text-left">
              <h4 className={`serif text-xl font-bold mb-2 ${currentTheme.accent}`}>📬 나의 발자취를 한 편의 오디오북으로</h4>
              {subscriptionDone ? (
                <p className="text-sm text-slate-600 font-medium leading-relaxed max-w-xl">
                  ✨ 구독 신청이 완료되었습니다. 당신의 향기가 담긴 오디오북이 곧 도착합니다.
                </p>
              ) : (
                <p className="text-sm text-slate-600 font-medium leading-relaxed max-w-xl">
                  추후 채널 구독 시, 기기에 축적해둔 나만의 목소리 흔적 수필들을 <b>전용 헌정 오디오북(MP3)</b>으로 엮어 보내드립니다.
                </p>
              )}
            </div>
            {!subscriptionDone && (
              <div className="flex flex-col sm:flex-row space-y-2 sm:space-y-0 sm:space-x-2 w-full md:w-auto shrink-0">
                <input 
                  type="email" 
                  value={subscriptionEmail}
                  onChange={(e) => setSubscriptionEmail(e.target.value)}
                  placeholder="example@email.com" 
                  className={`px-4 py-3 bg-white border-2 ${currentTheme.borderSoft} rounded-2xl text-sm text-slate-800 focus:outline-none focus:border-orange-500 w-full sm:w-64 shadow-inner`}
                />
                <button 
                  onClick={handleSubscribe}
                  disabled={isSubscribing}
                  className="px-6 py-3 rounded-2xl text-white text-sm font-bold transition shrink-0 shadow-md"
                  style={{ backgroundColor: currentTheme.accentHex }}
                >
                  {isSubscribing ? "신청 중..." : "신청하기"}
                </button>
              </div>
            )}
          </div>
        </div>

        {/* Saved Records list */}
        <div className="glass-card-heavy p-8 rounded-3xl mt-8 border border-white shadow-xl mb-12">
          <h3 className="serif text-xl font-bold text-blue-950 mb-5">📜 내 기기에 저장된 나의 흔적들</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-5 max-h-60 overflow-y-auto custom-scroll pr-2">
            {savedRecords.length > 0 ? (
              savedRecords.map((rec, idx) => (
                <div key={idx} className="bg-slate-50/80 backdrop-blur-sm p-4 rounded-2xl border border-slate-200 shadow-sm flex flex-col justify-between">
                  <div>
                    <div className="flex items-center space-x-2 mb-2">
                      <span className="text-xs font-bold px-2 py-0.5 rounded-full bg-orange-100 text-orange-700">
                        {rec.type === 'voice' ? '🎙️ 목소리' : rec.type === 'scent' ? '🧪 조향' : '✉️ 편지'}
                      </span>
                      <span className="text-[10px] text-slate-400 font-medium">{new Date(rec.time).toLocaleTimeString()}</span>
                    </div>
                    <h4 className="text-sm font-bold text-slate-800 serif mb-1">{rec.title}</h4>
                    <p className="text-xs text-slate-600 line-clamp-2 leading-relaxed">{rec.detail}</p>
                  </div>
                  {rec.audio && (
                    <audio src={rec.audio} controls className="w-full mt-3 h-8 text-xs" />
                  )}
                </div>
              ))
            ) : (
              <p className="text-sm text-slate-500 font-medium italic">오늘 남겨주신 소중한 흔적(조향, 편지, 추모)들이 여기에 보관됩니다. 먼저 목소리 녹음 등을 진행해 주세요. ✨</p>
            )}
          </div>
        </div>

      </div>

      <ScentCertificateModal 
        isOpen={showScentModal} 
        onClose={() => setShowScentModal(false)} 
        theme={currentTheme}
      />
    </motion.div>
  );
}

export default Chamber;
