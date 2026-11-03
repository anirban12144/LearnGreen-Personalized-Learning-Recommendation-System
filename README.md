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

The Random Forest m
