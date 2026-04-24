"""
Content Writer Agent
Uses Claude to generate Russian marketing copy for nail/beauty master websites.
"""
import json
import anthropic

SYSTEM_PROMPT = """You are an expert Russian copywriter specializing in beauty industry websites.
You write for nail masters, beauty salons, and wellness studios.

Your copy is:
- Warm and personal (speaks directly to the client)
- Professional but approachable
- Focused on results, emotions, and trust
- Always 100% in Russian

Always respond with valid JSON only, no markdown, no extra text."""


def generate_content(client: anthropic.Anthropic, business_info: dict) -> dict:
    """
    Calls Claude to generate all text content for the website.
    Returns a dict with content for each section.
    """
    services_raw = business_info.get("services", "Маникюр, Педикюр, Наращивание")
    services_list = [s.strip() for s in services_raw.split(",")]

    prices_default = []
    for service in services_list:
        service_lower = service.lower()
        if "маникюр" in service_lower:
            prices_default.append({"name": service, "price": "от 1 500 ₽"})
        elif "педикюр" in service_lower:
            prices_default.append({"name": service, "price": "от 2 000 ₽"})
        elif "наращ" in service_lower:
            prices_default.append({"name": service, "price": "от 3 000 ₽"})
        elif "гель" in service_lower or "покрыт" in service_lower:
            prices_default.append({"name": service, "price": "от 1 200 ₽"})
        elif "дизайн" in service_lower:
            prices_default.append({"name": service, "price": "от 300 ₽"})
        else:
            prices_default.append({"name": service, "price": "уточняйте"})

    prompt = f"""Create professional website content for a nail/beauty master.

Business details:
- Name: {business_info['master_name']}
- Services: {', '.join(services_list)}
- City: {business_info.get('city', 'ваш город')}
- Experience: {business_info.get('experience_years', '5')} years
- Happy clients: {business_info.get('clients_count', '500')}+
- Works completed: {business_info.get('works_count', '2000')}+

Return ONLY valid JSON with this exact structure:

{{
  "hero": {{
    "headline": "short powerful headline 5-8 words in Russian",
    "subheadline": "1-2 sentences about key benefits in Russian",
    "cta_button": "3-4 word button text, e.g. 'Записаться на приём'"
  }},
  "about": {{
    "title": "section title, e.g. 'О мастере'",
    "text": "3-4 warm sentences about the master in Russian",
    "badge1_label": "label under years number, e.g. 'лет опыта'",
    "badge2_label": "label under clients number, e.g. 'довольных клиентов'",
    "badge3_label": "label under works number, e.g. 'выполненных работ'"
  }},
  "services": {{
    "title": "section title",
    "subtitle": "1 sentence description",
    "items": [
      {{"name": "service name", "description": "1 sentence benefit-focused description", "emoji": "relevant emoji"}}
    ]
  }},
  "prices": {{
    "title": "section title",
    "subtitle": "1 sentence",
    "note": "short note about pricing, e.g. 'Точную стоимость уточняйте при записи'",
    "items": {json.dumps(prices_default, ensure_ascii=False)}
  }},
  "reviews": {{
    "title": "section title",
    "subtitle": "1 sentence",
    "items": [
      {{"name": "Russian female name + last initial", "text": "genuine 2-3 sentence review", "service": "service name", "rating": 5}},
      {{"name": "Russian female name + last initial", "text": "genuine 2-3 sentence review", "service": "service name", "rating": 5}},
      {{"name": "Russian female name + last initial", "text": "genuine 2-3 sentence review", "service": "service name", "rating": 5}}
    ]
  }},
  "contact": {{
    "title": "section title",
    "subtitle": "1 sentence call-to-action"
  }},
  "footer": {{
    "tagline": "short tagline 3-5 words"
  }}
}}

For services.items generate one item for each of: {', '.join(services_list)}
Make reviews sound genuine and specific, not generic."""

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=4000,
        system=[{
            "type": "text",
            "text": SYSTEM_PROMPT,
            "cache_control": {"type": "ephemeral"}
        }],
        messages=[{"role": "user", "content": prompt}]
    )

    raw = response.content[0].text.strip()

    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
        raw = raw.strip()

    return json.loads(raw)
