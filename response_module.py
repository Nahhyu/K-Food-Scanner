# Response_module.py

def build_response(intent: str, food: str, result, input_type="image"):
    """
    intent + 쿼리 결과를 기반으로 자연스러운 영어 문장을 생성한다.
    텍스트 입력일 때만 토핑 관련 정보 포함.
    """

    # ============================
    # 1) 음식 이름 확인
    # ============================
    if intent == "check_food_name":
        return f"This dish appears to be **{food}**."


    # ============================
    # 2) 음식 알레르기 확인 (check_allergy)
    # ============================
    if intent == "check_allergy":
        allergens = result  # list

        if not allergens:
            if input_type == "text":
                return (
                    f"The main dish **{food}** contains no identifiable allergens. "
                    f"Toppings might still include potential allergens depending on customization."
                )
            return f"The dish **{food}** does not contain any known allergens."

        allergens_str = ", ".join(allergens)

        if input_type == "text":
            return (
                f"The main dish **{food}** contains the following allergens: {allergens_str}. "
                f"Keep in mind that toppings may add additional allergens depending on the customization."
            )

        return f"This dish contains the following allergens: {allergens_str}. Please be cautious."


    # ============================
    # 3) 섭취 가능 여부 (check_edibility)
    # ============================
    if intent == "check_edibility":
        edible = result["edible"]
        food_allergens = result["food_allergens"]
        conflict = result["conflict"]

        if edible:
            if input_type == "text":
                return (
                    f"You can safely eat **{food}**. "
                    f"No allergens matching your condition were found in the dish or its possible toppings."
                )
            return f"You can safely eat **{food}**. It does not contain your allergen."

        # 알레르기 충돌 있음
        conflict_str = ", ".join(conflict)
        if input_type == "text":
            return (
                f"You should avoid **{food}**. The dish or its toppings include: {conflict_str}, "
                f"which matches your allergy."
            )

        return f"You should avoid **{food}**. It contains {conflict_str}, which matches your allergy."


    # ============================
    # 4) 음식 재료 조회 (check_ingredients)
    # ============================
    if intent == "check_ingredients":
        ingredients = result.get("ingredients", result)  # 이미지일 경우 list, 텍스트일 경우 dict

        if isinstance(ingredients, list):
            ing_str = ", ".join(ingredients) if ingredients else "No ingredients found."
            if input_type == "text":
                return f"The main dish **{food}** contains: {ing_str}. Additional toppings may apply depending on customization."
            return f"The dish **{food}** is made with: {ing_str}."

        # 텍스트 입력일 때 toppings 포함
        if input_type == "text":
            main_ing = ", ".join(ingredients) if ingredients else "No ingredients found."
            toppings = result.get("toppings", [])
            toppings_str = ", ".join(toppings) if toppings else "no additional toppings"

            return (
                f"The main dish **{food}** is made with: {main_ing}. "
                f"Toppings may include: {toppings_str}."
            )


    # ============================
    # 5) 토핑 알레르기 조회 (check_topping_allergy)
    # ============================
    if intent == "check_topping_allergy":
        if input_type == "image":
            return "Topping details are only available in text mode."

        topping_allergens = result  # dict { topping: [a1, a2] }

        if not topping_allergens:
            return f"No topping allergen information found for **{food}**."

        response = [f"Topping allergen details for **{food}**:"]
        for topping, allergens in topping_allergens.items():
            if allergens:
                response.append(f"- {topping}: {', '.join(allergens)}")
            else:
                response.append(f"- {topping}: No allergens")

        return "\n".join(response)


    # ============================
    # 6) 토핑 재료 조회 (check_topping_ingredient)
    # ============================
    if intent == "check_topping_ingredient":
        if input_type == "image":
            return "Topping information is available only for text-based questions."

        toppings = result
        if not toppings:
            return f"No toppings found for **{food}**."

        return f"The toppings for **{food}** include: {', '.join(toppings)}."


    # ============================
    # 7) 토핑 섭취 가능 여부 (check_topping_edibility)
    # ============================
    if intent == "check_topping_edibility":
        if input_type == "image":
            return "Topping edibility can only be checked in text mode."

        edible = result["edible"]
        conflict = result["conflict"]

        if edible:
            return f"You can safely eat the toppings for **{food}**. No allergens matching your condition were found."

        response = ["Some toppings may be unsafe for you due to allergen conflicts:"]
        for topping, allergens in conflict.items():
            response.append(f"- {topping}: {', '.join(allergens)}")

        return "\n".join(response)


    # ============================
    # unknown intent fallback
    # ============================
    return "I'm not sure what you're asking. Could you rephrase your question?"
