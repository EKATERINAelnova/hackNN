const { useState, useRef, useEffect } = React;

const AdminPage = () => {
  const chartRef = useRef(null);
  const chartInstance = useRef(null); // Отдельная ref для хранения экземпляра графика
  const [selectedSubject, setSelectedSubject] = useState('Все предметы');
  const [selectedTeacher, setSelectedTeacher] = useState('Все преподаватели');
  const [sortOrder, setSortOrder] = useState('none');
  
  const teachersData = [
    { name: 'Тальяна Ковалёва', subject: 'Веб-программирование', score: 65 },
    { name: 'Сергей Матвеев', subject: 'ООП', score: 59 },
    { name: 'Лилия Бражник', subject: 'Базы данных', score: 80 },
    { name: 'Самарина Татьяна', subject: 'Криптография', score: 56 },
    { name: 'Родин Самсон', subject: 'Алгоритмы', score: 72 },
    { name: 'Согатин Николай', subject: 'Сети', score: 88 },
    { name: 'Тальяна Ковалёва', subject: 'Фронтенд', score: 70 },
    { name: 'Сергей Матвеев', subject: 'Базы данных', score: 75 }
  ];

  const comments = [
    { name: 'Самарина Татьяна', text: 'Объясняет сложные темы непонятно', correct: false },
    { name: 'Лилия Бражник', text: 'Завышает всем баллы', correct: true },
    { name: 'Тальяна Ковалёва', text: 'Интересные лекции, но строгие дедлайны', correct: true },
    { name: 'Сергей Матвеев', text: 'Много практических заданий', correct: true },
    { name: 'Самарина Татьяна', text: 'Необъективна на экзаменах', correct: false },
    { name: 'Родин Самсон', text: 'Отличный преподаватель, всё понятно', correct: true },
    { name: 'Согатин Николай', text: 'Слишком сложные задания', correct: false }
  ];

  // Получаем уникальные предметы и преподавателей
  const subjects = ['Все предметы', ...new Set(teachersData.map(t => t.subject))];
  const teachers = ['Все преподаватели', ...new Set(teachersData.map(t => t.name))];

  // Фильтрация данных
  let filteredData = teachersData.filter(t => 
    (selectedSubject === 'Все предметы' || t.subject === selectedSubject) &&
    (selectedTeacher === 'Все преподаватели' || t.name === selectedTeacher)
  );

  // Фильтрация комментариев
  const filteredComments = selectedTeacher === 'Все преподаватели' 
    ? comments 
    : comments.filter(c => c.name === selectedTeacher);

  // Сортировка данных
  if (sortOrder === 'asc') {
    filteredData = [...filteredData].sort((a, b) => a.score - b.score);
  } else if (sortOrder === 'desc') {
    filteredData = [...filteredData].sort((a, b) => b.score - a.score);
  }

  // Создание и обновление графика
  useEffect(() => {
    if (!chartRef.current) return;

    const ctx = chartRef.current.getContext('2d');
    
    // Уничтожаем предыдущий график, если он существует
    if (chartInstance.current) {
      chartInstance.current.destroy();
    }

    // Создаем новый график только если есть данные для отображения
    if (filteredData.length > 0) {
      chartInstance.current = new Chart(ctx, {
        type: 'bar',
        data: {
          labels: filteredData.map(t => t.name),
          datasets: [{
            label: 'Оценка',
            data: filteredData.map(t => t.score),
            backgroundColor: 'rgba(193, 39, 44, 0.7)',
            borderColor: 'rgba(193, 39, 45, 1)',
            borderWidth: 1,
            barPercentage: 0.6
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            y: {
              beginAtZero: true,
              max: 100,
              ticks: { stepSize: 10 }
            },
            x: {
              ticks: {
                autoSkip: false,
                maxRotation: 45,
                minRotation: 45
              }
            }
          }
        }
      });
    }

    // Функция очистки при размонтировании
    return () => {
      if (chartInstance.current) {
        chartInstance.current.destroy();
        chartInstance.current = null;
      }
    };
  }, [filteredData, sortOrder]);

  return (
    
    <div className="admin-page-container">
      
      <div className="filters-row">
        <div className="filter-group">
          <label htmlFor="subject-select">Предмет:</label>
          <select
            id="subject-select"
            value={selectedSubject}
            onChange={(e) => setSelectedSubject(e.target.value)}
          >
            {subjects.map(subj => (
              <option key={subj} value={subj}>{subj}</option>
            ))}
          </select>
        </div>
        
        <div className="filter-group">
          <label htmlFor="teacher-select">Преподаватель:</label>
          <select
            id="teacher-select"
            value={selectedTeacher}
            onChange={(e) => setSelectedTeacher(e.target.value)}
          >
            {teachers.map(teacher => (
              <option key={teacher} value={teacher}>{teacher}</option>
            ))}
          </select>
        </div>

        <div className="filter-group">
          <label htmlFor="sort-select">Сортировка:</label>
          <select
            id="sort-select"
            value={sortOrder}
            onChange={(e) => setSortOrder(e.target.value)}
          >
            <option value="none">Без сортировки</option>
            <option value="asc">По возрастанию</option>
            <option value="desc">По убыванию</option>
          </select>
        </div>
      </div>
      
      <div className="chart-wrapper">
        {filteredData.length > 0 ? (
          <canvas ref={chartRef} height="400"></canvas>
        ) : (
          <div className="no-data-message">Нет данных для отображения графика</div>
        )}
      </div>

      <div className="comments-section">
        <h3>
          {selectedTeacher === 'Все преподаватели' 
            ? 'Комментарии по всем преподавателям' 
            : `Комментарии о преподавателе: ${selectedTeacher}`}
        </h3>
        
        {filteredComments.length > 0 ? (
          <div className="comments-grid">
            {filteredComments.map((comment, index) => (
              <div 
                key={index}
                className={`comment-card ${comment.correct ? 'correct' : 'incorrect'}`}
              >
                {selectedTeacher === 'Все преподаватели' && (
                  <div className="comment-teacher">
                    Преподаватель: <strong>{comment.name}</strong>
                  </div>
                )}
                <div className="comment-header">
                  {comment.correct ? (
                    <span className="correct-icon">✅ Корректно</span>
                  ) : (
                    <span className="incorrect-icon">❌ Некорректно</span>
                  )}
                </div>
                <div className="comment-text">
                  {comment.text}
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="no-comments">
            Нет комментариев {selectedTeacher === 'Все преподаватели' ? 'по выбранным критериям' : 'о данном преподавателе'}
          </div>
        )}
      </div>
    </div>
  );
};