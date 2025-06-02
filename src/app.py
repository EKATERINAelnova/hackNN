from flask import Flask, request, jsonify
from flask_cors import CORS
from survey import get_first_question, get_next_question, validate_answer
from summarization import summarize
from rentability import rentability
import subprocess
import atexit

app = Flask(__name__)
CORS(app)

survey_history = []
current_question = None
survey_active = False
negative_counter = 0
question_counter = 0

ollama_process = None

def start_ollama():
    global ollama_process
    if ollama_process is None:
        ollama_process = subprocess.Popen(
            ["ollama", "serve"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        atexit.register(stop_ollama)

def stop_ollama():
    global ollama_process
    if ollama_process:
        ollama_process.terminate()
        ollama_process = None

@app.route('/api/start_survey', methods=['POST'])
def start_survey():
    global survey_active, survey_history, current_question, negative_counter, question_counter
    
    start_ollama()

    survey_history = []
    negative_counter = 0
    question_counter = 0
    survey_active = True
    
    current_question = get_first_question()
    
    return jsonify({
        'status': 'survey_started',
        'question': current_question,
        'question_number': question_counter + 1
    })

@app.route('/api/submit_answer', methods=['POST'])
def submit_answer():
    global survey_active, survey_history, current_question, negative_counter, question_counter
    
    if not survey_active:
        return jsonify({'error': 'Survey is not active'}), 400
    
    data = request.json
    answer = data.get('answer')
    
    if not answer:
        return jsonify({'error': 'Answer is required'}), 400
    
    survey_history.append({
        'question': current_question,
        'answer': answer
    })
    
    negative_counter += validate_answer(current_question, answer)
    question_counter += 1
    
    if negative_counter >= 3 or question_counter >= 10:
        survey_active = False
        return jsonify({
            'status': 'survey_completed',
            'summary': get_summary()
        })
    
    current_question = get_next_question(survey_history)
    
    return jsonify({
        'status': 'next_question',
        'question': current_question,
        'question_number': question_counter + 1,
        'negative_count': negative_counter
    })

@app.route('/api/summary', methods=['GET'])
def get_summary():
    answers_text = '\n'.join([f"Вопрос: {item['question']}\nОтвет: {item['answer']}" for item in survey_history])
    
    summary_response = summarize(answers_text)
    summary_text = summary_response if isinstance(summary_response, str) else summary_response.json()["response"]
    
    rentability_response = rentability(answers_text)
    is_rentable = bool(int(rentability_response if isinstance(rentability_response, str) else rentability_response.json()["response"]))
    
    return jsonify({
        'summary': summary_text,
        'is_rentable': is_rentable,
        'answers': survey_history
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)