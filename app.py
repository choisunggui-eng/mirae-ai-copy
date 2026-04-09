# -*- coding: utf-8 -*-
import streamlit as st
import google.generativeai as genai
import base64

# 1. 페이지 설정
st.set_page_config(page_title="미래아이엔씨 AI 카피 치트키", page_icon="🔵", layout="centered")

# 2. 로고 이미지를 가져오기 위한 함수
def get_image_base64(path):
    with open(path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
    return encoded_string

# 3. 과장님의 야심작 디자인 + 미래아이엔씨 로고 (최종 CSS)
st.markdown("""
    <style>
    /* 배경색: 깔끔한 흰색 */
    .stApp {
        background-color: #FFFFFF;
    }
    
    /* 로고 중앙 정렬 및 크기 조절 */
    .logo-container {
        display: flex;
        justify-content: center;
        margin-top: 1rem;
        margin-bottom: 2rem;
    }
    .logo-container img {
        max-width: 250px;
    }

    /* 사이드바 스타일링: 다크 네이비로 시크하게 */
    [data-testid="stSidebar"] {
        background-color: #1E1E2F !important;
        color: #FFFFFF !important;
        border-right: 1px solid #111111;
    }
    [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3, [data-testid="stSidebar"] label, [data-testid="stSidebar"] p {
        color: #FFFFFF !important;
    }
    [data-testid="stSidebar"] .stTextInput>div>div>input {
        background-color: rgba(255, 255, 255, 0.1);
        color: #FFFFFF;
        border-color: rgba(255, 255, 255, 0.2) !important;
    }

    /* 메인 타이틀: 과장님 특유의 위트 살리기 */
    .main-title-container {
        text-align: center;
        margin-bottom: 2rem;
    }
    .main-title {
        color: #333333;
        font-size: 1.8rem;
        font-weight: 800;
        margin-bottom: 0.5rem;
    }
    .main-title span {
        color: #0033FF; /* 미래 블루 */
    }
    .sub-title {
        color: #666666;
        font-size: 1.1rem;
        font-weight: 400;
        line-height: 1.5;
    }

    /* 강조 박스: 신뢰감 있는 다크 네이비 그라데이션 */
    .black-box {
        background: linear-gradient(135deg, #1E1E2F 0%, #0033FF 100%);
        color: #FFFFFF;
        padding: 2rem;
        border-radius: 12px;
        text-align: center;
        margin-bottom: 2.5rem;
        box-shadow: 0 10px 20px rgba(0,51,255,0.2);
    }
    .black-box-title {
        color: #FFD700;
        font-weight: bold;
        font-size: 1.2rem;
        margin-bottom: 0.5rem;
    }
    .black-box-content {
        font-size: 1.1rem;
        font-weight: 500;
        line-height: 1.6;
    }

    /* 입력창 라벨 스타일: 더 얇고 깔끔하게 */
    .stTextInput label {
        color: #333333 !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
    }
    
    /* 입력창 테두리색: 더 옅게 */
    .stTextInput>div>div>input {
        border-color: #E2E8F0 !important;
        border-radius: 6px !important;
    }

    /* 네이버 상품 번호 입력창 스타일 */
    .stNumberInput div div input {
        border-radius: 6px !important;
        border-color: #E2E8F0 !important;
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

    /* 결과 박스: 그냥 일반적인 깔끔한 마감 */
    .result-box {
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 1.5rem;
        background-color: #F8FAFC; /* 아주 연한 회색 배경 */
        line-height: 1.7;
        color: #333333;
    }
    
    /* 팁 캡션 스타일 */
    [data-testid="stMarkdownContainer"] .tip-caption {
        color: #888888;
        font-size: 0.85rem;
        margin-top: 0.3rem;
    }
    </style>
    """, unsafe_allow_html=True)

# 4. 사이드바 - 설정 최소화 (API 키는 Secrets로 이미 해결됨)
with st.sidebar:
    # 깃허브에 올린 mirae_logo.png 파일을 불러와서 사이드바 하단에도 은은하게 표시
    try:
        image_base64 = get_image_base64("mirae_logo.png")
        st.markdown(f'<div class="logo-container"><img src="data:image/png;base64,{image_base64}" style="max-width:180px;"></div>', unsafe_allow_html=True)
    except: pass
    
    st.write("---")
    st.markdown(f'<h2 style="color:#FFFFFF; text-align:center;">MIRAE I&C</h2>', unsafe_allow_html=True)
    st.markdown(f'<p style="text-align:center;">AI 카피라이팅 엔진 v1.0</p>', unsafe_allow_html=True)
    
    st.write("---")
    try:
        api_key = st.secrets["GEMINI_API_KEY"]
        st.success("✅ 회사 전용 AI 엔진 가동 중")
    except:
        api_key = None
        st.warning("⚠️ Secrets 키 설정 필요")
    
    st.info("과장님이 개발한 고효율 카피 자동 생성기입니다.")

# 5. 메인 화면 구성 - 로고 삽입
try:
    # 깃허브에 올린 mirae_logo.png 파일을 중앙에 표시
    image_base64 = get_image_base64("mirae_logo.png")
    st.markdown(f'<div class="logo-container"><img src="data:image/png;base64,{image_base64}"></div>', unsafe_allow_html=True)
except: pass

st.markdown("""
<div class="main-title-container">
    <div class="main-title">🔥 최성규 과장의 야심작, 카피계의 '치트키'</div>
    <div class="sub-title">"아직도 광고 카피 직접 짜세요?<br>그 시간, 저희가 벌어다 드립니다."</div>
</div>
""", unsafe_allow_html=True)

# 6. 강조 박스
st.markdown("""
<div class="black-box">
    <div class="black-box-title">밤새 고민해도 안 나오던 CTR 대폭발 카피, 단 3초 만에 끝내세요.</div>
    <div class="black-box-content">상위 0.1% 퍼포먼스 마케터의 데이터가 녹아든 AI 엔진이 당신의 카피를 180도 바꿉니다.</div>
</div>
""", unsafe_allow_html=True)

# 7. 네이버 상품 번호 입력 섹션
with st.container():
    col_n, col_b = st.columns([3, 1])
    with col_n:
        st.markdown(f'<p style="color:#333333; font-weight:600;">🛒 네이버 상품 번호로 자동 입력하기</p>', unsafe_allow_html=True)
        # number_input은 정수만 받도록 설정
        naver_id = st.number_input("", value=0, step=1, label_visibility="collapsed")
        st.markdown(f'<p class="tip-caption">상품 번호를 입력하면 제품명·키워드를 자동으로 불러옵니다.</p>', unsafe_allow_html=True)
    with col_b:
        st.write("") # 간격 조절
        if st.button("🔍 자동 입력", disabled=True):
            pass # 나중에 기능 추가 가능 (현재는 버튼만 표시)

st.write("---") # 구분선

# 8. 제품 정보 입력 섹션 (2열 배치)
with st.container():
    st.markdown(f'<p style="color:#333333; font-weight:600; font-size: 1.1rem; margin-bottom:1rem;">📝 제품 정보 입력</p>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        product = st.text_input("📦 제품명 (Product)", placeholder="예: 꽈배기")
    with col2:
        keywords = st.text_input("✨ 핵심 키워드 (Keywords)", placeholder="예: 개별포장, 쫄깃함")

target = st.text_input("👥 타겟 고객 (Target Audience)", placeholder="예: 30대 바쁜 직장인")

st.write("") # 간격 조절

# 9. 생성 로직
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
            2. 미래아이엔씨만의 전문성이 느껴지는 세련된 문체.
            3. 적절한 이모지를 사용하여 가독성을 높일 것.
            4. 각 카피는 제목과 본문 느낌으로 구분해서 써줘.
            """
            
            with st.spinner('AI가 고효율 카피를 도출하고 있습니다...'):
                response = model.generate_content(prompt)
                st.balloons() # 성공 축하 풍선!
                st.markdown(f'<div class="result-box" style="white-space: pre-wrap;">{response.text}</div>', unsafe_allow_html=True)
                st.caption("Produced by Mirae I&C Marketing Solution")
        except Exception as e:
            st.error(f"오류 발생: {e}")
