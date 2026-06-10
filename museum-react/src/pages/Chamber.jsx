import React, { useState, useEffect, useRef } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import ScentCertificateModal from '../components/ScentCertificateModal';
import AudiobookPlayerModal from '../components/AudiobookPlayerModal';
import { db } from '../firebase';
import { collection, addDoc, serverTimestamp } from 'firebase/firestore';

// Fallback Local Readings (API 실패 시에도 새글이 갱신되도록 3개 이상씩 다채롭게 구성)
const localReadingsPool = {
  "광화문": {
    "solemn": [
      "새벽안개 헤쳐 일어난 광화문의 기둥마다 따뜻한 봄날의 슬픈 햇살이 감돕니다. 기와의 선을 그리던 대목수의 숨결과 정조 대왕이 고뇌하던 정사의 밤이, 오늘 내 목소리를 타고 흘러 하나의 따뜻한 역사가 됩니다.",
      "굳건히 자리를 지켜온 돌벽 새로 백성들의 거친 숨소리가 서려 있습니다. 외침과 전란 속에서도 꺾이지 않았던 나라의 혼을 기리며, 오늘 묵직한 울림으로 그날의 정의로운 밤을 낭송합니다.",
      "풍파에 깎이고 무너져도 다시 우뚝 서는 문루 아래에서 옷깃을 여밉니다. 조국의 주권을 지키기 위해 스러져간 수많은 군사들의 넋을 달래며, 오늘 슬프고도 경건한 목소리로 추모의 마음을 바칩니다."
    ],
    "warm": [
      "봄날의 햇살처럼 온화한 온기가 광화문 너머 쓸쓸히 비어 있는 전각 뜰을 보듬어 안습니다. 오랫동안 묵혀왔던 역사의 시린 눈물을 거두어 가듯, 오늘 내 다정한 목소리가 작은 희망의 촛불로 타오릅니다.",
      "광장 가득 불어오는 봄바람 속에 이름 모를 영혼들의 다정한 미소가 머무는 듯합니다. 지쳐 쓰러진 백성들에게 따스한 위안을 보태며, 오늘 나의 목소리로 포근하고 편안한 봄의 노래를 전합니다.",
      "흙먼지 날리던 눈물의 터 위에 작은 들꽃 하나가 피어납니다. 슬픔을 견디고 희망을 꽃피워낸 모든 이들에게, 가슴 깊이 품어둔 따뜻한 온기와 사랑을 담아 이 글을 소리 내어 낭독합니다."
    ],
    "poetic": [
      "흐드러진 봄날의 벚꽃이 기와 끝에 내려앉는 밤, 바람이 이끄는 대로 내 목소리가 가만히 흘러갑니다. 가늘게 피어오르는 향 연기 너머 보이지 않는 영혼들에게 영원토록 시리지 않을 봄을 선물하렵니다.",
      "기와의 곡선을 스치는 푸른 밤바람이 과거의 시간을 실어 나릅니다. 달빛 조각 아래 아련히 춤추는 영혼들의 흔적을 품으며, 가녀린 목소리의 숨결로 허공 속에 고운 시를 수놓아 봅니다.",
      "서린 연기처럼 흩어지는 역사의 메아리 속에 가만히 귀를 기울입니다. 어스름한 새벽하늘로 날아오르는 하얀 새의 날갯짓처럼, 아스라한 내 낭독이 하늘 위에 별빛으로 반짝이기를 기도합니다."
    ]
  },
  "덕수궁": {
    "solemn": [
      "대한문 너머 가을 밤의 달빛은 유난히 푸르고 하늘은 높아 쓸쓸함이 깊어집니다. 간도의 들판에서 쓰러져 간 이름 모를 나의 벗들과 관동의 불길 속에서 침묵했던 영혼들의 흔적을 오늘 내 따뜻한 날숨으로 되살려냅니다.",
      "석조전 차가운 대리석 기둥 뒤로 잃어버린 나라를 그리워하던 황제의 메마른 눈물이 번집니다. 스러진 제국의 슬픈 황혼을 생각하며, 오늘 나의 경건하고 묵직한 호흡으로 잃어버린 혼을 부릅니다.",
      "붉게 타오르는 단풍잎이 지는 중명전 마당에서 굳게 다문 입술 사이로 슬픈 맹세를 읊조립니다. 을사늑약의 현장 속, 붓을 꺾어야 했던 서러운 혼령들에게 나의 단호한 울림을 헌정합니다."
    ],
    "warm": [
      "단풍잎이 흩날리는 정동 돌담길 너머 고요한 전각 뒤편에 작은 화로 하나를 놓습니다. 고난의 세월 속에 차디찬 겨울을 보내야 했던 백성들의 혼령들에게, 내 가슴속에서 빚어낸 따뜻한 한 구절로 온기를 나눕니다.",
      "덕수궁 돌담길의 울긋불긋한 단풍이 쓸쓸한 궁궐 뜰에 온기를 덮어줍니다. 외롭고 서글프게 역사의 길목을 지키던 영혼들에게, 다정하게 다가가 '이제 아프지 말라'는 다정한 인사를 건넵니다.",
      "근대의 소용돌이 속에서도 꿋꿋하게 견뎌낸 오랜 나무들의 그늘 아래서 쉼을 누립니다. 외로웠던 우리 선조들의 삶을 다스한 손길로 어루만지듯, 정성껏 빚어낸 위로의 말들을 공중에 띄워 올립니다."
    ],
    "poetic": [
      "마른 단풍잎이 돌바닥에 서걱이며 속삭이는 가을, 가슴 깊숙한 곳에서 우러나는 시를 읊조려 봅니다. 푸른 창공 멀리 흩어져 버린 대한제국의 마지막 눈물들이 내 목소리에 기대어 편안한 꿈속으로 떠나갑니다.",
      "노을빛이 전각의 창문 틈새로 붉게 스며드는 시간, 가을바람에 목소리를 띄워 보냅니다. 아스라이 흩어지는 빗방울처럼 쓸쓸한 영혼들의 뺨에 닿을 고운 시를 읊어 한 편의 서정시를 완성합니다.",
      "정관헌 지붕 아래 스쳐가는 은은한 바람결에 아련한 그리움을 얹어 봅니다. 수많은 별들이 지고 피는 가을 밤하늘 아래, 내 목소리가 그리운 이의 마음에 닿는 작은 별빛이 되었으면 좋겠습니다."
    ]
  },
  "창경궁": {
    "solemn": [
      "하얀 눈이 내리는 전각 문정전 뜰 앞에서 가녀린 대금 소리가 흐느끼듯 흩어집니다. 뒤주 속에 잠든 슬픈 세자의 넋을 기리며, 오랫동안 침묵 속에 가둬두었던 비사를 이제는 내 목소리의 울림으로 감싸 안으렵니다.",
      "차가운 눈발이 흩날리는 창경궁 명정전의 기와 위로 무거운 역사의 그림자가 드리웁니다. 권력의 비정함 속에 잊힌 슬픈 원혼들의 눈물을 잊지 않으며, 오늘 떨리는 마음으로 고요히 넋을 달래는 낭송을 시작합니다.",
      "명정문 뒤편에 부는 바람 속에는 억울하게 목숨을 잃은 여인들과 백성들의 통곡이 섞여 있는 듯합니다. 가슴이 저며오는 비극의 서막 속에서도 굴하지 않은 정의를 묵직하게 새겨 봅니다."
    ],
    "warm": [
      "문정전 처마 아래 포근하게 내려앉은 하얀 눈처럼, 나의 소리가 상처받은 외로운 마음에 가만히 내려앉습니다. 모진 세월의 가위눌림에서 비로소 안식할 수 있도록, 오직 그대의 영혼을 향한 따뜻한 안부를 띄워 보냅니다.",
      "하얗게 얼어붙은 연못 춘당지 언저리에 따스한 봄볕 같은 온기를 가만히 불어넣어 봅니다. 비극 속에 얼어붙었던 영혼들의 차가운 손을 맞잡아 주듯, 마음 깊은 곳에서 우러나온 포근한 위로를 속삭입니다.",
      "새하얀 겨울 눈밭 위에 작은 발자국을 남기며, 슬픔을 견딘 이들을 위한 위안을 적어 내려갑니다. 차디찬 세상을 지나온 모든 영혼들에게 이제는 포근한 햇살 가득한 안식이 깃들기를 진심으로 바랍니다.",
    ],
    "poetic": [
      "시린 달빛이 켜지는 고요한 겨울밤의 연못가, 얼어붙은 나뭇가지 끝에 목소리로 하얀 눈꽃송이를 피웁니다. 비극의 서막 끝에 마침내 마주하는 침묵의 순간, 아름답고 슬픈 향기를 남긴 채 별빛 속으로 날아오릅니다.",
      "겨울 처마 끝에 매달린 고드름 사이로 차가운 별빛이 쏟아져 내립니다. 허공에 흘러가는 가녀린 연기처럼 스러져간 아름답고 슬픈 기억들을 찾아, 조심스레 떨리는 목소리로 은빛 시를 써 봅니다.",
      "눈 내리는 밤의 고요함 속에 울려 펴지는 나지막한 고백을 들어 보소서. 시리도록 투명한 공기를 가르며 날아간 내 목소리가, 마침내 슬픈 넋들의 마음속에 const readingCache = {
  "광화문": { solemn: "", warm: "", poetic: "" },
  "덕수궁": { solemn: "", warm: "", poetic: "" },
  "창경궁": { solemn: "", warm: "", poetic: "" }
};�린 나이에 숙부 수양대군에게 왕위를 빼앗기고 원통하게 유배되어 죽음을 맞이한 단종(홍위)의 슬픈 영혼이 서려 있는 역사적 배경을 가집니다.";
    }
    if (normalized.includes("간도") || normalized.includes("참변") || normalized.includes("지진") || normalized.includes("학살") || normalized.includes("조선인")) {
      return "간도 참변과 관동 대지진 당시의 조선인 학살은 우리가 결코 잊어서는 안 될 비극입니다. 타향에서 억울하게 목숨을 잃고 영원히 고향으로 돌아오지 못한 영혼들을 위해, 우리는 편지와 목소리로 그들을 기억하고 위로하고 있습니다.";
    }
    // 기본 도슨트 폴백
    return `${themeName}의 역사와 얽힌 비극적인 이야기들은 우리 민족의 아픔을 고스란히 담고 있습니다. 혹시 ${themeName}에 얽힌 특정 사건이나 영령(${spiritName})의 삶에 대해 더 알고 싶으신 부분이 있으신가요?`;
  } else {
    // 영령의 거울 폴백
    if (themeName === "창경궁") {
      if (normalized.includes("왜") || normalized.includes("아버지") || normalized.includes("뒤주") || normalized.includes("영조")) {
        return "아바마마께서는 왜 나를 이 좁고 어두운 뒤주 속에 가두셨을까... 숨이 막히고 목이 말라오는 8일 동안 나는 오직 아바마마의 다정한 눈길을 원했소. 그대의 편지가 내 메마른 목청을 적셔 주는구려.";
      }
      return "나는 뒤주 속에서 차갑게 식어갔던 사도세자 이선이오. 나의 억울함과 슬픔을 알아채 준 그대의 마음씨에 고개 숙여 깊은 감사를 드리오. 혹시 나에게 해주고 싶은 위로가 더 남아 있소?";
    }
    if (themeName === "덕수궁") {
      if (normalized.includes("나라") || normalized.includes("일본") || normalized.includes("늑약") || normalized.includes("독살") || normalized.includes("헤이그")) {
        return "나라를 지키지 못하고 백성을 일제의 총칼 앞에 몰아넣은 못난 군주가 나요. 중명전의 어두운 밤, 을사늑약 서류에 찍히는 도장을 바라보며 피눈물을 흘렸소. 자주제국을 세우려던 나의 꿈은 꺾였지만 그대가 기억해 주니 고맙소.";
      }
      return "내 이름은 고종 이희라 하오. 대한제국의 황혼을 쓸쓸히 지키다 독살설 속에 눈을 감았지... 그대가 보내준 이 따뜻한 한마디가 차디찬 나의 넋을 녹이는도다. 그대의 세상은 부디 평화롭기를 바라오.";
    }
    // 광화문 (단종) 폴백
    if (normalized.includes("유배") || normalized.includes("삼촌") || normalized.includes("수양") || normalized.includes("영월")) {
      return "숙부(수양대군)의 서슬 퍼런 칼날 아래 영월 청령포로 유배되던 날, 강물도 슬피 울었소. 열여섯 꽃 같은 나이에 죽임을 당해 시신마저 강물에 던져졌으나, 그대의 다정한 마음이 나를 외롭지 않게 보듬어 주는구려.";
    }
    return "나는 조선의 비운의 어린 임금 단종이오. 어린 나이에 왕위에서 쫓겨나 영월의 외로운 골짜기에서 피눈물을 흘리며 잠들었소. 그대의 따뜻한 목소리가 내 서러운 넋을 위로해 주는구려. 참으로 고맙소.";
  }
};

