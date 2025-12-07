# app.py

import streamlit as st
from PIL import Image

from clip_module import predict_food
from intent_module import predict_intent
from Query import run_query
from response_module import build_response
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
input_type = (
    "text" if (has_text and not has_image)
    else "image+text" if (has_image and has_text)
    else "image"
)


# =============================================
# 1) intent & allergen extraction (텍스트 기반)
# =============================================
intent = predict_intent(user_text) if has_text else "check_food_name"
user_allergens = extract_allergens_from_text(user_text) if has_text else []


# =============================================
# 2) FOOD detection
# =============================================
food_detected = None

# text only → 텍스트에서 음식명 추출
if input_type == "text":
    food_detected = extract_food_from_text(user_text)

# 이미지 포함 → CLIP 우선, 실패 시 텍스트 보조
if input_type != "text" and has_image:
    image = Image.open(uploaded_img).convert("RGB")
    st.image(image, caption="Uploaded Image", use_column_width=True)

    st.write("🔍 Detecting food using CLIP…")
    food_detected = predict_food(image, food_labels)

    if not food_detected and has_text:
        st.write("🔄 CLIP detection failed, trying to parse food from text…")
        food_detected = extract_food_from_text(user_text)

if not food_detected:
    st.error("⚠ Unable to detect food. Please specify it in text or upload a valid image.")
    st.stop()

st.success(f"Detected Food: **{food_detected}**")

if user_allergens:
    st.write(f"Detected allergens: {', '.join(user_allergens)}")


# =============================================
# 3) intent guard
# =============================================
# 텍스트-only에서만 토핑 기능 허용
if input_type != "text" and "topping" in intent:
    intent = "unknown"

st.write(f"Intent detected: **{intent}**")


# =============================================
# 4) query execution
# =============================================
result = run_query(
    intent=intent,
    food=food_detected,
    allergens=user_allergens,
    input_type=input_type,
)


# =============================================
# 5) build response
# =============================================
response_text = build_response(
    intent=intent,
    food=food_detected,
    result=result,
    input_type=input_type,
)


# =============================================
# 6) output
# =============================================
st.subheader("🧾 Analysis Result")
st.write(response_text)
