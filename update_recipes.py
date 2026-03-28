import os
import re

# File paths
index_path = '/home/mbolding/Desktop/cookbook/index.html'
recipes_dir = '/home/mbolding/Desktop/cookbook/recipes/'

# 1. Update index.html
with open(index_path, 'r', encoding='utf-8') as f:
    index_content = f.read()

# Pattern to find recipe cards
card_pattern = re.compile(
    r'(<article class="recipe-card" id="([^"]+)" data-category="[^"]+">)\s*(<!--.*?-->)?\s*<div class="recipe-card-content">\s*<span class="card-emoji">([^<]+)</span>',
    re.DOTALL
)

# Store emojis for later use in recipe files
recipe_emojis = {}

def update_card(match):
    full_card_start = match.group(1)
    card_id = match.group(2)
    comment = match.group(3) if match.group(3) else ""
    emoji = match.group(4)
    
    # Store emoji mapping by recipe file name (derived from card_id or we'll get it from href later)
    # Actually, let's find the href in the same card
    href_match = re.search(r'href="recipes/([^"]+\.html)"', index_content[match.end():match.end()+500])
    if href_match:
        recipe_filename = href_match.group(1)
        recipe_emojis[recipe_filename] = emoji
    
    new_card_content = f'{full_card_start}\n        {comment}\n        <div class="recipe-card-emoji-container">\n          <span class="card-emoji">{emoji}</span>\n        </div>\n        <div class="recipe-card-content">'
    return new_card_content

# We need to be careful with the replacement. 
# The card-emoji span should be removed from recipe-card-content.
# The new container should be before recipe-card-content.

# Let's do it more robustly
new_index_content = index_content

# Find all cards
cards = list(card_pattern.finditer(index_content))
offset = 0

for match in cards:
    full_match = match.group(0)
    card_start = match.group(1)
    comment = match.group(3) if match.group(3) else ""
    emoji = match.group(4)
    
    # Find href
    href_match = re.search(r'href="recipes/([^"]+\.html)"', index_content[match.end():match.end()+500])
    if href_match:
        recipe_filename = href_match.group(1)
        recipe_emojis[recipe_filename] = emoji

    replacement = f'{card_start}\n        {comment}\n        <div class="recipe-card-emoji-container">\n          <span class="card-emoji">{emoji}</span>\n        </div>\n        <div class="recipe-card-content">'
    
    # The original match ends after <span class="card-emoji">...</span>
    # We replaced it with the new container and opening div of recipe-card-content
    
    # Update new_index_content
    start = match.start() + offset
    end = match.end() + offset
    new_index_content = new_index_content[:start] + replacement + new_index_content[end:]
    offset += len(replacement) - len(full_match)

with open(index_path, 'w', encoding='utf-8') as f:
    f.write(new_index_content)

print(f"Updated index.html. Found {len(recipe_emojis)} recipes.")

# 2. Update individual recipe files
for filename, emoji in recipe_emojis.items():
    filepath = os.path.join(recipes_dir, filename)
    if not os.path.exists(filepath):
        print(f"Warning: {filepath} not found.")
        continue
        
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if <img> is active (not commented out)
    # The current files have them commented out like <!-- <img ... -->
    if '<img' in content and not re.search(r'<!--\s*<img[^>]+class="recipe-hero-image"[^>]*-->', content):
         # If there is an active img, we don't add the emoji (as per instructions)
         # Wait, if it matches <img but NOT commented out, then it's active.
         # Actually, all current ones ARE commented out.
         pass
    
    # Check if already has the container
    if 'recipe-hero-emoji-container' in content:
        continue

    # Find <article class="recipe-detail"> and <div class="recipe-detail-content">
    # Add container before recipe-detail-content
    insertion = f'      <div class="recipe-hero-emoji-container">\n        <span class="recipe-hero-emoji">{emoji}</span>\n      </div>\n      '
    
    new_content = content.replace('<div class="recipe-detail-content">', insertion + '<div class="recipe-detail-content">')
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)

print("Updated recipe files.")

# Handle template.html separately if needed
template_path = os.path.join(recipes_dir, 'template.html')
if os.path.exists(template_path):
    with open(template_path, 'r', encoding='utf-8') as f:
        content = f.read()
    if 'recipe-hero-emoji-container' not in content:
        insertion = f'      <div class="recipe-hero-emoji-container">\n        <span class="recipe-hero-emoji">🍴</span>\n      </div>\n      '
        new_content = content.replace('<div class="recipe-detail-content">', insertion + '<div class="recipe-detail-content">')
        with open(template_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print("Updated template.html with default emoji.")
