# -*- coding: utf-8 -*-
import streamlit as st
import google.generativeai as genai

# 1. 페이지 설정
st.set_page_config(page_title="바이브코딩", page_icon="🔥", layout="centered")

# 2. 디자인 (CSS)
st.markdown("""
    <style>
    .stApp { background-color: #FFFFFF; }
    .main-title { color: #FF4B4B; font-size: 2.2rem; font-weight: bold; text-align: center; }
    .main-quote { color: #1E293B; font-size: 1.3rem; text-align: center; margin-bottom: 2rem; }
    .black-box { background-color: #1E1E2F; color: #FFFFFF; padding: 2rem; border-radius: 12px; text-align: center; margin-bottom: 2.5rem; }
    .result-box { border: 2px dashed #CBD5E1; border-radius: 10px; padding: 2rem; background-color: #F8FAFC; }
    .stButton>button { width: 100%; background-color: #1E3A8A; color: white; border-radius: 8px; font-weight: bold; height: 3.2em; }
    </style>
    """, unsafe_allow_html=True)

# 3. 사이드바
with st.sidebar:
    st.header("🔑 구글 AI 설정")
    try:
        # 클라우드 배포 시 Secrets에서 키를 가져옴
        api_key = st.secrets["GEMINI_API_KEY"]
        st.success("✅ AI 엔진이 준비되었습니다.")
    except:
        # 로컬 테스트 시 혹은 키 설정 전 안내
        api_key = None
        st.warning("⚠️ API 키 설정이 필요합니다 (Secrets)")
    
    st.info("미래아이엔씨 전용 모드로 작동 중입니다. 제품 정보만 입력 후 생성 버튼을 눌러주세요.")

# 4. 메인 화면
st.markdown('<div class="main-title">🔥 최성규 과장의 야심작, 카피계의 \'치트키\'</div>', unsafe_allow_html=True)
st.markdown('<div class="main-quote">"아직도 광고 카피 직접 짜세요?<br><span style="color:#FF4B4B; font-weight:bold;">그 시간, 제가 직접 다 드릴게요."</span></div>', unsafe_allow_html=True)

st.markdown("""
<div class="black-box">
    <div style="color: #FF4B4B; font-weight: bold; margin-bottom: 0.8rem;">밤새 고민해도 안 나오던 CTR 대폭발 카피, 단 3초 만에 끝내세요.</div>
    <div style="font-size: 1.25rem;">상위 0.1% 퍼포먼스 마케터의 AI 엔진이 당신의 카피를 180도 바꿉니다.</div>
</div>
""", unsafe_allow_html=True)

# 5. 입력창
col1, col2 = st.columns(2)
with col1: product = st.text_input("📦 제품명", value="꽈배기")
with col2: keywords = st.text_input("✨ 키워드", value="개별포장, 달달한")
target = st.text_input("👥 타겟 고객", value="사무직 직장인")

# 6. 생성 로직 (에러 우회 버전)
if st.button("🚀 광고 카피 생성하기"):
    if not api_key:
        st.error("사이드바에 API 키를 넣어주세요!")
    else:
        try:
            genai.configure(api_key=api_key)
            
            # [핵심] 사용 가능한 모델 중 하나를 자동으로 선택합니다.
            model_name = 'gemini-1.5-flash' # 기본값
            try:
                for m in genai.list_models():
                    if 'generateContent' in m.supported_generation_methods:
                        model_name = m.name
                        break
            except:
                pass # 리스트를 못 불러오면 기본값 사용
            
            model = genai.GenerativeModel(model_name)
            prompt = f"너는 대한민국 상위 0.1% 마케터야. {product}(특징: {keywords})를 {target}에게 팔기 위한 고효율 광고 카피 5개를 이모지를 섞어서 매력적으로 써줘."
            
            with st.spinner('상위 0.1% 마케터의 뇌 가동 중...'):
                response = model.generate_content(prompt)
                st.success("카피 생성 완료!")
                st.markdown(f'<div class="result-box" style="color:#1E293B; white-space: pre-wrap;">{response.text}</div>', unsafe_allow_html=True)
        except Exception as e:
            st.error(f"오류가 발생했습니다: {e}\n\n사이드바의 API 키가 정확한지 확인해 주세요!")
else:
    st.markdown('<div class="result-box" style="text-align:center; color:#888;">이곳에 AI가 생성한 카피가 표시됩니다.</div>', unsafe_allow_html=True)