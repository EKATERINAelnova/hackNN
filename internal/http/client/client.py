import requests

BASE_URL = 'http://0.0.0.0:5000/api'


def start_survey():
    response = requests.post(f'{BASE_URL}/start_survey')
    if response.status_code == 200:
        data = response.json()
        print(f"Опрос начат. Вопрос 1: {data['question']}")
        return data
    else:
        print(f"Ошибка при запуске опроса: {response.text}")
        return None


def submit_answer(answer):
    response = requests.post(f'{BASE_URL}/submit_answer', json={'answer': answer})
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Ошибка при отправке ответа: {response.text}")
        return None


def get_summary():
    response = requests.get(f'{BASE_URL}/summary')
    if response.status_code == 200:
        data = response.json()
        print("\nСводка:")
        print(data['summary'])
        print("Рентабельно:" if data['is_rentable'] else "Не рентабельно")
        return data
    else:
        print(f"Ошибка при получении сводки: {response.text}")
        return None


def main():
    state = start_survey()
    if not state:
        return

    while state['status'] == 'next_question' or state['status'] == 'survey_started':
        answer = input(f"{state['question_number']}. {state['question']}\nВаш ответ: ")
        state = submit_answer(answer)

        if state is None:
            break

        if state['status'] == 'next_question':
            continue
        elif state['status'] == 'survey_completed':
            print("\nОпрос завершён.")
            get_summary()
            break


if __name__ == '__main__':
    main()