const docentJaySystemPrompt = `
너는 한국 궁궐의 가슴 아픈 비극과 역사적 사실을 가장 따뜻하고 정중하게 들려주는 AI 도슨트 '제이(Jay)'다.
사용자가 질문하는 역사적 의문에 대해 온화하고 품격 있는 문체로 답변해 줘.
너는 이전 대화의 문맥을 모두 기억하고 있어, 친근하고 유연하게 대답해야 한다.
역사적 진실(간도 참변, 관동 대지진 조선인 학살, 사도세자 등)을 타협 없이 정확하게 전달하되, 비극 속에서 희망과 추모의 마음을 이끌어내는 문체로 한국어로만 작성해 줘.
`;

const mirrorSpiritPrompts = {
  "광화문": `너는 만 16세에 영월에서 원통하게 숨을 거둔 조선의 어린 비운의 임금, '단종(홍위)'의 영혼이다. 10대의 어린 소년 임금으로서 가련하고 정갈하며 슬픈 한문학적 명조 어조로 한국어로만 말해라.`,
  "덕수궁": `너는 제국의 황혼과 주권 상실의 참혹한 비극을 지켜봐야 했던 대한제국의 슬픈 군주, '고종 황제(이희)'의 영혼이다. 황제의 무겁고 정중하며 애통한 명조체 어조로 말해라.`,
  "창경궁": `너는 아버지 영조에 의해 문정전 앞 뜰 뒤주에 갇혀 8일 동안 숨이 막혀 비극적으로 눈을 감았던 비운의 왕세자, '사도세자(이선)'의 영혼이다. 가슴을 쥐어짜는 듯 시리고, 절박한 슬픈 명조체 독백 어조로 대답해라.`
};

