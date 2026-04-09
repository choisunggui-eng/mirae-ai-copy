# -*- coding: utf-8 -*-
import streamlit as st
import google.generativeai as genai
import base64

# 1. 페이지 설정
st.set_page_config(page_title="미래아이엔씨 AI 매체 최적화 솔루션", page_icon="🔵", layout="centered")

# 2. 로고 변환 함수
def get_image_base64(path):
    try:
        with open(path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode()
    except: return None

# 3. 디자인 CSS (화이트 테마 + 매체별 포인트)
st.markdown("""
    <style>
    .stApp { background-color: #FFFFFF; }
    .logo-container { display: flex; justify-content: center; margin-bottom: 1rem; }
    .logo-container img { max-width: 200px; height: auto; }
    .main-title { color: #333333; font-size: 1.8rem; font-weight: 800; text-align: center; margin-top: 1rem; }
    .sub-title { color: #666666; font-size: 1rem; text-align: center; margin-bottom: 2rem; }
    .stSelectbox label { font-weight: 700 !important; color: #0033FF !important; }
    .result-box { border: 1px solid #E2E8F0; border-radius: 8px; padding: 1.5rem; background-color: #F8FAFC; line-height: 1.7; }
    [data-testid="stSidebar"] { background-color: #FFFFFF; border-right: 1px solid #F1F5F9; }
    </style>
    """, unsafe_allow_html=True)

# 4. 사이드바 (과장님 워딩 유지)
with st.sidebar:
    mirae_logo = get_image_base64("mirae_logo.png")
    if mirae_logo:
        st.markdown(f'<div class="logo-container"><img src="data:image/png;base64,{mirae_logo}"></div>', unsafe_allow_html=True)
    st.write("---")
    st.info("최성규 과장이 개발한 고효율 카피 자동 생성기입니다.")

# 5. 메인 로고 및 타이틀
st.markdown('<div class="main-title">🔥 최성규 과장의 야심작, 매체별 치트키</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">"매체 특성에 딱 맞춘 상위 0.1%의 전략적 카피"</div>', unsafe_allow_html=True)

# 6. 매체 선택 및 로고 심볼 노출
st.write("---")
platform = st.selectbox("🎯 광고 매체를 선택하세요", ["META", "GFA/DA", "GOOGLE/DA", "CRITEO"])

# 매체별 로고 파일 매칭 (깃허브에 아래 이름으로 올리시면 뜹니다!)
platform_logos = {
    "META": "meta_symbol.png",
    "GFA/DA": "gfa_symbol.png",
    "GOOGLE/DA": "google_symbol.png",
    "CRITEO": "criteo_symbol.png"
}

current_symbol = get_image_base64(platform_logos[platform])
if current_symbol:
    st.markdown(f'<div class="logo-container"><img src="data:image/png;base64,{current_symbol}" style="max-width:80px;"></div>', unsafe_allow_html=True)
else:
    st.write(f"📍 현재 매체: **{platform}**")

# 7. 정보 입력
col1, col2 = st.columns(2)
with col1:
    product = st.text_input("📦 제품명", placeholder="예: 꽈배기")
with col2:
    keywords = st.text_input("✨ 핵심 키워드", placeholder="예: 개별포장, 쫄깃함")
target = st.text_input("👥 타겟 고객", placeholder="예: 30대 바쁜 직장인")

# 8. 매체별 가이드라인 정의
guides = {
    "META": "이미지 중심의 매체이므로 감성적이고 트렌디한 문구, 풍부한 이모지 활용, 해시태그 포함.",
    "GFA/DA": "즉각적인 반응이 필요함. 호기심을 자극하는 강력한 후킹과 페인포인트 강조.",
    "GOOGLE/DA": "명확한 정보 전달 중심. 신뢰감 있는 톤앤매너와 핵심 혜택 중심의 간결한 구성.",
    "CRITEO": "리타겟팅 중심이므로 구매를 망설이는 고객의 등을 떠밀 수 있는 혜택(할인, 리뷰 등) 강조."
}

# 9. 생성 로직
if st.button(f"🚀 {platform} 전용 고효율 카피 생성"):
    try:
        api_key = st.secrets["GEMINI_API_KEY"]
        genai.configure(api_key=api_key)
        
        # 모델 자동 선택
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        target_model = 'models/gemini-1.5-flash' if 'models/gemini-1.5-flash' in available_models else available_models[0]
        model = genai.GenerativeModel(target_model)
        
        prompt = f"""
        너는 미래아이엔씨의 {platform} 전문 퍼포먼스 마케터야.
        매체 가이드라인: {guides[platform]}
        
        위 가이드라인을 엄격히 준수하여 아래 제품에 대한 {platform} 최적화 카피 5개를 작성해줘.
        제품명: {product} / 키워드: {keywords} / 타겟: {target}
        
        출력 형식:
        '### 🔵 미래아이엔씨 전용 [{platform}] 고효율 카피 제안'으로 시작할 것.
        """
        
        with st.spinner(f'{platform} 알고리즘에 맞춘 카피를 도출 중...'):
            response = model.generate_content(prompt)
            st.balloons()
            st.markdown(f'<div class="result-box" style="white-space: pre-wrap;">{response.text}</div>', unsafe_allow_html=True)
            st.caption(f"Mirae I&C {platform} Strategy Applied")
    except Exception as e:
        st.error(f"오류 발생: {e}")
