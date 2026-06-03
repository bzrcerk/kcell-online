# KCell Online

KCell Online — учебный интернет-магазин на Django. Проект показывает полный базовый сценарий покупки: пользователь регистрируется, просматривает каталог, добавляет товары в корзину и оформляет заказ с именем клиента и номером телефона. Дополнительно в проекте есть REST API для категорий, товаров, корзины, заказов и JWT-авторизации.

## Что реализовано

- Витрина магазина с HTML-шаблонами Django: каталог, карточка товара, корзина, оформление заказа, вход и регистрация.
- REST API на Django REST Framework.
- JWT-аутентификация через `djangorestframework-simplejwt`.
- Хранение товаров, категорий, корзины и заказов в PostgreSQL.
- Загрузка изображений товаров через `ImageField`.
- Docker-конфигурация для backend и PostgreSQL.

## Используемые технологии

- Python 3.12
- Django 6
- Django REST Framework
- Simple JWT
- PostgreSQL 16
- psycopg2-binary
- Pillow
- django-cors-headers
- Docker и Docker Compose
- HTML-шаблоны Django

## Архитектура проекта

Проект построен как monolith backend-приложение Django с разделением бизнес-логики по приложениям.

```text
kcell-online/
├── backend/
│   ├── backend/                 # Django project: settings, urls, wsgi/asgi
│   ├── apps/
│   │   ├── accounts/            # регистрация пользователей и auth endpoints
│   │   ├── products/            # категории, товары, каталог и storefront views
│   │   ├── cart/                # корзина пользователя и позиции корзины
│   │   └── orders/              # заказы и позиции заказов
│   ├── templates/
│   │   ├── storefront/          # страницы магазина
│   │   └── registration/        # страницы входа и регистрации
│   ├── manage.py
│   ├── requirements.txt
│   └── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

### Основные модули

#### `backend/backend`

Главная конфигурация Django-проекта:

- подключение приложений;
- настройки базы данных PostgreSQL;
- настройки Django REST Framework;
- JWT-аутентификация;
- маршрутизация корневых URL.

#### `apps.products`

Отвечает за каталог:

- модель `Category` хранит категории товаров;
- модель `Product` хранит товары, описание, цену и изображение;
- REST endpoints `/api/products/` и `/api/categories/`;
- storefront views для каталога, карточки товара, корзины и checkout flow.

#### `apps.cart`

Отвечает за корзину пользователя:

- `Cart` связан с пользователем один-к-одному;
- `CartItem` хранит товар и количество;
- REST endpoints `/api/carts/` и `/api/cart-items/`.

#### `apps.orders`

Отвечает за оформление заказов:

- `Order` хранит данные клиента, контакты, сумму, статус и дату создания;
- `OrderItem` сохраняет состав заказа;
- REST endpoints `/api/orders/` и `/api/order-items/`.

#### `apps.accounts`

Отвечает за регистрацию и JWT-login:

- `/api/register/` — создание пользователя;
- `/api/login/` — получение access/refresh токенов;
- `/api/refresh/` — обновление access token.

## Маршруты приложения

### HTML-страницы

| URL | Назначение |
| --- | --- |
| `/` | Каталог товаров |
| `/products/<id>/` | Карточка товара |
| `/cart/` | Корзина авторизованного пользователя |
| `/checkout/` | Оформление заказа |
| `/signup/` | Регистрация |
| `/login/` | Вход |
| `/logout/` | Выход |
| `/admin/` | Django admin |

### REST API

| URL | Назначение |
| --- | --- |
| `/api/register/` | Регистрация пользователя |
| `/api/login/` | Получение JWT token pair |
| `/api/refresh/` | Обновление JWT access token |
| `/api/products/` | CRUD товаров |
| `/api/categories/` | CRUD категорий |
| `/api/carts/` | CRUD корзины |
| `/api/cart-items/` | CRUD позиций корзины |
| `/api/orders/` | CRUD заказов |
| `/api/order-items/` | CRUD позиций заказа |

## Запуск проекта через Docker

> Рекомендуемый способ запуска — Docker Compose, потому что проект настроен на PostgreSQL.

### 1. Клонировать репозиторий

```bash
git clone <repository-url>
cd kcell-online
```

### 2. Создать файл окружения

Создайте файл `.env` в корне проекта:

```env
POSTGRES_DB=online_shop
POSTGRES_USER=shop_user
POSTGRES_PASSWORD=shop_password
POSTGRES_HOST=db
POSTGRES_PORT=5432
```

### 3. Запустить backend и базу данных

Если в репозитории используется только Django backend, удобнее запустить backend и PostgreSQL так:

```bash
docker compose up --build backend db
```

После запуска приложение будет доступно по адресу:

```text
http://localhost:8000/
```

Django admin:

```text
http://localhost:8000/admin/
```

> В `docker-compose.yml` также описан сервис `frontend`. Его можно запускать, если в проект добавлено отдельное frontend-приложение с собственным `Dockerfile`.

### 4. Создать администратора

В отдельном терминале выполните:

```bash
docker compose exec backend python manage.py createsuperuser
```

### 5. Добавить данные

Через Django admin можно создать:

1. категории товаров;
2. товары;
3. изображения товаров;
4. пользователей, корзины и заказы для проверки.

## Локальный запуск без Docker

Локальный запуск также возможен, но для него нужен доступный PostgreSQL.

### 1. Создать и активировать virtual environment

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
```

Для Windows PowerShell:

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 2. Установить зависимости

```bash
pip install -r requirements.txt
```

### 3. Настроить переменные окружения

Пример для Linux/macOS:

```bash
export POSTGRES_DB=online_shop
export POSTGRES_USER=shop_user
export POSTGRES_PASSWORD=shop_password
export POSTGRES_HOST=localhost
export POSTGRES_PORT=5432
```

Пример для Windows PowerShell:

```powershell
$env:POSTGRES_DB="online_shop"
$env:POSTGRES_USER="shop_user"
$env:POSTGRES_PASSWORD="shop_password"
$env:POSTGRES_HOST="localhost"
$env:POSTGRES_PORT="5432"
```

### 4. Применить миграции

```bash
python manage.py migrate
```

### 5. Создать администратора

```bash
python manage.py createsuperuser
```

### 6. Запустить сервер

```bash
python manage.py runserver
```

Приложение откроется по адресу:

```text
http://127.0.0.1:8000/
```

## Проверка REST API

### Регистрация

```bash
curl -X POST http://localhost:8000/api/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "demo",
    "email": "demo@example.com",
    "password": "strong-password-123",
    "password_confirm": "strong-password-123"
  }'
```

### Получение JWT token

```bash
curl -X POST http://localhost:8000/api/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "demo",
    "password": "strong-password-123"
  }'
```

Ответ содержит `access` и `refresh`. Access token нужно передавать в защищённые endpoints:

```bash
curl http://localhost:8000/api/orders/ \
  -H "Authorization: Bearer <access-token>"
```

## Работа с данными

Типичный flow проверки проекта:

1. Создать суперпользователя.
2. Зайти в `/admin/`.
3. Добавить категории и товары.
4. Зарегистрировать обычного пользователя через `/signup/` или `/api/register/`.
5. Открыть каталог `/`.
6. Добавить товары в корзину.
7. Перейти в `/checkout/` и оформить заказ.
8. Проверить созданный заказ в Django admin или через `/api/orders/`.

## Команды для разработки

Запуск миграций:

```bash
python manage.py migrate
```

Создание новых миграций:

```bash
python manage.py makemigrations
```