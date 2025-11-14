Step 1: Create Project Structure

    # Create project
    mkdir my-fastapi-project
    cd my-fastapi-project
    
    # Create virtual environment
    python -m venv venv
    
    # Activate it
    # On Linux/Mac:
    source venv/bin/activate
    
    # On Windows:
    venv\Scripts\activate
    
    # You'll see (venv) in your terminal prompt
    
Step 2: Install FastAPI & Dependencies

    # Install packages
    pip install fastapi uvicorn[standard] sqlalchemy pydantic-settings python-multipart
    
    # For dev dependencies
    pip install pytest black ruff
    
Step 3: Save Dependencies
bash

    # Save to requirements.txt (like package.json)
    pip freeze > requirements.txt
    
Your requirements.txt will look like:

    annotated-types==0.6.0
    anyio==4.2.0
    click==8.1.7
    fastapi==0.109.0
    h11==0.14.0
    httptools==0.6.1
    idna==3.6
    pydantic==2.5.3
    pydantic-core==2.14.6
    pydantic-settings==2.1.0
    python-dotenv==1.0.0
    python-multipart==0.0.6
    PyYAML==6.0.1
    sniffio==1.3.0
    sqlalchemy==2.0.25
    starlette==0.35.1
    typing-extensions==4.9.0
    uvicorn==0.27.0
    uvloop==0.19.0
    watchfiles==0.21.0
    websockets==12.0

Step 4: Create Project Files
Directory Structure:

    my-fastapi-project/
    ├── venv/                    # Virtual environment (ignored in git)
    ├── app/
    │   ├── __init__.py
    │   ├── main.py
    │   ├── config.py
    │   ├── api/
    │   │   ├── __init__.py
    │   │   └── v1/
    │   │       ├── __init__.py
    │   │       └── endpoints/
    │   │           ├── __init__.py
    │   │           └── users.py
    │   ├── models/
    │   │   ├── __init__.py
    │   │   └── user.py
    │   ├── schemas/
    │   │   ├── __init__.py
    │   │   └── user.py
    │   └── db/
    │       ├── __init__.py
    │       └── session.py
    ├── tests/
    │   └── __init__.py
    ├── .env
    ├── .gitignore
    ├── requirements.txt
    └── README.md
    
Create all folders:

    mkdir -p app/{api/v1/endpoints,models,schemas,db}
    mkdir tests

Create __init__.py files:

    touch app/__init__.py
    touch app/api/__init__.py
    touch app/api/v1/__init__.py
    touch app/api/v1/endpoints/__init__.py
    touch app/models/__init__.py
    touch app/schemas/__init__.py
    touch app/db/__init__.py
    touch tests/__init__.py

Step 5: Create Basic Files
app/main.py:

    from fastapi import FastAPI
    from app.api.v1.endpoints import users
    
    app = FastAPI(title="My FastAPI Project", version="1.0.0")
    
    # Include routers
    app.include_router(users.router, prefix="/api/v1/users", tags=["users"])
    
    @app.get("/")
    def read_root():
        return {"message": "Welcome to FastAPI!"}
    
    @app.get("/health")
    def health_check():
        return {"status": "healthy"}

app/api/v1/endpoints/users.py:

    from fastapi import APIRouter
    
    router = APIRouter()
    
    @router.get("/")
    def get_users():
        return {"users": [{"id": 1, "name": "John"}, {"id": 2, "name": "Jane"}]}
    
    @router.get("/{user_id}")
    def get_user(user_id: int):
        return {"id": user_id, "name": "John Doe"}
    
    @router.post("/")
    def create_user(name: str, email: str):
        return {"id": 1, "name": name, "email": email}
.env:

    DATABASE_URL=sqlite:///./sql_app.db
    SECRET_KEY=your-secret-key-change-this-in-production
    DEBUG=True
    ```
    
    **`.gitignore`:**
    ```
    # Python
    __pycache__/
    *.py[cod]
    *$py.class
    *.so
    .Python
    
    # Virtual Environment
    venv/
    env/
    ENV/
    
    # Environment variables
    .env
    
    # Database
    *.db
    *.sqlite
    
    # IDE
    .vscode/
    .idea/
    *.swp
    *.swo
    
    # Testing
    .pytest_cache/
    .coverage
    htmlcov/
    
    # Build
    dist/
    build/
    *.egg-info/

Step 6: Run Your App

    # Make sure venv is activated (you should see (venv) in terminal)
    # If not: source venv/bin/activate
    
    # Run the app
    uvicorn app.main:app --reload
    
    # Or with host and port
    uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
    ```
    
    **Output:**
    ```
    INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
    INFO:     Started reloader process [28720]
    INFO:     Started server process [28722]
    INFO:     Waiting for application startup.
    INFO:     Application startup complete.
    
Visit:

API: http://127.0.0.1:8000
Interactive docs: http://127.0.0.1:8000/docs
Alternative docs: http://127.0.0.1:8000/redoc

Step 7: Future Usage
When you come back to the project:

    cd my-fastapi-project
    
    # Activate virtual environment
    source venv/bin/activate  # Linux/Mac
    # or
    venv\Scripts\activate  # Windows
    
    # Install dependencies (if cloning or on new machine)
    pip install -r requirements.txt
    
    # Run
    uvicorn app.main:app --reload

To add new packages:
    # Install
    pip install sqlalchemy alembic
    
    # Update requirements.txt
    pip freeze > requirements.txt

To share with team:

    # They clone your repo and run:
    python -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt


pip vs Poetry Quick Comparison

## pip vs Poetry — Quick Comparison

| Task               | pip                                    | Poetry                           |
|-------------------|-----------------------------------------|----------------------------------|
| Install tool       | ✅ Built-in                             | ❌ Must install                  |
| Create venv        | `python -m venv venv`                   | `poetry init` (auto creates venv) |
| Activate venv      | `source venv/bin/activate`              | `poetry shell`                   |
| Add package        | `pip install fastapi`                   | `poetry add fastapi`             |
| Save dependencies  | `pip freeze > requirements.txt`         | Automatic                        |
| Install deps       | `pip install -r requirements.txt`       | `poetry install`                 |
| Run app            | `uvicorn app.main:app`                  | `poetry run uvicorn app.main:app` |

My Honest Opinion
Use pip if:

✅ You want simplicity (you do!)
✅ You're learning
✅ Small to medium projects
✅ You don't want extra tools

Poetry adds value when:

Large projects with many dependencies
Complex dependency conflicts
Publishing packages to PyPI
You want npm-like workflows

For FastAPI backend, pip is totally fine! 🎉
