"""
HTML Builder Agent
Generates a standalone HTML page with the full raymarching + dot-matrix
Three.js animation from the original nail1 template, re-skinned in a
soft beauty-industry pink palette.
"""
import html as html_lib


def _esc(value) -> str:
    return html_lib.escape(str(value))


def _stars(rating: int) -> str:
    return '★' * rating + '☆' * (5 - rating)


def _build_services_grid(items: list) -> str:
    fallback_emojis = ['💅', '✨', '🌸', '💎', '🪄', '🌿']
    delays = ['reveal-delay-1', 'reveal-delay-2', 'reveal-delay-3',
              'reveal-delay-4', 'reveal-delay-5', 'reveal-delay-6']
    cards = []
    for i, item in enumerate(items[:6]):
        delay = delays[i % len(delays)]
        name = _esc(item.get('name', ''))
        desc = _esc(item.get('description', ''))
        emoji = item.get('emoji', fallback_emojis[i % len(fallback_emojis)])
        badge = '<div class="feature-badge">Популярное</div>' if i == 0 else ''
        cards.append(f'''
      <div class="feature-card reveal {delay}">
        {badge}
        <div class="feature-emoji">{emoji}</div>
        <div class="feature-title">{name}</div>
        <div class="feature-desc">{desc}</div>
      </div>''')
    return '\n'.join(cards)


def _build_portfolio_grid(count: int = 6) -> str:
    labels = ['Маникюр', 'Дизайн', 'Наращивание', 'Педикюр', 'Комплекс', 'Арт']
    items = []
    for i in range(count):
        label = labels[i % len(labels)]
        delay = f'reveal-delay-{(i % 6) + 1}'
        items.append(f'''
      <div class="portfolio-item reveal {delay}">
        <div class="portfolio-placeholder">
          <span class="portfolio-placeholder-icon">+</span>
        </div>
        <div class="portfolio-label">{label}</div>
      </div>''')
    return '\n'.join(items)


def _build_prices_rows(items: list) -> str:
    rows = []
    delays = ['reveal-delay-1', 'reveal-delay-2', 'reveal-delay-3',
              'reveal-delay-4', 'reveal-delay-5', 'reveal-delay-6']
    for i, item in enumerate(items):
        delay = delays[i % len(delays)]
        name = _esc(item.get('name', ''))
        price = _esc(item.get('price', ''))
        featured_class = ' price-row--featured' if i == 0 else ''
        rows.append(f'''
      <div class="price-row{featured_class} reveal {delay}">
        <span class="price-name">{name}</span>
        <span class="price-dots"></span>
        <span class="price-val">{price}</span>
      </div>''')
    return '\n'.join(rows)


def _build_reviews(items: list) -> str:
    delays = ['reveal-delay-1', 'reveal-delay-2', 'reveal-delay-3']
    review_dates = ['Март 2026', 'Февраль 2026', 'Январь 2026']
    cards = []
    for i, item in enumerate(items[:3]):
        delay = delays[i % len(delays)]
        name = _esc(item.get('name', ''))
        text = _esc(item.get('text', ''))
        service = _esc(item.get('service', ''))
        rating = item.get('rating', 5)
        stars = _stars(rating)
        initial = name[0].upper() if name else '?'
        date = review_dates[i % len(review_dates)]
        cards.append(f'''
      <div class="review-card reveal {delay}">
        <div class="review-stars">{stars}</div>
        <p class="review-text">{text}</p>
        <div class="review-footer">
          <div class="review-avatar">{initial}</div>
          <div class="review-meta">
            <span class="review-name">{name}</span>
            <span class="review-service">{service}</span>
          </div>
          <span class="review-date">{date}</span>
        </div>
      </div>''')
    return '\n'.join(cards)


def _build_contact_links(business_info: dict) -> str:
    links = []
    phone = business_info.get('phone', '')
    instagram = business_info.get('instagram', '')
    telegram = business_info.get('telegram', '')
    address = business_info.get('address', '')
    city = business_info.get('city', '')

    if phone:
        links.append(f'<a href="tel:{_esc(phone)}" class="contact-link"><span class="contact-link-icon">☎</span>{_esc(phone)}</a>')
    if instagram:
        links.append(f'<a href="https://instagram.com/{_esc(instagram)}" target="_blank" class="contact-link"><span class="contact-link-icon">◈</span>@{_esc(instagram)}</a>')
    if telegram:
        links.append(f'<a href="https://t.me/{_esc(telegram)}" target="_blank" class="contact-link"><span class="contact-link-icon">✈</span>@{_esc(telegram)}</a>')
    if city or address:
        location = ', '.join(filter(None, [city, address]))
        links.append(f'<span class="contact-link"><span class="contact-link-icon">✦</span>{_esc(location)}</span>')

    return '\n'.join(links)


