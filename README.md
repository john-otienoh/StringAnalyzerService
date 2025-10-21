# String Analyzer API

A RESTful API built with FastAPI and SQLite that analyzes strings and stores computed properties.

Features

- Analyze and store string properties

- Retrieve strings with advanced filters

- Query strings using natural language

- Delete stored strings

##  Setup Instructions

1. Clone the repository
```bash
git clone https://github.com/john-otienoh/StringAnalyzerService</br>
cd StringServiceAnalyzer
```

2. Create and activate a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # for macOS/Linux
venv\Scripts\activate     # for Windows
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Run locally
```bash
uvicorn api.main:app --reload
```

## Project Structure

```bash
string-analyzer/
│
├── main.py
├── db/
│   └── database.py
├── models/
│   └── string_analyzer.py
├── routers/
│   ├── __init__.py
│   ├── string_analyzer.py
│   └── filters.py
├── schemas/
│   ├── __init__.py
│   └── string_analyzer.py
├── services/
│   ├── string_service.py
│   └── filter_service.py
├── utils/
│   └── compute.py
└── __init__.py
│
├── tests/
│   └── test_api.py
│
├── requirements.txt
├── .gitignore
├── README.md
├── Procfile
├── runtime.txt
└── .env.example
```

### Dependencies

- FastAPI
- SQLModel
- SQLite
- Pydantic
- Uvicorn
- Pytest
- python-dotenv

Install automatically via `requirements.txt`.


## API Documentation

### Base URL

```URL
http://localhost:8000
```

### 1. Create / Analyze String

**POST /strings**

```json
Request Body:
{
  "value": "string to analyze"
}
```

**201 Created**

```json
{
  "id": "sha256_hash_value",
  "value": "string to analyze",
  "properties": {
    "length": 16,
    "is_palindrome": false,
    "unique_characters": 12,
    "word_count": 3,
    "sha256_hash": "abc123...",
    "character_frequency_map": {
      "s": 2,
      "t": 3
    }
  },
  "created_at": "2025-08-27T10:00:00Z"
}
```

### 2. Get Specific String

**GET /strings/{string_value}**
  **200 OK** – Returns stored string information.

### 3. Get All Strings (with filtering)

**GET /strings**
Query parameters:

```bash
is_palindrome=true
min_length=5
max_length=20
word_count=2
contains_character=a
```

**200 OK** – Returns filtered list.

### 4. Natural Language Filtering

**GET /strings/filter-by-natural-language**

```bash
?query=all single word palindromic strings
```

**200 OK** – AI-powered filter parsing.

### 5. Delete String

**DELETE /strings/{string_value}**
**204 No Content** – Deletes string entry.

