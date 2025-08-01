import os
import asyncio
import json
import requests # Импортируем requests
import telegram

# ... (список PROFESSIONS остается без изменений) ...

# --- НОВАЯ, ПЕРЕПИСАННАЯ ФУНКЦИЯ ---
def get_gemini_response(api_key, prompt):
    """Запрашивает уникальный текст у Gemini через прямой HTTP-запрос."""
    
    # Используем самый последний стабильный URL для модели gemini-pro
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={api_key}"
    
    headers = {
        'Content-Type': 'application/json'
    }
    
    data = {
        "contents": [{
            "parts": [{
                "text": prompt
            }]
        }]
    }
    
    try:
        print("1. Отправляю прямой HTTP-запрос в Gemini API...")
        response = requests.post(url, headers=headers, data=json.dumps(data))
        
        # Проверяем, успешен ли запрос
        if response.status_code == 200:
            response_json = response.json()
            # Извлекаем текст из сложной структуры ответа
            text = response_json['candidates'][0]['content']['parts'][0]['text']
            print("2. Ответ от Gemini успешно получен.")
            return text.strip()
        else:
            # Если ошибка, выводим ее текст
            print(f"Ошибка от Gemini API. Статус: {response.status_code}, Ответ: {response.text}")
            return None
            
    except Exception as e:
        print(f"Произошла ошибка при отправке HTTP-запроса: {e}")
        return None

# ... (функции post_to_telegram и main остаются БЕЗ ИЗМЕНЕНИЙ) ...
# Убедитесь, что в функции main используется ваш длинный, качественный промпт,
# а не тестовый.

async def post_to_telegram(bot_token, channel_id, text_to_post):
    # ... (код без изменений) ...

async def main():
    # ... (код без изменений) ...

if __name__ == "__main__":
    asyncio.run(main())
