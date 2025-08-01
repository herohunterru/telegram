import os
import asyncio
import google.generativeai as genai
import telegram

# --- НОВАЯ ЧАСТЬ: Список профессий ---
# Мы вынесли все профессии в список. Скрипт будет выбирать одну по порядку.
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
    """Запрашивает уникальный текст у Gemini."""
    try:
        print("1. Конфигурирую Gemini API...")
        genai.configure(api_key=api_key)
        # Новый, правильный код
        model = genai.GenerativeModel('gemini-1.5-latest')
        
        print(f"2. Отправляю запрос в Gemini...")
        response = model.generate_content(prompt)
        
        if response.text:
            print("3. Ответ от Gemini успешно получен.")
            return response.text.strip()
        else:
            print("Ошибка: Gemini вернул пустой ответ.")
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
        # Используем HTML для более надежного форматирования ссылок
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
    
    # --- НОВАЯ ЧАСТЬ: Получаем номер запуска от GitHub Actions ---
    # Это наш способ "помнить", какой пост был последним.
    run_number_str = os.getenv("GITHUB_RUN_NUMBER", "1")
    run_number = int(run_number_str)
    
    # Выбираем профессию из списка, циклически переходя к следующей при каждом запуске
    profession_index = (run_number - 1) % len(PROFESSIONS)
    selected_profession = PROFESSIONS[profession_index]
    print(f"Номер запуска: {run_number}. Выбрана профессия: '{selected_profession}'")


    if not all([gemini_key, bot_token, channel_id]):
        print("Критическая ошибка: Не найдены все секреты...")
        return

    # --- НОВАЯ ЧАСТЬ: ВАШ ПРОФЕССИОНАЛЬНЫЙ ПРОМПТ ---
    # Мы используем f-string (f"...") для вставки выбранной профессии прямо в текст промпта.
        # --- ВАШ СТАРЫЙ ПРОМПТ (временно отключен) ---
    # prompt = f"""
    # РОЛЬ: HR-эксперт и копирайтер для Telegram.
    # ... (весь остальной текст)
    # """

    # --- НОВЫЙ ТЕСТОВЫЙ ПРОМПТ ---
    prompt = f"Напиши короткий HR-кейс про профессию: {selected_profession}. Упомяни сайт herohunter.ru"
    
    # Шаг 1: Получаем идею для поста от Gemini
    post_text = get_gemini_response(gemini_key, prompt)
    
    # Шаг 2: Публикуем идею в Telegram
    if post_text:
        await post_to_telegram(bot_token, channel_id, post_text)

if __name__ == "__main__":
    asyncio.run(main())
