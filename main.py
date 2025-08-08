import os
import asyncio
import google.generativeai as genai
import telegram

# Список профессий для выбора
PROFESSIONS = [
    "Директор по электронной коммерции", "Руководитель отдела по работе с маркетплейсами",
    "Менеджер по работе с маркетплейсами", "Аккаунт-менеджер маркетплейсов",
    "Контент-менеджер", "Аналитик маркетплейсов", "E-commerce аналитик",
    "Специалист по продвижению на маркетплейсах", "Менеджер по трафику",
    "Специалист по ценообразованию", "Интернет-маркетолог", "Бренд-менеджер",
    "SEO-специалист", "SMM-менеджер", "Руководитель склада", "Начальник отдела логистики",
    "Специалист по фулфилменту", "Специалист по управлению товарными запасами",
    "Кладовщик", "Сборщик заказов", "Специалист по маркировке",
    "Финансовый менеджер / Аналитик", "Бухгалтер", "Менеджер по работе с клиентами",
    "Специалист службы поддержки", "Категорийный менеджер", "Менеджер по закупкам",
    "Юрист", "Менеджер ozon", "Менеджер wildberries", "директор по маркетингу"
]

def get_gemini_response(api_key, prompt):
    """Запрашивает уникальный текст у Gemini с использованием официальной библиотеки."""
    try:
        print("1. Конфигурирую Gemini API...")
        genai.configure(api_key=api_key)
        
        # --- ИЗМЕНЕНИЕ ЗДЕСЬ: Используем модель Flash ---
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        
        print("2. Отправляю запрос в Gemini (модель Flash)...")
        response = model.generate_content(prompt)
        
        if response.text:
            print("3. Ответ от Gemini успешно получен.")
            return response.text.strip()
        else:
            # Добавим вывод для отладки, если ответ пустой
            print(f"Ошибка: Gemini вернул пустой ответ. Причина блокировки: {response.prompt_feedback.block_reason}")
            return None
            
    except Exception as e:
        print(f"Произошла ошибка при работе с Gemini API: {e}")
        return None

async def post_to_telegram(bot_token, channel_id, text_to_post):
    """Отправляет сообщение в Telegram-канал."""
    if not text_to_post:
        print("Текст для поста пустой. Публикация отменена.")
        return False
    
    try:
        print("4. Инициализирую Telegram-бота...")
        bot = telegram.Bot(token=bot_token)
        
        print(f"5. Отправляю сообщение в канал {channel_id}...")
        await bot.send_message(
            chat_id=channel_id,
            text=text_to_post,
            parse_mode='HTML'
        )
        print("6. Сообщение успешно отправлено в Telegram!")
        return True
        
    except Exception as e:
        print(f"Произошла ошибка при отправке в Telegram: {e}")
        return False

async def main():
    """Главная асинхронная функция, которая запускает весь процесс."""
    gemini_key = os.getenv("GEMINI_API_KEY")
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    channel_id = os.getenv("TELEGRAM_CHANNEL_ID")
    run_number_str = os.getenv("GITHUB_RUN_NUMBER", "1")
    run_number = int(run_number_str)
    
    profession_index = (run_number - 1) % len(PROFESSIONS)
    selected_profession = PROFESSIONS[profession_index]
    print(f"Номер запуска: {run_number}. Выбрана профессия: '{selected_profession}'")

    if not all([gemini_key, bot_token, channel_id]):
        print("Критическая ошибка: Не найдены все секреты...")
        return

    prompt = f"""
ROLE: Expert recruiter and storyteller.
CONTEXT: Write for HeroHunter recruitment agency's Telegram channel. Audience: HR directors and team leads in Moscow.
TASK: Create a compelling, plausible, success story about finding a {selected_profession}, avoid Splashy phrases.
LANGUAGE: russian
STRUCTURE:
🎯 Headline: "found [profession] in Moscow in (8,9,10,11,12,13,14) days"
🤔 Problem: Specific client pain (project scaling, increase in work volume, business growth)
💡 Solution: Our unique approach (where we searched, how we convinced)
📞 CTA: Natural call-to-action with https://herohunter.ru/
RULES:
- Max 700 characters
- Use 4-5 relevant emojis
- Include specific details: timeframes (8,9,10,11,12,13,14 days) 
- Mention one concrete search method (open search on job sites, partner recommendations)
- No lists or bullet points
TONE: Confident professional who knows recruitment secrets.
AVOID: Splashy phrases, Generic phrases like "individual approach", "comprehensive solution".
"""
    
    post_text = get_gemini_response(gemini_key, prompt)
    
    if post_text:
        await post_to_telegram(bot_token, channel_id, post_text)

if __name__ == "__main__":
    asyncio.run(main())
