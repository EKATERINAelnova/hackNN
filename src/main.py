from survey import survey
from ollama import start_ollama_server
from summarization import summarize
from rentability import rentability

def pipeline() :
    
    # Запуск llama3
    start_ollama_server()

    # Опрос
    answers = survey()

    # Суммаризация
    print("\n📝 Итог опроса:")
    print(summarize(answers))

    # Рентабельность
    isRent = bool(int(rentability(answers)))
    print("\nРентабельность отзывов:", isRent)

if __name__ == '__main__' :
    pipeline()