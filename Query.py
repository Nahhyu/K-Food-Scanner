# Query.py

from neo4j import GraphDatabase
from config import NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD, NEO4J_DATABASE

driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))


# =============================
# 공통 Neo4j 실행 함수
# =============================
def run_query_neo4j(query: str, params: dict):
    with driver.session(database=NEO4J_DATABASE) as session:
        result = session.run(query, **params)
        return result.data()


# =============================
# 1) 음식 → 알레르겐 전체 조회 (check_allergy)
# =============================
def query_food_allergens(food_name: str):
    query = """
    MATCH (f:Food {name: $food})
    OPTIONAL MATCH (f)-[:HAS_INGREDIENT]->(ing:Ingredient)
    OPTIONAL MATCH (f)-[:HAS_ALLERGEN]->(a1:Allergen)
    OPTIONAL MATCH (ing)-[:HAS_ALLERGEN]->(a2:Allergen)
    RETURN DISTINCT coalesce(a1.name, a2.name) AS allergen
    """
    records = run_query_neo4j(query, {"food": food_name})
    return [r["allergen"] for r in records if r["allergen"]]


# =============================
# 2) user allergy ∈ 음식 알레르겐? (check_edibility)
# =============================
def query_edibility(food_name: str, user_allergens: list):
    food_allergens = query_food_allergens(food_name)

    conflict = [a for a in user_allergens if a in food_allergens]

    return {
        "food_allergens": food_allergens,
        "conflict": conflict,
        "edible": len(conflict) == 0
    }


# =============================
# 3) 음식 → 모든 재료 조회 (check_ingredients)
# =============================
def query_food_ingredients(food_name: str):
    query = """
    MATCH (f:Food {name: $food})
    OPTIONAL MATCH (f)-[:HAS_INGREDIENT]->(ing:Ingredient)
    RETURN DISTINCT ing.name AS ingredient
    """
    records = run_query_neo4j(query, {"food": food_name})
    return [r["ingredient"] for r in records if r["ingredient"]]


# =============================
# 4) 음식 → topping 재료 조회 (check_topping_ingredient)
# =============================
def query_topping_ingredients(food_name: str):
    query = """
    MATCH (f:Food {name: $food})
    OPTIONAL MATCH (f)-[:HAS_TOPPING]->(t:Topping)
    RETURN DISTINCT t.name AS topping
    """
    records = run_query_neo4j(query, {"food": food_name})
    return [r["topping"] for r in records if r["topping"]]


# =============================
# 5) topping → 알레르겐 전체 조회 (check_topping_allergy)
# =============================
def query_topping_allergens(food_name: str):
    toppings = query_topping_ingredients(food_name)

    result = {}
    for t in toppings:
        query = """
        MATCH (t:Topping {name: $topping})
        OPTIONAL MATCH (t)-[:HAS_ALLERGEN]->(a:Allergen)
        RETURN DISTINCT a.name AS allergen
        """
        records = run_query_neo4j(query, {"topping": t})
        allergens = [r["allergen"] for r in records if r["allergen"]]
        result[t] = allergens

    return result


# =============================
# 6) topping edibility (check_topping_edibility)
# =============================
def query_topping_edibility(food_name: str, user_allergens: list):
    top_allergens = query_topping_allergens(food_name)

    conflict = {}
    for topping, allergens in top_allergens.items():
        bad = [a for a in user_allergens if a in allergens]
        if bad:
            conflict[topping] = bad

    return {
        "topping_allergens": top_allergens,
        "conflict": conflict,
        "edible": len(conflict) == 0
    }


# =============================
# 7) intent 라우팅 (패치 적용됨!)
# =============================
def run_query(intent: str, food: str, allergens: list, input_type="image"):
    """
    사용자 의도와 입력 유형에 따라 적절한 쿼리를 실행한다.

    - 기본 intent(check_allergy, check_edibility, check_ingredients)는 공통으로 동작한다.
    - 토핑 관련 intent(check_topping_*)는 텍스트 입력일 때만 허용한다.
    - 텍스트에서 재료 조회(check_ingredients)할 때는 토핑 목록도 함께 반환한다.
    """

    # -----------------------------
    # 텍스트-only일 때만 토핑 intent 허용
    # -----------------------------
    if input_type == "text":
        if intent == "check_topping_allergy":
            return query_topping_allergens(food)

        if intent == "check_topping_ingredient":
            return query_topping_ingredients(food)

        if intent == "check_topping_edibility":
            return query_topping_edibility(food, allergens)

    # -----------------------------
    # 공통 intent 처리
    # -----------------------------
    if intent == "check_allergy":
        return query_food_allergens(food)

    if intent == "check_edibility":
        return query_edibility(food, allergens)

    if intent == "check_ingredients":
        ingredients = query_food_ingredients(food)

        # 텍스트 입력이면 toppings도 추가 반환
        if input_type == "text":
            return {
                "ingredients": ingredients,
                "toppings": query_topping_ingredients(food)
            }

        return ingredients

    return None
