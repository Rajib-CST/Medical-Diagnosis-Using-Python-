# Medical Diagnosis Expert System

This is an Expert System Shell written in Python using [experta](https://pypi.org/project/experta/) which predicts the disease a person has according to the symptoms inputted. It now includes a Flask web interface that presents the knowledge base and its closest explainable matches.

## Installation

Use the below command to install all requirements of the project and then start the web app.

```bash
pip install -r requirements.txt
python app.py
```

Open http://127.0.0.1:5000 in a browser.

## Usage

The original command-line version can still be run with `python Main.py`. The website provides the same knowledge-base profiles through selectable symptom levels and ranks partial matches when there is no exact rule match.

This project is for educational purposes only and is not a medical diagnosis tool. Seek advice from a qualified healthcare professional for real symptoms.

## License
[MIT](https://choosealicense.com/licenses/mit/)
