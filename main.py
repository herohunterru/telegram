import os
import asyncio
import json
import requests
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
    """Запрашивает уникальный текст у Gemini через прямой HTTP-запрос."""
    
    # URL для API-запроса к модели gemini-pro
    # Новый, правильный код
url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={api_key}"
    
    headers = {
        'Content-Type': 'application/json'
    }
    
    # Формируем тело запроса в формате, который ожидает Google API
    data = {
        "contents": [{
            "parts": [{
                "text": prompt
            }]
        }]
    }
    
    try:
        print("1. Отправляю прямой HTTP-запрос в Gemini API...")
        response = requests.post(url, headers=headers, data=json.dumps(data), timeout=60) # Добавлен таймаут 60 секунд
        
        # Проверяем, успешен ли запрос (код 200)
        if response.status_code == 200:
            response_json = response.json()
            
            # Безопасно извлекаем текст из сложной структуры ответа
            try:
                text = response_json['candidates'][0]['content']['parts'][0]['text']
                print("2. Ответ от Gemini успешно получен.")
                return text.strip()
            except (KeyError, IndexError) as e:
                print(f"Ошибка: Не удалось разобрать ответ от Gemini. Структура ответа: {response_json}. Ошибка: {e}")
                return None
        else:
            # Если код ответа не 200, выводим ошибку
            print(f"Ошибка от Gemini API. Статус: {response.status_code}, Ответ: {response.text}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"Произошла ошибка при отправке HTTP-запроса: {e}")
        return None

async def post_to_telegram(bot_token, channel_id, text_to_post):
    """Отправляет сообщение в Telegram-канал."""
    if not text_to_post:
        print("Текст для поста пустой. Публикация отменена.")
        return False
    
    try:
        print("3. Инициализирую Telegram-бота...")
        bot = telegram.Bot(token=bot_token)
        
        print(f"4. Отправляю сообщение в канал {channel_id}...")
        await bot.send_message(
            chat_id=channel_id,
            text=text_to_post,
            parse_mode='HTML'
        )
        print("5. Сообщение успешно отправлено в Telegram!")
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

    # Ваш основной, качественный промпт
    prompt = f"""
РОЛЬ: HR-эксперт и копирайтер для Telegram.
СТИЛЬ: Кратко, по делу, без воды, русский язык.
ЗАДАЧА: Написать уникальный HR-кейс.
ПРАВИЛА: Пост строго до 700 символов, 3-5 релевантных эмодзи, без списков/маркеров.

ШАГ 1: Используй профессию: {selected_profession}.

ШАГ 2: Напиши пост строго по следующей структуре (каждый пункт с новой строки):
Заголовок: (яркий, с "Москва" и сутью кейса 🎯)
Проблема: (описание сложности 🤔)
Решение: (суть "фишки" 💡)
Вывод: (резюме и совет 📌)
CTA: (нативный призыв с сайтом <a href="https://herohunter.ru">herohunter.ru</a>)
"""
    
    post_text = get_gemini_response(gemini_key, prompt)
    
    if post_text:
        await post_to_telegram(bot_token, channel_id, post_text)

if __name__ == "__main__":
    asyncio.run(main())
