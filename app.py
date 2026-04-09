# -*- coding: utf-8 -*-
import streamlit as st
import google.generativeai as genai

# 1. 페이지 설정 (탭 이름과 아이콘)
st.set_page_config(page_title="미래아이엔씨 카피 치트키", page_icon="🔵", layout="centered")

# 2. 미래아이엔씨 전용 테마 디자인 (CSS)
st.markdown("""
    <style>
    /* 배경색: 미래아이엔씨의 깔끔한 느낌 */
    .stApp {
        background-color: #F8FAFC;
    }
    
    /* 메인 타이틀: 회사 로고 느낌 반영 */
    .main-title {
        color: #0033FF; /* 미래아이엔씨 블루 */
        font-size: 2.5rem;
        font-weight: 900;
        text-align: center;
        margin-bottom: 0.5rem;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
    }
    
    .sub-title {
        color: #333333;
        font-size: 1.2rem;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: 500;
    }

    /* 강조 박스: 신뢰감 있는 블랙/블루 조합 */
    .black-box {
        background: linear-gradient(135deg, #1E1E2F 0%, #0033FF 100%);
        color: #FFFFFF;
        padding: 2.5rem;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 2.5rem;
        box-shadow: 0 10px 20px rgba(0,51,255,0.2);
    }

    /* 입력창 라벨 스타일 */
    .stTextInput label {
        color: #1E293B !important;
        font-weight: bold !important;
    }

    /* 생성 버튼: 미래아이엔씨 블루 */
    .stButton>button {
        width: 100%;
        background-color: #0033FF !important;
        color: white !important;
        border-radius: 12px !important;
        font-weight: bold !important;
        height: 3.5em !important;
        border: none !important;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        background-color: #0022AA !important;
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,51,255,0.3);
    }

    /* 결과 박스: 깔끔하고 고급스러운 마감 */
    .result-box {
        border: 2px solid #E2E8F0;
        border-radius: 15px;
        padding: 2rem;
        background-color: #FFFFFF;
        box-shadow: inset 0 2px 4px rgba(0,0,0,0.05);
        line-height: 1.8;
    }
    
    /* 사이드바 스타일링 */
    [data-testid="stSidebar"] {
        background-color: #F1F5F9;
        border-right: 1px solid #E2E8F0;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. 사이드바 (Secrets 연동)
with st.sidebar:
    st.markdown(f'<h2 style="color:#0033FF;">MIRAE I&C</h2>', unsafe_allow_html=True)
    st.write("---")
    try:
        api_key = st.secrets["GEMINI_API_KEY"]
        st.success("✅ 회사 전용 AI 엔진 가동 중")
    except:
        api_key = None
        st.warning("⚠️ Secrets에 키를 등록해주세요.")
    
    st.info("미래아이엔씨 마케팅팀 전용 AI 카피라이팅 툴입니다. 제품 정보만 입력하면 고효율 카피가 생성됩니다.")

# 4. 메인 화면 구성
st.markdown('<div class="main-title">MIRAE I&C AI COPY-WRITER</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">"상위 0.1% 퍼포먼스 마케팅의 정수, 미래아이엔씨 AI 엔진"</div>', unsafe_allow_html=True)

st.markdown("""
<div class="black-box">
    <div style="color: #FFD700; font-weight: bold; font-size: 1.1rem; margin-bottom: 0.5rem;">[최성규 과장 특제 마케팅 솔루션]</div>
    <div style="font-size: 1.4rem; font-weight: bold; line-height: 1.4;">불필요한 고민 시간은 줄이고,<br>매출 성과는 극대화합니다.</div>
</div>
""", unsafe_allow_html=True)

# 5. 입력창 (2열 배치)
col1, col2 = st.columns(2)
with col1:
    product = st.text_input("📦 제품명 (Product)", placeholder="예: 꽈배기")
with col2:
    keywords = st.text_input("✨ 핵심 키워드 (Keywords)", placeholder="예: 개별포장, 쫄깃함")

target = st.text_input("👥 타겟 고객 (Target Audience)", placeholder="예: 30대 바쁜 직장인")

st.write("") # 간격 조절

# 6. 생성 로직
if st.button("🚀 미래아이엔씨 AI 카피 생성 시작"):
    if not api_key:
        st.error("API 키가 설정되지 않았습니다. 관리자에게 문의하세요.")
    else:
        try:
            genai.configure(api_key=api_key)
            
            # 모델 자동 선택
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
            
            with st.spinner('미래아이엔씨 AI가 최적의 카피를 도출하고 있습니다...'):
                response = model.generate_content(prompt)
                st.balloons() # 성공 축하 풍선!
                st.markdown(f'<div class="result-box" style="white-space: pre-wrap;">{response.text}</div>', unsafe_allow_html=True)
                st.caption("Produced by Mirae I&C Marketing Solution V2.0")
        except Exception as e:
            st.error(f"오류 발생: {e}")
