    backend/
    │
    ├── main.py                          # Application entry point
    ├── requirements.txt
    ├── .env
    │
    └── app/
        ├── __init__.py
        │
        ├── core/
        │   ├── __init__.py
        │   └── config.py                # Configuration
        │
        ├── models/
        │   ├── __init__.py
        │   └── item.py                  # Pydantic schemas
        │
        ├── db/
        │   ├── __init__.py
        │   └── database.py              # Database layer
        │
        ├── services/
        │   ├── __init__.py
        │   └── item_service.py          # Business logic
        │
        ├── controllers/                 # ⭐ NEW!
        │   ├── __init__.py
        │   └── item_controller.py       # Request handling
        │
        └── api/
            ├── __init__.py
            └── v1/                      # ⭐ API versioning!
                ├── __init__.py
                ├── router.py            # Main API router
                └── endpoints/
                    ├── __init__.py
                    └── items.py         # Item endpoints



🎯 Architecture Flow:
Request Flow:
─────────────

        Client Request
            ↓
        Route (items.py)
            ↓
        Controller (item_controller.py)
            ↓
        Service (item_service.py)
            ↓
        Database (database.py)
            ↓
        Response back to client
        
✨ Key Improvements:
1. Controllers Layer (NEW!)

Handles HTTP-specific logic
Validates requests
Manages error responses
Calls services for business logic

2. Routes (Endpoints)

Pure routing definitions
Minimal logic
Delegates to controllers
Clean and readable

3. API Versioning

/api/v1/items structure
Easy to add v2, v3 in future
Better API management


4. Separation of Concerns

        Routes       → Define endpoints
        Controllers  → Handle requests/responses
        Services     → Business logic
        Database     → Data access
        Models       → Data validation

🚀 New API Endpoints:

    GET    /api/v1/items                    # Get all items
    GET    /api/v1/items?completed=true     # Get completed items
    GET    /api/v1/items?completed=false    # Get pending items
    GET    /api/v1/items/{id}               # Get specific item
    POST   /api/v1/items                    # Create item
    PUT    /api/v1/items/{id}               # Update item
    DELETE /api/v1/items/{id}               # Delete item
    GET    /api/v1/items/statistics/summary # Get statistics


📝 Frontend Update Required:
Update your frontend API service to use the new endpoint:

    // frontend/src/services/api.js
    const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api/v1';




# ============================================
# main.py
# ============================================
    from fastapi import FastAPI
    from fastapi.middleware.cors import CORSMiddleware
    from app.api.v1.router import api_router
    from app.core.config import settings
    
    app = FastAPI(
        title=settings.PROJECT_NAME,
        description="A FastAPI backend with Routes & Controllers architecture",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc"
    )

    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include API router
    app.include_router(api_router, prefix=settings.API_V1_PREFIX)
    
    @app.get("/")
    async def root():
        return {
            "message": "Welcome to FastAPI Backend with Routes & Controllers",
            "docs": "/docs",
            "version": "1.0.0",
            "api_prefix": settings.API_V1_PREFIX
        }
    
    @app.get("/health")
    async def health_check():
        return {
            "status": "healthy",
            "version": "1.0.0"
        }
    
    if __name__ == "__main__":
        import uvicorn
        uvicorn.run(
            "main:app",
            host=settings.HOST,
            port=settings.PORT,
            reload=settings.DEBUG
        )
    

# ============================================
# app/__init__.py
# ============================================

    """FastAPI Application Package"""
    __version__ = "1.0.0"


# ============================================
# app/core/__init__.py
# ============================================

    """Core configuration module"""


# ============================================
# app/core/config.py
# ============================================

    from pydantic_settings import BaseSettings
    from typing import List
    
    class Settings(BaseSettings):
        """Application settings and configuration"""
        
        # Application
        PROJECT_NAME: str = "FastAPI Task Manager"
        VERSION: str = "1.0.0"
        DEBUG: bool = True
        
        # API
        API_V1_PREFIX: str = "/api/v1"
        
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


# ============================================
# app/models/__init__.py
# ============================================

    """Data models and schemas"""
    from .item import ItemBase, ItemCreate, ItemUpdate, ItemResponse
    
    __all__ = ["ItemBase", "ItemCreate", "ItemUpdate", "ItemResponse"]
    

