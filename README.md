# Complete Structured Full-Stack Application

## Project Structure

```
fullstack-app/
│
├── backend/                    # FastAPI Backend
│   ├── app/
│   │   ├── __init__.py
│   │   ├── core/
│   │   │   ├── __init__.py
│   │   │   └── config.py
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   └── item.py
│   │   ├── db/
│   │   │   ├── __init__.py
│   │   │   └── database.py
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   └── item_service.py
│   │   └── api/
│   │       ├── __init__.py
│   │       └── routes.py
│   ├── main.py
│   ├── requirements.txt
│   └── .env
│
└── frontend/                   # React Frontend
    ├── public/
    │   └── index.html
    ├── src/
    │   ├── components/
    │   │   ├── TaskForm.jsx
    │   │   ├── TaskItem.jsx
    │   │   └── TaskList.jsx
    │   ├── services/
    │   │   └── api.js
    │   ├── App.jsx
    │   └── index.js
    ├── package.json
    └── .env
```

---

## Backend Code

### `backend/main.py`

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="A FastAPI backend with structured architecture",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(router, prefix="/api")

@app.get("/")
async def root():
    return {
        "message": "Welcome to FastAPI Backend",
        "docs": "/docs",
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )
```

---

### `backend/app/__init__.py`

```python
"""FastAPI Application Package"""
__version__ = "1.0.0"
```

---

### `backend/app/core/__init__.py`

```python
"""Core configuration module"""
```

---

### `backend/app/core/config.py`

```python
from pydantic_settings import BaseSettings
from typing import List
import os

class Settings(BaseSettings):
    """Application settings and configuration"""
    
    # Application
    PROJECT_NAME: str = "FastAPI Task Manager"
    VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # CORS
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3000"
    ]
    
    # Database (for future SQL integration)
    DATABASE_URL: str = "sqlite:///./app.db"
    
    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()
```

---

### `backend/app/models/__init__.py`

```python
"""Data models and schemas"""
from .item import ItemBase, ItemCreate, ItemUpdate, ItemResponse

__all__ = ["ItemBase", "ItemCreate", "ItemUpdate", "ItemResponse"]
```

---

### `backend/app/models/item.py`

```python
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime

class ItemBase(BaseModel):
    """Base item schema with common attributes"""
    title: str = Field(..., min_length=1, max_length=200, description="Task title")
    description: str = Field(..., min_length=1, max_length=1000, description="Task description")
    completed: bool = Field(default=False, description="Completion status")

class ItemCreate(ItemBase):
    """Schema for creating a new item"""
    pass

class ItemUpdate(ItemBase):
    """Schema for updating an existing item"""
    pass

class ItemResponse(ItemBase):
    """Schema for item responses"""
    id: int = Field(..., description="Unique item identifier")
    created_at: datetime = Field(..., description="Creation timestamp")
    
    model_config = ConfigDict(from_attributes=True)
```

---

### `backend/app/db/__init__.py`

```python
"""Database layer"""
from .database import db

__all__ = ["db"]
```

---

### `backend/app/db/database.py`

```python
from typing import List, Optional, Dict
from datetime import datetime
import threading

class Database:
    """In-memory database implementation"""
    
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        """Singleton pattern implementation"""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(Database, cls).__new__(cls)
                    cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        """Initialize the database"""
        if self._initialized:
            return
        self.items: List[Dict] = []
        self.counter: int = 1
        self._initialized = True
    
    def get_all_items(self) -> List[Dict]:
        """Retrieve all items"""
        return self.items.copy()
    
    def get_item_by_id(self, item_id: int) -> Optional[Dict]:
        """Get a specific item by ID"""
        return next((item.copy() for item in self.items if item["id"] == item_id), None)
    
    def create_item(self, title: str, description: str, completed: bool) -> Dict:
        """Create a new item"""
        new_item = {
            "id": self.counter,
            "title": title,
            "description": description,
            "completed": completed,
            "created_at": datetime.now()
        }
        self.items.append(new_item)
        self.counter += 1
        return new_item.copy()
    
    def update_item(self, item_id: int, title: str, description: str, completed: bool) -> Optional[Dict]:
        """Update an existing item"""
        for item in self.items:
            if item["id"] == item_id:
                item["title"] = title
                item["description"] = description
                item["completed"] = completed
                return item.copy()
        return None
    
    def delete_item(self, item_id: int) -> bool:
        """Delete an item by ID"""
        for i, item in enumerate(self.items):
            if item["id"] == item_id:
                self.items.pop(i)
                return True
        return False
    
    def clear_all(self) -> None:
        """Clear all items (useful for testing)"""
        self.items.clear()
        self.counter = 1

