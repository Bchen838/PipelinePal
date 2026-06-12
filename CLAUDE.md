# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

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
- `app/routes/auth.py` — register/login endpoints using `werkzeug.security` for password hashing and `flask-jwt-extended` for JWT tokens
- `@jwt_required()` on all application routes once auth is complete
- React + TypeScript frontend (separate directory, TBD)
- PostgreSQL for production (swap `SQLALCHEMY_DATABASE_URI` in config/env)
