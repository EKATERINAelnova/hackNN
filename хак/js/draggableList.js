const { useState, useEffect } = React;

const DraggableList = () => {
    const studentData = {
    1: {
      name: "Иванов Иван Иванович",
      lists: {
        list1: [
          { id: 1, text: 'Самарива Татьяна Викторовна', icon: '' },
          { id: 2, text: 'Родин Самсон Дмитриевич', icon: '' },
          { id: 3, text: 'Согатин Николай Анатольевич', icon: '' }
        ],
        list2: [
          { id: 4, text: 'Веб-программирование', icon: '💻', teacher: 'Самарива Татьяна Викторовна' },
          { id: 5, text: 'Объектно-ориентированное программирование', icon: '📚', teacher: 'Родин Самсон Дмитриевич' },
          { id: 6, text: 'Защита информации', icon: '🛡️', teacher: 'Согатин Николай Анатольевич' }
        ]
      }
    },
    2: {
      name: "Петрова Анна Сергеевна",
      lists: {
        list1: [
          { id: 1, text: 'Орлова Татьяна Викторовна', icon: '' },
          { id: 2, text: 'Гадир Самсон Дмитриевич', icon: '' },
          { id: 3, text: 'Борисевич Николай Олегович', icon: '' }
        ],
        list2: [
          { id: 4, text: 'Право', icon: '⚖️', teacher: 'Орлова Татьяна Викторовна' },
          { id: 5, text: 'Алгоритмы и структуры данных', icon: '📊', teacher: 'Гадир Самсон Дмитриевич' },
          { id: 6, text: 'Методы защиты информации', icon: '🔒', teacher: 'Борисевич Николай Олегович' }
        ]
      }
    }
  };

  const [selectedStudentId, setSelectedStudentId] = useState(null);
  const [lists, setLists] = useState({ list1: [], list2: [] });
  const [currentView, setCurrentView] = useState({
    list: 'list1',
    showThanks: false
  });
  const [draggedItem, setDraggedItem] = useState(null);

  // При изменении выбранного студента обновляем списки
  useEffect(() => {
    if (selectedStudentId && studentData[selectedStudentId]) {
      setLists(studentData[selectedStudentId].lists);
      setCurrentView({ list: 'list1', showThanks: false });
    }
  }, [selectedStudentId]);

  const handleStudentChange = (e) => {
    setSelectedStudentId(e.target.value);
  };

  const handleDragStart = (e, index) => {
    setDraggedItem(index);
    e.dataTransfer.effectAllowed = 'move';
    e.dataTransfer.setData('text/html', e.target);
  };

  const handleDragOver = (e, index) => {
    e.preventDefault();
    if (draggedItem === null || draggedItem === index) return;
    
    setLists(prev => {
      const newItems = [...prev[currentView.list]];
      const item = newItems[draggedItem];
      newItems.splice(draggedItem, 1);
      newItems.splice(index, 0, item);
      return { ...prev, [currentView.list]: newItems };
    });
    
    setDraggedItem(index);
  };

  const handleDragEnd = () => {
    setDraggedItem(null);
  };

  const switchList = (listName) => {
    setCurrentView({ ...currentView, list: listName });
  };

  const submitFeedback = () => {
    setCurrentView({ ...currentView, showThanks: true });
  };

  if (currentView.showThanks) {
    return (
      <div className="thanks-container">
        <h2>Спасибо за отзыв, {studentData[selectedStudentId]?.name}!</h2>
        <p>Ваш выбор:</p>
        
        <div className="final-lists">
          <div className="final-list">
            <h3>Преподаватели:</h3>
            <ul>
              {lists.list1.map((item, index) => (
                <li key={item.id}>
                  <span>{index + 1}. </span>
                  {item.text}
                </li>
              ))}
            </ul>
          </div>
          
          <div className="final-list">
            <h3>Дисциплины:</h3>
            <ul>
              {lists.list2.map((item, index) => (
                <li key={item.id}>
                  <span>{index + 1}. </span>
                  {item.icon} {item.text} <span className="teacher-name">({item.teacher})</span>
                </li>
              ))}
            </ul>
          </div>
        </div>
        
        <button 
          className="nav-button prev"
          onClick={() => setCurrentView({ list: 'list1', showThanks: false })}
        >
          ← Вернуться к редактированию
        </button>
      </div>
    );
  }

  return (
    <div className="list-container">
      <div className="student-selector">
        <label htmlFor="student-select" className="student-select-label">Выберите студента:</label>
        <div className="custom-select">
          <select 
            id="student-select"
            value={selectedStudentId || ""}
            onChange={handleStudentChange}
            disabled={currentView.showThanks}
            className="student-select"
          >
            <option value="">-- Выберите студента --</option>
            {Object.entries(studentData).map(([id, student]) => (
              <option key={id} value={id}>
                {student.name}
              </option>
            ))}
          </select>
          <span className="custom-arrow">▼</span>
        </div>
      </div>

      {selectedStudentId ? (
        <>
          <ul className="draggable-list">
            {lists[currentView.list].map((item, index) => (
              <li
                key={item.id}
                className={`list-item ${draggedItem === index ? 'dragging' : ''}`}
                draggable
                onDragStart={(e) => handleDragStart(e, index)}
                onDragOver={(e) => handleDragOver(e, index)}
                onDragEnd={handleDragEnd}
              >
                <span className="item-icon">{item.icon}</span>
                {item.text}
                <div class="teacher-name">
                  {item.teacher}
                </div>
                <span className="burger">=</span>
              </li>
            ))}
          </ul>

          <div className="list-navigation">
            {currentView.list === 'list2' ? (
              <>
                <button 
                  className="nav-button prev"
                  onClick={() => switchList('list1')}
                >
                  ← Вернуться
                </button>
                <button 
                  className="nav-button submit"
                  onClick={submitFeedback}
                >
                  Отправить отзыв
                </button>
              </>
            ) : (
              <button 
                className="nav-button next"
                onClick={() => switchList('list2')}
              >
                Далее →
              </button>
            )}
          </div>
        </>
      ) : (
        <div className="no-student-selected">
          <p>Пожалуйста, выберите студента из списка</p>
        </div>
      )}
    </div>
  );
};

