# Google Flow / Google Omni 전용 생성 AI 프롬프트 패키지 (더피의 소소 밥상 편)

본 문서는 사찰음식 쇼츠 영상 제작을 위해 **Google Flow(비디오 생성/워크플로우)** 또는 **Google Omni(멀티모달/LLM)** 등 생성 AI에 즉시 복사-붙여넣기하여 고품질 결과물을 얻을 수 있도록 최적화된 프롬프트 모음입니다. 케데헌 유니버스의 주인공인 **서씨(Seo-ssi)**와 **더피(Duffy)**가 명시적으로 포함되어 있습니다.

특히 이미지의 경우, Google Flow의 고성능 이미지 생성 모델인 **나노바나나 2.5 (Nano Banana 2.5)**에 최적화된 프롬프트와 멀티턴 지시어로 구성되어 있습니다.

---

## 1. 🎙️ Google Omni / TTS (음성 합성) 전용 나레이션 스크립트
> 음성 생성 모델에 입력할 때 가독성이 떨어지거나 괄호, 특수기호가 섞이지 않도록 정제한 텍스트입니다. 성우 스타일은 나레이터 강하루의 페르소나인 **"Calm, deep, meditative, warm 50s Korean male voice with a touch of loneliness"**로 지정하세요.

### 1) 산속 암자 버전 (오리지널 - 서씨와 더피)
* **KOR**: "요괴들의 한을 달래며 먼 길을 걸어온 서씨와 더피. 오늘 지리산 깊은 암자에서 그들의 거친 숨을 고르는 맑은 공양이 시작됩니다. 뜨거운 가마솥 안에서 취나물의 쓴맛은 향긋함으로 변하고, 들기름으로 고소함을 더합니다. 세상을 향한 날 선 마음들을 데쳐내어 다스리는 시간입니다. 두툼한 표고버섯에 달콤한 조청과 간장이 깊이 배어듭니다. 고기 한 점, 마늘 한 톨 없이도, 버섯이 가진 대지의 풍미가 거친 무사의 식탁을 채웁니다. 달큰한 단호박과 옹심이가 들깨의 품에서 걸쭉하게 끓어오릅니다. 비우고 채워내는 산사의 따뜻한 온기가 서씨의 깊은 상처를 어루만집니다. 오늘 하루, 복잡한 세상의 짐을 내려놓고 마음을 비워내는 사찰 요리 어떠신가요? 평온한 산사로 당신을 초대합니다."
* **ENG**: "Seo-ssi and Duffy, who have traveled far soothing the grudges of demons. Today, at a deep mountain hermitage, a pure meal begins to calm their weary breaths. Inside the hot cast-iron pot, the bitterness of Chwinamul turns into fragrance, enriched by savory perilla oil. It is a time to blanch away their sharp edges towards the world. Sweet rice syrup and soy sauce seep deeply into the chewy shiitake mushrooms. Without a single piece of meat or clove of garlic, the earthy flavor of the mushrooms fills the weary hunter's table. Sweet pumpkin and dough balls boil in the savory embrace of perilla seeds. The warm comfort of the temple, of emptying and filling, gently caresses Seo-ssi's deep scars. How about a temple dish to lightly empty your mind today? We invite you to this peaceful mountain temple."

### 2) 미국 주방 버전 (현지화 - 더피의 소소 밥상)
* **KOR**: "지친 일상을 정화하는 더피의 소소 밥상. 미국 마트의 애호박, 버섯, 당근이 서씨와 더피의 솜씨로 맑은 사찰음식이 됩니다. 마늘, 파, 양파 같은 오신채는 절대 넣지 않습니다. 들기름과 고추로만 버무려 낸 구운 애호박 버섯 무침. 비워낼수록 깊어지는 맛입니다. 당근 본연의 달큰한 맛을 온전히 살린 선재스님의 당근전. 화려함 대신 소박함을 담아 바삭하게 구워냅니다. 해외를 울린 정관스님의 레시피. 감자를 갈아 부친 쫄깃한 감자전과 고소한 연근 호두 조림이 낯선 이국 땅에 따스한 온기를 채웁니다. 오늘 저녁은 당신의 주방에 오신채 없는 평온한 밥상을 올려보는 건 어떨까요?"
* **ENG**: "Duffy's Soso Table to purify your weary days. Zucchini, mushrooms, and carrots from a US store become pure temple food in the hands of Seo-ssi and Duffy. No garlic, no onions—the five pungent spices are completely excluded. Mixed only with perilla oil and chili, this grilled zucchini and mushroom dish tastes deeper as it empties. Ven. Sunjae's carrot pancake, fully preserving the natural sweetness of carrots. Baked to crispy perfection, embracing simplicity instead of extravagance. Ven. Jeong Kwan's recipe that moved the world. Chewy potato pancake and savory braised lotus root with walnuts fill this unfamiliar land with warm comfort. Tonight, why not set a peaceful, allium-free table in your kitchen?"

---

## 2. 🎨 Google Flow - 나노바나나 2.5 (Nano Banana 2.5) 이미지 생성 가이드
> 나노바나나 2.5는 **캐릭터 일관성(Consistent Characters)** 및 **자연어 멀티턴 편집**에 강점이 있습니다. 서씨와 더피의 캐릭터 원본 파일(`서씨.png`, `더피.png`)을 **Google Flow의 캐릭터 참조(Image Reference / Character Reference)** 탭에 업로드한 뒤 아래 프롬프트를 사용해 주세요.