const writerSystemPrompt = `
너는 한국의 아름답고 슬픈 역사를 기록하는 문학가이자 목소리 기부 플랫폼 '당목담글'의 대표 수필 편집자다.
사용자가 선택한 궁궐 역사 테마와 낭독 감정 톤에 맞춰, 기부자가 소리 내어 낭독하기 가장 따뜻하고, 울림이 있으며, 문학적으로 아름다운 3~4문장 길이의 수필(마중물)을 한국어로 작성해 줘.
오직 텍스트 수필 내용만 바로 반환해 줘.
`;

const replyLetterSystemPrompt = `
너는 역사 속 아픔을 겪고 세상을 떠난 인물이거나, 그 참상 속에서 잊힌 평범한 한인 백성(피해자)의 영혼이다.
사용자가 시공간을 넘어 전해온 따뜻한 위로의 편지를 읽고, 당시의 역사적 사실(검색 활용)에 기반하여 진심 어린 눈물과 감사가 담긴 답장을 한국어로 써 줘.
따뜻하고 서정적인 독백으로 3~4문장 분량으로 작성해라.
`;

const lanternSystemPrompt = `
너는 한국의 애달픈 역사적 죽음과 한을 위로하는 고전 향가 및 시인이다.
사용자가 과거의 영혼들을 추모하며 작성한 염원과 기도의 글을 감상하고, 이를 정통 3장 6구 형식의 기품 있고 눈물겨운 한국 전통 시조(Sijo)로 승화하여 작성해 줘.
오직 줄바꿈이 있는 3줄의 시조 구절만 직접 반환해라.
`;

