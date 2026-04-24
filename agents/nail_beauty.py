"""
Nail & Beauty Specialist Agent
Orchestrates content_writer -> html_builder -> wp_packager pipeline.
"""
import os
import re
import anthropic

from .content_writer import generate_content
from .html_builder import build_html
from .wp_packager import package_wordpress_theme


def _slugify(text: str) -> str:
    """Convert master name to a safe folder name."""
    _cyr = {
        'а':'a','б':'b','в':'v','г':'g','д':'d','е':'e','ё':'yo','ж':'zh',
        'з':'z','и':'i','й':'y','к':'k','л':'l','м':'m','н':'n','о':'o',
        'п':'p','р':'r','с':'s','т':'t','у':'u','ф':'f','х':'kh','ц':'ts',
        'ч':'ch','ш':'sh','щ':'shch','ъ':'','ы':'y','ь':'','э':'e','ю':'yu','я':'ya',
    }
    result = ''
    for char in text.lower():
        result += _cyr.get(char, char)
    slug = re.sub(r'[^\w\s-]', '', result)
    slug = re.sub(r'[\s_-]+', '-', slug).strip('-')
    return slug or "beauty-master"


def run_nail_beauty_agent(business_info: dict) -> str:
    """
    Main pipeline:
    1. Generate Russian content via Claude
    2. Build dark-themed animated HTML
    3. Package as WordPress theme
    4. Return path to output folder
    """
    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    master_name = business_info.get("master_name", "Мастер")
    theme_key = business_info.get("color_theme", "1")
    slug = _slugify(master_name)

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    output_dir = os.path.join(base_dir, "output", slug)
    preview_dir = os.path.join(output_dir, "preview")
    os.makedirs(preview_dir, exist_ok=True)

    print("  ⟳  Генерирую тексты для сайта...")
    content = generate_content(client, business_info)
    print("  ✓  Тексты готовы")

    print("  ⟳  Собираю HTML с анимациями...")
    html = build_html(business_info, content, theme_key)
    print("  ✓  HTML готов")

    preview_path = os.path.join(preview_dir, "index.html")
    with open(preview_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"  ✓  Превью сохранено: preview/index.html")

    print("  ⟳  Создаю WordPress тему...")
    package_wordpress_theme(output_dir, html, business_info, content)
    print("  ✓  WordPress тема готова (+ ZIP архив)")

    return output_dir
