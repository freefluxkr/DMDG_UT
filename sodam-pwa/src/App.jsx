import { useState, useRef, useEffect } from 'react';
import { Mic, ChevronLeft, ChevronRight, Check, RotateCcw, X } from 'lucide-react';
import { db } from './firebase';
import { collection, addDoc, getDocs, query, orderBy, serverTimestamp } from 'firebase/firestore';
import logoImage from './logo.png';
import bgImage from './bg-history.png'; // 캠페인에 맞게 배경 이미지를 쉽게 변경할 수 있습니다.

const sentences = [
  "가장 깊은 밤의 어둠 속에서도 빛을 잃지 않았던 당신을 기억합니다.\n우리의 목소리가 닿아 그날의 아픔이 조금이나마 따뜻해지기를 바랍니다.",
  "단순히 잊지 않는 것을 넘어, 우리는 함께 기억할 것입니다.\n당신이 지키려 했던 조선의 마지막 밤을, 이제는 우리가 목소리로 지켜내겠습니다.",
  "서로 다른 언어와 다른 얼굴을 하고 있지만, 슬픔을 공감하는 마음은 하나입니다.\n1895년 가을의 아픔을 넘어, 우리의 목소리가 작은 위로가 되기를 소망합니다."
];
const CURRENT_CAMPAIGN = "명성황후"; // 향후 다른 컨텐츠가 추가될 경우 이 값만 변경하면 DB가 완벽히 분리됩니다.

