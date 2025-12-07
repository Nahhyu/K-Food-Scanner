 (cd "$(git rev-parse --show-toplevel)" && git apply --3way <<'EOF' 
diff --git a/response_module.py b/response_module.py
index 392f69b085d3084fc3d6986ccd160ae18b9ccf80..1580426c174eae92359e6e724fa0620afcf3cf5d 100644
--- a/response_module.py
+++ b/response_module.py
@@ -46,69 +46,66 @@ def build_response(intent: str, food: str, result, input_type="image"):
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
-    if intent == "check_ingredients":
-        ingredients = result.get("ingredients", result)  # 이미지일 경우 list, 텍스트일 경우 dict
-
-        if isinstance(ingredients, list):
-            ing_str = ", ".join(ingredients) if ingredients else "No ingredients found."
-            if input_type == "text":
-                return f"The main dish **{food}** contains: {ing_str}. Additional toppings may apply depending on customization."
-            return f"The dish **{food}** is made with: {ing_str}."
-
-        # 텍스트 입력일 때 toppings 포함
-        if input_type == "text":
-            main_ing = ", ".join(ingredients) if ingredients else "No ingredients found."
-            toppings = result.get("toppings", [])
-            toppings_str = ", ".join(toppings) if toppings else "no additional toppings"
-
-            return (
-                f"The main dish **{food}** is made with: {main_ing}. "
-                f"Toppings may include: {toppings_str}."
-            )
+    if intent == "check_ingredients":
+        # 텍스트 입력의 경우 재료 + 토핑 모두 출력
+        if input_type == "text" and isinstance(result, dict):
+            main_ing = ", ".join(result.get("ingredients", [])) or "No ingredients found."
+            toppings = result.get("toppings", [])
+            toppings_str = ", ".join(toppings) if toppings else "no additional toppings"
+
+            return (
+                f"The main dish **{food}** is made with: {main_ing}. "
+                f"Toppings may include: {toppings_str}."
+            )
+
+        # 이미지 입력(또는 일반 리스트 결과)의 경우 재료만 출력
+        ingredients = result.get("ingredients", result) if isinstance(result, dict) else result
+        ing_str = ", ".join(ingredients) if ingredients else "No ingredients found."
+        return f"The dish **{food}** is made with: {ing_str}."
 
 
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
 
EOF
)
