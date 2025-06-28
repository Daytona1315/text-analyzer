# Task Analyzer

**Task Analyzer** is a Flask-based web application for analyzing text and uploaded files. Users can input text directly or upload files to get detailed text statistics.

## Features

- 📄 Analyze text for:
  - Number of characters
  - Number of words
  - Number of numbers
  - Number of punctuation marks
  - Number of spaces
- 📂 Upload and process files:
  - Supported formats: `.txt`, `.doc`, `.docx`, `.pdf`
  - Automatic text extraction depending on file type
- ⚡ Dynamic updates via [HTMX](https://htmx.org) (no page reload)

## Tech Stack

- Python 3.11+
- Flask
- HTMX + Bootstrap 5
- Poetry (dependency management)