# Singleton database instance
db = Database()
```

---

### `backend/app/services/__init__.py`

```python
"""Business logic services"""
from .item_service import item_service

__all__ = ["item_service"]
```

---

### `backend/app/services/item_service.py`

```python
from typing import List, Optional
from app.db.database import db
from app.models.item import ItemCreate, ItemUpdate, ItemResponse

class ItemService:
    """Service layer for item operations"""
    
    @staticmethod
    def get_all_items() -> List[ItemResponse]:
        """Get all items"""
        items = db.get_all_items()
        return [ItemResponse(**item) for item in items]
    
    @staticmethod
    def get_item(item_id: int) -> Optional[ItemResponse]:
        """Get a specific item by ID"""
        item = db.get_item_by_id(item_id)
        if item:
            return ItemResponse(**item)
        return None
    
    @staticmethod
    def create_item(item_data: ItemCreate) -> ItemResponse:
        """Create a new item"""
        new_item = db.create_item(
            title=item_data.title,
            description=item_data.description,
            completed=item_data.completed
        )
        return ItemResponse(**new_item)
    
    @staticmethod
    def update_item(item_id: int, item_data: ItemUpdate) -> Optional[ItemResponse]:
        """Update an existing item"""
        updated_item = db.update_item(
            item_id=item_id,
            title=item_data.title,
            description=item_data.description,
            completed=item_data.completed
        )
        if updated_item:
            return ItemResponse(**updated_item)
        return None
    
    @staticmethod
    def delete_item(item_id: int) -> bool:
        """Delete an item"""
        return db.delete_item(item_id)
    
    @staticmethod
    def get_completed_items() -> List[ItemResponse]:
        """Get all completed items"""
        all_items = db.get_all_items()
        completed = [item for item in all_items if item["completed"]]
        return [ItemResponse(**item) for item in completed]
    
    @staticmethod
    def get_pending_items() -> List[ItemResponse]:
        """Get all pending (not completed) items"""
        all_items = db.get_all_items()
        pending = [item for item in all_items if not item["completed"]]
        return [ItemResponse(**item) for item in pending]

item_service = ItemService()
```

---

### `backend/app/api/__init__.py`

```python
"""API routes"""
```

---

### `backend/app/api/routes.py`

```python
from fastapi import APIRouter, HTTPException, status, Query
from typing import List
from app.models.item import ItemCreate, ItemUpdate, ItemResponse
from app.services.item_service import item_service

router = APIRouter()

@router.get(
    "/items",
    response_model=List[ItemResponse],
    tags=["items"],
    summary="Get all items",
    description="Retrieve all items from the database"
)
async def get_items(
    completed: bool = Query(None, description="Filter by completion status")
):
    """Get all items, optionally filtered by completion status"""
    if completed is None:
        return item_service.get_all_items()
    elif completed:
        return item_service.get_completed_items()
    else:
        return item_service.get_pending_items()

@router.get(
    "/items/{item_id}",
    response_model=ItemResponse,
    tags=["items"],
    summary="Get item by ID",
    description="Retrieve a specific item by its ID"
)
async def get_item(item_id: int):
    """Get a specific item by ID"""
    item = item_service.get_item(item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with id {item_id} not found"
        )
    return item

@router.post(
    "/items",
    response_model=ItemResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["items"],
    summary="Create new item",
    description="Create a new item in the database"
)
async def create_item(item: ItemCreate):
    """Create a new item"""
    return item_service.create_item(item)

@router.put(
    "/items/{item_id}",
    response_model=ItemResponse,
    tags=["items"],
    summary="Update item",
    description="Update an existing item by ID"
)
async def update_item(item_id: int, item: ItemUpdate):
    """Update an existing item"""
    updated_item = item_service.update_item(item_id, item)
    if not updated_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with id {item_id} not found"
        )
    return updated_item

@router.delete(
    "/items/{item_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["items"],
    summary="Delete item",
    description="Delete an item by ID"
)
async def delete_item(item_id: int):
    """Delete an item"""
    success = item_service.delete_item(item_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with id {item_id} not found"
        )
    return None

