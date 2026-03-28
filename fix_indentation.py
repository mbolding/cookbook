import os
import re

recipes_dir = '/home/mbolding/Desktop/cookbook/recipes/'

for filename in os.listdir(recipes_dir):
    if not filename.endswith('.html'):
        continue
    
    filepath = os.path.join(recipes_dir, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Fix the double indentation issue
    # Looking for:
    # 12 spaces <div class="recipe-hero-emoji-container">
    # 8 spaces <span class="recipe-hero-emoji">
    # 6 spaces </div>
    # 6 spaces <div class="recipe-detail-content">
    
    # Wait, my previous script's insertion was:
    # f'      <div class="recipe-hero-emoji-container">\n        <span class="recipe-hero-emoji">{emoji}</span>\n      </div>\n      '
    
    # Let's just use a regex to fix it
    new_content = re.sub(
        r'([ ]+)<div class="recipe-hero-emoji-container">\s*<span class="recipe-hero-emoji">([^<]+)</span>\s*</div>\s*([ ]+)<div class="recipe-detail-content">',
        r'      <div class="recipe-hero-emoji-container">\n        <span class="recipe-hero-emoji">\2</span>\n      </div>\n      <div class="recipe-detail-content">',
        content,
        flags=re.MULTILINE
    )
    
    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Fixed indentation for {filename}")