def build_html(business_info: dict, content: dict, theme_key: str = "1") -> str:
    master_name = _esc(business_info.get('master_name', 'Мастер'))
    exp_years = _esc(business_info.get('experience_years', '5'))
    clients_count = _esc(business_info.get('clients_count', '500'))
    works_count = _esc(business_info.get('works_count', '2000'))

    hero = content.get('hero', {})
    about = content.get('about', {})
    services = content.get('services', {})
    prices = content.get('prices', {})
    reviews = content.get('reviews', {})
    contact = content.get('contact', {})
    footer_data = content.get('footer', {})

    hero_headline = _esc(hero.get('headline', master_name))
    hero_subheadline = _esc(hero.get('subheadline', ''))
    hero_cta = _esc(hero.get('cta_button', 'Записаться'))

    about_title = _esc(about.get('title', 'О мастере'))
    about_text = _esc(about.get('text', ''))
    badge1_label = _esc(about.get('badge1_label', 'лет опыта'))
    badge2_label = _esc(about.get('badge2_label', 'довольных клиентов'))
    badge3_label = _esc(about.get('badge3_label', 'выполненных работ'))

    services_title = _esc(services.get('title', 'Услуги'))
    services_subtitle = _esc(services.get('subtitle', ''))
    services_grid = _build_services_grid(services.get('items', []))
    portfolio_grid = _build_portfolio_grid(6)

    prices_title = _esc(prices.get('title', 'Прайс'))
    prices_subtitle = _esc(prices.get('subtitle', ''))
    prices_note = _esc(prices.get('note', ''))
    prices_rows = _build_prices_rows(prices.get('items', []))

    reviews_title = _esc(reviews.get('title', 'Отзывы'))
    reviews_subtitle = _esc(reviews.get('subtitle', ''))
    reviews_cards = _build_reviews(reviews.get('items', []))

    contact_title = _esc(contact.get('title', 'Контакты'))
    contact_subtitle = _esc(contact.get('subtitle', ''))
    contact_links = _build_contact_links(business_info)

    footer_tagline = _esc(footer_data.get('tagline', ''))

    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{master_name}</title>
  <link href="https://fonts.googleapis.com/css2?family=Geist:wght@300;400;500;600&family=Instrument+Serif:ital@0;1&display=swap" rel="stylesheet">
  <style>
    :root {{
      --bg: #FDEEF0;
      --bg-soft: #FBE1E5;
      --bg-warm: #F5D5DA;
      --text: #3D1E24;
      --text-muted: rgba(61, 30, 36, 0.62);
      --text-faded: rgba(61, 30, 36, 0.35);
      --text-ghost: rgba(61, 30, 36, 0.22);
      --border: rgba(61, 30, 36, 0.10);
      --border-strong: rgba(61, 30, 36, 0.22);
      --accent: #C84A5E;
      --accent-soft: #D96F82;
    }}

    * {{ margin: 0; padding: 0; box-sizing: border-box; outline: none !important; }}
    html {{
      scroll-behavior: smooth;
      overflow-x: clip;
    }}
    body {{
      width: 100%; min-height: 100%; overflow-x: hidden;
      background: var(--bg);
      color: var(--text);
      font-family: 'Geist', -apple-system, BlinkMacSystemFont, sans-serif;
    }}

    /* ===== 3D BACKGROUND ===== */
    #crt-frame {{
      position: absolute; top: 0; left: 0;
      width: 100%; height: 100%; z-index: 0; overflow: hidden; pointer-events: none;
    }}
    #crt-frame canvas {{ display: block; width: 100% !important; height: 100% !important; pointer-events: none; }}

    /* ===== HERO ===== */
    .hero-wrapper {{ position: relative; width: 100%; height: 100vh; overflow: hidden; background: var(--bg); }}
    .hero-fade {{
      position: absolute; bottom: 0; left: 0; width: 100%; height: 55%;
      background: linear-gradient(to top, var(--bg) 0%, var(--bg) 8%, transparent 100%);
      z-index: 5; pointer-events: none;
    }}
    .hero-fade-top {{
      position: absolute; top: 0; left: 0; width: 100%; height: 20%;
      background: linear-gradient(to bottom, var(--bg) 0%, var(--bg) 5%, transparent 100%);
      z-index: 5; pointer-events: none;
    }}
    #hero-overlay {{
      position: relative; width: 100%; height: 100%;
      z-index: 10; pointer-events: none;
      display: flex; flex-direction: column;
    }}

    /* ===== NAV ===== */
    .nav {{
      position: fixed; top: 0; left: 0; right: 0; z-index: 100;
      display: flex; align-items: center; justify-content: space-between;
      padding: 24px 48px; pointer-events: auto;
      transition: background 0.4s ease, backdrop-filter 0.4s ease, border-color 0.4s ease;
    }}
    .nav.scrolled {{
      background: rgba(253, 238, 240, 0.85);
      -webkit-backdrop-filter: blur(20px);
      backdrop-filter: blur(20px);
      border-bottom: 1px solid var(--border);
    }}
    .nav-brand {{ display: flex; align-items: center; gap: 10px; text-decoration: none; }}
    .nav-brand-dot {{
      width: 8px; height: 8px; background: var(--accent);
      box-shadow: 0 0 12px rgba(200, 74, 94, 0.5);
      animation: pulse 1.2s steps(2) infinite;
    }}
    @keyframes pulse {{ 0%,100% {{ opacity:1; }} 50% {{ opacity:0.2; }} }}
    .nav-brand-text {{
      font-size: 13px; font-weight: 500; color: var(--text);
      letter-spacing: 2px; text-transform: uppercase;
    }}
    .nav-links {{ display: flex; align-items: center; gap: 36px; }}
    .nav-links a {{
      font-size: 13px; font-weight: 400; color: var(--text-muted);
      text-decoration: none; letter-spacing: 0.5px; transition: color 0.25s ease;
    }}
    .nav-links a:hover {{ color: var(--text); }}
    .nav-cta {{
      font-size: 13px !important; font-weight: 500 !important;
      color: #fff !important; background: var(--accent);
      padding: 10px 24px; border-radius: 100px;
      transition: background 0.25s ease, transform 0.25s ease !important;
    }}
    .nav-cta:hover {{ background: var(--accent-soft); color: #fff !important; }}

    /* Hamburger */
    .nav-hamburger {{
      display: none; flex-direction: column; justify-content: center; gap: 5px;
      width: 32px; height: 32px; background: none; border: none;
      cursor: pointer; padding: 4px; pointer-events: auto; z-index: 100;
    }}
    .nav-hamburger span {{
      display: block; width: 100%; height: 1.5px;
      background: var(--text); transition: transform 0.3s ease, opacity 0.3s ease;
    }}
    .nav-hamburger.open span:nth-child(1) {{ transform: translateY(6.5px) rotate(45deg); }}
    .nav-hamburger.open span:nth-child(2) {{ opacity: 0; }}
    .nav-hamburger.open span:nth-child(3) {{ transform: translateY(-6.5px) rotate(-45deg); }}

    .mobile-menu {{
      display: none; position: fixed; top: 0; left: 0;
      width: 100%; height: 100%; background: rgba(253, 238, 240, 0.96);
      z-index: 50; flex-direction: column; align-items: center;
      justify-content: center; gap: 0; opacity: 0;
      pointer-events: none; transition: opacity 0.3s ease;
      -webkit-backdrop-filter: blur(20px); backdrop-filter: blur(20px);
    }}
    .mobile-menu.open {{ opacity: 1; pointer-events: auto; }}
    .mobile-menu a {{
      font-size: 28px; font-weight: 300; color: var(--text-muted);
      text-decoration: none; padding: 16px 0; transition: color 0.25s ease;
    }}
    .mobile-menu a:hover {{ color: var(--text); }}
    .mobile-menu .mobile-cta {{
      margin-top: 24px; font-size: 14px; font-weight: 500;
      color: #fff; background: var(--accent);
      padding: 14px 36px; border-radius: 100px;
    }}

    /* ===== HERO CONTENT ===== */
    .hero-content {{
      flex: 1; display: flex; flex-direction: column;
      justify-content: flex-end; padding: 0 48px 44px; pointer-events: none;
    }}
    .hero-h1 {{
      font-family: 'Instrument Serif', Georgia, serif;
      font-size: clamp(48px, 9vw, 130px);
      font-weight: 400; color: var(--text); line-height: 0.95;
      letter-spacing: -2px; margin-bottom: 28px;
      opacity: 0; transition: opacity 0.9s cubic-bezier(0.25,0.1,0.25,1) 0.6s;
    }}
    .hero-h1.anim-in {{ opacity: 1; }}
    .hero-h1 .thin {{ color: var(--text-faded); font-style: italic; }}
    .hero-row {{
      display: flex; align-items: flex-end;
      justify-content: space-between; gap: 40px; pointer-events: none;
    }}
    .hero-sub {{
      font-size: 13px; font-weight: 300; color: var(--text-muted);
      line-height: 1.8; max-width: 560px;
      text-shadow: 0 2px 16px rgba(253,238,240,0.9), 0 0 60px rgba(253,238,240,0.9);
      opacity: 0; transition: opacity 0.7s cubic-bezier(0.25,0.1,0.25,1) 0.9s;
    }}
    .hero-sub.anim-in {{ opacity: 1; }}
    .hero-actions {{
      display: flex; align-items: center; gap: 12px; flex-shrink: 0;
      pointer-events: auto;
      opacity: 0; transition: opacity 0.7s cubic-bezier(0.25,0.1,0.25,1) 1.05s;
    }}
    .hero-actions.anim-in {{ opacity: 1; }}
    .btn-primary {{
      position: relative; display: inline-flex; align-items: center; gap: 10px;
      padding: 13px 28px; background: transparent; color: #fff;
      font-family: 'Geist', sans-serif; font-size: 13px; font-weight: 500;
      border: 1px solid var(--accent); border-radius: 100px; cursor: pointer;
      letter-spacing: 0.2px; white-space: nowrap; overflow: hidden; isolation: isolate;
      text-decoration: none;
    }}
    .btn-primary::before {{
      content: ''; position: absolute; inset: 0; background: var(--accent);
      border-radius: inherit; transform: scaleX(1); transform-origin: left center;
      transition: transform 0.35s cubic-bezier(0.4,0,0.2,1); z-index: -1;
    }}
    .btn-primary:hover::before {{ transform: scaleX(0); transform-origin: right center; }}
    .btn-primary:hover {{ color: var(--accent); }}

    /* ===== STATS BAR ===== */
    .hero-bottom {{
      display: flex; align-items: center; justify-content: space-between;
      padding: 24px 48px; pointer-events: none;
    }}
    .hero-stats {{ display: flex; gap: 48px; }}
    .hero-stat {{
      display: flex; flex-direction: column; gap: 4px;
      opacity: 0; transition: opacity 0.6s cubic-bezier(0.25,0.1,0.25,1);
    }}
    .hero-stat:nth-child(1) {{ transition-delay: 1.2s; }}
    .hero-stat:nth-child(2) {{ transition-delay: 1.32s; }}
    .hero-stat:nth-child(3) {{ transition-delay: 1.44s; }}
    .hero-stat.anim-in {{ opacity: 1; }}
    .hero-stat-val {{
      font-size: 18px; font-weight: 500; color: var(--text); letter-spacing: -0.5px;
    }}
    .hero-stat-label {{
      font-size: 11px; font-weight: 400; color: var(--text-faded);
      letter-spacing: 0.5px; text-transform: uppercase;
    }}

    /* ===== ENTRANCE ANIMATIONS ===== */
    #crt-frame {{
      opacity: 0; transition: opacity 2.5s cubic-bezier(0.25,0.1,0.25,1) 0.8s;
    }}
    #crt-frame.visible {{ opacity: 1; }}
    .hero-fade, .hero-fade-top {{
      opacity: 0; transition: opacity 2s cubic-bezier(0.25,0.1,0.25,1) 1.0s;
    }}
    .hero-fade.anim-in, .hero-fade-top.anim-in {{ opacity: 1; }}
    .nav-brand, .nav-links a, .nav-hamburger {{
      opacity: 1; transform: translateY(0);
    }}

    /* ===== SECTIONS ===== */
    .section {{ position: relative; z-index: 10; background: var(--bg); }}
    .section-inner {{ max-width: 1280px; margin: 0 auto; width: 100%; }}
    .section-label {{
      font-size: 10px; font-weight: 500; color: var(--text-ghost);
      letter-spacing: 3px; text-transform: uppercase; margin-bottom: 24px;
    }}
    .section-heading {{
      font-family: 'Instrument Serif', Georgia, serif;
      font-size: clamp(32px, 5vw, 68px); font-weight: 400;
      color: var(--text); line-height: 1.05; letter-spacing: -1.5px;
      max-width: 700px; margin-bottom: 72px;
    }}
    .section-heading .thin {{ color: var(--text-faded); font-style: italic; }}
    .section-sub {{
      font-size: 13px; font-weight: 300; color: var(--text-muted);
      line-height: 1.7; max-width: 500px; margin-top: -48px; margin-bottom: 72px;
    }}

    /* About */
    .section-about {{ padding: 160px 48px 120px; }}
    .about-grid {{
      display: grid; grid-template-columns: 380px 1fr; gap: 80px; align-items: start;
    }}
    .about-photo-placeholder {{
      width: 100%; aspect-ratio: 3 / 4;
      background: var(--bg-warm); border: 1px solid var(--border-strong);
      display: flex; flex-direction: column; align-items: center;
      justify-content: center; gap: 14px;
      color: var(--text-faded); font-size: 11px;
      letter-spacing: 2px; text-transform: uppercase;
    }}
    .about-photo-placeholder::before {{
      content: ''; width: 52px; height: 52px;
      border: 1px solid var(--border-strong); border-radius: 50%; display: block;
    }}
    .about-photo-placeholder::after {{ content: 'ФОТО МАСТЕРА'; }}
    .about-right {{ display: flex; flex-direction: column; gap: 40px; }}
    .about-text {{
      font-size: 16px; font-weight: 300; color: var(--text-muted); line-height: 1.8;
    }}
    .about-stats {{
      display: flex; flex-direction: row;
      border-top: 1px solid var(--border); border-left: 1px solid var(--border);
    }}
    .about-stat {{
      flex: 1; padding: 24px 20px;
      border-right: 1px solid var(--border); border-bottom: 1px solid var(--border);
    }}
    .about-stat-val {{
      font-family: 'Instrument Serif', Georgia, serif;
      font-size: clamp(32px, 4vw, 52px); font-weight: 400;
      color: var(--text); letter-spacing: -2px; line-height: 1;
    }}
    .about-stat-label {{
      font-size: 11px; font-weight: 300; color: var(--text-faded);
      text-transform: uppercase; letter-spacing: 1px; margin-top: 8px;
    }}

    /* Services */
    .section-services {{ padding: 120px 48px; background: var(--bg-soft); }}
    .features-grid {{
      display: grid; grid-template-columns: repeat(3, 1fr);
      gap: 1px; background: var(--border);
      border: 1px solid var(--border);
    }}
    .feature-card {{
      background: var(--bg-soft); padding: 48px 40px;
      display: flex; flex-direction: column; gap: 16px;
      transition: background 0.35s ease; position: relative;
    }}
    .feature-card:hover {{ background: var(--bg); }}
    .feature-badge {{
      position: absolute; top: 16px; right: 16px;
      font-size: 10px; font-weight: 500; letter-spacing: 1.5px; text-transform: uppercase;
      color: var(--accent); border: 1px solid var(--accent);
      padding: 4px 10px; border-radius: 100px;
    }}
    .feature-emoji {{ font-size: 32px; line-height: 1; margin-bottom: 4px; }}
    .feature-title {{ font-size: 16px; font-weight: 500; color: var(--text); }}
    .feature-desc {{ font-size: 13px; font-weight: 300; color: var(--text-muted); line-height: 1.7; }}

    /* Portfolio (внутри секции Services) */
    .portfolio-section-label {{
      font-size: 10px; font-weight: 500; color: var(--text-ghost);
      letter-spacing: 3px; text-transform: uppercase; margin: 72px 0 32px;
    }}
    .portfolio-grid {{
      display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px;
    }}
    .portfolio-item {{ display: flex; flex-direction: column; gap: 10px; }}
    .portfolio-placeholder {{
      aspect-ratio: 4 / 3; background: var(--bg-warm);
      border: 1px solid var(--border-strong);
      display: flex; align-items: center; justify-content: center;
      transition: background 0.3s ease, border-color 0.3s ease;
    }}
    .portfolio-placeholder:hover {{ background: var(--bg); border-color: var(--accent); }}
    .portfolio-placeholder-icon {{
      font-size: 20px; color: var(--text-ghost); font-weight: 300; line-height: 1;
    }}
    .portfolio-label {{
      font-size: 11px; font-weight: 400; color: var(--text-faded);
      letter-spacing: 1px; text-transform: uppercase; text-align: center;
    }}

    /* Prices */
    .section-prices {{ padding: 120px 48px; border-top: 1px solid var(--border); }}
    .prices-list {{ max-width: 720px; }}
    .price-row {{
      display: flex; align-items: baseline; gap: 12px;
      padding: 20px 0; border-bottom: 1px solid var(--border);
    }}
    .price-row--featured {{
      padding: 24px 20px; margin: 0 -20px;
      background: var(--bg-warm); border-bottom: 1px solid var(--border-strong);
    }}
    .price-row--featured .price-name {{ font-size: 16px; font-weight: 500; }}
    .price-row--featured .price-val {{ font-size: 17px; font-weight: 600; }}
    .price-name {{ font-size: 15px; font-weight: 400; color: var(--text); white-space: nowrap; }}
    .price-dots {{
      flex: 1; border-bottom: 1px dashed var(--border-strong);
      margin-bottom: 4px; min-width: 32px;
    }}
    .price-val {{ font-size: 15px; font-weight: 500; color: var(--accent); white-space: nowrap; }}
    .prices-note {{
      font-size: 12px; color: var(--text-faded); margin-top: 24px;
      font-style: italic; letter-spacing: 0.3px;
    }}

    /* Reviews */
    .section-reviews {{ padding: 120px 48px; background: var(--bg-soft); border-top: 1px solid var(--border); }}
    .reviews-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 24px; }}
    .review-card {{
      background: var(--bg); border: 1px solid var(--border); padding: 36px 32px;
      display: flex; flex-direction: column; gap: 20px;
      transition: border-color 0.35s ease, transform 0.35s ease;
    }}
    .review-card:hover {{ border-color: var(--accent); transform: translateY(-3px); }}
    .review-stars {{ font-size: 16px; color: var(--accent); letter-spacing: 3px; }}
    .review-text {{ font-size: 14px; font-weight: 300; color: var(--text-muted); line-height: 1.85; flex: 1; }}
    .review-footer {{
      display: flex; align-items: center; gap: 12px;
      border-top: 1px solid var(--border); padding-top: 16px;
    }}
    .review-avatar {{
      width: 36px; height: 36px; flex-shrink: 0;
      background: var(--bg-warm); border: 1px solid var(--border-strong);
      border-radius: 50%; display: flex; align-items: center; justify-content: center;
      font-size: 14px; font-weight: 500; color: var(--accent);
      font-family: 'Instrument Serif', Georgia, serif;
    }}
    .review-meta {{ display: flex; flex-direction: column; gap: 2px; flex: 1; }}
    .review-name {{ font-size: 13px; font-weight: 500; color: var(--text); }}
    .review-service {{ font-size: 11px; color: var(--text-faded); letter-spacing: 0.5px; text-transform: uppercase; }}
    .review-date {{ font-size: 11px; color: var(--text-ghost); white-space: nowrap; }}

    /* Contact */
    .section-contact {{
      padding: 160px 48px; display: flex; flex-direction: column;
      align-items: center; text-align: center;
      border-top: 1px solid var(--border);
    }}
    .contact-heading {{
      font-family: 'Instrument Serif', Georgia, serif;
      font-size: clamp(36px, 5.5vw, 76px); font-weight: 400;
      color: var(--text); line-height: 1.05; letter-spacing: -1.5px;
      max-width: 700px; margin-bottom: 20px;
    }}
    .contact-sub {{
      font-size: 14px; font-weight: 300; color: var(--text-muted);
      line-height: 1.7; max-width: 480px; margin-bottom: 48px;
    }}
    .contact-links {{ display: flex; flex-direction: column; gap: 16px; align-items: center; }}
    .contact-link {{
      display: inline-flex; align-items: center; gap: 12px;
      font-size: 15px; font-weight: 400; color: var(--text);
      text-decoration: none; transition: color 0.25s ease;
    }}
    .contact-link:hover {{ color: var(--accent); }}
    .contact-link-icon {{ font-size: 16px; color: var(--accent); }}

    /* Footer */
    .footer {{
      position: relative; z-index: 10; background: var(--bg);
      border-top: 1px solid var(--border);
      padding: 48px; display: flex; align-items: center; justify-content: space-between;
    }}
    .footer-left {{ display: flex; align-items: center; gap: 10px; }}
    .footer-dot {{ width: 6px; height: 6px; background: var(--accent); }}
    .footer-brand {{
      font-size: 12px; font-weight: 500; color: var(--text-muted);
      letter-spacing: 2px; text-transform: uppercase;
    }}
    .footer-right {{ font-size: 11px; color: var(--text-faded); letter-spacing: 0.3px; }}
    .footer-tagline {{
      font-family: 'Instrument Serif', Georgia, serif;
      font-size: 13px; font-style: italic; color: var(--text-faded);
    }}

    /* Scroll reveal */
    .reveal {{
      opacity: 0; transform: translateY(40px);
      transition: opacity 0.8s cubic-bezier(0.25,0.1,0.25,1), transform 0.8s cubic-bezier(0.25,0.1,0.25,1);
    }}
    .reveal.visible {{ opacity: 1; transform: translateY(0); }}
    .reveal-delay-1 {{ transition-delay: 0.1s; }}
    .reveal-delay-2 {{ transition-delay: 0.2s; }}
    .reveal-delay-3 {{ transition-delay: 0.3s; }}
    .reveal-delay-4 {{ transition-delay: 0.35s; }}
    .reveal-delay-5 {{ transition-delay: 0.4s; }}
    .reveal-delay-6 {{ transition-delay: 0.5s; }}

    /* ===== RESPONSIVE ===== */
    @media (max-width: 768px) {{
      .nav {{ padding: 16px 24px; }}
      .nav-links {{ display: none; }}
      .nav-hamburger {{ display: flex; }}
      .mobile-menu {{ display: flex; }}
      .hero-content {{ padding: 0 24px 32px; }}
      .hero-h1 {{ font-size: clamp(40px, 12vw, 64px); letter-spacing: -1px; margin-bottom: 20px; }}
      .hero-row {{ flex-direction: column; align-items: flex-start; gap: 20px; }}
      .hero-sub {{ font-size: 12px; max-width: 100%; }}
      .hero-bottom {{ padding: 16px 24px; }}
      .hero-stats {{ gap: 24px; }}
      .section-about {{ padding: 100px 24px 80px; }}
      .about-grid {{ grid-template-columns: 1fr; gap: 32px; }}
      .about-photo-placeholder {{ aspect-ratio: 4 / 3; max-height: 260px; }}
      .about-stats {{ flex-direction: column; }}
      .portfolio-grid {{ grid-template-columns: repeat(2, 1fr); gap: 8px; }}
      .section-services {{ padding: 80px 24px; }}
      .features-grid {{ grid-template-columns: 1fr; }}
      .feature-card {{ padding: 32px 24px; }}
      .section-prices {{ padding: 80px 24px; }}
      .section-reviews {{ padding: 80px 24px; }}
      .reviews-grid {{ grid-template-columns: 1fr; gap: 16px; }}
      .section-contact {{ padding: 100px 24px; }}
      .footer {{ padding: 32px 24px; flex-direction: column; gap: 16px; align-items: flex-start; }}
    }}
  </style>
