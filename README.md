# Система аутентификации и авторизации на FastAPI

## Описание проекта

Решение тестового задания по разработке backend-приложения с собственной системой аутентификации и авторизации. Проект включает:

- **Backend**: Полнофункциональная система аутентификации на FastAPI с JWT-токенами
- **База данных**: Поддержка SQLite, Postgres(не тестировала) с использованием SQLAlchemy и Alembic
- **Frontend**: Демонстрационный интерфейс на Vue.js (реализован для тестирования API)
- **Основные функции**: Регистрация, вход, управление пользователями, система ролей, мягкое удаление

### !!! Важное примечание !!!

Данный проект разработан на основе [моего собственного FastAPI-пресета](https://github.com/Iwlj4s/FastAPIPreset), который я создала ранее для ускорения разработки backend-приложений. Это объясняет:

 - Структуру проекта - многослойная архитектура 

 - Наличие дополнительных фич - система валидации, контекст запросов, generic response schemas

 - Проработанную инфраструктуру - миграции, конфигурация, утилиты

Все эти компоненты были частью пресета и адаптированы под требования данного ТЗ. Основное внимание уделено реализации именно тех функций, которые указаны в задании.

 > **! Примечание !**: Я Backend разраб - фронтенд не претендует на качественно сделанный продукт. Я его добавила просто потому что почему бы и нет.Считайте, что дизайн сделал deepseek по промпту: вот тебе мои эндпоинты, сделай что-нибудь симпатичное

## Реализованные возможности

### Аутентификация и авторизация
- Система JWT-аутентификации (без использования встроенных решений фреймворков)
- Регистрация с валидацией данных
- Логин/логаут с использованием cookies
- Идентификация пользователя при последующих обращениях

### Управление пользователями
- Полный CRUD для пользователей
- Мягкое удаление (soft delete) с флагом `is_active`
- Разделение на обычных пользователей и администраторов
- Возможность обновления профиля

### Система разграничения прав доступа
- Две роли: пользователь (`is_admin=False`) и администратор (`is_admin=True`)
- Проверка прав доступа на уровне эндпоинтов
- Админ-панель для управления пользователями
- Обработка ошибок 401 (Unauthorized) и 403 (Forbidden)

### Бизнес-объекты (посты)
- Модель `Post` для демонстрации работы с ресурсами
- CRUD операции для постов
- Валидация прав доступа (пользователь может редактировать только свои посты)

## Структура проекта
```
test_tech/
├── backend/                   # FastAPI 
│   ├── context/               # Контекст запросов
│   ├── DAO/                   # Data Access Object layer
│   ├── database/              # Конфигурация базы данных и модели
│   ├── helpers/               # Вспомогательные функции
│   ├── services/              # Бизнес-логика и валидация
│   ├── repository/            # Слой бизнес-логики
│   ├── routes/                # API эндпоинты
│   ├── migrations/            # Миграции базы данных
│   ├── .env                   # Переменные окружения
│   ├── alembic.ini            # Конфигурация Alembic
│   ├── config.py              # Настройки приложения
│   ├── main.py                # Точка входа FastAPI
│   ├── requirements.txt       # Python зависимости
│   └── README.md              # Документация
│
└── frontend/                  # Vue.js демо-интерфейс
    ├── src/
    │   ├── components/        # Компоненты Vue
    │   ├── stores/           # Pinia хранилища
    │   └── router/           # Маршрутизация
    ├── package.json          # Зависимости Node.js
    └── vite.config.js        # Конфигурация Vite
```
---

## Быстрый старт

### Требования
- Python 3.11+ (использовала: 3.11.9)
- SQLite (используется по умолчанию) или PostgreSQL (можно свапнуться на нее, но не тестировала)
- pip (менеджер пакетов Python)
- Node.js 18+ (только для демо-фронтенда)

### Установка и настройка

1. **Клонирование или загрузка проекта**:
```bash
# Если используете git
git clone https://github.com/Iwlj4s/test_tech.git
cd test_tech

# Или просто скачайте и распакуйте файлы проекта
```
2. **Настройка виртуального окружения**:
```bash
cd backend
python -m venv .venv

# Активация виртуального окружения:
# Windows:
.venv\Scripts\activate

# macOS/Linux:
source .venv/bin/activate
```

3. **Установка зависимостей**:

```bash
pip install -r requirements.txt
```

### Конфигурация базы данных

***Вариант A: SQLite***
 - Используется по умолчанию в проекте

 - Не требует дополнительной установки

 - Все миграции уже настроены для SQLite

 - БД вы получаете с установкой репозитория, там есть пользователи

    #### Пользователи в БД

    | email | password |
    |----------|-------------|
    | admin@gmail.com | adminpass |
    | admin2@gmail.com | admin2pass | 
    | bob@gmail.com | bobpass | 
    | mashka@gmail.com | mashkapass | 
    | sam@gmail.com | sampass | 
    | charlie@gmail.com | charliepass|

    Думаю вы поняли логику
 
 ***Вариант B: PostgreSQL (Не тестировала)***

 > **Примечание**: В проекте использовалась SQLite. Переключение на PostgreSQL возможно, но не тестировалось.

1. Запустите службу PostgreSQL:
2. Создайте базу данных:
```bash
psql -U postgres -c "CREATE DATABASE test_tech;"
```
### Конфигурация окружения

1. Создайте файл `.env` в директории `backend/`:
```env
# Конфигурация базы данных
# Выберите SQLite или PostgreSQL:

# SQLite (Разработка) - ИСПОЛЬЗУЕТСЯ ПО УМОЛЧАНИЮ
DB_LITE="sqlite+aiosqlite:///test_tech.db"
DB_LITE_FOR_ALEMBIC="sqlite:///test_tech.db"

# PostgreSQL (Не тестировалась)
DB_HOST=localhost
DB_PORT=5432
DB_NAME=test_tech
DB_USER=your_postgres_username
DB_PASSWORD=your_postgres_password
DATABASE_URL_POSTGRE="postgresql+asyncpg://your_username:your_password@localhost:5432/test_tech"
DATABASE_URL_ALEMBIC_POSTGRE="postgresql://your_username:your_password@localhost:5432/test_tech"

# JWT Аутентификация
SECRET_KEY=your_secret_key
ALGORITHM=HS256
```
2. Сгенерируйте `SECRET_KEY`:
```bash
# Используя Node.js (если установлен):
node -e "console.log(require('crypto').randomBytes(32).toString('hex'))"

# Или используя Python:
python -c "import secrets; print(secrets.token_hex(32))"
```

### Миграции базы данных с Alembic

1. Настройте Alembic в `alembic.ini`:
```ini
sqlalchemy.url = sqlite:///test_tech.db
# ИЛИ для PostgreSQL (не тестировала):
# sqlalchemy.url = postgresql://your_username:your_password@localhost:5432/test_tech
```
2. Примените миграции:
```bash
# Создайте начальную миграцию (если нужно)
alembic revision --autogenerate -m "Initial migration"

# Примените миграции
alembic upgrade head
```

### Запуск приложения
1. Запуск FastAPI
```bash
cd backend

uvicorn main:app --reload
```
2. Доступ к приложению
 - API Сервер: http://127.0.0.1:8000

 - Интерактивная документация: http://127.0.0.1:8000/docs

 - Альтернативная документация: http://127.0.0.1:8000/redoc

Лично я использую [Yaak](https://yaak.app/), удобно, красиво

### Установка и запуск фронтенда
1. Перейдите в директорию фронтенда и установите зависимости
```bash
cd frontend

npm install
```

![alt text](<git img/image2.png>)

Вот это я просто заигнорила, вроде все работает

2. Запустите фронтенд
``` bash
npm run dev
```

Фронтенд будет доступен по адресу: http://localhost:5173

 > **Примечание**: Фронтенд не претендует на качественно сделанный продукт. Я его добавила просто потому что почему бы и нет.
    Считайте, что дизайн сделал deepseek по промпту: вот тебе мои эндпоинты, сделай что-нибудь симпатичное

## Эндпоинты API

### Аутентификация
 - POST `/api/v1/users/sign_up` - Регистрация нового пользователя

 - POST `/api/v1/users/sign_in` - Вход в систему (токен сохраняется в cookie)

 - POST `/api/v1/users/logout` - Выход из системы

### Управление профилем (требует аутентификации)
 - GET `/api/v1/users/me/` - Получить текущего пользователя

 - PATCH `/api/v1/users/me/update` - Обновить профиль

 - DELETE `/api/v1/users/me/delete` - Удалить свой аккаунт (мягкое удаление)

 - GET `/api/v1/users/me/posts` - Получить свои посты

 - GET `/api/v1/users/me/post/{post_id}` - Получить конкретный пост текущего пользователя

 ### Пользователи (публичные)
 - GET `/api/v1/users/` - Получить всех пользователей

 - GET `/api/v1/users/user/{user_id}` - Получить профиль пользователя по ID

 ### Администратор (требует прав администратора)
 - PATCH `/api/v1/admin/users/promote_to_admin/{user_id}` - Назначить администратором

 - PATCH `/api/v1/admin/users/demote_from_admin/{user_id}` - Снять права администратора

 - DELETE `/api/v1/admin/users/delete/{user_id}` - Удалить пользователя (с указанием причины)

 - GET `/api/v1/admin/users/deleted` - Получить список удаленных пользователей

### Посты
 - GET `/api/v1/posts/` - Получить все посты (публичный)

 - GET `/api/v1/posts/post/{post_id}` - Получить пост по ID

 - GET `/api/v1/posts/{user_id}/posts` - Получить посты конкретного пользователя

 - POST `/api/v1/posts/create_post` - Создать пост (требует аутентификации)

 - PATCH `/api/v1/posts/update_post/{post_id}` - Обновить пост (только свой)

 - DELETE `/api/v1/posts/delete_post/{post_id}` - Удалить пост (только свой)

## Модель базы данных

![alt text](<git img/Screenshot_5.png>)

### Схема прав доступа:

 - Пользователь (is_admin=False):
    
    Может управлять своим профилем и своими постами

 - Администратор (is_admin=True):
     
     Может управлять всеми пользователями, назначать/снимать права администратора, просматривать удаленных пользователей


## Вид фронта
Если вдруг у вас что-то произошло и фронт не захотел работать - просто покажу скрины, не зря же с дипсиком болтала ))

### Вход/Регистрация
![alt text](<git img/sign in.png>)

![alt text](<git img/sign up.png>)

### Профиль
![alt text](<git img/profile1.png>)

![alt text](<git img/profile2.png>)

### Лента 
![alt text](<git img/feed.png>)

### Админка
![alt text](<git img/admin panel.png>)

#### Удаленные пользователи
![alt text](<git img/deleted users.png>)