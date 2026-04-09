# -*- coding: utf-8 -*-
import streamlit as st
import google.generativeai as genai
import base64

# 1. 페이지 설정 (탭 이름과 아이콘)
st.set_page_config(page_title="미래아이엔씨 카피 치트키", page_icon="🔵", layout="centered")

# 2. 로고 이미지를 화면에 표시하기 위한 함수 (깃허브에 올린 mirae_logo.png 활용)
def get_image_base64(path):
    with open(path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
    return encoded_string

# 3. 초심플 회사 맞춤형 디자인 (CSS)
st.markdown("""
    <style>
    /* 배경색: 완전 흰색으로 깔끔하게 */
    .stApp {
        background-color: #FFFFFF;
    }
    
    /* 로고 중앙 정렬 */
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
        font-size: 2rem;
        font-weight: 800;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    
    .sub-title {
        color: #666666; /* 그레이 */
        font-size: 1.1rem;
        text-align: center;
        margin-bottom: 2.5rem;
        font-weight: 400;
    }

    /* 입력창 라벨 스타일: 더 얇고 깔끔하게 */
    .stTextInput label, .stTextArea label {
        color: #333333 !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
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
    
    /* 사이드바 스타일링: 더 튀지 않게 */
    [data-testid="stSidebar"] {
        background-color: #FFFFFF;
        border-right: 1px solid #F1F5F9;
    }
    </style>
    """, unsafe_allow_html=True)

# 4. 사이드바 (Secrets 연동) - 여기는 최소한의 정보만 표시
with st.sidebar:
    st.markdown(f'<h3 style="color:#0033FF; text-align:center;">MIRAE I&C</h3>', unsafe_allow_html=True)
    st.write("---")
    try:
        api_key = st.secrets["GEMINI_API_KEY"]
        st.success("✅ AI 엔진 준비 완료")
    except:
        api_key = None
        st.warning("⚠️ Secrets 설정 필요")
    
    st.info("회사 전용 카피라이팅 솔루션입니다.")

# 5. 메인 화면 구성 - 로고 삽입
try:
    # 깃허브에 올린 mirae_logo.png 파일을 불러와서 표시
    image_base64 = get_image_base64("mirae_logo.png")
    st.markdown(f'<div class="logo-container"><img src="data:image/png;base64,{image_base64}"></div>', unsafe_allow_html=True)
except Exception as e:
    # 로고 파일이 없으면 그냥 텍스트로 표시
    st.markdown('<div class="main-title">MIRAE I&C</div>', unsafe_allow_html=True)

st.markdown('<div class="main-title">AI 카피라이팅 솔루션</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">"미래아이엔씨의 전문성을 담아, 고효율 카피를 단 3초 만에"</div>', unsafe_allow_html=True)

# 6. 입력창 (2열 배치) - 깔끔하게
col1, col2 = st.columns(2)
with col1:
    product = st.text_input("📦 제품명 (Product)", placeholder="예: 꽈배기")
with col2:
    keywords = st.text_input("✨ 핵심 키워드 (Keywords)", placeholder="예: 개별포장, 쫄깃함")

target = st.text_input("👥 타겟 고객 (Target Audience)", placeholder="예: 30대 바쁜 직장인")

st.write("") # 간격 조절

# 7. 생성 로직
if st.button("🚀 회사 전용 AI 카피 생성"):
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