</head>
<body>

<!-- HERO -->
<div class="hero-wrapper" id="hero-top">
  <div id="crt-frame"></div>
  <div class="hero-fade"></div>
  <div class="hero-fade-top"></div>

  <div id="hero-overlay">
    <nav class="nav">
      <a class="nav-brand" href="#hero-top">
        <div class="nav-brand-dot"></div>
        <span class="nav-brand-text">{master_name}</span>
      </a>
      <div class="nav-links">
        <a href="#services">Услуги</a>
        <a href="#prices">Цены</a>
        <a href="#reviews">Отзывы</a>
        <a href="#contact" class="nav-cta">{hero_cta}</a>
      </div>
      <button class="nav-hamburger" id="hamburger" aria-label="Меню">
        <span></span><span></span><span></span>
      </button>
    </nav>

    <div class="mobile-menu" id="mobile-menu">
      <a href="#services" class="mobile-link">Услуги</a>
      <a href="#prices" class="mobile-link">Цены</a>
      <a href="#reviews" class="mobile-link">Отзывы</a>
      <a href="#contact" class="mobile-cta">{hero_cta}</a>
    </div>

    <div class="hero-content">
      <h1 class="hero-h1">
        {master_name}<br><span class="thin">{hero_headline}</span>
      </h1>
      <div class="hero-row">
        <p class="hero-sub">{hero_subheadline}</p>
        <div class="hero-actions">
          <a href="#contact" class="btn-primary">{hero_cta} →</a>
        </div>
      </div>
    </div>

    <div class="hero-bottom">
      <div class="hero-stats">
        <div class="hero-stat">
          <span class="hero-stat-val">{exp_years}+</span>
          <span class="hero-stat-label">{badge1_label}</span>
        </div>
        <div class="hero-stat">
          <span class="hero-stat-val">{clients_count}+</span>
          <span class="hero-stat-label">{badge2_label}</span>
        </div>
        <div class="hero-stat">
          <span class="hero-stat-val">{works_count}+</span>
          <span class="hero-stat-label">{badge3_label}</span>
        </div>
      </div>
    </div>
  </div>
