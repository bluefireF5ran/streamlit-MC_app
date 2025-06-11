import pandas as pd
from hero_image_urls import hero_image_urls
card_data = pd.DataFrame([
    {"name": "Spiderman",         "aspect": "Hero",       "tier": "S", "img": hero_image_urls["Moon Knight"], "type": "Event", "copies": 1},
    {"name": "Desperate Defense", "aspect": "Protection", "tier": "A", "img": "https://cdn.jsdelivr.net/gh/alaintxu/mc-ocr@main/images/accepted/09015.webp", "type": "Event", "copies": 3},
    {"name": "Gancho",            "aspect": "Aggression", "tier": "A", "img": "https://cdn.jsdelivr.net/gh/alaintxu/mc-ocr@main/images/accepted/01054.webp", "type": "Event", "copies": 2},
    {"name": "Wakanda Forever",   "aspect": "Hero",       "tier": "A", "img": "https://cdn.jsdelivr.net/gh/alaintxu/mc-ocr@main/images/accepted/01043b.webp", "type": "Event", "copies": 4},
])
