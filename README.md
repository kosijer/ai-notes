# **Project Name**

_A brief, engaging description of your project._

---

## **Table of Contents**

1. [Overview](#overview)
2. [Features](#features)
3. [Tech Stack](#tech-stack)
4. [Installation](#installation)
5. [Usage](#usage)
6. [Testing](#testing)
7. [Contributing](#contributing)
8. [License](#license)

---

## **Overview**

This project is a Python-based **Smart Notes Organizer** that allows users to create, categorize, and search notes with AI-powered features like sentiment analysis and automatic categorization. It uses the OpenAI API for intelligent features, such as automatically proposing the category, creating the summary, and detecting the sentiment of the note.

There is a clever search that runs through the `nlq_search` library, but currently, it doesn't always give relevant results, so it has to be investigated. The route with the query can be found in `app.py`, and the commented implementation is in the `index.html` template file.

Not sure if `nlq_search` uses some of the AI services or it just had "smart" logic. I will try to do the research tomorrow and maybe try to utilitse OpenAI for that purpose.

---

## **Features**

- Add, edit, delete, and view notes.
- Categorize notes into custom categories (e.g., Work, Personal).
- AI-powered features:
  - Automatic categorization based on note content.
  - Sentiment analysis of notes (Positive, Neutral, Negative).
  - Summarization of long notes.
- Search for notes using natural language queries.

---

## **Tech Stack**

- **Programming Language:** Python 3.x
- **Framework:** Flask
- **Database:** SQLite
- **Frontend:** HTML, CSS, JavaScript
- **AI Tools:** Hugging Face models, OpenAI API
- **Testing:** Pytest

---

## **Installation**

1. **Clone the repository:**

   ```bash
   git clone https://github.com/kosijer/ai-notes
   cd ai-notes
   ```

2. **Set up a virtual environment:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Linux/Mac
   venv\Scripts\activate     # On Windows
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

---

## **Usage**

1. Start the server by running `python app.py`.
2. Open your browser and go to `http://127.0.0.1:5000`.
3. Use the application to add, categorize, and search notes.

---

## **Testing**

To run tests:

1. Install testing dependencies (if not already installed):
   ```bash
   pip install pytest
   ```
2. Run the test suite:
   ```bash
   pytest
   ```

---

## **Contributing**

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-name`).
3. Commit your changes (`git commit -m "Add feature"`).
4. Push to the branch (`git push origin feature-name`).
5. Open a pull request.

---

## **License**

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## **Acknowledgments**

- [Flask Documentation](https://flask.palletsprojects.com/)
- [SQLite Documentation](https://sqlite.org/docs.html)
- [Hugging Face](https://huggingface.co/)