@router.get(
    "/stats",
    tags=["items"],
    summary="Get statistics",
    description="Get item statistics"
)
async def get_stats():
    """Get statistics about items"""
    all_items = item_service.get_all_items()
    completed_items = item_service.get_completed_items()
    pending_items = item_service.get_pending_items()
    
    return {
        "total": len(all_items),
        "completed": len(completed_items),
        "pending": len(pending_items),
        "completion_rate": (len(completed_items) / len(all_items) * 100) if all_items else 0
    }
```

---

### `backend/requirements.txt`

```
fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.5.0
pydantic-settings==2.1.0
python-dotenv==1.0.0
```

---

### `backend/.env`

```
PROJECT_NAME=FastAPI Task Manager
DEBUG=True
HOST=0.0.0.0
PORT=8000
```

---

## Frontend Code

### `frontend/package.json`

```json
{
  "name": "task-manager-frontend",
  "version": "1.0.0",
  "private": true,
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "axios": "^1.6.0",
    "lucide-react": "^0.263.1"
  },
  "scripts": {
    "start": "react-scripts start",
    "build": "react-scripts build",
    "test": "react-scripts test",
    "eject": "react-scripts eject"
  },
  "eslintConfig": {
    "extends": [
      "react-app"
    ]
  },
  "browserslist": {
    "production": [
      ">0.2%",
      "not dead",
      "not op_mini all"
    ],
    "development": [
      "last 1 chrome version",
      "last 1 firefox version",
      "last 1 safari version"
    ]
  },
  "devDependencies": {
    "react-scripts": "5.0.1",
    "tailwindcss": "^3.3.0"
  }
}
```

---

### `frontend/.env`

```
REACT_APP_API_URL=http://localhost:8000/api
```

---

### `frontend/public/index.html`

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <meta name="theme-color" content="#000000" />
    <meta name="description" content="Task Manager Application" />
    <title>Task Manager</title>
    <script src="https://cdn.tailwindcss.com"></script>
  </head>
  <body>
    <noscript>You need to enable JavaScript to run this app.</noscript>
    <div id="root"></div>
  </body>
</html>
```

---

### `frontend/src/index.js`

```javascript
import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
```

---

### `frontend/src/services/api.js`

```javascript
import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Error handler
api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', error);
    return Promise.reject(error);
  }
);

export const itemsAPI = {
  // Get all items
  getAll: async (completed = null) => {
    const params = completed !== null ? { completed } : {};
    const response = await api.get('/items', { params });
    return response.data;
  },

  // Get single item
  getById: async (id) => {
    const response = await api.get(`/items/${id}`);
    return response.data;
  },

  // Create item
  create: async (itemData) => {
    const response = await api.post('/items', itemData);
    return response.data;
  },

  // Update item
  update: async (id, itemData) => {
    const response = await api.put(`/items/${id}`, itemData);
    return response.data;
  },

  // Delete item
  delete: async (id) => {
    const response = await api.delete(`/items/${id}`);
    return response.data;
  },

  // Get statistics
  getStats: async () => {
    const response = await api.get('/stats');
    return response.data;
  },
};

export default api;
```

---

### `frontend/src/components/TaskForm.jsx`

```javascript
import React, { useState } from 'react';
import { Plus } from 'lucide-react';

const TaskForm = ({ onAddTask }) => {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = async () => {
    if (!title.trim() || !description.trim()) {
      alert('Please fill in all fields');
      return;
    }

    setIsSubmitting(true);
    try {
      await onAddTask({ title, description, completed: false });
      setTitle('');
      setDescription('');
    } catch (error) {
      console.error('Error adding task:', error);
      alert('Failed to add task');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="bg-white rounded-xl shadow-md p-6 mb-6">
      <h2 className="text-2xl font-bold text-gray-800 mb-4">Add New Task</h2>
      <div className="space-y-4">
        <input
          type="text"
          placeholder="Task title..."
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500"
          disabled={isSubmitting}
        />
        <textarea
          placeholder="Task description..."
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 resize-none"
          rows="3"
          disabled={isSubmitting}
        />
        <button
          onClick={handleSubmit}
          disabled={isSubmitting}
          className="w-full bg-indigo-600 text-white py-3 rounded-lg hover:bg-indigo-700 transition flex items-center justify-center gap-2 font-medium disabled:bg-indigo-400 disabled:cursor-not-allowed"
        >
          <Plus size={20} />
          {isSubmitting ? 'Adding...' : 'Add Task'}
        </button>
      </div>
    </div>
  );
};

export default TaskForm;
```