</div>

<!-- ABOUT -->
<section class="section section-about" id="about">
  <div class="section-inner">
    <div class="section-label reveal">О мастере</div>
    <h2 class="section-heading reveal reveal-delay-1">{about_title}</h2>
    <div class="about-grid">
      <div class="about-photo-placeholder reveal reveal-delay-2"></div>
      <div class="about-right">
        <p class="about-text reveal reveal-delay-3">{about_text}</p>
        <div class="about-stats">
          <div class="about-stat reveal reveal-delay-3">
            <div class="about-stat-val">{exp_years}</div>
            <div class="about-stat-label">{badge1_label}</div>
          </div>
          <div class="about-stat reveal reveal-delay-4">
            <div class="about-stat-val">{clients_count}+</div>
            <div class="about-stat-label">{badge2_label}</div>
          </div>
          <div class="about-stat reveal reveal-delay-5">
            <div class="about-stat-val">{works_count}+</div>
            <div class="about-stat-label">{badge3_label}</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>

<!-- SERVICES -->
<section class="section section-services" id="services">
  <div class="section-inner">
    <div class="section-label reveal">Что я делаю</div>
    <h2 class="section-heading reveal reveal-delay-1">{services_title}</h2>
    <p class="section-sub reveal reveal-delay-2">{services_subtitle}</p>
    <div class="features-grid">
      {services_grid}
    </div>
    <div class="portfolio-section-label reveal" id="portfolio">Примеры работ</div>
    <div class="portfolio-grid">
      {portfolio_grid}
    </div>
  </div>
