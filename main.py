#!/usr/bin/env python3
"""
Beauty Website Generator — Nail1 Edition
Entry point: collects business info via CLI, then runs the generation pipeline.
"""
import os
import sys
from dotenv import load_dotenv

load_dotenv()

from agents.nail_beauty import run_nail_beauty_agent


def ask(question: str, default: str = "") -> str:
    """Ask a question in terminal, return answer (or default if empty)."""
    hint = f" [{default}]" if default else ""
    try:
        answer = input(f"{question}{hint}: ").strip()
    except (KeyboardInterrupt, EOFError):
        print("\n\nОтменено.")
        sys.exit(0)
    return answer if answer else default


def print_header():
    print("\n" + "=" * 56)
    print("   ГЕНЕРАТОР САЙТОВ ДЛЯ БЬЮТИ-МАСТЕРОВ")
    print("   Стиль: Dark Science Lab")
    print("   Powered by Claude AI")
    print("=" * 56)


def collect_business_info() -> dict:
    print("\n📋 Расскажите о вашем бизнесе:")
    print("   (нажмите Enter чтобы использовать значение по умолчанию)\n")

    info = {}
    info["master_name"] = ask("Имя мастера или название студии")
    while not info["master_name"]:
        print("   ⚠️  Это поле обязательное")
        info["master_name"] = ask("Имя мастера или название студии")

    info["city"] = ask("Город", "Москва")
    info["address"] = ask("Улица и дом (или Enter пропустить)", "")

    print("\n💅 Услуги (через запятую):")
    info["services"] = ask(
        "Услуги",
        "Маникюр, Педикюр, Наращивание ногтей, Гель-лак, Дизайн ногтей"
    )

    print("\n📊 Статистика для сайта:")
    info["experience_years"] = ask("Лет опыта", "5")
    info["clients_count"] = ask("Довольных клиентов", "500")
    info["works_count"] = ask("Выполненных работ", "2000")

    print("\n📱 Контакты:")
    info["phone"] = ask("Телефон", "+7 (999) 000-00-00")
    info["instagram"] = ask("Instagram без @ (или Enter пропустить)", "")
    info["telegram"] = ask("Telegram без @ (или Enter пропустить)", "")

    return info


def main():
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("\n❌ Ошибка: не найден ANTHROPIC_API_KEY")
        print("   Создайте файл .env и добавьте:")
        print("   ANTHROPIC_API_KEY=ваш_ключ_api")
        print("   Получить ключ: https://console.anthropic.com/")
        sys.exit(1)

    print_header()

    business_info = collect_business_info()

    print("\n" + "-" * 56)
    print(f"🚀 Запускаю генерацию сайта для «{business_info['master_name']}»")
    print("   Подождите 30–60 секунд...\n")

    try:
        output_path = run_nail_beauty_agent(business_info)
    except Exception as e:
        print(f"\n❌ Ошибка при генерации: {e}")
        sys.exit(1)

    print("\n" + "=" * 56)
    print(f"✅ ГОТОВО!")
    print(f"\n📁 Папка с сайтом:")
    print(f"   {output_path}")
    print(f"\n🌐 Превью сайта:")
    print(f"   {output_path}/preview/index.html")
    print(f"\n📦 WordPress тема:")
    print(f"   {output_path}/wordpress-theme/")
    print(f"   (+ ZIP архив для загрузки в WP)")
    print("=" * 56)
    print()

    os.system(f'open "{output_path}"')
    preview = os.path.join(output_path, "preview", "index.html")
    os.system(f'open "{preview}"')


if __name__ == "__main__":
    main()
