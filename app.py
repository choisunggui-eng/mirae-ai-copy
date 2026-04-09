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

# 3. 과장님의 맞춤형 초심플 화이트 디자인 (CSS)
st.markdown("""
    <style>
    .stApp { background-color: #FFFFFF; }
    .logo-container { display: flex; justify-content: center; margin-bottom: 2rem; }
    .logo-container img { max-width: 250px; }
    .main-title { color: #333333; font-size: 1.8rem; font-weight: 800; text-align: center; margin-bottom: 0.5rem; }
    .sub-title { color: #666666; font-size: 1rem; text-align: center; margin-bottom: 2.5rem; font-weight: 400; line-height: 1.5; }
    .stTextInput label, .stTextArea label { color: #333333 !important; font-weight: 600 !important; font-size: 0.95rem !important; }
    .stTextInput>div>div>input, .stTextArea>div>div>textarea { border-color: #E2E8F0 !important; border-radius: 8px !important; }
    .stButton>button { width: 100%; background-color: #0033FF !important; color: white !important; border-radius: 8px !important; font-weight: bold !important; height: 3em !important; border: none !important; transition: all 0.2s ease; }
    .stButton>button:hover { background-color: #0022AA !important; transform: translateY(-1px); box-shadow: 0 4px 12px rgba(0,51,255,0.2); }
    .result-box { border: 1px solid #E2E8F0; border-radius: 8px; padding: 1.5rem; background-color: #F8FAFC; line-height: 1.7; color: #333333; }
    [data-testid="stSidebar"] { background-color: #FFFFFF; border-right: 1px solid #F1F5F9; }
    [data-testid="stSidebar"] h3, [data-testid="stSidebar"] p { color: #333333 !important; font-weight: 500 !important; }
    </style>
    """, unsafe_allow_html=True)

# 4. 사이드바 구성
with st.sidebar:
    try:
        image_base64 = get_image_base64("mirae_logo.png")
        st.markdown(f'<div class="logo-container" style="margin-bottom:1rem;"><img src="data:image/png;base64,{image_base64}" style="max-width:180px;"></div>', unsafe_allow_html=True)
    except: pass
    st.write("---")
    st.markdown(f'<h3 style="color:#0033FF; text-align:center;">MIRAE I&C</h3>', unsafe_allow_html=True)
    st.write("---")
    try:
        api_key = st.secrets["GEMINI_API_KEY"]
        st.success("✅ AI 엔진 준비 완료")
    except:
        api_key = None
        st.warning("⚠️ API 키 설정 필요")
    st.info("최성규 과장이 개발한 고효율 카피 자동 생성기입니다.")

# 5. 메인 화면 구성
try:
    image_base64 = get_image_base64("mirae_logo.png")
    st.markdown(f'<div class="logo-container"><img src="data:image/png;base64,{image_base64}"></div>', unsafe_allow_html=True)
except:
    st.markdown('<div class="main-title">MIRAE I&C</div>', unsafe_allow_html=True)

st.markdown('<div class="main-title">🔥 최성규 과장의 야심작, 카피계의 치트키</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">"아직도 광고 카피 직접 짜세요?<br>그 시간, 저희가 벌어다 드립니다."</div>', unsafe_allow_html=True)

# 6. 제품 정보 입력
st.markdown(f'<p style="color:#333333; font-weight:600; font-size: 1rem; margin-bottom:1rem;">📝 제품 정보 입력</p>', unsafe_allow_html=True)
col1, col2 = st.columns(2)
with col1:
    product = st.text_input("📦 제품명", placeholder="예: 꽈배기")
with col2:
    keywords = st.text_input("✨ 핵심 키워드", placeholder="예: 개별포장, 쫄깃함")
target = st.text_input("👥 타겟 고객", placeholder="예: 30대 바쁜 직장인")

# 7. 생성 로직 (워딩 수정됨)
if st.button("🚀 미래아이엔씨 고효율 카피 생성"):
    if not api_key:
        st.error("API 키가 설정되지 않았습니다.")
    else:
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            # 워딩 수정된 프롬프트
            prompt = f"""
            너는 광고 성과를 극대화하는 '미래아이엔씨'의 퍼포먼스 마케팅 전문가야.
            아래 정보를 바탕으로 클릭률(CTR)이 폭발하는 광고 카피 5개를 작성해줘.
            
            제품명: {product}
            핵심 키워드: {keywords}
            타겟: {target}
            
            출력 형식:
            '### 🔵 미래아이엔씨 전용 고효율 카피 제안'이라는 문구로 시작할 것.
            그 뒤에 각 카피별로 [헤드라인]과 [바디카피]를 구분해서 세련되게 작성해줘.
            """
            
            with st.spinner('AI가 데이터를 분석하여 카피를 추출 중입니다...'):
                response = model.generate_content(prompt)
                st.balloons()
                st.markdown(f'<div class="result-box" style="white-space: pre-wrap;">{response.text}</div>', unsafe_allow_html=True)
                st.caption("Developed by Mirae I&C")
        except Exception as e:
            st.error(f"오류 발생: {e}")
