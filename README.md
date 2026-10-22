# 🌌 Student Pass / Fail Predictor

**🔗 Live demo: [student-predictor on Streamlit](https://student-predictor-u5qhayjvfumnq34uhpwsq9.streamlit.app/)**

A small machine learning app that guesses whether a student will pass or fail, based on two things: how many hours they study per day and what they scored in their previous exam. I built it to practice taking a model from a notebook to something people can actually open and use in a browser.

<!-- Add a screenshot here after you take one:
![App screenshot](screenshot.png)
-->

## What it does

You move two sliders, press **Predict**, and the app shows the result along with how confident the model is. The whole page also changes its mood depending on the answer:

- **Before predicting:** a galaxy background with twinkling stars
- **Pass:** green aurora lights (and a few balloons 🎈)
- **Fail:** a deep wine-red theme

If you touch a slider afterwards, it goes back to the galaxy so an old result never sticks around.

## How it works

1. A Logistic Regression model (scikit-learn) is trained on a small dataset of `[study_hours, prev_score]` pairs.
2. The trained model is saved as `model.pkl` using joblib.
3. The Streamlit app loads that file once (cached) and predicts straight from the sliders' values.

Note: the training data is tiny (10 rows), so this is a learning and demo project, not a tool for real decisions about students.

## Tech stack

- Python
- scikit-learn, NumPy, joblib
- Streamlit (with custom CSS for the glass cards and animated themes)
- Deployed on Streamlit Community Cloud

## Run it locally

```bash
git clone https://github.com/YOUR-USERNAME/student-predictor.git
cd student-predictor
pip install -r requirements.txt
streamlit run streamlit_app.py
```

## Project structure

```
student-predictor/
├── streamlit_app.py      # the app (UI + prediction)
├── model.pkl             # trained model
├── requirements.txt
└── .streamlit/
    └── config.toml       # dark theme settings
```

## Made by

Fizza Irfan, Software Engineering student at the University of Lahore.