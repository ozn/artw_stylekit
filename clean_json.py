import json
import re

# Dosyayı oku
with open('out/ai_art_outline.json', 'r', encoding='utf-8') as f:
    content = f.read()

# Markdown temizle
content = content.strip()
if content.startswith('```json'):
    content = content[7:]
elif content.startswith('```'):
    content = content[3:]
    
if content.endswith('```'):
    content = content[:-3]

content = content.strip()

# JSON parse et
try:
    data = json.loads(content)
    
    # Temiz kaydet
    with open('out/ai_clean.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print("✓ JSON temizlendi ve kaydedildi")
except json.JSONDecodeError as e:
    print(f"❌ JSON hatası: {e}")
    print(f"İlk 200 karakter:\n{content[:200]}")