# ============================================
# app/models/item.py
# ============================================

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
    

# ============================================
# app/db/__init__.py
# ============================================

    """Database layer"""
    from .database import db
    
    __all__ = ["db"]
    

# ============================================
# app/db/database.py
# ============================================

    from typing import List, Optional, Dict
    from datetime import datetime
    import threading
    
    class Database:
        """In-memory database implementation with thread safety"""
        
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
    

# ============================================
# app/services/__init__.py
# ============================================

    """Business logic services"""
    from .item_service import ItemService
    
    __all__ = ["ItemService"]
    

# ============================================
# app/services/item_service.py
# ============================================

    from typing import List, Optional
    from app.db.database import db
    from app.models.item import ItemCreate, ItemUpdate, ItemResponse
    
    class ItemService:
        """Service layer for item business logic"""
        
        def get_all_items(self) -> List[ItemResponse]:
            """Get all items"""
            items = db.get_all_items()
            return [ItemResponse(**item) for item in items]
        
        def get_item_by_id(self, item_id: int) -> Optional[ItemResponse]:
            """Get a specific item by ID"""
            item = db.get_item_by_id(item_id)
            if item:
                return ItemResponse(**item)
            return None
        
        def create_item(self, item_data: ItemCreate) -> ItemResponse:
            """Create a new item"""
            new_item = db.create_item(
                title=item_data.title,
                description=item_data.description,
                completed=item_data.completed
            )
            return ItemResponse(**new_item)
        
        def update_item(self, item_id: int, item_data: ItemUpdate) -> Optional[ItemResponse]:
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
        
        def delete_item(self, item_id: int) -> bool:
            """Delete an item"""
            return db.delete_item(item_id)
        
        def get_completed_items(self) -> List[ItemResponse]:
            """Get all completed items"""
            all_items = db.get_all_items()
            completed = [item for item in all_items if item["completed"]]
            return [ItemResponse(**item) for item in completed]
        
        def get_pending_items(self) -> List[ItemResponse]:
            """Get all pending (not completed) items"""
            all_items = db.get_all_items()
            pending = [item for item in all_items if not item["completed"]]
            return [ItemResponse(**item) for item in pending]
        
        def get_statistics(self) -> dict:
            """Get item statistics"""
            all_items = self.get_all_items()
            completed_items = self.get_completed_items()
            pending_items = self.get_pending_items()
            
            total = len(all_items)
            completed = len(completed_items)
            pending = len(pending_items)
            completion_rate = (completed / total * 100) if total > 0 else 0
            
            return {
                "total": total,
                "completed": completed,
                "pending": pending,
                "completion_rate": round(completion_rate, 2)
            }


# ============================================
# app/controllers/__init__.py
# ============================================

    """Controllers for handling business logic"""
    from .item_controller import ItemController
    
    __all__ = ["ItemController"]
    

# ============================================
# app/controllers/item_controller.py
# ============================================

    from typing import List, Optional
    from fastapi import HTTPException, status
    from app.services.item_service import ItemService
    from app.models.item import ItemCreate, ItemUpdate, ItemResponse
    
    class ItemController:
        """Controller for item-related operations"""
        
        def __init__(self):
            self.service = ItemService()
        
        async def get_all_items(self, completed: Optional[bool] = None) -> List[ItemResponse]:
            """
            Get all items with optional filtering
            
            Args:
                completed: Filter by completion status (None for all items)
                
            Returns:
                List of items
            """
            try:
                if completed is None:
                    return self.service.get_all_items()
                elif completed:
                    return self.service.get_completed_items()
                else:
                    return self.service.get_pending_items()
            except Exception as e:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Error fetching items: {str(e)}"
                )
        
        async def get_item_by_id(self, item_id: int) -> ItemResponse:
            """
            Get a specific item by ID
            
            Args:
                item_id: The ID of the item to retrieve
                
            Returns:
                The requested item
                
            Raises:
                HTTPException: If item not found
            """
            item = self.service.get_item_by_id(item_id)
            if not item:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Item with id {item_id} not found"
                )
            return item
        
        async def create_item(self, item_data: ItemCreate) -> ItemResponse:
            """
            Create a new item
            
            Args:
                item_data: The item data to create
                
            Returns:
                The newly created item
            """
            try:
                return self.service.create_item(item_data)
            except Exception as e:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Error creating item: {str(e)}"
                )
        
        async def update_item(self, item_id: int, item_data: ItemUpdate) -> ItemResponse:
            """
            Update an existing item
            
            Args:
                item_id: The ID of the item to update
                item_data: The updated item data
                
            Returns:
                The updated item
                
            Raises:
                HTTPException: If item not found
            """
            updated_item = self.service.update_item(item_id, item_data)
            if not updated_item:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Item with id {item_id} not found"
                )
            return updated_item
        
        async def delete_item(self, item_id: int) -> dict:
            """
            Delete an item
            
            Args:
                item_id: The ID of the item to delete
                
            Returns:
                Success message
                
            Raises:
                HTTPException: If item not found
            """
            success = self.service.delete_item(item_id)
            if not success:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Item with id {item_id} not found"
                )
            return {"message": f"Item {item_id} deleted successfully"}
        
        async def get_statistics(self) -> dict:
            """
            Get statistics about items
            
            Returns:
                Statistics dictionary
            """
            try:
                return self.service.get_statistics()
            except Exception as e:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Error fetching statistics: {str(e)}"
                )


