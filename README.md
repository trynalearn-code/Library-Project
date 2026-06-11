Library Project:

The project is creating a library database. There are books, and members. You can update books, add books, remove books. Members can also be created, updated and deleted. Books can be borrowed by members, and timeframes will be noted.

Description:

Library API is a RESTful backend application built with FastAPI and MySQL.

The system manages books and library members through HTTP requests only.

Users can:

- Add books
- Update books
- Register members
- Activate and deactivate members
- Borrow books
- Return books
- Generate reports

The application follows a layered architecture:

Routes → Database Classes → MySQL

All operations are available through FastAPI Swagger UI or Postman.
------
Technologies-
- Python 3.12
- FastAPI
- MySQL 8
- Docker
- mysql-connector-python
- Uvicorn
- Logging
- Git & GitHub

----------

docker setup

Run MySQL using Docker:

docker run --name mysql-Library -e MYSQL_ROOT_PASSWORD=root -e MYSQL_DATABASE=soldiers_db -p 3306:3306 -d mysql:8

Verify container:
docker ps

Stop container:
docker stop library_mysql

Start container:
docker start library_mysql

Project Structure:

library-api/  
│  
├── app/  
│   ├── main.py  
│   ├── database/  
│   │   ├── db\_connection.py  
│   │   ├── book\_db.py  
│   │   └── member\_db.py  
│   ├── routes/  
│   │   ├── book\_routes.py  
│   │   ├── member\_routes.py  
│   │   └── report\_routes.py  
│   └── logs/  
│       └── app.log  
│  
├── README.md  
├── requirements.txt  
└── .gitignore



---

# database tables:

books

| שדה | הסבר |
| ----- | ----: |
| `id` | מפתח ראשי |
| `title` | כותרת הספר, עמודה לא ריקה, מקסימום 50 תווים |
| `author` | שם המחבר, עמודה לא ריקה, מקסימום 50 תווים |
| `genre` | **ערכי `genre` מותרים:**  Fiction | Non-Fiction | Science | History | Other — מומש כעמודת ENUM במסד הנתונים, כל ערך אחר מחזיר שגיאה, עמודה לא ריקה |
| `is_available` | האם הספר זמין להשאלה — FALSE מסמן הושאל עמודה לא ריקה |
| `borrowed_by_member_id` | מזהה החבר שמחזיק את הספר — NULL אם זמין |

# Genres:

- Fiction
- Non-Fiction
- Science
- History
- Other

### members

| שדה | הסבר |
| ----- | ----: |
| `id` | מפתח ראשי |
| `name` | שם החבר, עמודה לא ריקה, מקסימום 50 תווים |
| `email` | כתובת מייל — ייחודית, עמודה לא ריקה |
| `is_active` | האם החבר פעיל — FALSE לא יכול להשאיל עמודה לא ריקה |
| `total_borrows` | מונה סה"כ השאלות — עולה ב-1 בכל השאלה עמודה לא ריקה |
---

## System Rules
וקי מערכת

| חוק | נושא | הכלל |
| ----: | ----: | ----: |
| 1 | יצירת ספר | המשתמש שולח title/author/genre — המערכת מוסיפה `is_available=True`, `borrowed_by=NULL` |
| 2 | genre | חייב להיות Fiction / Non-Fiction / Science / History / Other — כל ערך אחר מחזיר שגיאה יש לוודא הן בהוספה (POST) והן בעדכון (PATCH) |
| 3 | יצירת חבר | המשתמש שולח name/email — המערכת מוסיפה `is_active=True`, `total_borrows=0` |
| 4 | email | חייב להיות ייחודי — אם קיים כבר מחזיר שגיאה |
| 5 | חבר לא פעיל | אם `is_active=False` — אי אפשר להשאיל ספר |
| 6 | ספר לא זמין | אי אפשר להשאיל ספר שכבר מושאל (`is_available=False`) |
| 7 | מקסימום ספרים | חבר לא יכול להחזיק יותר מ-3 ספרים בו-זמנית |
| 8 | החזרת ספר | ניתן להחזיר ספר רק אם הוא מושאל לאותו חבר שמחזיר אותו |

---

## Endpoints

### Books

| Method | Endpoint | תיאור |
| :---- | :---- | :---- |
| `POST` | `/books` | יצירת ספר |
| `GET` | `/books` | כל הספרים |
| `GET` | `/books/{id}` | ספר לפי ID |
| `PATCH` | `/books/{id}` | עדכון ספר |
| `PATCH` | `/books/{id}/borrow/{member_id}` | השאלת ספר לחבר |
| `PATCH` | `/books/{id}/return/{member_id}` | החזרת ספר מחבר |

### Members

| Method | Endpoint | תיאור |
| :---- | :---- | ----: |
| `POST` | `/members` | יצירת חבר |
| `GET` | `/members` | כל החברים |
| `GET` | `/members/{id}` | חבר לפי ID |
| `PATCH` | `/members/{id}` | עדכון חבר |
| `PATCH` | `/members/{id}/deactivate` | השבתת חבר |
| `PATCH` | `/members/{id}/activate` | הפעלת חבר |

### Reports

| Method | Endpoint | תיאור |
| :---- | :---- | ----- |
| `GET` | `/reports/summary` | דוח כללי |
| `GET` | `/reports/books-by-genre` | ספרים לפי ז'אנר |
| `GET` | `/reports/top-member` | החבר הכי פעיל |
---

## System Flow

Client Request

↓

FastAPI Route

↓

Database Class (BookDB / MemberDB)

↓

MySQL Database

↓

Response Returned To Client

### Example: Borrow Book

PATCH /books/1/borrow/2

↓

Validate book exists

↓

Validate member exists

↓

Validate member active

↓

Validate book available

↓

Validate member has fewer than 3 books

↓

Update book status

↓

Increment member borrow count

↓

Return success response

---

## Running The Project

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Start MySQL Container

```bash
docker start library_mysql
```

### Run FastAPI

```bash
uvicorn app.main:app --reload
```

### Open Swagger UI

```text
http://127.0.0.1:8000/docs
```

---

## Logging Format

The application logs all important actions using the following format:

```text
YYYY-MM-DD HH:MM:SS | LEVEL | MESSAGE
```

Examples:

```text
2026-06-07 10:30:12 | INFO  | POST /books called
2026-06-07 10:30:13 | ERROR | Book not found: 42
2026-06-07 10:30:14 | INFO  | Book 42 borrowed by member 7
```

Logging is performed:

- At the start of every REST endpoint
- Before database updates
- On every error
- At the successful completion of every REST endpoint