# intent_module.py

import re
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from intent_list import intent_templates


# =========================================
# 1) 전처리 함수
# =========================================
def preprocess(text: str) -> str:
    """
    유저 입력을 TF-IDF에 맞게 클린한 형태로 변환.
    """
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)  # 문장부호 제거
    text = re.sub(r"\s+", " ", text).strip()
    return text


# =========================================
# 2) 템플릿 flatten + 벡터화 준비
# =========================================
template_sentences = []
template_intents = []

for intent, sentences in intent_templates.items():
    for s in sentences:
        clean_s = preprocess(s)
        template_sentences.append(clean_s)
        template_intents.append(intent)

# TF-IDF 모델 생성
vectorizer = TfidfVectorizer()
template_vectors = vectorizer.fit_transform(template_sentences)


# =========================================
# 3) intent keyword bias 사전
# =========================================
keyword_bias = {
    "check_allergy": ["allergy", "allergen", "allergic", "dangerous"],
    "check_edibility": ["eat", "safe", "allergy", "trigger", "can i"],
    "check_food_name": ["name", "called", "identify", "what is"],
    "check_ingredients": ["ingredient", "made", "contain", "components"],
    "check_topping": ["topping", "add", "extra", "option"]  # 토핑 intent 추가 가능
}


def compute_keyword_boost(user_text: str, intent: str) -> float:
    """
    유저 입력 안에 intent 관련 키워드가 포함되면 가중치를 줘서
    TF-IDF 유사도를 강화한다.
    """
    score = 0.0
    for kw in keyword_bias.get(intent, []):
        if kw in user_text:
            score += 0.05
    return score


# =========================================
# 4) 최종 intent 예측 함수
# =========================================
def predict_intent(user_input: str, threshold: float = 0.25):
    """
    1) 유저 입력 전처리
    2) TF-IDF 유사도 계산
    3) intent keyword bias 보정
    4) 가장 높은 intent 반환
    """
    clean_text = preprocess(user_input)
    user_vec = vectorizer.transform([clean_text])

    # 1) 템플릿 전체와 cosine similarity 계산
    sims = cosine_similarity(user_vec, template_vectors)[0]

    # 2) keyword bias 적용
    adjusted_scores = []
    for sim, intent in zip(sims, template_intents):
        boost = compute_keyword_boost(clean_text, intent)
        adjusted_scores.append(sim + boost)

    # 3) 최고 점수 intent 선택
    best_idx = np.argmax(adjusted_scores)
    best_score = adjusted_scores[best_idx]
    best_intent = template_intents[best_idx]

    # 4) threshold 미달 → unknown intent
    if best_score < threshold:
        return "unknown"

    return best_intent