---

### `frontend/src/components/TaskItem.jsx`

```javascript
import React, { useState } from 'react';
import { Trash2, Edit2, Check, X } from 'lucide-react';

const TaskItem = ({ item, onUpdate, onDelete }) => {
  const [isEditing, setIsEditing] = useState(false);
  const [editTitle, setEditTitle] = useState(item.title);
  const [editDescription, setEditDescription] = useState(item.description);

  const handleSave = async () => {
    try {
      await onUpdate(item.id, {
        title: editTitle,
        description: editDescription,
        completed: item.completed,
      });
      setIsEditing(false);
    } catch (error) {
      console.error('Error updating task:', error);
      alert('Failed to update task');
    }
  };

  const handleCancel = () => {
    setEditTitle(item.title);
    setEditDescription(item.description);
    setIsEditing(false);
  };

  const handleToggleComplete = async () => {
    try {
      await onUpdate(item.id, {
        ...item,
        completed: !item.completed,
      });
    } catch (error) {
      console.error('Error toggling task:', error);
      alert('Failed to update task');
    }
  };

  const handleDelete = async () => {
    if (window.confirm('Are you sure you want to delete this task?')) {
      try {
        await onDelete(item.id);
      } catch (error) {
        console.error('Error deleting task:', error);
        alert('Failed to delete task');
      }
    }
  };

  if (isEditing) {
    return (
      <div className="bg-white p-5 rounded-lg border-2 border-indigo-200 shadow-sm">
        <div className="space-y-3">
          <input
            type="text"
            value={editTitle}
            onChange={(e) => setEditTitle(e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-indigo-500"
          />
          <textarea
            value={editDescription}
            onChange={(e) => setEditDescription(e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-indigo-500 resize-none"
            rows="2"
          />
          <div className="flex gap-2">
            <button
              onClick={handleSave}
              className="flex-1 bg-green-600 text-white py-2 rounded hover:bg-green-700 transition flex items-center justify-center gap-2"
            >
              <Check size={18} />
              Save
            </button>
            <button
              onClick={handleCancel}
              className="flex-1 bg-gray-400 text-white py-2 rounded hover:bg-gray-500 transition flex items-center justify-center gap-2"
            >
              <X size={18} />
              Cancel
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div
      className={`p-5 rounded-lg border-2 transition shadow-sm ${
        item.completed
          ? 'bg-green-50 border-green-200'
          : 'bg-white border-gray-200'
      }`}
    >
      <div className="flex items-start gap-4">
        <input
          type="checkbox"
          checked={item.completed}
          onChange={handleToggleComplete}
          className="mt-1 w-5 h-5 cursor-pointer accent-indigo-600"
        />
        <div className="flex-1">
          <h3
            className={`text-lg font-semibold ${
              item.completed ? 'line-through text-gray-500' : 'text-gray-800'
            }`}
          >
            {item.title}
          </h3>
          <p
            className={`text-sm mt-1 ${
              item.completed ? 'line-through text-gray-400' : 'text-gray-600'
            }`}
          >
            {item.description}
          </p>
          <p className="text-xs text-gray-400 mt-2">
            Created: {new Date(item.created_at).toLocaleString()}
          </p>
        </div>
        <div className="flex gap-2">
          <button
            onClick={() => setIsEditing(true)}
            className="p-2 text-blue-600 hover:bg-blue-50 rounded transition"
            title="Edit"
          >
            <Edit2 size={18} />
          </button>
          <button
            onClick={handleDelete}
            className="p-2 text-red-600 hover:bg-red-50 rounded transition"
            title="Delete"
          >
            <Trash2 size={18} />
          </button>
        </div>
      </div>
    </div>
  );
};

export default TaskItem;
```

---

### `frontend/src/components/TaskList.jsx`

