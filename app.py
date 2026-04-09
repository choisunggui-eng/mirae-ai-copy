# -*- coding: utf-8 -*-
import streamlit as st
import google.generativeai as genai
import base64

# 1. 페이지 설정 (탭 이름과 아이콘)
st.set_page_config(page_title="미래아이엔씨 AI 매체 최적화 솔루션", page_icon="🔵", layout="centered")

# 2. 로고 변환 함수 (이미지 파일을 웹 화면에 표시하기 위함)
def get_image_base64(path):
    try:
        with open(path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
        return encoded_string
    except: return None

# 3. 군더더기 없는 화이트 디자인 + 매체별 포인트 (CSS)
st.markdown("""
    <style>
    /* 배경색: 완전 흰색으로 깔끔하게 */
    .stApp {
        background-color: #FFFFFF;
    }
    
    /* 로고 중앙 정렬 및 크기 조절 (중앙 상단) */
    .logo-container {
        display: flex;
        justify-content: center;
        margin-top: 1rem;
        margin-bottom: 2rem;
    }
    .logo-container img {
        max-width: 200px; /* 로고 크기 조절 */
    }

    /* 타이틀 및 서브 타이틀: 회사 폰트 느낌 반영 */
    .main-title {
        color: #333333; /* 블랙 */
        font-size: 1.8rem;
        font-weight: 800;
        text-align: center;
        margin-top: 1rem;
        margin-bottom: 0.5rem;
    }
    
    .sub-title {
        color: #666666; /* 그레이 */
        font-size: 1rem;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: 400;
        line-height: 1.5;
    }

    /* 입력창 라벨 스타일: 더 얇고 깔끔하게 */
    .stTextInput label {
        color: #333333 !important;
        font-weight: 700 !important;
        font-size: 0.95rem !important;
    }
    
    /* 선택 박스 라벨 스타일: 미래 블루 포인트 */
    .stSelectbox label {
        color: #0033FF !important; /* 미래 블루 */
        font-weight: 700 !important;
        font-size: 0.95rem !important;
    }
    
    /* 입력창 테두리색: 더 옅게 */
    .stTextInput>div>div>input {
        border-color: #E2E8F0 !important;
        border-radius: 6px !important;
    }

    /* 생성 버튼: 미래아이엔씨 블루, 더 얇고 세련되게 */
    .stButton>button {
        width: 100%;
        background-color: #0033FF !important; /* 미래 블루 */
        color: white !important;
        border-radius: 6px !important;
        font-weight: bold !important;
        height: 2.8em !important;
        border: none !important;
        transition: all 0.2s ease;
    }
    
    .stButton>button:hover {
        background-color: #0022AA !important;
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(0,51,255,0.2);
    }

    /* 결과 박스: 깔끔한 그레이 마감 */
    .result-box {
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 1.5rem;
        background-color: #F8FAFC; /* 아주 연한 회색 배경 */
        line-height: 1.7;
        color: #333333;
    }
    
    /* 사이드바 스타일링: 과장님 맞춤 화이트 테마 */
    [data-testid="stSidebar"] {
        background-color: #FFFFFF;
        border-right: 1px solid #F1F5F9;
    }
    [data-testid="stSidebar"] h3, [data-testid="stSidebar"] p {
        color: #333333 !important;
        font-weight: 500 !important;
    }
    [data-testid="stSidebar"] div.stSuccess {
        background-color: #E6FFFA !important;
        color: #0D9488 !important;
    }
    [data-testid="stSidebar"] div.stInfo {
        background-color: #EFF6FF !important;
        color: #2563EB !important;
    }
    
/* 매체 심볼 스타일: 어떤 이미지가 들어와도 일정한 크기로 박제 */
    .symbol-container img {
        width: 60px !important;   /* 가로 길이를 고정 */
        height: 40px !important;  /* 세로 길이를 고정 */
        object-fit: contain;      /* 중요! 비율을 유지하면서 박스 안에 맞춤 */
        border: 1px solid #E2E8F0;
        border-radius: 4px;
        padding: 4px;
        background-color: #FFFFFF;
    }
    .symbol-container img {
        max-width: 50px; /* 심볼 크기 축소 */
        max-height: 40px;
        border: 1px solid #E2E8F0; /* 은은한 테두리 추가 */
        border-radius: 4px; /* 테두리 둥글게 */
        padding: 4px; /* 테두리 안쪽 여백 */
        background-color: #FFFFFF; /* 테두리 배경색 */
    }
    </style>
    """, unsafe_allow_html=True)

# 4. 사이드바 (Secrets 연동 및 워딩 유지)
with st.sidebar:
    # 깃허브에 올린 mirae_logo.png 파일을 불러와서 사이드바 하단에도 은은하게 표시
    try:
        mirae_logo = get_image_base64("mirae_logo.png")
        if mirae_logo:
            st.markdown(f'<div class="logo-container" style="margin-bottom:1rem;"><img src="data:image/png;base64,{mirae_logo}" style="max-width:180px;"></div>', unsafe_allow_html=True)
    except: pass
    
    st.write("---")
    st.markdown(f'<h3 style="color:#0033FF; text-align:center;">MIRAE I&C</h3>', unsafe_allow_html=True)
    st.markdown(f'<p style="text-align:center;">AI 매체 최적화 솔루션 v1.0</p>', unsafe_allow_html=True)
    
    st.write("---")
    try:
        api_key = st.secrets["GEMINI_API_KEY"]
        st.success("✅ 회사 전용 AI 엔진 가동 중")
    except:
        api_key = None
        st.warning("⚠️ Secrets 키 설정 필요")
    
    st.info("최성규 과장이 개발한 고효율 카피 자동 생성기입니다.")

# 5. [긴급 복구] 중앙 상단 메인 로고 삽입
try:
    # 깃허브에 올린 mirae_logo.png 파일을 중앙에 표시
    mirae_logo = get_image_base64("mirae_logo.png")
    if mirae_logo:
        st.markdown(f'<div class="logo-container"><img src="data:image/png;base64,{mirae_logo}"></div>', unsafe_allow_html=True)
except Exception as e: pass

# 메인 타이틀 및 서브 타이틀
st.markdown('<div class="main-title">🔥 최성규 과장의 야심작, 매체별 치트키</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">"매체 특성에 딱 맞춘 상위 0.1%의 전략적 카피"</div>', unsafe_allow_html=True)

st.write("---") # 구분선

# 6. 매체 선택 및 로고 심볼 노출 (과장님 요청 완벽 반영!)
# 매체별 로고 심볼 파일 매칭 (확장자 수기 붙이기 완료!)
platform_symbols = {
    "META": "meta_symbol.png",
    "GFA/DA": "gfa_symbol.png",
    "GOOGLE/DA": "google_symbol.png",
    "CRITEO": "criteo_symbol.png"
}

# st.columns를 활용하여 선택창과 심볼을 한 줄에 배치
col1_m, col2_s = st.columns([5, 1]) # 5:1 비율로 컬럼 나눔
with col1_m:
    platform = st.selectbox("🎯 광고 매체를 선택하세요", ["META", "GFA/DA", "GOOGLE/DA", "CRITEO"])
with col2_s:
    # 깃허브에서 가져온 심볼 파일을 인코딩하여 HTML로 표시
    symbol_base64 = get_image_base64(platform_symbols[platform])
    if symbol_base64:
        # 0.1% 마케터의 감각적인 디테일이 반영된 심볼 박스
        st.markdown(f'<div class="symbol-container"><img src="data:image/png;base64,{symbol_base64}"></div>', unsafe_allow_html=True)
    else:
        # 심볼 파일이 없으면 그냥 공백으로 표시 (에러 메시지 X)
        st.write("")

# 7. 제품 정보 입력 섹션 (2열 배치) - 깔끔하게
with st.container():
    st.markdown(f'<p style="color:#333333; font-weight:600; font-size: 1rem; margin-bottom:1rem;">📝 제품 정보 입력</p>', unsafe_allow_html=True)
    col1_i, col2_i = st.columns(2)
    with col1_i:
        product = st.text_input("📦 제품명 (Product)", placeholder="예: 연잎밥")
    with col2_i:
        keywords = st.text_input("✨ 핵심 키워드 (Keywords)", placeholder="예: 개별포장, 쫄깃함")

target = st.text_input("👥 타겟 고객 (Target Audience)", placeholder="예: 30대 바쁜 직장인")

st.write("") # 간격 조절

# 8. 매체별 가이드라인 정의 (AI에게 전달될 0.1% 전략)
guides = {
    "META": "이미지 중심의 매체이므로 감성적이고 트렌디한 문구, 풍부한 이모지 활용, 해시태그 포함.",
    "GFA/DA": "즉각적인 반응이 필요함. 호기심을 자극하는 강력한 후킹과 페인포인트 강조.",
    "GOOGLE/DA": "명확한 정보 전달 중심. 신뢰감 있는 톤앤매너와 핵심 혜택 중심의 간결한 구성.",
    "CRITEO": "리타겟팅 중심이므로 구매를 망설이는 고객의 등을 떠밀 수 있는 혜택(할인, 리뷰 등) 강조."
}

# 9. 생성 로직
if st.button(f"🚀 {platform} 전용 고효율 카피 생성 시작"):
    try:
        api_key = st.secrets["GEMINI_API_KEY"]
        genai.configure(api_key=api_key)
        
        # 모델 자동 선택 (gemini-1.5-flash)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # 미래아이엔씨 스타일의 전문적인 프롬프트
        prompt = f"""
        너는 미래아이엔씨의 {platform} 전문 퍼포먼스 마케터야.
        매체 가이드라인: {guides[platform]}
        
        위 가이드라인을 엄격히 준수하여 아래 제품에 대한 {platform} 최적화 카피 5개를 작성해줘.
        제품명: {product} / 키워드: {keywords} / 타겟: {target}
        
        출력 형식:
        '### 🔵 미래아이엔씨 전용 [{platform}] 고효율 카피 제안'으로 시작할 것.
        그 뒤에 각 카피별로 [헤드라인]과 [바디카피]를 구분해서 세련되게 작성해줘.
        """
        
        with st.spinner(f'{platform} 알고리즘에 맞춘 카피를 도출 중...'):
            response = model.generate_content(prompt)
            st.balloons() # 성공 축하 풍선!
            st.markdown(f'<div class="result-box" style="white-space: pre-wrap;">{response.text}</div>', unsafe_allow_html=True)
            st.caption(f"Mirae I&C {platform} Strategy Applied")
    except Exception as e:
        st.error(f"오류 발생: {e}")
