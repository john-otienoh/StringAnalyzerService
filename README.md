# String Analyzer API

A RESTful API built with FastAPI and SQLite that analyzes strings and stores computed properties.

Features

- Analyze and store string properties

- Retrieve strings with advanced filters

- Query strings using natural language

- Delete stored strings

## Tech Stack

Python 3.10+

FastAPI

SQLAlchemy

SQLite

##  Setup Instructions
1. Clone the repository
git clone https://github.com/john-otienoh/StringAnalyzerService</br>
cd StringServiceAnalyzer

2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # for macOS/Linux
venv\Scripts\activate     # for Windows

3. Install dependencies
pip install -r requirements.txt

4. Run locally
uvicorn api.main:app --reload



## API Endpoints
1. Create & Analyze String

POST /strings

```
{
  "value": "madam"
}
```


Response (201):
```
{
  "id": "4a7d1ed414474e4033ac29ccb8653d9b",
  "value": "madam",
  "properties": {
    "length": 5,
    "is_palindrome": true,
    "unique_characters": 3,
    "word_count": 1,
    "sha256_hash": "4a7d1ed414474e4033ac29ccb8653d9b",
    "character_frequency_map": {"m": 2, "a": 2, "d": 1}
  },
  "created_at": "2025-10-20T12:00:00Z"
}
```

2. Get Specific String

```
GET /strings/{string_value}
```

3. Filter Strings

```
GET /strings?is_palindrome=true&min_length=3&contains_character=a
```


4. Natural Language Filter
```
GET /strings/filter-by-natural-language?query=all single word palindromic strings
```

5. Delete String
```
DELETE /strings/{string_value}
```

