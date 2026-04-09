# -*- coding: utf-8 -*-
import streamlit as st
import google.generativeai as genai
import base64

# 1. 페이지 설정 (탭 이름과 아이콘)
st.set_page_config(page_title="미래아이엔씨 AI 카피 치트키", page_icon="🔵", layout="centered")

# 2. 로고 이미지를 가져오기 위한 함수
def get_image_base64(path):
    with open(path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
    return encoded_string

# 3. 과장님의 맞춤형 초심플 화이트 디자인 (최종 CSS)
st.markdown("""
    <style>
    /* 배경색: 완전 흰색으로 깔끔하게 */
    .stApp {
        background-color: #FFFFFF;
    }
    
    /* 로고 중앙 정렬 및 크기 조절 */
    .logo-container {
        display: flex;
        justify-content: center;
        margin-bottom: 2rem;
    }
    .logo-container img {
        max-width: 250px; /* 로고 크기 조절 */
    }

    /* 타이틀 및 서브 타이틀: 회사 폰트 느낌 반영 */
    .main-title {
        color: #333333; /* 블랙 */
        font-size: 1.8rem;
        font-weight: 800;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    
    .sub-title {
        color: #666666; /* 그레이 */
        font-size: 1rem;
        text-align: center;
        margin-bottom: 2.5rem;
        font-weight: 400;
        line-height: 1.5;
    }

    /* 입력창 라벨 스타일: 더 얇고 깔끔하게 */
    .stTextInput label, .stTextArea label {
        color: #333333 !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
    }
    
    /* 입력창 테두리색: 더 옅게 */
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        border-color: #E2E8F0 !important;
        border-radius: 8px !important;
    }

    /* 생성 버튼: 미래아이엔씨 블루, 더 얇고 세련되게 */
    .stButton>button {
        width: 100%;
        background-color: #0033FF !important; /* 미래 블루 */
        color: white !important;
        border-radius: 8px !important;
        font-weight: bold !important;
        height: 3em !important;
        border: none !important;
        transition: all 0.2s ease;
    }
    
    .stButton>button:hover {
        background-color: #0022AA !important;
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(0,51,255,0.2);
    }

    /* 결과 박스: 그냥 일반적인 깔끔한 마감 */
    .result-box {
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 1.5rem;
        background-color: #F8FAFC; /* 아주 연한 회색 배경 */
        line-height: 1.7;
        color: #333333;
    }
    
    /* 사이드바 스타일링: 과장님 요청 (흰색 배경 + 검정 글씨) */
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
    </style>
    """, unsafe_allow_html=True)

# 4. 사이드바 (Secrets 연동 및 워딩 수정)
with st.sidebar:
    # 깃허브에 올린 mirae_logo.png 파일을 불러와서 사이드바 하단에도 은은하게 표시
    try:
        image_base64 = get_image_base64("mirae_logo.png")
        st.markdown(f'<div class="logo-container" style="margin-bottom:1rem;"><img src="data:image/png;base64,{image_base64}" style="max-width:180px;"></div>', unsafe_allow_html=True)
    except: pass
    
    st.write("---")
    st.markdown(f'<h3 style="color:#0033FF; text-align:center;">MIRAE I&C</h3>', unsafe_allow_html=True)
    st.markdown(f'<p style="text-align:center;">AI 카피라이팅 엔진 v1.0</p>', unsafe_allow_html=True)
    
    st.write("---")
    try:
        api_key = st.secrets["GEMINI_API_KEY"]
        st.success("✅ 회사 전용 AI 엔진 가동 중")
    except:
        api_key = None
        st.warning("⚠️ Secrets 설정 필요")
    
    # 워딩 수정: '최성규 과장' 실명 삽입!
    st.info("최성규 과장이 개발한 고효율 카피 자동 생성기입니다.")

# 5. 메인 화면 구성 - 로고 삽입
try:
    # 깃허브에 올린 mirae_logo.png 파일을 중앙에 표시
    image_base64 = get_image_base64("mirae_logo.png")
    st.markdown(f'<div class="logo-container"><img src="data:image/png;base64,{image_base64}"></div>', unsafe_allow_html=True)
except Exception as e:
    # 로고 파일이 없으면 그냥 텍스트로 표시
    st.markdown('<div class="main-title">MIRAE I&C</div>', unsafe_allow_html=True)

st.markdown('<div class="main-title">🔥 최성규 과장의 야심작, 카피계의 치트키</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">"아직도 광고 카피 직접 짜세요?<br>그 시간, 저희가 벌어다 드립니다."</div>', unsafe_allow_html=True)

# 6. 네이버 상품 번호 입력 칸 삭제 (주석 처리)
# st.write("---")
# st.markdown(f'<p style="color:#333333; font-weight:600;">🛒 네이버 상품 번호로 자동 입력하기</p>', unsafe_allow_html=True)
# naver_id = st.number_input("", value=0, step=1, label_visibility="collapsed")
# st.markdown(f'<p class="tip-caption">상품 번호를 입력하면 제품명·키워드를 자동으로 불러옵니다.</p>', unsafe_allow_html=True)
# if st.button("🔍 자동 입력", disabled=True):
#     pass
# st.write("---") 

# 7. 제품 정보 입력 섹션 (2열 배치) - 깔끔하게
with st.container():
    st.markdown(f'<p style="color:#333333; font-weight:600; font-size: 1rem; margin-bottom:1rem;">📝 제품 정보 입력</p>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        product = st.text_input("📦 제품명 (Product)", placeholder="예: 꽈배기")
    with col2:
        keywords = st.text_input("✨ 핵심 키워드 (Keywords)", placeholder="예: 개별포장, 쫄깃함")

target = st.text_input("👥 타겟 고객 (Target Audience)", placeholder="예: 30대 바쁜 직장인")

st.write("") # 간격 조절

# 8. 생성 로직
if st.button("🚀 회사 전용 AI 카피 생성 시작"):
    if not api_key:
        st.error("API 키가 설정되지 않았습니다. 관리자에게 문의하세요.")
    else:
        try:
            genai.configure(api_key=api_key)
            
            # 모델 자동 선택 (gemini-1.5-flash)
            model_name = 'gemini-1.5-flash'
            try:
                for m in genai.list_models():
                    if 'generateContent' in m.supported_generation_methods:
                        model_name = m.name
                        break
            except: pass
            
            model = genai.GenerativeModel(model_name)
            
            # 미래아이엔씨 스타일의 전문적인 프롬프트
            prompt = f"""
            너는 대한민국 최고의 퍼포먼스 마케팅 대행사인 '미래아이엔씨'의 수석 카피라이터야.
            아래 정보를 바탕으로 클릭률(CTR)이 폭발하는 광고 카피 5개를 작성해줘.
            
            제품명: {product}
            핵심 키워드: {keywords}
            타겟: {target}
            
            조건:
            1. 타겟의 페인 포인트(Pain Point)를 정확히 찌를 것.
            2. 미래아이엔씨만의 전문성이 느껴지는 세련된 문