```javascript
import React from 'react';
import TaskItem from './TaskItem';

const TaskList = ({ items, onUpdate, onDelete, loading }) => {
  if (loading) {
    return (
      <div className="text-center py-12">
        <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600"></div>
        <p className="mt-4 text-gray-600">Loading tasks...</p>
      </div>
    );
  }

  if (items.length === 0) {
    return (
      <div className="text-center py-12 bg-white rounded-lg shadow-sm">
        <p className="text-gray-500 text-lg">No tasks yet. Add your first task above!</p>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      {items.map((item) => (
        <TaskItem
          key={item.id}
          item={item}
          onUpdate={onUpdate}
          onDelete={onDelete}
        />
      ))}
    </div>
  );
};

export default TaskList;
```

---

### `frontend/src/App.jsx`

```javascript
import React, { useState, useEffect } from 'react';
import { itemsAPI } from './services/api';
import TaskForm from './components/TaskForm';
import TaskList from './components/TaskList';
import { CheckCircle, Clock, BarChart3 } from 'lucide-react';

function App() {
  const [items, setItems] = useState([]);
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState('all'); // all, pending, completed

  useEffect(() => {
    fetchData();
  }, [filter]);

  const fetchData = async () => {
    setLoading(true);
    try {
      const filterParam = filter === 'all' ? null : filter === 'completed';
      const [itemsData, statsData] = await Promise.all([
        itemsAPI.getAll(filterParam),
        itemsAPI.getStats(),
      ]);
      setItems(itemsData);
      setStats(statsData);
    } catch (error) {
      console.error('Error fetching data:', error);
      alert('Failed to load tasks');
    } finally {
      setLoading(false);
    }
  };

  const handleAddTask = async (taskData) => {
    const newItem = await itemsAPI.create(taskData);
    setItems([...items, newItem]);
    fetchData(); // Refresh stats
  };

  const handleUpdateTask = async (id, taskData) => {
    const updatedItem = await itemsAPI.update(id, taskData);
    setItems(items.map((item) => (item.id === id ? updatedItem : item)));
    fetchData(); // Refresh stats
  };

  const handleDeleteTask = async (id) => {
    await itemsAPI.delete(id);
    setItems(items.filter((item) => item.id !== id));
    fetchData(); // Refresh stats
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50 py-8 px-4">
      <div className="max-w-5xl mx-auto">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-5xl font-bold text-gray-800 mb-2">
            Task Manager Pro
          </h1>
          <p className="text-gray-600 text-lg">
            FastAPI + React Full Stack Application
          </p>
        </div>

        {/* Statistics */}
        {stats && (
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
            <div className="bg-white rounded-xl shadow-md p-6 flex items-center gap-4">
              <div className="bg-blue-100 p-3 rounded-full">
                <BarChart3 className="text-blue-600" size={24} />
              </div>
              <div>
                <p className="text-gray-600 text-sm">Total Tasks</p>
                <p className="text-2xl font-bold text-gray-800">{stats.total}</p>
              </div>
            </div>

            <div className="bg-white rounded-xl shadow-md p-6 flex items-center gap-4">
              <div className="bg-green-100 p-3 rounded-full">
                <CheckCircle className="text-green-600" size={24} />
              </div>
              <div>
                <p className="text-gray-600 text-sm">Completed</p>
                <p className="text-2xl font-bold text-gray-800">{stats.completed}</p>
              </div>
            </div>

            <div className="bg-white rounded-xl shadow-md p-6 flex items-center gap-4">
              <div className="bg-yellow-100 p-3 rounded-full">
                <Clock className="text-yellow-600" size={24} />
              </div>
              <div>
                <p className="text-gray-600 text-sm">Pending</p>
                <p className="text-2xl font-bold text-gray-800">{stats.pending}</p>
              </div>
            </div>
          </div>
        )}

        {/* Filter Tabs */}
        <div className="bg-white rounded-xl shadow-md p-2 mb-6 flex gap-2">
          <button
            onClick={() => setFilter('all')}
            className={`flex-1 py-3 px-4 rounded-lg font-medium transition ${
              filter === 'all'
                ? 'bg-indigo-600 text-white'
                : 'text-gray-600 hover:bg-gray-100'
            }`}
          >
            All Tasks
          </button>
          <button
            onClick={() => setFilter('pending')}
            className={`flex-1 py-3 px-4 rounded-lg font-medium transition ${
              filter === 'pending'
                ? 'bg-indigo-600 text-white'
                : 'text-gray-600 hover:bg-gray-100'
            }`}
          >
            Pending
          </button>
          <button
            onClick={() => setFilter('completed')}
            className={`flex-1 py-3 px-4 rounded-lg font-medium transition ${
              filter === 'completed'
                ? 'bg-indigo-600 text-white'
                : 'text-gray-600 hover:bg-gray-100'
            }`}
          >
            Completed
          </button>
        </div>

        {/* Task Form */}
        <TaskForm onAddTask={handleAddTask} />

        {/* Task List */}
        <TaskList
          items={items}
          onUpdate={handleUpdateTask}
          onDelete={handleDeleteTask}
          loading={loading}
        />

        {/* Footer */}
        <div className="mt-8 text-center text-gray-500 text-sm">
          <p>Built with FastAPI & React | Full Stack Application</p>
        </div>
      </div>
    </div>
  );
}

export default App;
```

