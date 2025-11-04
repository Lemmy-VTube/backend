<div align="center">
# 🌸 Backend Template

_An elegant, modular, and production-ready boilerplate for building Python backend services with FastAPI._

![anime-banner](https://i.redd.it/t64rltdqx90e1.gif)

[![Stars](https://img.shields.io/github/stars/Kitty-Ilnazik/backend-template?color=ffb3d1&style=for-the-badge)](https://github.com/Kitty-Ilnazik/backend-template/stargazers)
[![Forks](https://img.shields.io/github/forks/Kitty-Ilnazik/backend-template?color=ffc8a2&style=for-the-badge)](https://github.com/Kitty-Ilnazik/backend-template/network/members)
[![Issues](https://img.shields.io/github/issues/Kitty-Ilnazik/backend-template?color=a5d8ff&style=for-the-badge)](https://github.com/Kitty-Ilnazik/backend-template/issues)
[![License](https://img.shields.io/github/license/Kitty-Ilnazik/backend-template?color=caffbf&style=for-the-badge)](LICENSE)

</div>

---

## 🐾 Overview (English)

This Backend Template provides a solid foundation for building scalable, maintainable, and production-ready Python backend services. It is designed to help developers start new projects quickly without worrying about boilerplate setup. The template emphasizes modularity, clear project structure, and best practices, including async database operations, caching, middleware support, and structured API responses.
With this template, you can focus on building your application logic while the foundation handles configuration, logging, database initialization, and API versioning. It is suitable for building RESTful APIs, microservices, or any backend service that requires reliability, scalability, and maintainability.

---

## 🌍 Translations

| 🌐 Language | 🏷 Code | 🔗 Link                                     |
| :---------- | :----- | :------------------------------------------ |
| Russian     | `ru`   | [README.ru.md](readme_locales/README.ru.md) |
| Ukrainian   | `uk`   | [README.uk.md](readme_locales/README.uk.md) |
| Tatar       | `tt`   | [README.tt.md](readme_locales/README.tt.md) |
| Uzbek       | `uz`   | [README.uz.md](readme_locales/README.uz.md) |
| Kazakh      | `kk`   | [README.kk.md](readme_locales/README.kk.md) |
| English     | `en`   | [README.md](README.md)                      |

---

## 🛠️ Tools and Libraries

- ⚡ **fastapi** — modern, fast (high-performance) web framework for building APIs with Python.
- 🔥 **uvicorn** — lightning-fast ASGI server for running FastAPI apps.
- 🧩 **pydantic-settings** — settings management using Pydantic.
- 💾 **sqlalchemy + aiosqlite** — async ORM and DB driver.
- 🔁 **redis** — a client for Redis, used for caching.
- 🧱 **alembic** — a database migration tool.
- ✨ **ruff** — an extremely fast Python linter and formatter.
- 🚀 **uv** — an extremely fast package manager and bundler for Python.

---

## 📁 Project Structure

```
// Directory tree (3 levels, limited to 200 entries)
├── .gitignore
├── .python-version
├── Dockerfile
├── LICENSE
├── README.md
├── example.alembic.ini
├── pyproject.toml
├── ruff.toml
├── tests\
├── src\
│   ├── .env.example
│   ├── config.py
│   ├── app.py
│   ├── run.py
│   ├── api\
│   │   ├── v1\
│   │   │   ├── __init__.py
│   │   │   ├── admin.py
│   │   │   └── user.py
│   │   ├── __init.py__
│   │   └── common.py
│   ├── database\
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── models\
│   │   └── repositories\
│   ├── middlewares\
│   │   └── rate_limit.py
│   ├── schemas\
│   │   └── __init__.py
│   ├── services\
│   │   └── redis_service.py
│   └── utils\
│       ├── api_structure.py
│       ├── command_runner.py
│       ├── endpoints.py
│       ├── exceptions.py
│       ├── logger.py
│       ├── migration_database.py
│       └── responses.py
└── uv.lock
```

---

## 📄 Description of Important Files

| 📂 Folder                    | 🧠 Description                                         |
| :--------------------------- | :----------------------------------------------------- |
| `src/api/`                   | Contains API routes and versioned modules.             |
| `src/api/v1/`                | API version 1 endpoints (admin, user, etc.).           |
| `src/database/`              | Database initialization, ORM models, and repositories. |
| `src/database/models/`       | SQLAlchemy ORM models.                                 |
| `src/database/repositories/` | CRUD repositories for working with the database.       |
| `src/middlewares/`           | Middleware for rate limiting and request processing.   |
| `src/schemas/`               | Pydantic schemas for request/response validation.      |
| `src/services/`              | Application services (e.g., Redis).                    |
| `src/utils/`                 | Utilities: logging, exceptions, responses, etc.        |
| `tests/`                     | Unit and integration tests.                            |

---

## 🚀 Setup and Running

### Installing Redis

Redis is used for caching and rate limiting.

**For Windows:**

1.  Download the `.msi` installer from the Microsoft's repository: [https://github.com/microsoftarchive/redis/releases](https://github.com/microsoftarchive/redis/releases)
2.  Run the `.msi` file and follow the installer instructions.

**For Linux:**

- **Arch Linux:**
  ```bash
  sudo pacman -S redis
  sudo systemctl start redis
  sudo systemctl enable redis
  ```
- **Debian/Ubuntu:**
  ```bash
  sudo apt update
  sudo apt install redis-server
  sudo systemctl enable redis-server
  sudo systemctl start redis-server
  ```
- **Fedora:**
  ```bash
  sudo dnf install redis
  sudo systemctl start redis
  sudo systemctl enable redis
  ```

**For macOS:**

```bash
brew install redis
brew services start redis
```

### Running without Docker

#### Using `uv` (recommended)

1.  **Install `uv`:**

    ```bash
    curl -LsSf https://astral.sh/uv/install.sh | sh
    ```

    Or for Windows:

    ```powershell
    irm https://astral.sh/uv/install.ps1 | iex
    ```

2.  **Clone the repository and navigate to the folder:**

    ```bash
    git clone https://github.com/Kitty-Ilnazik/backend-template.git
    cd backend-template
    ```

3.  **Configure environment variables:**
    Copy the example `.env` file and fill it with your data:

    ```bash
    cp src/.env.example src/.env
    ```

    Open `src/.env` and enter values for `REDIS_URL` and `DB_URL`.

4.  **Install dependencies and run:**
    ```bash
    uv run start
    ```

#### Without `uv`

1.  **Clone the repository and navigate to the folder:**

    ```bash
    git clone https://github.com/Kitty-Ilnazik/backend-template.git
    cd backend-template
    ```

2.  **Configure environment variables:**
    Copy the example `.env` file and fill it with your data:

    ```bash
    cp src/.env.example src/.env
    ```

    Open `src/.env` and enter values for `REDIS_URL` and `DB_URL`.

3.  **Create and activate a virtual environment:**

    - **Windows:**
      ```bash
      python -m venv .venv
      .venv/Scripts/activate
      ```
    - **macOS/Linux:**
      ```bash
      python3 -m venv .venv
      . .venv/bin/activate
      ```

4.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

5.  **Run the bot:**
    ```bash
    python src/run.py
    ```

### Running with Docker

1.  **Install Docker:**

    - **Arch Linux:**
      ```bash
      sudo pacman -S docker
      sudo systemctl start docker
      sudo systemctl enable docker
      sudo usermod -aG docker $USER # Add user to docker group
      newgrp docker # Apply group changes
      ```
    - **Debian/Ubuntu:**
      ```bash
      sudo apt update
      sudo apt install docker.io
      sudo systemctl start docker
      sudo systemctl enable docker
      sudo usermod -aG docker $USER
      newgrp docker
      ```
    - **Fedora:**
      ```bash
      sudo dnf install docker
      sudo systemctl start docker
      sudo systemctl enable docker
      sudo usermod -aG docker $USER
      newgrp docker
      ```
    - **Windows/macOS:** Install Docker Desktop from the official Docker website.

2.  **Build and run the Docker image:**

    ```bash
    docker build -t backend-template .
    ```

    - `docker build`: Command to build a Docker image.
    - `-t backend-template`: Assigns the tag (name) `backend-template` to the created image.
    - `.`: Indicates that the Dockerfile is in the current directory.

    ```bash
    docker run -d --name my-backend --env-file src/.env backend-template
    ```

    - `docker run`: Command to run a Docker container.
    - `-d`: Runs the container in detached mode.
    - `--name my-backend`: Assigns the name `my-backend` to the running container.
    - `--env-file src/.env`: Instructs Docker to use environment variables from `src/.env` inside the container.
    - `backend-template`: The name of the Docker image to run.

---

## 🗄 Using DB Migrations (Alembic)

1.  **Alembic Configuration:**
    Copy the example Alembic configuration file:

    ```bash
    cp example.alembic.ini alembic.ini
    ```

    Open `alembic.ini` and change the path to the `.env` file in the `[alembic]` section to `src/.env`.

2.  **Create and apply a migration:**

    ```bash
    uv run migrate commit "Initial migration"
    ```

---

## 🧹 Using Ruff

Ruff is used for code formatting and error checking.

```bash
uv run ruff check .
uv run ruff format .
```

---