function App() {
  const [currentIdx, setCurrentIdx] = useState(0);
  const [isRecording, setIsRecording] = useState(false);
  const [isDone, setIsDone] = useState(false);
  
  const [audioUrl, setAudioUrl] = useState(null);
  const mediaRecorderRef = useRef(null);
  const audioChunksRef = useRef([]);

  const [showNicknameModal, setShowNicknameModal] = useState(false);
  const [showFameModal, setShowFameModal] = useState(false);
  const [nickname, setNickname] = useState('');
  const [participants, setParticipants] = useState([]);
  const [playingAudioId, setPlayingAudioId] = useState(null); // 현재 재생 중인 오디오 ID
  const audioObjRef = useRef(null); // 오디오 재생 객체 참조
  
  const [listenedIds, setListenedIds] = useState(new Set()); // 다시 들은 오디오 ID 추적

  useEffect(() => {
    const fetchParticipants = async () => {
      try {
        // 컬렉션 경로를 campaigns/명성황후/participants 로 세분화하여 독립적인 DB 구성
        const q = query(collection(db, "campaigns", CURRENT_CAMPAIGN, "participants"), orderBy("createdAt", "desc"));
        const querySnapshot = await getDocs(q);
        const data = [];
        querySnapshot.forEach((doc) => {
          // 절대 위치 대신 회전각과 약간의 상하 들쭉날쭉 마진만 줌 (겹침 방지)
          const randomRot = Math.floor(Math.random() * 30) - 15; // -15도 ~ +15도
          const randomMarginTop = Math.floor(Math.random() * 20) - 10;
          data.push({ ...doc.data(), id: doc.id, randRot: randomRot, randMarginTop: randomMarginTop });
        });
        setParticipants(data);
      } catch (error) {
        console.error("Error fetching participants:", error);
      }
    };
    fetchParticipants();
  }, []);

  const handlePrev = () => {
    setCurrentIdx((prev) => (prev > 0 ? prev - 1 : sentences.length - 1));
    resetRecording();
  };
  
  const handleNext = () => {
    setCurrentIdx((prev) => (prev < sentences.length - 1 ? prev + 1 : 0));
    resetRecording();
  };

  const resetRecording = () => {
    setIsRecording(false);
    setIsDone(false);
    setAudioUrl(null);
    audioChunksRef.current = [];
    if (mediaRecorderRef.current && mediaRecorderRef.current.state !== 'inactive') {
      mediaRecorderRef.current.stop();
    }
  };

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const mediaRecorder = new MediaRecorder(stream);
      mediaRecorderRef.current = mediaRecorder;
      audioChunksRef.current = [];

      mediaRecorder.ondataavailable = (e) => {
        if (e.data.size > 0) {
          audioChunksRef.current.push(e.data);
        }
      };

      mediaRecorder.onstop = () => {
        const audioBlob = new Blob(audioChunksRef.current, { type: 'audio/webm' });
        const url = URL.createObjectURL(audioBlob);
        setAudioUrl(url);
      };

      mediaRecorder.start();
      setIsRecording(true);
    } catch (err) {
      console.error("마이크 접근 오류:", err);
      alert("마이크 접근 권한을 허용해주세요!");
    }
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current && mediaRecorderRef.current.state !== 'inactive') {
      mediaRecorderRef.current.stop();
      mediaRecorderRef.current.stream.getTracks().forEach(track => track.stop());
    }
    setIsRecording(false);
    setIsDone(true);
  };

  const handleMicClick = () => {
    if (isDone) return;
    if (!isRecording) {
      startRecording();
    } else {
      stopRecording();
    }
  };

  const handleSaveClick = () => {
    setShowNicknameModal(true);
  };

  const handleSaveAndDownload = async () => {
    if (!nickname.trim()) return;

    try {
      let audioBase64 = null;

      const blobToBase64 = (blob) => {
        return new Promise((resolve, reject) => {
          const reader = new FileReader();
          reader.readAsDataURL(blob);
          reader.onloadend = () => resolve(reader.result);
          reader.onerror = reject;
        });
      };

      if (audioChunksRef.current.length > 0) {
        const audioBlob = new Blob(audioChunksRef.current, { type: 'audio/webm' });
        audioBase64 = await blobToBase64(audioBlob);
      }

      // 데이터 저장 시에도 동일하게 특정 캠페인 경로로 저장
      const docRef = await addDoc(collection(db, "campaigns", CURRENT_CAMPAIGN, "participants"), {
        nickname: nickname.trim(),
        sentenceIndex: currentIdx,
        audioBase64: audioBase64,
        createdAt: serverTimestamp()
      });
      
      const newPart = { 
        id: docRef.id, nickname: nickname.trim(), sentenceIndex: currentIdx, audioBase64: audioBase64,
        randRot: 0, randMarginTop: 0 // 새로 추가된 건 정가운데(맨 앞)에 바르게 배치
      };
      
      setParticipants([newPart, ...participants]);
      setShowNicknameModal(false);

      if (audioBase64) {
        const a = document.createElement('a');
        a.href = audioBase64;
        a.download = `sodam_voice_donation_${currentIdx + 1}.webm`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
      }
      
      setShowFameModal(true);
    } catch (error) {
      console.error("Error saving participant: ", error);
      alert("데이터 저장 중 오류가 발생했습니다.");
    }
  };

  const playParticipantAudio = (participant) => {
    if (!participant.audioBase64) return;
    
    // 다시 들은 ID 목록에 추가
    setListenedIds(prev => {
      const newSet = new Set(prev);
      newSet.add(participant.id);
      return newSet;
    });
    
    if (audioObjRef.current) {
      audioObjRef.current.pause();
      if (playingAudioId === participant.id) {
        setPlayingAudioId(null);
        audioObjRef.current = null;
        return;
      }
    }

    const audio = new Audio(participant.audioBase64);
    audioObjRef.current = audio;
    setPlayingAudioId(participant.id);
    
    audio.play();
    audio.onended = () => {
      setPlayingAudioId(null);
      audioObjRef.current = null;
    };
  };

  return (
    <div className="app-container">
      <div className="app-content-wrapper">
        <header className="header white-header">
          <img src={logoImage} alt="StoryBridge" className="new-logo" />
          <div className="header-text-content">
            <span className="header-slogan">'사람과 마음을 연결하는 세상에서 가장 따뜻한 이어읽기 플랫폼'</span>
            <div className="header-title-row">
              <h1>당목담글</h1>
              <p>당신의 목소리로 다음 글을 읽어주세요</p>
            </div>
          </div>
        </header>

        <main className="carousel-container">
          <div 
            className="carousel-slides"
            style={{ transform: `translateX(-${currentIdx * 100}%)` }}
          >
            {sentences.map((text, idx) => (
              <div key={idx} className={`slide ${idx === currentIdx ? 'active' : ''}`}>
                <div className="card">
                  <p>{text}</p>
                </div>
              </div>
            ))}
          </div>
          
          <div className="controls">
            <button className="control-btn" onClick={handlePrev} disabled={isRecording}>
              <ChevronLeft size={24} />
            </button>
            
            <div className="dots">
              {sentences.map((_, idx) => (
                <span 
                  key={idx} 
                  className={`dot ${idx === currentIdx ? 'active' : ''}`}
                />
              ))}
            </div>
            
            <button className="control-btn" onClick={handleNext} disabled={isRecording}>
              <ChevronRight size={24} />
            </button>
          </div>
        </main>

        <section className="recorder-section">
          {!isDone ? (
            <>
              <button 
                className={`mic-btn ${isRecording ? 'recording' : ''}`}
                onClick={handleMicClick}
              >
                <Mic size={32} />
              </button>
              <div className="status-text">
                {isRecording ? "녹음 중입니다... (다시 눌러 완료)" : "버튼을 눌러 낭독을 시작하세요"}
              </div>
            </>
          ) : (
            <div className="playback-container" style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '15px' }}>
              <span className="success-message">
                <Check size={18} style={{ display: 'inline', verticalAlign: 'text-bottom', marginRight: '5px' }} />
                녹음 완료! 들어보시겠어요?
              </span>
              {audioUrl && (
                <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '10px' }}>
                  <audio controls src={audioUrl} style={{ height: '40px', borderRadius: '20px' }} />
                  <button 
                    onClick={handleSaveClick}
                    style={{ background: 'var(--muted-teal)', color: 'var(--cream-main)', padding: '8px 16px', borderRadius: '12px', textDecoration: 'none', fontWeight: 'bold', fontSize: '0.9rem', border: '2px solid var(--dark-brown)', cursor: 'pointer', boxShadow: '3px 3px 0px var(--dark-brown)', transition: 'all 0.2s ease' }}
                  >
                    ⬇️ 기부하고 저장하기
                  </button>
                </div>
              )}
              <button 
                onClick={resetRecording}
                style={{ background: 'var(--soft-pink)', border: '2px solid var(--dark-brown)', color: 'var(--dark-brown)', padding: '8px 16px', borderRadius: '12px', cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '8px', fontWeight: 'bold', boxShadow: '3px 3px 0px var(--dark-brown)', transition: 'all 0.2s ease' }}
              >
                <RotateCcw size={16} /> 다시 녹음하기
              </button>
            </div>
          )}
        </section>

        {/* Floating Action Button for Hall of Fame */}
        <button className="fab-button" onClick={() => setShowFameModal(true)}>
          🏆 <span className="fab-text">명단 보기</span>
        </button>
      </div>

      {/* Nickname Input Modal */}
      {showNicknameModal && (
        <div className="modal-overlay">
          <div className="modal">
            <h3>목소리 기부 💌</h3>
            <p>참여자 명단에 등록할<br/>기부자님의 닉네임을 적어주세요.</p>
            <input 
              type="text" 
              value={nickname}
              onChange={(e) => setNickname(e.target.value)}
              placeholder="예: 대한독립만세"
              maxLength={10}
              className="modal-input"
            />
            <div className="modal-buttons">
              <button onClick={() => setShowNicknameModal(false)} className="btn-cancel">취소</button>
              <button onClick={handleSaveAndDownload} className="btn-confirm">기부하기</button>
            </div>
          </div>
        </div>
      )}

      {/* Hall of Fame Modal (Pin Board) */}
      {showFameModal && (
        <div 
          className="fame-modal-overlay"
          style={{
            backgroundImage: `linear-gradient(rgba(253, 245, 235, 0.85), rgba(253, 245, 235, 0.85)), url(${bgImage})`
          }}
        >
          <div className="fame-modal-header">
            <h2>명예의 전당 🏆</h2>
            <button className="close-btn" onClick={() => setShowFameModal(false)}>
              <X size={28} />
            </button>
          </div>
          <div className="clothesline-container">
            {participants.length === 0 ? (
              <div className="empty-polaroid">
                <p>첫 번째 기부자가<br/>되어주세요!</p>
              </div>
            ) : (
              participants.map((p, index) => {
                const isLatest = index === 0;
                const isListened = listenedIds.has(p.id);
                return (
                  <div 
                    key={index} 
                    className={`polaroid-wrapper ${isLatest ? 'latest' : ''}`}
                    style={{
                      transform: `translateY(${p.randMarginTop || 0}px)`,
                      zIndex: isLatest ? 100 : participants.length - index
                    }}
                  >
                    <div 
                      className="polaroid-pin-container"
                      style={{
                        transform: `rotate(${p.randRot || 0}deg)`
                      }}
                    >
                      <div className="pin"></div>
                      <div 
                        className={`polaroid ${p.audioBase64 ? 'clickable' : ''} ${playingAudioId === p.id ? 'playing' : ''} ${isListened ? 'listened' : ''}`}
                        onClick={() => playParticipantAudio(p)}
                      >
                        <div className="polaroid-photo">
                          <Mic size={24} className={`polaroid-icon ${playingAudioId === p.id ? 'pulse-icon' : ''}`} />
                          <span>{p.sentenceIndex + 1}번 낭독</span>
                        </div>
                        <div className="polaroid-caption">{p.nickname}</div>
                      </div>
                    </div>
                  </div>
                );
              })
            )}
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