---

## Installation & Setup Instructions

### Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the server
python main.py

# Server will be running at http://localhost:8000
# API docs available at http://localhost:8000/docs
```

---

### Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm start

# Application will open at http://localhost:3000
```

---

## API Endpoints

### Items

- **GET** `/api/items` - Get all items (optional query: `?completed=true/false`)
- **GET** `/api/items/{id}` - Get specific item
- **POST** `/api/items` - Create new item
- **PUT** `/api/items/{id}` - Update item
- **DELETE** `/api/items/{id}` - Delete item
- **GET** `/api/stats` - Get statistics

### Example API Request

```bash
# Create a new task
curl -X POST "http://localhost:8000/api/items" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "My First Task",
    "description": "This is a test task",
    "completed": false
  }'
```

---

## Features

### Backend Features
✅ RESTful API with FastAPI
✅ Structured architecture (MVC pattern)
✅ Pydantic models for validation
✅ Comprehensive error handling
✅ CORS enabled
✅ Auto-generated API documentation
✅ Singleton database pattern
✅ Service layer architecture

### Frontend Features
✅ Modern React with Hooks
✅ Component-based architecture
✅ Axios for API calls
✅ Real-time task management
✅ Task filtering (All/Pending/Completed)
✅ Statistics dashboard
✅ Edit/Delete functionality
✅ Responsive design with Tailwind CSS
✅ Loading states
✅ Error handling

---

## Project Architecture

### Backend Architecture
```
Request → Routes → Services → Database
         ↓
    Models (Validation)
```

### Frontend Architecture
```
App Component
├── TaskForm (Create tasks)
├── TaskList (Display tasks)
│   └── TaskItem (Individual task)
└── API Service (HTTP calls)
```

---

## Environment Variables

### Backend `.env`
```
PROJECT_NAME=FastAPI Task Manager
DEBUG=True
HOST=0.0.0.0
PORT=8000
```

### Frontend `.env`
```
REACT_APP_API_URL=http://localhost:8000/api
```

---

## Testing the Application

### Test Backend
```bash
# Visit API documentation
http://localhost:8000/docs

# Health check
curl http://localhost:8000/health
```

### Test Frontend
1. Open http://localhost:3000
2. Add a new task
3. Mark it as complete
4. Edit the task
5. Delete the task

---

## Future Enhancements

- [ ] Add PostgreSQL/MySQL database
- [ ] Add user authentication (JWT)
- [ ] Add task categories/tags
- [ ] Add due dates and priorities
- [ ] Add file attachments
- [ ] Add search functionality
- [ ] Add task sorting
- [ ] Add pagination
- [ ] Add unit tests
- [ ] Add Docker support
- [ ] Add CI/CD pipeline

---

## Troubleshooting

### CORS Issues
If you encounter CORS errors, ensure:
1. Backend is running on port 8000
2. Frontend is running on port 3000
3. ALLOWED_ORIGINS in config.py includes your frontend URL

### Port Already in Use
```bash
# Backend (kill process on port 8000)
# Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# macOS/Linux:
lsof -ti:8000 | xargs kill -9

# Frontend (kill process on port 3000)
# Windows:
netstat -ano | findstr :3000
taskkill /PID <PID> /F

# macOS/Linux:
lsof -ti:3000 | xargs kill -9
```

---

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

---

## License

MIT License - feel free to use this project for learning and commercial purposes.

---

## Contact & Support

For issues and questions, please open an issue on GitHub or contact the development team.

**Happy Coding! 🚀**
