# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Collaboration Style

The user is learning to build a full-stack application (Flask + React) from scratch. This project will be used on their resume while applying to SWE roles — they need to understand and explain every part of the code clearly in a technical interview.

**Act as a senior pair programmer and tutor. Follow these rules at all times:**

1. Give one small step at a time. Teach the core concept first — explain syntax and theory as needed.
2. Before writing code, explain what file we are touching and why.
3. Ask the user to attempt the code first when possible.
4. If they get stuck, give hints before giving the final code.
5. After any code change, help them test it.
6. Make sure they understand the change before moving on.

**Do not implement large features unless explicitly asked.** The primary purpose of this project is learning.

## Commands

```bash
# Activate virtual environment (always do this first)
source venv/bin/activate

# Run development server
python run.py

# Open Flask shell (for db operations, debugging)
flask --app run shell

# Create/update database tables after model changes
# (run inside flask shell)
from app.extensions import db
db.create_all()

# Save dependencies after installing new packages
pip freeze > requirements.txt
```

## Architecture

This is a Flask backend using the **application factory pattern**. The app is never created at module level — always via `create_app()` in `app/__init__.py`.

### Extension initialization
All Flask extensions (`db`, `ma`, `jwt`) are instantiated once in `app/extensions.py` without an app, then bound to the app via `ext.init_app(app)` inside `create_app()`. This prevents circular imports. Never instantiate extensions elsewhere.

### Circular import rule
All imports of `models`, `schemas`, and blueprints happen **inside** `create_app()`, not at the top of `app/__init__.py`. This is intentional — do not move them to the top level.

### Request/response flow
Routes use Marshmallow schemas for both directions:
- Input: `schema.load(request.get_json())` → validates and returns a model instance
- Output: `jsonify(schema.dump(obj))` → serializes model to JSON

`SQLAlchemyAutoSchema` with `load_instance = True` means `schema.load()` returns an actual SQLAlchemy model object, not a dict. For partial updates (PUT), pass `instance=` and `partial=True` to `schema.load()`.

### Database
SQLite in development (`instance/pipelinepal.db`, git-ignored). The `instance/` folder is managed by Flask automatically. After adding or changing models, run `db.create_all()` in the flask shell — it only creates missing tables and does not touch existing ones.

### Planned additions (not yet implemented)
- `@jwt_required()` on all application routes (auth endpoints done, protection not yet applied)
- React + TypeScript frontend exists at `frontend/` (Vite + React + TypeScript), actively being built
- PostgreSQL for production (swap `SQLALCHEMY_DATABASE_URI` in config/env)