</section>

<!-- PRICES -->
<section class="section section-prices" id="prices">
  <div class="section-inner">
    <div class="section-label reveal">Стоимость</div>
    <h2 class="section-heading reveal reveal-delay-1">{prices_title}</h2>
    <p class="section-sub reveal reveal-delay-2">{prices_subtitle}</p>
    <div class="prices-list">
      {prices_rows}
      <p class="prices-note">{prices_note}</p>
    </div>
  </div>
</section>

<!-- REVIEWS -->
<section class="section section-reviews" id="reviews">
  <div class="section-inner">
    <div class="section-label reveal">Что говорят клиенты</div>
    <h2 class="section-heading reveal reveal-delay-1">{reviews_title}</h2>
    <p class="section-sub reveal reveal-delay-2">{reviews_subtitle}</p>
    <div class="reviews-grid">
      {reviews_cards}
    </div>
  </div>
</section>

<!-- CONTACT -->
<section class="section section-contact" id="contact">
  <div class="section-inner" style="display:flex;flex-direction:column;align-items:center;text-align:center;">
    <div class="section-label reveal">Связаться</div>
    <h2 class="contact-heading reveal reveal-delay-1">{contact_title}</h2>
    <p class="contact-sub reveal reveal-delay-2">{contact_subtitle}</p>
    <div class="contact-links reveal reveal-delay-3">
      {contact_links}
    </div>
  </div>
</section>

<!-- FOOTER -->
<footer class="footer">
  <div class="section-inner" style="display:flex;align-items:center;justify-content:space-between;width:100%;gap:24px;flex-wrap:wrap;">
    <div class="footer-left">
      <div class="footer-dot"></div>
      <span class="footer-brand">{master_name}</span>
    </div>
    <span class="footer-tagline">{footer_tagline}</span>
    <div class="footer-right">© 2026 {master_name}. Все права защищены.</div>
  </div>
</footer>

<!-- ========= THREE.JS VIA IMPORTMAP (full raymarching scene) ========= -->
<script type="importmap">
{{
  "imports": {{
    "three": "https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.module.js",
    "three/addons/": "https://cdn.jsdelivr.net/npm/three@0.160.0/examples/jsm/"
  }}
}}
</script>