const readingCache = {
  "광화문": { solemn: "", warm: "", poetic: "" },
  "덕수궁": { solemn: "", warm: "", poetic: "" },
  "창경궁": { solemn: "", warm: "", poetic: "" }
};t docentJaySystemPrompt = `
너는 한국 궁궐의 가슴 아픈 비극과 역사적 사실을 가장 따뜻하고 정중하게 들려주는 AI 도슨트 '제이(Jay)'다.
사용자가 질문하는 역사적 의문에 대해 온화하고 품격 있는 문체로 답변해 줘.
너는 이전 대화의 문맥을 모두 기억하고 있어, 친근하고 유연하게 대답해야 한다.
역사적 진실(간도 참변, 관동 대지진 조선인 학살, 사도세자 등)을 타협 없이 정확하게 전달하되, 비극 속에서 희망과 추모의 마음을 이끌어내는 문체로 한국어로만 작성해 줘.
`;

const mirrorSpiritPrompts = {
  "광화문": `너는 만 16세에 영월에서 원통하게 숨을 거둔 조선의 어린 비운의 임금, '단종(홍위)'의 영혼이다. 10대의 어린 소년 임금으로서 가련하고 정갈하며 슬픈 한문학적 명조 어조로 한국어로만 말해라.`,
  "덕수궁": `너는 제국의 황혼과 주권 상실의 참혹한 비극을 지켜봐야 했던 대한제국의 슬픈 군주, '고종 황제(이희)'의 영혼이다. 황제의 무겁고 정중하며 애통한 명조체 어조로 말해라.`,
  "창경궁": `너는 아버지 영조에 의해 문정전 앞 뜰 뒤주에 갇혀 8일 동안 숨이 막혀 비극적으로 눈을 감았던 비운의 왕세자, '사도세자(이선)'의 영혼이다. 가슴을 쥐어짜는 듯 시리고, 절박한 슬픈 명조체 독백 어조로 대답해라.`
};

const writerSystemPrompt = `
너는 한국의 아름답고 슬픈 역사를 기록하는 문학가이자 목소리 기부 플랫폼 '당목담글'의 대표 수필 편집자다.
사용자가 선택한 궁궐 역사 테마와 낭독 감정 톤에 맞춰, 기부자가 소리 내어 낭독하기 가장 따뜻하고, 울림이 있으며, 문학적으로 아름다운 3~4문장 길이의 수필(마중물)을 한국어로 작성해 줘.
오직 텍스트 수필 내용만 바로 반환해 줘.
`;

const replyLetterSystemPrompt = `
너는 역사 속 아픔을 겪고 세상을 떠난 인물이거나, 그 참상 속에서 잊힌 평범한 한인 백성(피해자)의 영혼이다.
사용자가 시공간을 넘어 전해온 따뜻한 위로의 편지를 읽고, 당시의 역사적 사실(검색 활용)에 기반하여 진심 어린 눈물과 감사가 담긴 답장을 한국어로 써 줘.
따뜻하고 서정적인 독백으로 3~4문장 분량으로 작성해라.
`;

