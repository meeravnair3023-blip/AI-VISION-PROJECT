# AI-VISION-PROJECT
AI-powered product recognition system that detects items from images and retrieves structured data from a database. Built using FastAPI, Ollama (LLaVA), LangChain, MySQL, and Gradio. Implements strict validation, intelligent search logic, and scalable backend design for real-world applications.
# AI Vision Product Recognition System

An end-to-end AI-powered application that detects products from images and retrieves structured product information such as category and pricing from a database.

This project integrates computer vision, large language models, and backend services to build a scalable and practical product recognition system.

---

## Features

* Image-based product detection using a vision-language model (LLaVA via Ollama)
* Structured JSON output with strict validation using Pydantic
* Intelligent product matching supporting variations, brands, and aliases
* MySQL database integration for product catalog management
* FastAPI backend with well-defined API structure and error handling
* Gradio-based interface for interactive user experience
* Modular architecture for easy extensibility and maintenance

---

## Technology Stack

* Backend: FastAPI
* AI Model: Ollama (LLaVA) via LangChain
* Database: MySQL (SQLAlchemy ORM)
* Validation: Pydantic
* User Interface: Gradio
* Programming Language: Python

---

## Project Structure

```id="j9kl2p"
app/
 ├── api/                # FastAPI routes
 ├── services/           # AI processing and database logic
 ├── schemas/            # Pydantic models
 ├── db/                 # Database models and session
 ├── core/               # Configuration settings
 └── ui/                 # Gradio interface
```

---

## System Workflow

```id="z8n1xb"
Image Input → AI Model → JSON Parsing → Validation → 
Normalization → Database Lookup → API Response → UI Display
```

---

## API Endpoint

### POST /api/v1/recognize/image

#### Request

* Content-Type: multipart/form-data
* Field: image

#### Success Response

```json id="d3m4qa"
{
  "status": "success",
  "recognized": true,
  "item_name": "laptop",
  "display_name": "Laptop - 15 inch",
  "category": "electronics",
  "price": 54999.00,
  "currency": "INR",
  "confidence": 0.94,
  "source": "image_upload",
  "message": "Item identified and price retrieved successfully"
}
```

---

## Error Handling

| Scenario                 | Status Code | Error Code             |
| ------------------------ | ----------- | ---------------------- |
| Unsupported image format | 400         | INVALID_IMAGE_FORMAT   |
| File too large           | 400         | FILE_TOO_LARGE         |
| Invalid AI response      | 502         | INVALID_MODEL_RESPONSE |
| Item not recognized      | 422         | ITEM_NOT_RECOGNIZED    |
| Database unavailable     | 503         | DB_CONNECTION_ERROR    |
| Low-quality image        | 422         | FRAME_QUALITY_TOO_LOW  |
| Model timeout            | 504         | MODEL_TIMEOUT          |

---

## Setup Instructions

### 1. Install dependencies

```id="g5w8sn"
pip install -r requirements.txt
```

### 2. Run FastAPI server

```id="k2l9mv"
uvicorn app.main:app --reload
```

### 3. Launch Gradio interface

```id="p0q7rt"
python app/ui/gradio_app.py
```

---

## Access Points

* FastAPI documentation: http://127.0.0.1:8000/docs
* Gradio interface: http://127.0.0.1:7860

---

## Example UI Output

```id="n4x6bp"
Item Detected Successfully

Product: Laptop - 15 inch
Category: electronics
Price: 54999 INR
Confidence: 94%
```

---

## Future Enhancements

* Fuzzy search for improved matching accuracy
* Advanced brand detection mechanisms
* Support for large-scale product catalogs
* Mobile application integration (Flutter)
* Real-time video frame recognition

---