<script type="module">
  import * as THREE from 'three';
  import {{ EffectComposer }} from 'three/addons/postprocessing/EffectComposer.js';
  import {{ RenderPass }} from 'three/addons/postprocessing/RenderPass.js';
  import {{ ShaderPass }} from 'three/addons/postprocessing/ShaderPass.js';

  // ============ DEVICE / GPU DETECTION ============
  const isMobile = /Android|iPhone|iPad|iPod|webOS|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent)
    || (navigator.maxTouchPoints > 1 && window.innerWidth < 1024);
  const gpuTier = (() => {{
    const gl = document.createElement('canvas').getContext('webgl');
    if (!gl) return 'low';
    const ext = gl.getExtension('WEBGL_debug_renderer_info');
    const gpu = ext ? gl.getParameter(ext.UNMASKED_RENDERER_WEBGL).toLowerCase() : '';
    if (/apple gpu|apple m/.test(gpu)) return 'high';
    if (/swiftshader|llvmpipe|mali-4|adreno 3/.test(gpu)) return 'low';
    if (/intel(?!.*(iris|uhd|arc))/.test(gpu)) return 'low';
    if (/mali-g[567]|adreno [45]|intel (iris|uhd)/.test(gpu)) return 'mid';
    return 'high';
  }})();

  const qualityPresets = {{
    low:  {{ pixelRatio: 1.0,  marchSteps: 48, aoSteps: 2, dotSize: 6.0, dotGap: 3.0 }},
    mid:  {{ pixelRatio: 1.25, marchSteps: 64, aoSteps: 3, dotSize: 5.0, dotGap: 2.5 }},
    high: {{ pixelRatio: 1.5,  marchSteps: 80, aoSteps: 3, dotSize: 5.0, dotGap: 2.5 }},
  }};
  let currentTier = isMobile ? 'low' : gpuTier;
  let quality = {{ ...qualityPresets[currentTier] }};

  // Settings
  const settings = {{
    dither:     {{ enabled: true, dotSize: quality.dotSize, dotGap: quality.dotGap, brightness: 0.9, contrast: 0.65 }},
    scene:      {{ gooeyness: 1.20, speed: 0.70 }}
  }};

  // ============ SETUP ============
  const scene = new THREE.Scene();
  // Soft pink background (matches CSS var --bg #FDEEF0)
  scene.background = new THREE.Color(0xFDEEF0);

  const crtFrame = document.getElementById('crt-frame');
  let size = {{ width: window.innerWidth, height: window.innerHeight }};

  const camera = new THREE.PerspectiveCamera(60, size.width / size.height, 0.1, 100);
  camera.position.set(0, 0, 5);

  const renderer = new THREE.WebGLRenderer({{ antialias: false, powerPreference: 'high-performance' }});
  renderer.setSize(size.width, size.height);
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, quality.pixelRatio));
  crtFrame.appendChild(renderer.domElement);

  // ============ MOUSE ============
  const mouse = new THREE.Vector2(0, 0);
  let mouseInScene = false;
  let mousePressed = false;
  let mouseSphereRadius = 0.0;
  const mouseSphereTargetRadius = 0.55;
  const mouseSphereClickRadius = 0.95;
  const mouseWorld = new THREE.Vector3(0, 0, 0);
  const mouseWorldTarget = new THREE.Vector3(0, 0, 0);
  const mouseDamping = 0.15;
  let pageVisible = true;

  const onPointerMove = (e) => {{
    mouseInScene = true;
    const x = e.clientX ?? (e.touches && e.touches[0] ? e.touches[0].clientX : 0);
    const y = e.clientY ?? (e.touches && e.touches[0] ? e.touches[0].clientY : 0);
    mouse.x = (x / window.innerWidth) * 2 - 1;
    mouse.y = -(y / window.innerHeight) * 2 + 1;
  }};
  document.addEventListener('mousemove', onPointerMove, {{ passive: true }});
  document.addEventListener('touchmove', onPointerMove, {{ passive: true }});
  document.addEventListener('mouseenter', () => {{ mouseInScene = true; }}, {{ passive: true }});
  document.addEventListener('mouseleave', () => {{ mouseInScene = false; }}, {{ passive: true }});
  document.addEventListener('touchstart', (e) => {{ mouseInScene = true; mousePressed = true; onPointerMove(e); }}, {{ passive: true }});
  document.addEventListener('touchend',   () => {{ mousePressed = false; mouseInScene = false; }}, {{ passive: true }});
  document.addEventListener('visibilitychange', () => {{
    pageVisible = !document.hidden;
    if (document.hidden) mouseInScene = false;
  }});
  document.addEventListener('mousedown', () => {{ mousePressed = true; }}, {{ passive: true }});
  document.addEventListener('mouseup',   () => {{ mousePressed = false; }}, {{ passive: true }});

  // ============ RAYMARCHING QUAD (PINK PALETTE) ============
  const quadGeometry = new THREE.PlaneGeometry(2, 2);
  const quadMaterial = new THREE.ShaderMaterial({{
    uniforms: {{
      uTime: {{ value: 0 }},
      uResolution: {{ value: new THREE.Vector2(size.width, size.height) }},
      uCameraPos: {{ value: camera.position.clone() }},
      uCameraTarget: {{ value: new THREE.Vector3(0, 0, 0) }},
      uPixelRatio: {{ value: Math.min(window.devicePixelRatio, 1.5) }},
      uGooeyness: {{ value: settings.scene.gooeyness }},
      uSpeed: {{ value: settings.scene.speed }},
      uMouseSpherePos: {{ value: new THREE.Vector3(0, 0, 0) }},
      uMouseSphereRadius: {{ value: 0.0 }},
    }},
    vertexShader: `
      varying vec2 vUv;
      void main() {{
        vUv = uv;
        gl_Position = vec4(position, 1.0);
      }}
    `,
    fragmentShader: `
      precision highp float;
      #define MARCH_STEPS ` + quality.marchSteps + `
      #define AO_STEPS ` + quality.aoSteps + `
      uniform float uTime;
      uniform vec2 uResolution;
      uniform vec3 uCameraPos;
      uniform vec3 uCameraTarget;
      uniform float uPixelRatio;
      uniform float uGooeyness;
      uniform float uSpeed;
      uniform vec3 uMouseSpherePos;
      uniform float uMouseSphereRadius;
      varying vec2 vUv;

      float smin(float a, float b, float k) {{
        float h = clamp(0.5 + 0.5*(b-a)/k, 0.0, 1.0);
        return mix(b, a, h) - k*h*(1.0-h);
      }}
      float sdSphere(vec3 p, vec3 c, float r) {{ return length(p-c)-r; }}

      float sceneCompound(vec3 p, float t, float k) {{
        float a1 = t*0.5, a2 = t*0.5 + 3.14159;
        vec3 c1 = vec3(cos(a1)*2.4 + sin(t*0.25)*0.3, sin(a1*0.6)*0.8 + cos(t*0.4)*0.2, sin(a1*0.35)*0.6);
        vec3 c2 = vec3(cos(a2)*2.4 + sin(t*0.3)*0.3,  sin(a2*0.6)*0.8 - cos(t*0.35)*0.2, sin(a2*0.35)*0.6);
        float s1 = sdSphere(p, c1, 1.2 + 0.07*sin(t*2.5));
        float s2 = sdSphere(p, c2, 1.05 + 0.07*cos(t*2.0));
        vec3 c3 = c1 + vec3(sin(t*1.8)*0.9, cos(t*2.2)*0.9, sin(t*1.5)*0.6);
        vec3 c4 = c2 + vec3(-cos(t*1.5)*0.8, sin(t*1.9)*0.8, -cos(t*1.7)*0.5);
        float s3 = sdSphere(p, c3, 0.55);
        float s4 = sdSphere(p, c4, 0.5);
        vec3 c5 = vec3(sin(t*0.7)*3.0, cos(t*0.55)*1.2, cos(t*0.45)*0.7);
        vec3 c6 = vec3(-cos(t*0.65)*2.8, sin(t*0.75)*1.0, sin(t*0.5)*0.8);
        float s5 = sdSphere(p, c5, 0.6);
        float s6 = sdSphere(p, c6, 0.55);
        float d = smin(s1, s2, k);
        d = smin(d, s3, k*0.7);
        d = smin(d, s4, k*0.7);
        d = smin(d, s5, k*0.8);
        d = smin(d, s6, k*0.8);
        return d;
      }}

      float sceneSDF(vec3 p) {{
        float t = uTime*uSpeed;
        float k = uGooeyness;
        float d = sceneCompound(p, t, k);
        if (uMouseSphereRadius > 0.001) {{
          float ms = sdSphere(p, uMouseSpherePos, uMouseSphereRadius);
          d = smin(d, ms, k*0.8);
        }}
        return d;
      }}
      vec3 calcNormal(vec3 p) {{
        const float eps = 0.001;
        vec2 h = vec2(eps, 0.0);
        return normalize(vec3(
          sceneSDF(p+h.xyy) - sceneSDF(p-h.xyy),
          sceneSDF(p+h.yxy) - sceneSDF(p-h.yxy),
          sceneSDF(p+h.yyx) - sceneSDF(p-h.yyx)
        ));
      }}
      float calcAO(vec3 pos, vec3 nor) {{
        float occ = 0.0; float sca = 1.0;
        for (int i=0; i<AO_STEPS; i++) {{
          float h = 0.02 + 0.15*float(i);
          float d = sceneSDF(pos + h*nor);
          occ += (h-d)*sca;
          sca *= 0.9;
        }}
        return clamp(1.0 - 3.0*occ, 0.0, 1.0);
      }}
      float fresnel(vec3 v, vec3 n, float p) {{
        return pow(1.0 - max(dot(v, n), 0.0), p);
      }}
      float cheapShadow(vec3 pos, vec3 lightDir) {{
        float d1 = sceneSDF(pos + lightDir*0.15);
        float d2 = sceneSDF(pos + lightDir*0.4);
        float d3 = sceneSDF(pos + lightDir*0.8);
        return clamp(0.3 + 0.7*smoothstep(0.0, 0.3, min(min(d1,d2),d3)), 0.0, 1.0);
      }}
      mat3 setCamera(vec3 ro, vec3 ta, float cr) {{
        vec3 cw = normalize(ta-ro);
        vec3 cp = vec3(sin(cr), cos(cr), 0.0);
        vec3 cu = normalize(cross(cw, cp));
        vec3 cv = normalize(cross(cu, cw));
        return mat3(cu, cv, cw);
      }}

      void main() {{
        vec2 fragCoord = vUv * uResolution;
        vec2 uv = (2.0*fragCoord - uResolution) / uResolution.y;
        vec3 ro = uCameraPos;
        vec3 ta = uCameraTarget;
        mat3 ca = setCamera(ro, ta, 0.0);
        vec3 rd = ca * normalize(vec3(uv, 1.8));
        float t = 0.0;
        float d;
        vec3 p;
        bool hit = false;
        for (int i=0; i<MARCH_STEPS; i++) {{
          p = ro + rd*t;
          d = sceneSDF(p);
          if (d < 0.002) {{ hit = true; break; }}
          t += d*0.9;
          if (t > 15.0) break;
        }}
        // Soft pink background gradient
        vec3 col = vec3(0.99, 0.93, 0.94);
        col += vec3(-0.03, -0.02, -0.01) * (1.0 - uv.y*0.5);
        if (hit) {{
          vec3 nor = calcNormal(p);
          vec3 viewDir = normalize(ro-p);
          vec3 lightPos1 = vec3(3.0, 4.0, 5.0);
          vec3 lightPos2 = vec3(-4.0, 2.0, -3.0);
          vec3 lightDir1 = normalize(lightPos1-p);
          vec3 lightDir2 = normalize(lightPos2-p);
          float diff1 = max(dot(nor, lightDir1), 0.0);
          float diff2 = max(dot(nor, lightDir2), 0.0);
          vec3 halfDir1 = normalize(lightDir1+viewDir);
          vec3 halfDir2 = normalize(lightDir2+viewDir);
          float spec1 = pow(max(dot(nor, halfDir1), 0.0), 64.0);
          float spec2 = pow(max(dot(nor, halfDir2), 0.0), 32.0);
          float sha1 = cheapShadow(p + nor*0.01, lightDir1);
          float sha2 = cheapShadow(p + nor*0.01, lightDir2);
          float ao = calcAO(p, nor);
          float fres = fresnel(viewDir, nor, 3.0);
          float sss = max(0.0, dot(viewDir, -lightDir1)) * 0.3;
          // Beauty palette: rose / peach / coral
          vec3 baseColor1 = vec3(0.90, 0.40, 0.50);  // deep rose
          vec3 baseColor2 = vec3(0.98, 0.78, 0.78);  // soft pink
          vec3 baseColor3 = vec3(0.97, 0.62, 0.55);  // coral
          float mix1 = sin(p.x*1.5 + uTime*0.5)*0.5 + 0.5;
          float mix2 = cos(p.y*2.0 - uTime*0.3)*0.5 + 0.5;
          vec3 baseColor = mix(baseColor1, baseColor2, mix1);
          baseColor = mix(baseColor, baseColor3, mix2*0.35);
          vec3 diffuse = baseColor * (diff1*sha1*vec3(1.0, 0.97, 0.93)*0.85 + diff2*sha2*vec3(0.9, 0.7, 0.72)*0.4);
          vec3 specular = vec3(1.0, 0.95, 0.92)*spec1*sha1*0.65 + vec3(1.0, 0.85, 0.85)*spec2*sha2*0.3;
          vec3 ambient = baseColor * vec3(0.18, 0.14, 0.14) * ao;
          vec3 rim = mix(vec3(1.0, 0.75, 0.8), vec3(1.0, 0.5, 0.6), mix1) * fres * 0.55;
          vec3 subsurface = baseColor * sss * vec3(1.0, 0.4, 0.45);
          col = ambient + diffuse + specular + rim + subsurface;
          // Subtle iridescence
          float iri = fres*0.3;
          vec3 iriCol = vec3(
            sin(dot(nor, vec3(1.0,0.0,0.0))*6.0 + uTime)*0.5 + 0.5,
            sin(dot(nor, vec3(0.0,1.0,0.0))*6.0 + uTime*1.3)*0.5 + 0.5,
            sin(dot(nor, vec3(0.0,0.0,1.0))*6.0 + uTime*0.7)*0.5 + 0.5
          );
          col += iriCol * iri * 0.6;
        }}
        col = col / (col + vec3(1.0));
        col = pow(col, vec3(1.0/2.2));
        float vig = 1.0 - 0.12 * dot(uv*0.5, uv*0.5);
        col *= vig;
        gl_FragColor = vec4(col, 1.0);
      }}
    `,
    depthWrite: false,
    depthTest: false
  }});

  const quad = new THREE.Mesh(quadGeometry, quadMaterial);
  quad.frustumCulled = false;
  const quadScene = new THREE.Scene();
  const quadCamera = new THREE.OrthographicCamera(-1, 1, 1, -1, 0, 1);
  quadScene.add(quad);

  // ============ DOT-MATRIX SHADER (pink background, dark-rose dots) ============
  const DotMatrixShader = {{
    uniforms: {{
      tDiffuse: {{ value: null }},
      uResolution: {{ value: new THREE.Vector2(size.width, size.height) }},
      uDotSize: {{ value: settings.dither.dotSize }},
      uDotGap:  {{ value: settings.dither.dotGap }},
      uBrightness: {{ value: settings.dither.brightness }},
      uContrast:   {{ value: settings.dither.contrast }},
      uThreshold:  {{ value: 0.03 }},
      uDotColor: {{ value: new THREE.Vector3(0.24, 0.12, 0.14) }},   // dark rose
      uBgColor:  {{ value: new THREE.Vector3(0.99, 0.93, 0.94) }},   // soft pink
      uDitherEnabled: {{ value: 1.0 }},
      uTime: {{ value: 0 }}
    }},
    vertexShader: `
      varying vec2 vUv;
      void main() {{ vUv = uv; gl_Position = vec4(position, 1.0); }}
    `,
    fragmentShader: `
      precision highp float;
      uniform sampler2D tDiffuse;
      uniform vec2 uResolution;
      uniform float uDotSize, uDotGap, uBrightness, uContrast, uThreshold;
      uniform vec3 uDotColor, uBgColor;
      uniform float uDitherEnabled;
      varying vec2 vUv;

      void main() {{
        vec2 uv = vUv;
        vec3 scene = texture2D(tDiffuse, uv).rgb;
        if (uDitherEnabled < 0.5) {{
          gl_FragColor = vec4(scene, 1.0);
          return;
        }}
        vec2 px = uv * uResolution;
        float sp = uDotSize + uDotGap;
        vec2 cell = floor(px / sp);
        vec2 center = (cell + 0.5) * sp;
        vec2 sUV = center / uResolution;
        vec3 c = texture2D(tDiffuse, sUV).rgb;
        // Invert so BRIGHT scene pixels (blobs) become LARGER dark-rose dots
        // on soft pink background.
        float lum = dot(c, vec3(0.299, 0.587, 0.114)) * uBrightness;
        lum = clamp((lum - 0.5) / uContrast + 0.5, 0.0, 1.0);
        // Emphasize blob intensity: use distance from bg lum
        float bgLum = dot(uBgColor, vec3(0.299, 0.587, 0.114));
        float contrastToBg = clamp(abs(lum - bgLum) * 3.0, 0.0, 1.0);
        if (contrastToBg < uThreshold) {{
          gl_FragColor = vec4(uBgColor, 1.0);
          return;
        }}
        float maxR = uDotSize * 0.5;
        float r = mix(0.3, maxR, pow(contrastToBg, uContrast));
        vec2 d = px - center;
        float dist = length(d);
        float mask = 1.0 - smoothstep(r - 0.5, r + 0.5, dist);
        // Tint dots with a touch of the scene color for softness
        vec3 tintedDot = mix(uDotColor, c * 0.6 + uDotColor*0.4, 0.3);
        vec3 result = mix(uBgColor, tintedDot, mask);
        gl_FragColor = vec4(result, 1.0);
      }}
    `
  }};

  // ============ POST-PROCESSING ============
  const composer = new EffectComposer(renderer);
  composer.setSize(size.width, size.height);
  composer.addPass(new RenderPass(quadScene, quadCamera));
  const dotMatrixPass = new ShaderPass(DotMatrixShader);
  composer.addPass(dotMatrixPass);
  dotMatrixPass.uniforms.uResolution.value.set(size.width, size.height);

  // ============ SCROLL PARALLAX ============
  let scrollY = 0;
  let smoothScrollY = 0;
  window.addEventListener('scroll', () => {{ scrollY = window.scrollY; }}, {{ passive: true }});

  // ============ ANIMATION LOOP ============
  const clock = new THREE.Clock();
  const raycaster = new THREE.Raycaster();
  const _forward = new THREE.Vector3();
  let resizeTimeout = null;

  function animate() {{
    if (!pageVisible) return;
    const dt = Math.min(clock.getDelta(), 0.05);
    const elapsed = clock.elapsedTime;

    const targetR = mouseInScene ? (mousePressed ? mouseSphereClickRadius : mouseSphereTargetRadius) : 0.0;
    const fadeSpeed = mouseInScene ? (mousePressed ? 10.0 : 6.0) : 3.0;
    const step = Math.min(1.0, fadeSpeed * dt);
    mouseSphereRadius += (targetR - mouseSphereRadius) * step;
    if (mouseSphereRadius < 0.005 && !mouseInScene) mouseSphereRadius = 0.0;

    // Mouse -> world projection
    raycaster.setFromCamera(mouse, camera);
    const rayDir = raycaster.ray.direction;
    const rayOrigin = raycaster.ray.origin;
    _forward.subVectors(new THREE.Vector3(0,0,0), camera.position).normalize();
    const dist = camera.position.length();
    const tr = dist / rayDir.dot(_forward);
    mouseWorldTarget.copy(rayOrigin).addScaledVector(rayDir, tr);
    mouseWorld.lerp(mouseWorldTarget, mouseDamping);

    // Smooth scroll parallax
    smoothScrollY += (scrollY - smoothScrollY) * 0.1;
    const vh = window.innerHeight;
    const scrollProgress = Math.min(smoothScrollY / vh, 1.0);
    camera.position.y = scrollProgress * 1.5;
    camera.position.z = 5 + scrollProgress * 0.8;

    quadMaterial.uniforms.uMouseSpherePos.value.copy(mouseWorld);
    quadMaterial.uniforms.uMouseSphereRadius.value = mouseSphereRadius;
    quadMaterial.uniforms.uTime.value = elapsed;
    quadMaterial.uniforms.uCameraPos.value.copy(camera.position);
    dotMatrixPass.uniforms.uTime.value = elapsed;

    composer.render();
  }}
  renderer.setAnimationLoop(animate);

  // ============ RESIZE ============
  function handleResize() {{
    size = {{ width: window.innerWidth, height: window.innerHeight }};
    camera.aspect = size.width / size.height;
    camera.updateProjectionMatrix();
    const pr = Math.min(window.devicePixelRatio, quality.pixelRatio);
    renderer.setPixelRatio(pr);
    renderer.setSize(size.width, size.height);
    quadMaterial.uniforms.uResolution.value.set(size.width, size.height);
    quadMaterial.uniforms.uPixelRatio.value = pr;
    dotMatrixPass.uniforms.uResolution.value.set(size.width, size.height);
    composer.setSize(size.width, size.height);
  }}
  window.addEventListener('resize', () => {{
    clearTimeout(resizeTimeout);
    renderer.domElement.style.width = window.innerWidth + 'px';
    renderer.domElement.style.height = window.innerHeight + 'px';
    resizeTimeout = setTimeout(handleResize, 200);
  }}, {{ passive: true }});