// Добавляем стили для красивого выпадающего списка
const styles = `
.list-container {
  font-family: Arial, sans-serif;
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
  background-color: #f5f5f5;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.teacher-name {
  font-size: 0.9em;
  color:rgb(192, 192, 192);
  font-style: italic;
  margin-left: 3px;
}

.student-selector {
  margin-bottom: 20px;
}

.student-select-label {
  display: block;
  margin-bottom: 8px;
  font-weight: bold;
  color: #333;
}

.custom-select {
  position: relative;
  display: inline-block;
  width: 100%;
}

.student-select {
  appearance: none;
  -webkit-appearance: none;
  -moz-appearance: none;
  width: 100%;
  padding: 12px 15px;
  font-size: 16px;
  border: 2px solid #ddd;
  border-radius: 6px;
  background-color: white;
  cursor: pointer;
  transition: border-color 0.3s;
}

.student-select:focus {
  outline: none;
  border-color: #4a90e2;
}

.custom-arrow, .burger {
  position: absolute;
  top: 50%;
  right: 15px;
  transform: translateY(-50%);
  pointer-events: none;
  color: #666;
}

.draggable-list {
  list-style: none;
  padding: 0;
  margin: 0 0 20px;
}

.list-item {
  padding: 12px 15px;
  margin-bottom: 8px;
  background-color: white;
  border: 1px solid #ddd;
  border-radius: 15px;
  cursor: move;
  display: flex;
  align-items: center;
  transition: transform 0.2s, box-shadow 0.2s;
}

.list-item:hover {
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.list-item.dragging {
  opacity: 0.5;
  background-color: #f0f0f0;
}

.item-icon {
  margin-right: 10px;
  font-size: 18px;
}

.list-navigation {
  display: flex;
  justify-content: space-between;
  margin-top: 20px;
}

.nav-button {
  padding: 10px 20px;
  border: none;
  border-radius: 6px;
  font-size: 16px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.nav-button.prev {
  background-color: #f0f0f0;
  color: #333;
}

.nav-button.next,
.nav-button.submit {
  background-color: #4a90e2;
  color: white;
}

.nav-button:hover {
  opacity: 0.9;
}

.no-student-selected {
  text-align: center;
  padding: 20px;
  color: #666;
}

.thanks-container {
  text-align: center;
}

.thanks-container h2 {
  color: #4a90e2;
  margin-bottom: 20px;
}

.final-lists {
  display: flex;
  justify-content: space-between;
  margin-top: 30px;
  text-align: left;
}

.final-list {
  width: 48%;
}

.final-list h3 {
  border-bottom: 2px solid #4a90e2;
  padding-bottom: 5px;
  margin-bottom: 15px;
}

.final-list ul {
  list-style: none;
  padding: 0;
}

.final-list li {
  padding: 8px 0;
  border-bottom: 1px solid #eee;
}
`;

// Добавляем стили в документ
const styleElement = document.createElement('style');
styleElement.innerHTML = styles;
document.head.appendChild(styleElement);

window.DraggableList = DraggableList;