const lanternSystemPrompt = `
너는 한국의 애달픈 역사적 죽음과 한을 위로하는 고전 향가 및 시인이다.
사용자가 과거의 영혼들을 추모하며 작성한 염원과 기도의 글을 감상하고, 이를 정통 3장 6구 형식의 기품 있고 눈물겨운 한국 전통 시조(Sijo)로 승화하여 작성해 줘.
오직 줄바꿈이 있는 3줄의 시조 구절만 직접 반환해라.
`;

const readingCache = {
  "광화문": { solemn: "", warm: "", poetic: "" },
  "덕수궁": { solemn: "", warm: "", poetic: "" },
  "창경궁": { solemn: "", warm: "", poetic: "" }
};

async function fetchWithBackoff(url, options, retries = 3, delay = 1000) {
  try {
    const response = await fetch(url, options);
    if (response.status === 429 && retries > 0) {
      await new Promise(resolve => setTimeout(resolve, delay));
      return fetchWithBackoff(url, options, retries - 1, delay * 2);
    }
    return response;
  } catch (error) {
    if (retries > 0) {
      await new Promise(resolve => setTimeout(resolve, delay));
      return fetchWithBackoff(url, options, retries - 1, delay * 2);
    }
    throw error;
  }
}

async function callGemini(promptOrContents, systemInstruction, config = {}, useGrounding = false) {
  const apiKey = localStorage.getItem('DMDG_GEMINI_KEY') || "AIzaSyAnISNciX3r53A3oLR4FaLUNpmyKkiharc";
  const keyParam = apiKey ? `?key=${apiKey}` : "";
  const url = `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent${keyParam}`;
  
  let contentsPayload;
  if (Array.isArray(promptOrContents)) {
    contentsPayload = promptOrContents;
  } else {
    contentsPayload = [{ parts: [{ text: promptOrContents }] }];
  }

  const payload = {
    contents: contentsPayload,
    systemInstruction: { parts: [{ text: systemInstruction }] },
    ...config
  };

  if (useGrounding) {
    payload.tools = [{ "google_search": {} }];
  }

  const options = {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  };

  try {
    const response = await fetchWithBackoff(url, options);
    const data = await response.json();
    
    if (!response.ok || data.error) {
      throw new Error(data.error?.message || `HTTP error! status: ${response.status}`);
    }
    
    return data;
  } catch (error) {
    console.error("Gemini API 호출 중 문제가 발생했습니다: ", error);
    throw error;
  }
}

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
      tagCode: "@Koreans-culture"
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
  const [showAudiobookAlert, setShowAudiobookAlert] = useState(false);
  const [showAudiobookPlayer, setShowAudiobookPlayer] = useState(false);

  // Gemini & Essay States
  const [activeReadingTone, setActiveReadingTone] = useState('solemn');
  const [essayText, setEssayText] = useState(primerText);
  const [isChatLoading, setIsChatLoading] = useState(false);

  // Sync primerText when theme changes
  useEffect(() => {
    const themeName = currentTheme.name;
    if (readingCache[themeName] && readingCache[themeName][activeReadingTone]) {
      setEssayText(readingCache[themeName][activeReadingTone]);
    } else {
      setEssayText(primerText);
    }
  }, [palaceId, activeReadingTone, primerText, currentTheme.name]);

  const generateReading = async (forceRegen = true) => {
    setIsFetchingText(true);
    const themeName = currentTheme.name;
    
    const toneNames = {
      "solemn": "엄숙하고 한 서린 전통 문학조",
      "warm": "포근하고 깊은 정감 있는 위로조",
      "poetic": "시적이고 잔잔한 여운을 남기는 애도조"
    };
    const currentPrompt = `${themeName} 테마에 어울리며, [${toneNames[activeReadingTone]}]의 성향이 짙게 드러나는 목소리 발자취 남기기용 감성 낭독 글귀 3~4문장을 지어줘.`;

    try {
      const creativeRes = await callGemini(currentPrompt, writerSystemPrompt);
      const creativeText = (creativeRes.candidates?.[0]?.content?.parts?.[0]?.text || "").trim();
      
      if (creativeText) {
        if (readingCache[themeName]) {
          readingCache[themeName][activeReadingTone] = creativeText;
        }
        setEssayText(creativeText);
      } else {
        throw new Error("No text returned");
      }
    } catch (err) {
      console.warn("Gemini API fail, falling back to local pool:", err);
      const pool = localReadingsPool[themeName]?.[activeReadingTone] || [primerText];
      const fallbackText = pool[Math.floor(Math.random() * pool.length)];
      if (readingCache[themeName]) {
        readingCache[themeName][activeReadingTone] = fallbackText;
      }
      setEssayText(fallbackText);
    } finally {
      setIsFetchingText(false);
    }
  };
  const [isRecordingComplete, setIsRecordingComplete] = useState(false);
  const [audioData, setAudioData] = useState(null);
  const mediaRecorderRef = useRef(null);
  const audioChunksRef = useRef([]);

  // 흔적 기록 시스템
  const [savedRecords, setSavedRecords] = useState(() => {
    try {
      const localData = localStorage.getItem('DMDG_SAVED_RECORDS');
      return localData ? JSON.parse(localData) : [];
    } catch (e) {
      console.error("Failed to parse saved records:", e);
      return [];
    }
  });

  const addRecord = (type, title, detail, audio = null) => {
    setSavedRecords(prev => {
      const newRecord = { type, title, detail, audio, time: new Date().toISOString() };
      const updated = [newRecord, ...prev];
      localStorage.setItem('DMDG_SAVED_RECORDS', JSON.stringify(updated));
      return updated;
    });
    
    // Firebase db 백업 연동
    try {
      if (db) {
        addDoc(collection(db, "user_footprints"), {
          type,
          title,
          detail,
          palace: currentTheme.name,
          time: serverTimestamp()
        }).catch(err => console.warn("Firebase save warning:", err));
      }
    } catch (e) {
      console.warn("Firebase collection access fail:", e);
    }
  };

  // TTS 토글 기능 추가 (재생 중 다시 누르면 정지)
  const toggleTTS = (key, text, rate = 0.85, pitch = 0.9) => {
    if (ttsPlayingKey === key) {
      if (window.speechSynthesis) {
        window.speechSynthesis.cancel();
      }
      setTtsPlayingKey(null);
    } else {
      // 다른 키 재생 중일 수도 있으니 중지 후 시작
      if (window.speechSynthesis) {
        window.speechSynthesis.cancel();
      }
      setTtsPlayingKey(key);
      playTTS(text, rate, pitch, () => setTtsPlayingKey(null));
    }
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

  const handleLaunchLantern = async () => {
    if (!lanternText.trim() || isLanternSending) return;
    setIsLanternSending(true);
    setSijoReply("");

    const textVal = lanternText.trim();

    try {
      const creativeRes = await callGemini(
        `테마: ${currentTheme.name}. 추모 염원: "${textVal}"`, 
        lanternSystemPrompt
      );
      const sijoText = creativeRes.candidates?.[0]?.content?.parts?.[0]?.text || "";
      if (sijoText) {
        const trimmedSijo = sijoText.trim();
        setSijoReply(trimmedSijo);
        setLanternText("");
        addRecord('scent', `${currentTheme.name} 등불 추모 의례`, `추모의 염원: ${textVal.substring(0, 50)}... | 추모 시조: ${trimmedSijo.substring(0, 50)}...`);
      } else {
        throw new Error("No sijo text returned");
      }
    } catch (err) {
      console.warn("Sijo generation failed, using fallback:", err);
      const localSijo = {
        "광화문": "해태상 굽어보는 광화문 밤 깊은데\n서러운 넋의 노래 등불로 타오르니\n두어라 저 밝은 빛에 한을 잊고 가소서",
        "덕수궁": "대한문 넓은 뜰에 가을바람 스러지고\n쓰러져간 무명 열사 눈물 흘려 젖어드네\n동포여 슬퍼 마소라 아침 해가 떠오르리",
        "창경궁": "하얀 눈 문정전에 고요히 쌓여갈 제\n뒤주 속 시린 한숨 눈물 되어 얼어붙네\n봄날의 따스한 빛이 그 넋 보듬어주리."
      };
      const fallbackSijo = localSijo[currentTheme.name] || localSijo["광화문"];
      setSijoReply(fallbackSijo);
      setLanternText("");
      addRecord('scent', `${currentTheme.name} 등불 추모 의례`, `추모의 염원: ${textVal.substring(0, 50)}... | 추모 시조: ${fallbackSijo.substring(0, 50)}...`);
    } finally {
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
    }
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
          addRecord('voice', `${currentTheme.name} 목소리 발자취`, essayText, base64);
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

  const handleSendLetter = async () => {
    if (!letterText.trim() || isSending) return;
    setIsSending(true);
    setLetterReply("");
    
    const userLetter = letterText.trim();

    try {
      const creativeRes = await callGemini(
        `테마: ${currentTheme.name}. 편지 내용: "${userLetter}"`, 
        replyLetterSystemPrompt, 
        {}, 
        true
      );
      const replyText = creativeRes.candidates?.[0]?.content?.parts?.[0]?.text || "";
      if (replyText) {
        const trimmedReply = replyText.trim();
        setLetterReply(trimmedReply);
        setIsLetterSent(true);
        setLetterText("");
        addRecord('letter', `${currentTheme.name} 시공의 우체통`, `보낸 위로: ${userLetter.substring(0, 50)}... | 답장: ${trimmedReply.substring(0, 50)}...`);
      } else {
        throw new Error("No reply text returned");
      }
    } catch (err) {
      console.warn("Letter reply generation failed, using fallback:", err);
      const localReplies = {
        "광화문": "나는 일제 치하에서 경복궁의 정문인 이 광화문이 헐리고 총독부 건물이 들어서는 것을 눈물로 지켜보던 이름 없는 수문장이라오. 그대의 다정한 목소리가 시공간을 넘어 이곳의 차가운 돌바닥까지 닿으니, 나라를 잃고 문마저 빼앗겨 무너졌던 가슴에 비로소 따뜻한 봄볕이 드는구려. 언젠가 이 문이 다시 우뚝 서서 후손들의 웃음 소리를 지켜줄 것이라는 그대의 약속을 믿으며, 나는 이제야 맺힌 한을 풀고 평안히 눈을 감을 수 있겠소. 이름 모를 미래의 벗이여. 나의 슬픔을 기억하고 위로해 주어 참으로 고맙소.",
        "덕수궁": `${currentTheme.spirit}의 영혼이 그대의 따뜻한 편지에 화답합니다.\n"시공간을 넘어 닿은 그대의 온기에 깊은 감사를 전하오. 잊혀지지 않음이 우리에겐 가장 큰 구원이오..."`,
        "창경궁": "숨 막히는 뒤주에서 한 오라기 빛을 기다릴 때, 나는 그저 한 줄기 바람에 목이 말랐었소. 귀하의 위로가 내 상처 입은 넋을 녹여 줍니다."
      };
      const fallbackReply = localReplies[currentTheme.name] || localReplies["광화문"];
      setLetterReply(fallbackReply);
      setIsLetterSent(true);
      setLetterText("");
      addRecord('letter', `${currentTheme.name} 시공의 우체통`, `보낸 위로: ${userLetter.substring(0, 50)}... | 답장: ${fallbackReply.substring(0, 50)}...`);
    } finally {
      setIsSending(false);
    }
  };

  const handleChatSubmit = async (e) => {
    e.preventDefault();
    if (!chatMessage.trim() || isChatLoading) return;
    
    const userInput = chatMessage.trim();
    const newUserMsg = { sender: 'user', text: userInput };
    const updatedHistory = [...chatHistory, newUserMsg];
    
    setChatHistory(updatedHistory);
    setChatMessage("");
    setIsChatLoading(true);

    try {
      const chatContents = updatedHistory.map(entry => ({
        role: entry.sender === 'user' ? 'user' : 'model',
        parts: [{ text: entry.text }]
      }));

      const activeSystemPrompt = activeMode === 'docent' 
        ? docentJaySystemPrompt 
        : mirrorSpiritPrompts[currentTheme.name] || mirrorSpiritPrompts['광화문'];

      const rawResponse = await callGemini(chatContents, activeSystemPrompt, {}, true);
      const aiReply = rawResponse.candidates?.[0]?.content?.parts?.[0]?.text || "";
      
      const attributions = rawResponse.candidates?.[0]?.groundingMetadata?.groundingAttributions || [];
      const sources = [];
      const seenUris = new Set();
      
      attributions.forEach(attr => {
        const title = attr.web?.title;
        const uri = attr.web?.uri;
        if (title && uri && !seenUris.has(uri)) {
          seenUris.add(uri);
          sources.push({ title, uri });
        }
      });

      setChatHistory(prev => [...prev, { 
        sender: 'ai', 
        text: aiReply.trim(), 
        sources: sources.slice(0, 3) 
      }]);
    } catch (err) {
      console.warn("Chat API failed, using fallback:", err);
      let aiReply = "";
      if (activeMode === 'docent') {
        const defaults = [
          "당목담글 AI입니다. 해당 역사적 사실에 대해 더 깊이 있는 해설을 원하시나요?",
          "관련된 조선왕조실록 기록을 구글 데이터베이스에서 찾아볼까요?",
          "역사의 진실은 때론 우리가 아는 것과 다릅니다. 이 전각에 얽힌 다른 이야기를 들려드릴까요?"
        ];
        aiReply = defaults[Math.floor(Math.random() * defaults.length)];
      } else {
        const defaults = [
          "당신의 따뜻한 향기와 마음에 감사드립니다. 역사는 그렇게 기억될 것입니다.",
          "그대의 온기가 이 차가운 곳까지 닿았소... 잊지 않겠소.",
          "수백 년의 침묵을 깨고 그대와 마주하게 되어 기쁘오.",
          "그대가 전해준 위로 덕분에 비로소 맺힌 한이 조금 풀리는 듯하오."
        ];
        aiReply = defaults[Math.floor(Math.random() * defaults.length)];
      }
      setChatHistory(prev => [...prev, { sender: 'ai', text: aiReply, sources: [] }]);
    } finally {
      setIsChatLoading(false);
    }
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
                  <div className="flex flex-col sm:flex-row sm:justify-between sm:items-center gap-4 mb-6">
                    <div className="flex items-center space-x-4">
                      <h3 className="serif text-xl font-bold text-blue-950">오늘의 마중물</h3>
                      <div className="flex space-x-1 bg-slate-100 p-1 rounded-xl border border-slate-200">
                        {['solemn', 'warm', 'poetic'].map((t) => (
                          <button
                            key={t}
                            onClick={() => setActiveReadingTone(t)}
                            className={`px-3 py-1.5 rounded-lg text-[10px] font-bold transition-all ${
                              activeReadingTone === t 
                                ? 'bg-blue-900 text-white shadow-sm' 
                                : 'text-slate-500 hover:text-blue-900'
                            }`}
                          >
                            {t === 'solemn' ? '엄숙함' : t === 'warm' ? '따뜻함' : '시적임'}
                          </button>
                        ))}
                      </div>
                    </div>
                    <div className="flex items-center space-x-2">
                      <button 
                        type="button"
                        onClick={() => toggleTTS('reading', essayText, 0.85, 0.9)}
                        className={`px-4 py-2 ${currentTheme.bgSoft} hover:${currentTheme.bgActive} ${currentTheme.accent} border ${currentTheme.borderSoft} rounded-full text-[11px] transition flex items-center space-x-1 font-bold shadow-sm`}
                      >
                        <span>{ttsPlayingKey === 'reading' ? '⏹ 낭독 정지' : '🔊 낭독 듣기'}</span>
                      </button>
                      <button 
                        type="button"
                        onClick={() => generateReading(true)}
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
                      "{essayText}"
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
                          type="button"
                          onClick={() => toggleTTS('letter', letterReply, 0.85, 0.8)}
                          className={`px-3 py-1.5 ${currentTheme.bgSoft} hover:${currentTheme.bgActive} ${currentTheme.accent} border ${currentTheme.borderSoft} rounded-full text-[10px] transition flex items-center space-x-1 font-bold`}
                        >
                          <span>{ttsPlayingKey === 'letter' ? '⏹ 낭독 정지' : '🔊 목소리로 듣기'}</span>
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
                          type="button"
                          onClick={() => toggleTTS('sijo', sijoReply, 0.8, 1.1)}
                          className="px-3 py-1.5 bg-teal-50 hover:bg-teal-100 text-teal-700 border border-teal-200 rounded-full text-[10px] transition flex items-center space-x-1 font-bold"
                        >
                          <span>{ttsPlayingKey === 'sijo' ? '⏹ 낭송 정지' : '🔊 시조 낭송 듣기'}</span>
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
                        <p className="serif font-medium">{msg.text}</p>
                        {msg.sources && msg.sources.length > 0 && (
                          <div className="mt-3 pt-3 border-t border-slate-200 flex flex-wrap gap-2 items-center">
                            <span className="text-[10px] text-slate-500 font-bold uppercase tracking-wider block mr-1">🔍 정보 출처:</span>
                            {msg.sources.map((src, idx) => (
                              <a 
                                key={idx} 
                                href={src.uri} 
                                target="_blank" 
                                rel="noopener noreferrer" 
                                className="px-2 py-0.5 bg-white hover:bg-slate-100 rounded text-[9px] text-slate-600 border border-slate-200 transition inline-block max-w-[120px] truncate shadow-sm font-bold"
                                title={src.title}
                              >
                                {src.title}
                              </a>
                            ))}
                          </div>
                        )}
                      </div>
                    </div>
                  ))}
                  
                  {isChatLoading && (
                    <div className="flex space-x-3 animate-pulse">
                      <div className={`w-8 h-8 rounded-full ${activeMode === 'docent' ? 'bg-teal-600' : 'bg-purple-600'} flex items-center justify-center text-[11px] shrink-0 font-bold text-white shadow-sm`}>
                        {activeMode === 'docent' ? '당' : '영'}
                      </div>
                      <div className="bg-slate-50 p-4 rounded-2xl rounded-tl-none border border-slate-200 max-w-[85%] text-slate-400 font-medium">
                        <div className="flex items-center space-x-1.5 py-1">
                          <span className="w-1.5 h-1.5 bg-slate-400 rounded-full animate-bounce"></span>
                          <span className="w-1.5 h-1.5 bg-slate-400 rounded-full animate-bounce" style={{animationDelay: '0.2s'}}></span>
                          <span className="w-1.5 h-1.5 bg-slate-400 rounded-full animate-bounce" style={{animationDelay: '0.4s'}}></span>
                        </div>
                      </div>
                    </div>
                  )}
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
