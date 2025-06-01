const ActivityChart = () => {
  const chartRef = useRef(null);
  const [selectedSubject, setSelectedSubject] = useState('Все предметы');
  const [selectedTeacher, setSelectedTeacher] = useState('Все преподаватели');
  
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

  // Получаем уникальные предметы и преподавателей
  const subjects = ['Все предметы', ...new Set(teachersData.map(t => t.subject))];
  const teachers = ['Все преподаватели', ...new Set(teachersData.map(t => t.name))];

  // Фильтрация данных
  const filteredData = teachersData.filter(t => 
    (selectedSubject === 'Все предметы' || t.subject === selectedSubject) &&
    (selectedTeacher === 'Все преподаватели' || t.name === selectedTeacher)
  );

  useEffect(() => {
    if (!chartRef.current || filteredData.length === 0) return;
    
    const ctx = chartRef.current.getContext('2d');
    
    const chart = new Chart(ctx, {
      type: 'bar', // Изменено на столбчатую диаграмму
      data: {
        labels: filteredData.map(t => t.name),
        datasets: [{
          label: 'Оценка',
          data: filteredData.map(t => t.score),
          backgroundColor: [
            'rgba(255, 99, 132, 0.7)',
            'rgba(54, 162, 235, 0.7)',
            'rgba(255, 206, 86, 0.7)',
            'rgba(75, 192, 192, 0.7)',
            'rgba(153, 102, 255, 0.7)',
            'rgba(255, 159, 64, 0.7)'
          ],
          borderColor: [
            'rgba(255, 99, 132, 1)',
            'rgba(54, 162, 235, 1)',
            'rgba(255, 206, 86, 1)',
            'rgba(75, 192, 192, 1)',
            'rgba(153, 102, 255, 1)',
            'rgba(255, 159, 64, 1)'
          ],
          borderWidth: 1,
          barPercentage: 0.6 // Ширина столбцов
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            display: false
          },
          tooltip: {
            callbacks: {
              title: (context) => `${filteredData[context[0].dataIndex].name}`,
              label: (context) => [
                `Предмет: ${filteredData[context.dataIndex].subject}`,
                `Оценка: ${context.raw}`
              ]
            }
          }
        },
        scales: {
          y: {
            beginAtZero: true,
            max: 100,
            grid: {
              color: 'rgba(0, 0, 0, 0.05)'
            },
            title: {
              display: true,
              text: 'Оценка'
            }
          },
          x: {
            grid: {
              display: false
            },
            ticks: {
              autoSkip: false,
              maxRotation: 45,
              minRotation: 45
            }
          }
        },
        layout: {
          padding: {
            bottom: filteredData.length > 5 ? 50 : 30 // Адаптивный отступ
          }
        }
      }
    });

    return () => chart.destroy();
  }, [filteredData]);

  return (
    <div style={{ padding: '20px', maxWidth: '100%' }}>
      <div style={{
        display: 'flex',
        gap: '20px',
        marginBottom: '20px',
        flexWrap: 'wrap'
      }}>
        <div>
          <label>Предмет: </label>
          <select 
            value={selectedSubject}
            onChange={(e) => setSelectedSubject(e.target.value)}
            style={{ padding: '8px', minWidth: '200px', borderRadius: '4px', border: '1px solid #ddd' }}
          >
            {subjects.map(subj => (
              <option key={subj} value={subj}>{subj}</option>
            ))}
          </select>
        </div>
        
        <div>
          <label>Преподаватель: </label>
          <select 
            value={selectedTeacher}
            onChange={(e) => setSelectedTeacher(e.target.value)}
            style={{ padding: '8px', minWidth: '200px', borderRadius: '4px', border: '1px solid #ddd' }}
          >
            {teachers.map(teacher => (
              <option key={teacher} value={teacher}>{teacher}</option>
            ))}
          </select>
        </div>
      </div>
      
      <div style={{
        position: 'relative',
        height: '500px',
        width: '100%',
        margin: '0 auto'
      }}>
        <canvas ref={chartRef} />
      </div>
    </div>
  );
};