# ============================================
# app/api/__init__.py
# ============================================

    """API routes"""


# ============================================
# app/api/v1/__init__.py
# ============================================

    """API Version 1"""


# ============================================
# app/api/v1/router.py
# ============================================

    from fastapi import APIRouter
    from app.api.v1.endpoints import items
    
    api_router = APIRouter()
    
    # Include all endpoint routers
    api_router.include_router(
        items.router,
        prefix="/items",
        tags=["items"]
    )


# ============================================
# app/api/v1/endpoints/__init__.py
# ============================================

    """API endpoints"""


# ============================================
# app/api/v1/endpoints/items.py
# ============================================

    from fastapi import APIRouter, Query, status
    from typing import List, Optional
    from app.controllers.item_controller import ItemController
    from app.models.item import ItemCreate, ItemUpdate, ItemResponse
    
    router = APIRouter()
    controller = ItemController()
    
    @router.get(
        "",
        response_model=List[ItemResponse],
        summary="Get all items",
        description="Retrieve all items from the database with optional filtering by completion status"
    )
    async def get_items(
        completed: Optional[bool] = Query(
            None,
            description="Filter by completion status: true for completed, false for pending, null for all"
        )
    ):
        """Get all items with optional filtering"""
        return await controller.get_all_items(completed=completed)
    
    
    @router.get(
        "/{item_id}",
        response_model=ItemResponse,
        summary="Get item by ID",
        description="Retrieve a specific item by its unique identifier"
    )
    async def get_item(item_id: int):
        """Get a specific item by ID"""
        return await controller.get_item_by_id(item_id)
    
    
    @router.post(
        "",
        response_model=ItemResponse,
        status_code=status.HTTP_201_CREATED,
        summary="Create new item",
        description="Create a new item in the database"
    )
    async def create_item(item: ItemCreate):
        """Create a new item"""
        return await controller.create_item(item)
    
    
    @router.put(
        "/{item_id}",
        response_model=ItemResponse,
        summary="Update item",
        description="Update an existing item by its ID"
    )
    async def update_item(item_id: int, item: ItemUpdate):
        """Update an existing item"""
        return await controller.update_item(item_id, item)
    
    
    @router.delete(
        "/{item_id}",
        status_code=status.HTTP_200_OK,
        summary="Delete item",
        description="Delete an item by its ID"
    )
    async def delete_item(item_id: int):
        """Delete an item"""
        return await controller.delete_item(item_id)
    
    
    @router.get(
        "/statistics/summary",
        summary="Get statistics",
        description="Get statistical summary of all items including total, completed, and pending counts"
    )
    async def get_stats():
        """Get statistics about items"""
        return await controller.get_statistics()
    

# ============================================
# requirements.txt
# ============================================

    # fastapi==0.104.1
    # uvicorn[standard]==0.24.0
    # pydantic==2.5.0
    # pydantic-settings==2.1.0
    # python-dotenv==1.0.0


# ============================================
# .env
# ============================================

    # PROJECT_NAME=FastAPI Task Manager
    # DEBUG=True
    # HOST=0.0.0.0
    # PORT=8000
    # API_V1_PREFIX=/api/v1
