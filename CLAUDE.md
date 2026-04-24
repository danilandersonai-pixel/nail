# CLAUDE.md

Инструкции для Claude Code при работе с этим проектом.

## Что это за проект

CLI-система на Python, которая генерирует сайты для бьюти-мастеров
(маникюр, педикюр, наращивание) в эстетике **«Dark Science Lab»**:

- Тёмный фон (#020203) — как в оригинальном шаблоне nail1
- Шрифты: Instrument Serif (заголовки) + Geist (тело) — точно как в шаблоне
- Three.js анимация частиц с соединительными линиями (из CDN r128)
- Плавные анимации появления, hover-эффекты, мобильное меню
- 7 секций: Hero → О мастере → Услуги → Цены → Отзывы → Контакты → Footer

Тексты генерируются через Anthropic Claude API. На выходе — превью-HTML
и WordPress-тема с ZIP-архивом.

## Как запускать

```bash
# Установить зависимости (один раз)
pip3 install -r requirements.txt

# Запустить генератор
python3 main.py
```

Перед первым запуском: скопировать `.env.example` → `.env` и вставить
`ANTHROPIC_API_KEY`.

## Архитектура: цепочка агентов

```
main.py
  └── agents/nail_beauty.py          # оркестратор ниши
        ├── agents/content_writer.py  # Claude API → тексты (JSON)
        ├── agents/html_builder.py    # тексты → единый HTML (ink on paper)
        └── agents/wp_packager.py     # HTML → WordPress тема + ZIP
```

`main.py` собирает данные через CLI-диалог, затем вызывает
`run_nail_beauty_agent(business_info)`.

## Что делает каждый агент

**`content_writer.generate_content(client, business_info)`**
- Принимает: `anthropic.Anthropic` + словарь `business_info`
- Отдаёт: словарь `content` с секциями `hero / about / services / prices / contact / footer` (и др.)
- Один вызов Claude API, ответ всегда JSON

**`html_builder.build_html(business_info, content, theme_key="1")`**
- Принимает: данные бизнеса, контент, номер темы (игнорируется — стиль один)
- Отдаёт: строку с полным HTML (CSS + Three.js-JS встроены)
- Claude API не вызывает — чистая Python-сборка по шаблону
- **Важно**: параметр `theme_key` сохранён только ради совместимости сигнатуры.
  Визуальный стиль один: «чернила на бумаге», без вариаций

**`wp_packager.package_wordpress_theme(output_dir, html, business_info, content)`**
- Создаёт `wordpress-theme/` (PHP-файлы) + ZIP-архив
- Транслитерация кириллицы в slug через словарь `_cyr` внутри функции

## Структура output/

```
output/
  [slug-мастера]/
    preview/index.html          # открыть в браузере
    wordpress-theme/            # PHP-тема для WP
    [slug]-theme.zip            # готов к загрузке в WordPress
```

## Анимации и визуал

Генерируемый HTML использует **Three.js r128** через CDN
(`cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js`). Локальная
установка не нужна. Все эффекты встроены в один HTML-файл.

Ключевые компоненты в `html_builder.py`:
- `createBranch / createInkLeaf / createPlantCluster` — процедурная
  генерация чернильных растений (рекурсивные ветки + листья с контуром)
- `createCrosshatchGround` — плоскость с короткими штрихами (эффект кросс-хатча)
- `createFloatingParticles` — парящие чёрные точки
- `animate` — покачивание растений, дрейф камеры вперёд по скроллу,
  плавание частиц

Механика станций:
- `#scroll-spacer` задаёт 500vh невидимой высоты — это даёт дистанцию скролла
- Контент в `#content-layer` зафиксирован (`position: fixed`)
- `onScroll` считает, какая станция активна (0–4), и переключает класс
  `.active` — это запускает cross-fade через CSS `transition: opacity`
- Камера в 3D-сцене тоже едет вперёд вместе со скроллом

## Добавление новой ниши

1. Создать `agents/новая_ниша.py` с функцией `run_новая_ниша_agent(business_info) -> str`
2. Добавить нишу в словарь `NICHES` в `main.py`
3. При необходимости расширить или заменить станции в `html_builder.py`

## Ключевые ограничения

- `html_builder.py` не вызывает Claude — только подставляет данные в шаблон
- `content_writer.py` генерирует цены-заглушки автоматически по ключевым
  словам в названиях услуг
- WordPress-тема работает без плагинов, но требует WordPress 5.0+

## Язык пользователя

Владелец — не разработчик (vibe coder).
**Объяснения всегда на русском, простым языком, без программистского жаргона.**
Перед любым изменением — объяснить что и зачем.
