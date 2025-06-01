const { useState } = React;

const DraggableList = () => {
  const [lists, setLists] = useState({
    list1: [
      { id: 1, text: 'Самарива Татьяна Викторовна', icon: '' },
      { id: 2, text: 'Родин Самсон Дмитриевич', icon: '' },
      { id: 3, text: 'Согатин Николай Анатольевич', icon: '' }
    ],
    list2: [
      { id: 4, text: 'Веб-программирование', icon: '💻' },
      { id: 5, text: 'Объектно-ориентированное программирование', icon: '📚' },
      { id: 6, text: 'Защита', icon: '🛡️' }
    ]
  });

  const [currentView, setCurrentView] = useState({
    list: 'list1',
    showThanks: false
  });

  const [draggedItem, setDraggedItem] = useState(null);

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
        <h2>Спасибо за отзыв!</h2>
        <p>Ваш рейтинг:</p>
        
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
                  {item.icon} {item.text}
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
    </div>
  );
};

window.DraggableList = DraggableList;