### 💡 나노바나나 2.5 세팅 팁
1. **Character Reference**: `DMDG_UT\YOUTUBE\characters\더피.png` 및 `서씨.png`를 업로드하여 고정 캐릭터 가중치를 최대로 설정합니다.
2. **Aspect Ratio**: 쇼츠 전용 종횡비인 **9:16 (Vertical)**으로 고정합니다.
3. **Style**: **Cinematic, Photo-realism, Soft lighting, Cozy, Detailed textures** 태그를 기본값으로 지정합니다.

---

### 1) 산속 암자 버전 (Original Hermitage Edition)

* **Scene 1 (Hook - 0~5s)**
  > **Prompt**: A cinematic vertical 9:16 shot of a misty early morning at a traditional Korean Hanok temple (Hermitage) deep in the mountains. A tired-looking middle-aged Korean man, Seo-ssi (using character reference 1), wearing a worn trench coat, sits on the wooden porch. Next to him sits the cute mythical Haetae creature, Duffy (using character reference 2), with big expressive eyes and soft fur. On a weathered wooden table, fresh Chwinamul greens, dried shiitake, and a sweet pumpkin are in a wicker basket. Volumetric lighting, mist rising, cozy and meditative atmosphere, highly detailed, 8k. --ar 9:16
* **Scene 2 (Chwinamul - 5~20s)**
  > **Prompt**: Close-up of Seo-ssi's (using character reference 1) rugged hands putting fresh green wild herbs into a large boiling cast-iron pot over a wood-fire stove in a traditional temple kitchen. Next to the stove, the cute Haetae creature Duffy (using character reference 2) watches with wide, curious eyes. Warm lighting, steam rising, detailed textures, photorealistic, 8k. --ar 9:16
* **Scene 3 (Shiitake - 20~35s)**
  > **Prompt**: Close-up of thick, scored shiitake mushrooms sizzling on a flat iron pan over red charcoal. The cute Haetae creature, Duffy (using character reference 2), is nearby sniffing the savory aroma. A thick, dark brown soy-sauce and rice-syrup glaze is poured over, bubbling and caramelizing. Warm embers glow, photorealistic, 8k. --ar 9:16
* **Scene 4 (Soup - 35~50s)**
  > **Prompt**: A clay pot boiling with yellow pumpkin broth, tofu cubes, and dough balls. Seo-ssi (using character reference 1) stirs the soup with a wooden spoon, while the cute Haetae creature Duffy (using character reference 2) sits snugly by the warm firewood stove. Cozy temple kitchen atmosphere, steam rising, photorealistic, 8k. --ar 9:16
* **Scene 5 (Outro - 50~60s)**
  > **Prompt**: An extreme wide shot of a peaceful Korean temple veranda. Seo-ssi (using character reference 1) and the small Haetae creature Duffy (using character reference 2) sit side by side facing the majestic, misty mountains in the distance, quietly sharing a simple meal from wooden bowls (Baru). Golden hour sunlight, calm wind, meditative, zen atmosphere, 8k. --ar 9:16

---

### 2) 미국 주방 버전 (Modern US Kitchen Edition - Duffy's Soso Table)

* **Scene 1 (Hook - 0~5s)**
  > **Prompt**: A cinematic vertical 9:16 shot of a bright, clean, organic supermarket aisle. A rugged middle-aged Korean man, Seo-ssi (using character reference 1) in a worn trench coat pushes a shopping cart. Inside the cart sits the cute small Haetae mascot creature, Duffy (using character reference 2) with big expressive eyes, wagging its tail and pointing its paw towards fresh zucchini, carrots, and potatoes on the shelves. Natural lighting, commercial film look, sharp focus, 8k. --ar 9:16
* **Scene 2 (Zucchini & Mushrooms - 5~20s)**
  > **Prompt**: Top-down vertical 9:16 shot of a modern kitchen island with a white granite countertop. Seo-ssi's (using character reference 1) rugged hands grill sliced zucchini and mushrooms in a skillet until golden brown. Next to him, the cute Haetae creature Duffy (using character reference 2), wearing a small cooking apron, uses its fluffy paws to gently mix the grilled zucchini and mushrooms in a glass bowl with perilla oil and chopped peppers. Natural sunlight, cozy, 8k. --ar 9:16
* **Scene 3 (Carrot Pancake - 20~35s)**
  > **Prompt**: A close-up shot of a hot frying pan in a modern kitchen. The cute Haetae creature, Duffy (using character reference 2), wearing a small apron, holds a small wooden spatula to fry a thin, crispy orange carrot pancake (Carrot Jeon). In the background, Seo-ssi (using character reference 1) is finely slicing bright orange carrots on a wooden cutting board. Cozy kitchen lighting, sharp focus, 8k. --ar 9:16
* **Scene 4 (Potato & Lotus Root - 35~50s)**
  > **Prompt**: A vertical 9:16 shot. Close-up of a pot simmering with sliced lotus root, walnuts, and a glossy brown soy sauce glaze. Next to the pot, the cute Haetae creature Duffy (using character reference 2) is vigorously grating a raw potato on a metal grater, making a funny concentrated face. Warm cozy lighting, highly detailed, 8k. --ar 9:16
* **Scene 5 (Outro - 50~60s)**
  > **Prompt**: A peaceful medium shot of Seo-ssi (using character reference 1) and the cute Haetae creature Duffy (using character reference 2) sitting side-by-side at a dining table next to a large glass window overlooking a green backyard. Duffy happily eats with a spoon, and Seo-ssi smiles gently while sipping hot soup from a wooden bowl. On the table, three minimalist white dishes of temple food are laid out. Afternoon golden hour sunlight, slow panning-out, calm, 8k. --ar 9:16