</script>

<!-- ========= UI SCRIPT (navigation, smooth scroll, reveal, entrance) ========= -->
<script>
document.addEventListener('DOMContentLoaded', function() {{
  // Mobile menu
  const hamburger = document.getElementById('hamburger');
  const mobileMenu = document.getElementById('mobile-menu');
  hamburger.addEventListener('click', () => {{
    hamburger.classList.toggle('open');
    mobileMenu.classList.toggle('open');
  }});
  mobileMenu.querySelectorAll('a').forEach(link => {{
    link.addEventListener('click', () => {{
      hamburger.classList.remove('open');
      mobileMenu.classList.remove('open');
    }});
  }});

  // Nav scrolled state
  const mainNav = document.querySelector('.nav');
  window.addEventListener('scroll', () => {{
    mainNav.classList.toggle('scrolled', window.scrollY > 80);
  }}, {{ passive: true }});

  // Trigger .visible on .reveal elements currently in viewport
  function triggerVisibleReveals() {{
    document.querySelectorAll('.reveal:not(.visible)').forEach(el => {{
      const rect = el.getBoundingClientRect();
      if (rect.top < window.innerHeight && rect.bottom > 0) {{
        el.classList.add('visible');
      }}
    }});
  }}

  // Smooth scroll with reveal trigger on completion
  function smoothScrollTo(targetY, duration) {{
    const startY = window.scrollY;
    const diff = targetY - startY;
    const startTime = performance.now();
    function ease(t) {{ return t<0.5 ? 4*t*t*t : 1 - Math.pow(-2*t+2, 3)/2; }}
    function step(now) {{
      const elapsed = now - startTime;
      const p = Math.min(elapsed / duration, 1);
      window.scrollTo(0, startY + diff * ease(p));
      if (p < 1) {{
        requestAnimationFrame(step);
      }} else {{
        // Scroll finished — force-reveal anything now in view
        triggerVisibleReveals();
      }}
    }}
    requestAnimationFrame(step);
  }}

  // All internal hash links with smooth scroll
  document.querySelectorAll('a[href^="#"]').forEach(link => {{
    link.addEventListener('click', function(e) {{
      const href = this.getAttribute('href');
      if (!href || href === '#') return;
      const target = document.querySelector(href);
      if (!target) return;
      e.preventDefault();
      const navH = 80;
      const targetY = target.getBoundingClientRect().top + window.scrollY - navH;
      smoothScrollTo(targetY, 900);
    }});
  }});

  // Scroll reveal via IntersectionObserver — fires 150px before element enters viewport
  const revealObs = new IntersectionObserver((entries) => {{
    entries.forEach(e => {{ if (e.isIntersecting) e.target.classList.add('visible'); }});
  }}, {{ threshold: 0.01, rootMargin: '150px 0px' }});
  document.querySelectorAll('.reveal').forEach(el => revealObs.observe(el));

  // Immediate reveal for elements visible on page load
  triggerVisibleReveals();
  setTimeout(triggerVisibleReveals, 400);

  // Also trigger reveals on manual scroll (throttled)
  let scrollThrottle = false;
  window.addEventListener('scroll', () => {{
    if (!scrollThrottle) {{
      scrollThrottle = true;
      requestAnimationFrame(() => {{ triggerVisibleReveals(); scrollThrottle = false; }});
    }}
  }}, {{ passive: true }});

  // Entrance animation
  requestAnimationFrame(() => requestAnimationFrame(() => {{
    document.getElementById('crt-frame').classList.add('visible');
    document.querySelector('.hero-fade').classList.add('anim-in');
    document.querySelector('.hero-fade-top').classList.add('anim-in');
    document.querySelector('.nav-brand').classList.add('anim-in');
    document.querySelectorAll('.nav-links a').forEach(el => el.classList.add('anim-in'));
    document.querySelector('.nav-hamburger').classList.add('anim-in');
    document.querySelector('.hero-h1').classList.add('anim-in');
    document.querySelector('.hero-sub').classList.add('anim-in');
    document.querySelector('.hero-actions').classList.add('anim-in');
    document.querySelectorAll('.hero-stat').forEach(el => el.classList.add('anim-in'));
  }}));
}});
</script>
</body>
</html>"""
