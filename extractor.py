# extractor.py

from config import food_labels, allergens_labels


def extract_food_from_text(text: str):
    """
    텍스트에서 음식명을 추출한다.
    단순 부분 문자열 매칭 방식.
    """
    text = text.lower()
    for food in food_labels:
        if food.lower() in text:
            return food
    return None


def extract_allergens_from_text(text: str):
    """
    텍스트에서 알레르겐을 찾는다.
    복수 개일 수도 있으므로 리스트로 반환.
    """
    text = text.lower()
    found = []

    for allergen in allergens_labels:
        if allergen.lower() in text:
            found.append(allergen)

    return list(set(found))  # 중복 제거

