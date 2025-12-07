import torch
from PIL import Image
from transformers import CLIPProcessor, CLIPModel
import streamlit as st

# 🔥 config 값 불러오기
from config import (
    MODEL_PATH,
    DEVICE,
    NORMALIZE_EMBEDDINGS,
)


# ============================================
# 1) Fine-tuned CLIP 모델 로드 (Streamlit 캐시)
# ============================================

@st.cache_resource
def load_clip_model():
    """
    Fine-tuned(LoRA merge) CLIP 모델을 로드해서 반환한다.
    Streamlit 캐시로 한 번만 로드됨.
    """
    model = CLIPModel.from_pretrained(MODEL_PATH)
    processor = CLIPProcessor.from_pretrained(MODEL_PATH)
    model.to(DEVICE)
    model.eval()
    return processor, model


processor, model = load_clip_model()


# ============================================
# 2) 이미지 → 음식 라벨 예측 함수
# ============================================

def predict_food(image: Image.Image, candidate_foods: list[str]) -> str:
    """
    Fine-tuned CLIP을 이용해 이미지와 가장 유사한 음식 레이블을 선택한다.
    - image: PIL Image
    - candidate_foods: ["kimbap", "bibimbap", "tteokbokki", ...]
    """

    if not candidate_foods:
        raise ValueError("Food 후보 레이블이 비어 있습니다.")

    # ------ 1. 이미지 임베딩 ------
    image_inputs = processor(images=image, return_tensors="pt").to(DEVICE)

    with torch.no_grad():
        image_features = model.get_image_features(**image_inputs)

    # 정규화 ON/OFF는 config에서 설정
    if NORMALIZE_EMBEDDINGS:
        image_features = image_features / image_features.norm(dim=-1, keepdim=True)

    # ------ 2. 텍스트 임베딩 ------
    text_inputs = processor(
        text=candidate_foods,
        return_tensors="pt",
        padding=True
    ).to(DEVICE)

    with torch.no_grad():
        text_features = model.get_text_features(**text_inputs)

    if NORMALIZE_EMBEDDINGS:
        text_features = text_features / text_features.norm(dim=-1, keepdim=True)

    # ------ 3. 코사인 유사도 계산 ------
    similarities = image_features @ text_features.T  # shape: (1, N)
    pred_idx = similarities.argmax(dim=-1).item()

    return candidate_foods[pred_idx]
