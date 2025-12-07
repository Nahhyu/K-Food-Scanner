# app.py

import streamlit as st
from PIL import Image

from clip_module import predict_food
from intent_module import predict_intent
from Query_module import run_query
from Response_module import build_response
from extractor import extract_food_from_text, extract_allergens_from_text

from config import food_labels


# ===============================
# Streamlit Layout
# ===============================
st.set_page_config(page_title="K-Food Scanner", layout="centered")
st.title("🍱 K-Food Scanner")

st.subheader("📝 Input Section")

uploaded_img = st.file_uploader("Upload a food image (optional)", type=["jpg", "jpeg", "png"])
user_text = st.text_input("Enter your question or description (optional)")


# Input flags
has_image = uploaded_img is not None
has_text = bool(user_text.strip())


# Both empty?
if not has_image and not has_text:
    st.info("Please upload an image or type your question to begin.")
    st.stop()


# =============================================
# determine mode
# =============================================
# 🔥 핵심 규칙: 이미지가 하나라도 있으면 → 무조건 image mode
input_type = "image" if has_image else "text"



# =============================================
# 1) FOOD detection
# =============================================
food_detected = None

# 텍스트에서 food 찾기 (텍스트 있어도 이미지 모드는 유지됨)
if has_text:
    food_detected = extract_food_from_text(user_text)

# 텍스트에서 못 찾고 이미지가 있는 경우 → CLIP
if not food_detected and has_image:
    image = Image.open(uploaded_img).convert("RGB")
    st.image(image, caption="Uploaded Image", use_column_width=True)

    st.write("🔍 Detecting food using CLIP…")
    food_detected = predict_food(image, food_labels)

if not food_detected:
    st.error("⚠ Unable to detect food. Please specify it in text or upload a valid image.")
    st.stop()

st.success(f"Detected Food: **{food_detected}**")



# =============================================
# 2) allergen extraction (텍스트일 때만)
# =============================================
user_allergens = extract_allergens_from_text(user_text) if has_text else []
if user_allergens:
    st.write(f"Detected allergens: {', '.join(user_allergens)}")



# =============================================
# 3) intent classification
# =============================================
if has_text:
    intent = predict_intent(user_text)
else:
    intent = "check_food_name"

# 🔥 topping intent 차단 규칙: 이미지가 있으면 무조건 금지
if has_image and "topping" in intent:
    intent = "unknown"

st.write(f"Intent detected: **{intent}**")



# =============================================
# 4) query execution
# =============================================
result = run_query(
    intent=intent,
    food=food_detected,
    allergens=user_allergens,
    input_type=input_type    # 🔥 이미지 있으면 토핑 자동 비활성
)



# =============================================
# 5) build response
# =============================================
response_text = build_response(
    intent=intent,
    food=food_detected,
    result=result,
    input_type=input_type
)



# =============================================
# 6) output
# =============================================
st.subheader("🧾 Analysis Result")
st.write(response_text)
