# =======================
# MODEL 관련 설정
# =======================
MODEL_PATH = "./merged_clip_lora"
DEVICE = "cuda"  # "cpu"로 강제도 가능
NORMALIZE_EMBEDDINGS = True  # 임베딩 정규화 여부


# =======================
# NEO4J
# =======================
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "qwer1234"
NEO4J_DATABASE = "neo4j-2025-11-27T08-12-34"


# =========================
# 음식, 토핑, 알레르겐 리스트
# =========================

topping_labels = [
    "abalone",
    "bacon",
    "bean_sprouts",
    "beans",
    "beef",
    "cheese",
    "crab",
    "egg",
    "eggs",
    "fish_cake",
    "flying fish roe",
    "fried dumpling",
    "ham",
    "kimchi",
    "macaroni",
    "noodles",
    "peanut",
    "pine_nut",
    "pork",
    "ramen",
    "rice_cake",
    "seasoned_red_pepper_sauce",
    "sesame",
    "shellfish",
    "shiitake_mushroom",
    "shrimp",
    "squid",
    "suasage",
    "tofu",
    "tteok",
    "tuna",
    "walnut",
    "wheat_rice_cake",
]

food_labels = [
    "Andong_Jjimdak",
    "Beef Seaweed Soup",
    "beef_bulgogi",
    "beef_tartere_Bibimbap",
    "bibim_naengmyeon",
    "bone stew",
    "budaejjigae",
    "cheese_Jjimdak",
    "Cheese_Tteokbokki",
    "chive_pancake",
    "clam_kalguksu",
    "cream_tteokbokki",
    "dak_kalguksu",
    "Dried Pollack and Seaweed Soup",
    "flying_fish_roe_bibimbap",
    "Galbitang",
    "ganjanggejang",
    "garlic_pig's_trotters",
    "gungjung_tteokbokki",
    "jang_kalguksu",
    "Jeonju_Bibimbap",
    "kimchi stewed ribs",
    "kimchi tofu Stew",
    "kimchi_fried_rice",
    "kimchi_pancake",
    "kongbul",
    "mackerel_bibimbap",
    "meat_japchae",
    "mul_naengmyeon",
    "osam_bulgogi",
    "Pacific Saury Kimchi Stew",
    "Perilla Seaweed Soup",
    "perilla_leaf_kalguksu",
    "pig's_trotters_ salad",
    "Pork gukbap",
    "Pork Kimchi Stew",
    "potato_pancake",
    "pyongyang_naengmyeon",
    "Rose_Tteokbokki",
    "samgyetang",
    "Seafood Soft Tofu Stew",
    "seafood_japchae",
    "seafood_kalguksu",
    "seafood_pancake",
    "seasood_samgyetang",
    "Soft tofu Stew",
    "Spam Kimchi Stew",
    "Spicy Braised Pork Ribs",
    "spicy_pig's_trotters",
    "stewed ribs",
    "Sundae-gukbap",
    "tteokbokki",
    "Tuna Kimchi Stew",
    "Tuna Seaweed Soup",
    "Tuna_Bibimbap",
    "yangnyeomgejang",
]

allergens_labels = [
    "Beef",
    "Buckwheat",
    "Chicken",
    "Crustacean",
    "Egg",
    "Fish",
    "Milk",
    "Mollusk",
    "Nuts",
    "Pork",
    "Sesame",
    "Shellfish",
    "Soybean",
    "Sulfite",
    "Tomato",
    "Wheat",
    "Fruit(Pear)"
]
