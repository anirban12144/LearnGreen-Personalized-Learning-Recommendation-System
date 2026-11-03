# 🌱 LearnGreen – Personalized Learning Recommendation System

### Machine Learning | Python | Streamlit | Random Forest

LearnGreen is a Machine Learning-based Personalized Learning Recommendation System designed to provide students with suitable learning resources based on their academic performance, interests, preferred learning styles, and previously completed topics.

The system uses a Random Forest classification model to evaluate learning suitability and generate five ranked learning recommendations through an interactive Streamlit dashboard.

---

## 📌 1. Project Overview

Traditional learning systems often provide similar learning materials to every student without considering their individual abilities, interests, and learning preferences.

LearnGreen addresses this problem by analyzing individual student profiles and recommending suitable learning resources.

The system aims to make learning more personalized, accessible, and effective through Machine Learning.

---

## 🎯 2. Project Objectives

* Develop a personalized learning recommendation system.
* Analyze students' academic performance.
* Identify individual learning interests and preferences.
* Consider preferred learning styles and formats.
* Track previously completed learning topics.
* Generate ranked and suitable learning recommendations.
* Improve the overall learning experience through Machine Learning.

---

## ⚙️ 3. Key Features

* **Student Profile Analysis:** Collects student information and learning preferences.
* **Academic Performance Analysis:** Evaluates recent academic performance.
* **Interest-Based Recommendations:** Considers students' selected learning interests.
* **Learning Style Selection:** Supports different learning preferences.
* **Completed Topic Tracking:** Avoids recommending already completed topics.
* **Personalized Recommendations:** Generates five ranked learning recommendations.
* **Recommendation Scoring:** Displays suitability scores for recommended resources.
* **Interactive Dashboard:** Provides an easy-to-use Streamlit interface.
* **Machine Learning Integration:** Uses a trained Random Forest classification model.

---

## 🧠 4. Machine Learning Algorithm

### Random Forest Classifier

LearnGreen uses the Random Forest classification algorithm to evaluate the suitability of learning resources.

Random Forest is an ensemble learning algorithm that combines multiple decision trees to improve classification performance.

**Working Process:**

1. Collect student learning information.
2. Process student-related features.
3. Pass the input features to the trained Random Forest model.
4. Evaluate learning resource suitability.
5. Calculate recommendation scores.
6. Rank the suitable resources.
7. Display the top five recommendations.

### Why Random Forest?

* Handles multiple input features.
* Combines predictions from multiple decision trees.
* Can model nonlinear relationships.
* Reduces overfitting compared with relying on a single decision tree.

---

## 📊 5. Dataset Description

The project uses synthetic learning-related datasets.

The dataset information includes:

| Dataset Component    | Details                       |
| -------------------- | ----------------------------- |
| Student Interactions | 2,500 records                 |
| Student Features     | 10 columns                    |
| Learning Resources   | 104 resources                 |
| Data Type            | Structured data               |
| Application          | Learning suitability analysis |

The student interaction data supports model training and evaluation, while the learning resource dataset provides information used to generate recommendations.

---

## 📈 6. Model Performance

The Random Forest model was evaluated using 500 held-out test records.

| Evaluation Metric |  Score |
| ----------------- | -----: |
| Accuracy          | 86.80% |
| Precision         | 94.06% |
| Recall            | 90.62% |
| F1-Score          | 92.31% |

### Evaluation Metrics Explained

* **Accuracy:** Measures the proportion of correctly classified predictions.
* **Precision:** Measures how many positive predictions were correct.
* **Recall:** Measures how many actual positive cases were identified.
* **F1-Score:** Represents the harmonic mean of precision and recall.

---

## 🛠️ 7. Technologies Used

| Technology    | Purpose                         |
| ------------- | ------------------------------- |
| Python        | Main programming language       |
| Streamlit     | Interactive web application     |
| Scikit-learn  | Machine Learning implementation |
| Random Forest | Classification algorithm        |
| Pandas        | Data manipulation               |
| NumPy         | Numerical operations            |
| Matplotlib    | Data visualization              |
| Joblib        | Model serialization             |

---

## 🖥️ 8. Application Screenshots

### LearnGreen Dashboard

The dashboard allows students to enter their academic information, interests, learning preferences, and completed topics.

![LearnGreen Dashboard](screenshots/dashboard.png)

### Personalized Learning Recommendations

The system displays five ranked recommendations based on the student's profile and learning suitability.

![Learning Recommendations](screenshots/recommendations.png)

---

## 📂 9. Project Structure

```text
LearnGreen-Personalized-Learning-Recommendation-System/
│
├── src/
│   ├── streamlit_app.py
│   └── recommender.py
│
├── data/
│   └── Dataset files
│
├── outputs/
│   └── suitability_model.joblib
│
├── screenshots/
│   ├── dashboard.png
│   └── recommendations.png
│
├── requirements.txt
├── README.md
├── .gitignore
└── LICENSE
```

---

## 🚀 10. Installation and Setup

Follow these steps to run LearnGreen on your local machine.

### Step 1: Clone the Repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

### Step 2: Navigate to the Project Directory

```bash
cd LearnGreen-Personalized-Learning-Recommendation-System
```

### Step 3: Create a Virtual Environment

```bash
python -m venv .venv
```

### Step 4: Activate the Virtual Environment

**Windows:**

```powershell
.venv\Scripts\activate
```

**Linux / macOS:**

```bash
source .venv/bin/activate
```

### Step 5: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 6: Run the Application

```bash
streamlit run src/streamlit_app.py
```

### Step 7: Open the Application

Open your browser and visit:

```text
http://localhost:8501
```

---

## 🔮 11. Future Scope

The project can be enhanced through:

* Integration of additional educational resources.
* Improved recommendation algorithms.
* Student learning progress tracking.
* Adaptive learning pathways.
* Integration of more advanced Machine Learning techniques.
* Personalized learning analytics and reporting.

---

## 🎓 12. Project Information

**Project Name:** LearnGreen – Personalized Learning Recommendation System

**Project Domain:** Machine Learning

**Project Type:** Academic Project

**Student Name:** Anirban Sadhukhan

**Student Code:** BWU/BCA/24/086

**Department:** Department of Computational Sciences

**University:** Brainware University

**Group:** GR-1

---

## 👨‍💻 13. Author

**Anirban Sadhukhan**

Machine Learning Project – Personalized Learning Recommendation System.

---

## ⭐ 14. Acknowledgement

This project was developed as part of an academic learning initiative to explore the practical application of Machine Learning in personalized education.

If you find this project useful, consider giving the repository a ⭐ on GitHub.
