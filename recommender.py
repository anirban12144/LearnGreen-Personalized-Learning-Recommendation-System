from pathlib import Path
import json
import pandas as pd
import streamlit as st

# --------------------------------------------------
# 1. PROJECT PATHS AND CONFIGURATION
# --------------------------------------------------

PROJECT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_DIR / "data"
OUTPUT_DIR = PROJECT_DIR / "outputs"

RESOURCES_FILE = DATA_DIR / "learning_resources.csv"
INTERACTIONS_FILE = DATA_DIR / "student_learning_interactions.csv"
METRICS_FILE = OUTPUT_DIR / "evaluation_metrics.json"

st.set_page_config(
    page_title="LearnGreen | Personalized Learning",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------------------------------------
# 2. LOAD DATA
# --------------------------------------------------

@st.cache_data
def load_resources():
    if RESOURCES_FILE.exists():
        return pd.read_csv(RESOURCES_FILE)
    return pd.DataFrame()


@st.cache_data
def load_interactions():
    if INTERACTIONS_FILE.exists():
        return pd.read_csv(INTERACTIONS_FILE)
    return pd.DataFrame()


@st.cache_data
def load_metrics():
    if METRICS_FILE.exists():
        with open(METRICS_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    return {}


resources = load_resources()
interactions = load_interactions()
metrics = load_metrics()

# --------------------------------------------------
# 3. GREEN DASHBOARD DESIGN
# --------------------------------------------------

st.markdown("""
<style>
    .stApp {
        background-color: #f5f8f5;
        color: #183b2b;
    }

    [data-testid="stSidebar"] {
        background-color: #e6f2e9;
    }

    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] p {
        color: #174b32;
    }

    .hero {
        background: linear-gradient(120deg, #176b45, #35a66b);
        padding: 30px;
        border-radius: 18px;
        color: white;
        margin-bottom: 25px;
    }

    .hero h1 {
        color: white;
        font-size: 34px;
        margin-bottom: 8px;
    }

    .hero p {
        color: #effff4;
        font-size: 16px;
    }

    .metric-card {
        background: white;
        padding: 22px;
        border-radius: 14px;
        border: 1px solid #dce9df;
        box-shadow: 0 3px 12px rgba(28, 85, 52, 0.06);
        margin-bottom: 10px;
    }

    .metric-label {
        color: #64806d;
        font-size: 14px;
    }

    .metric-value {
        color: #176b45;
        font-size: 29px;
        font-weight: 700;
        margin-top: 7px;
    }

    .resource-card {
        background: white;
        border: 1px solid #dce9df;
        border-radius: 14px;
        padding: 18px;
        margin-bottom: 14px;
    }

    .resource-card h4 {
        color: #176b45;
        margin-bottom: 8px;
    }

    .tag {
        display: inline-block;
        background: #e5f5e9;
        color: #176b45;
        padding: 5px 10px;
        border-radius: 20px;
        margin: 3px 5px 3px 0;
        font-size: 12px;
    }

    .section-heading {
        color: #176b45;
        font-size: 25px;
        font-weight: 700;
        margin-bottom: 12px;
    }

    div.stButton > button[kind="primary"] {
        background-color: #218653;
        border: none;
        border-radius: 9px;
        color: white;
    }

    div.stButton > button[kind="primary"]:hover {
        background-color: #176b45;
        color: white;
    }

    .footer {
        text-align: center;
        color: #718778;
        padding: 25px 0 10px 0;
        font-size: 13px;
    }

    a {
        color: #218653 !important;
    }
</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# 4. HELPER FUNCTIONS
# --------------------------------------------------

def metric_card(label, value):
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def get_column(options, columns):
    """Find the first matching column name."""
    for option in options:
        if option in columns:
            return option
    return None


def make_recommendations(
    interest,
    learning_style,
    performance_score,
    completed_topics,
    top_n
):
    """
    Simple recommendation ranking based on interest,
    preferred learning style, and completed topics.
    """

    if resources.empty:
        raise ValueError(
            "learning_resources.csv was not found or is empty."
        )

    df = resources.copy()

    category_col = get_column(
        ["category", "resource_category"],
        df.columns
    )

    topic_col = get_column(["topic"], df.columns)

    type_col = get_column(
        ["resource_type", "learning_style"],
        df.columns
    )

    difficulty_col = get_column(["difficulty"], df.columns)

    if category_col is None or topic_col is None:
        raise ValueError(
            "The resources CSV must contain category and topic columns."
        )

    df["Recommendation Score"] = 0

    # Match the student's subject interest.
    interest_match = (
        df[category_col].astype(str).str.strip().str.lower()
        == interest.strip().lower()
    )

    df.loc[interest_match, "Recommendation Score"] += 3

    # Match the student's preferred learning style.
    if type_col:
        style_match = (
            df[type_col].astype(str).str.strip().str.lower()
            == learning_style.strip().lower()
        )

        df.loc[style_match, "Recommendation Score"] += 2

    # Give beginner resources a small preference
    # when the performance score is lower.
    if difficulty_col:
        if performance_score < 40:
            df.loc[
                df[difficulty_col].astype(str).str.lower()
                == "beginner",
                "Recommendation Score"
            ] += 2

        elif performance_score < 70:
            df.loc[
                df[difficulty_col].astype(str).str.lower()
                == "intermediate",
                "Recommendation Score"
            ] += 2

        else:
            df.loc[
                df[difficulty_col].astype(str).str.lower()
                == "advanced",
                "Recommendation Score"
            ] += 2

    # Avoid recommending topics the student has completed.
    completed_lower = {
        str(topic).strip().lower()
        for topic in completed_topics
        if str(topic).strip()
    }

    df["Already Completed"] = (
        df[topic_col].astype(str).str.strip().str.lower()
        .isin(completed_lower)
    )

    df = df.sort_values(
        by=["Already Completed", "Recommendation Score"],
        ascending=[True, False]
    )

    # Prefer different topics instead of repeating the same topic.
    df = df.drop_duplicates(subset=[topic_col], keep="first")

    # Show the highest-ranked recommendations.
    results = df.head(top_n).copy()

    # Put the recommendation score into a readable percentage.
    # This is a ranking score, NOT a trained model probability.
    results["Match Score"] = (
        results["Recommendation Score"]
        / max(1, int(df["Recommendation Score"].max()))
        * 100
    ).round(0).astype(int).astype(str) + "%"

    results = results.drop(
        columns=["Recommendation Score", "Already Completed"],
        errors="ignore"
    )

    return results.reset_index(drop=True)


def show_resource_cards(data):
    if data.empty:
        st.info("No learning resources are available.")
        return

    topic_col = get_column(["topic"], data.columns)
    category_col = get_column(
        ["category", "resource_category"], data.columns
    )
    type_col = get_column(["resource_type"], data.columns)
    difficulty_col = get_column(["difficulty"], data.columns)
    time_col = get_column(["estimated_minutes"], data.columns)
    description_col = get_column(["description"], data.columns)
    url_col = get_column(["url"], data.columns)

    for _, row in data.iterrows():
        topic = row.get(topic_col, "Learning Resource") if topic_col else "Learning Resource"
        category = row.get(category_col, "General") if category_col else "General"
        resource_type = row.get(type_col, "Resource") if type_col else "Resource"
        difficulty = row.get(difficulty_col, "Not specified") if difficulty_col else "Not specified"
        description = row.get(description_col, "") if description_col else ""
        duration = row.get(time_col, "") if time_col else ""
        url = row.get(url_col, "") if url_col else ""

        st.markdown(
            f"""
            <div class="resource-card">
                <h4>{topic}</h4>
                <span class="tag">{category}</span>
                <span class="tag">{resource_type}</span>
                <span class="tag">{difficulty}</span>
                <p>{description}</p>
                <p><b>Estimated time:</b> {duration} minutes</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        if isinstance(url, str) and url.startswith(("https://", "http://")):
            st.link_button("Open Learning Resource", url)


# --------------------------------------------------
# 5. SIDEBAR NAVIGATION
# --------------------------------------------------

with st.sidebar:
    st.markdown("# 🌿 LearnGreen")
    st.caption("Personalized Learning Platform")
    st.divider()

    page_options = [
        "Dashboard",
        "Student Profile",
        "Recommendations",
        "Model Insights"
    ]

    if "main_navigation" not in st.session_state:
        st.session_state["main_navigation"] = "Dashboard"

    current_page = st.session_state["main_navigation"]

    if current_page not in page_options:
        current_page = "Dashboard"

    page = st.radio(
        "Navigation",
        page_options,
        index=page_options.index(current_page),
        key="navigation_radio"
    )

    st.session_state["main_navigation"] = page

    st.divider()
    st.caption("Learn • Grow • Succeed")


# --------------------------------------------------
# 6. DASHBOARD PAGE
# --------------------------------------------------

if page == "Dashboard":

    st.markdown(
        """
        <div class="hero">
            <h1>Welcome to LearnGreen 🌿</h1>
            <p>
                Discover learning resources that match your interests,
                preferred learning style, and learning progress.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        metric_card("Learning Resources", len(resources))

    with c2:
        metric_card("Student Interactions", len(interactions))

    with c3:
        accuracy = metrics.get("accuracy")
        accuracy_text = (
            f"{accuracy * 100:.1f}%"
            if isinstance(accuracy, (int, float))
            else "N/A"
        )
        metric_card("Model Accuracy", accuracy_text)

    with c4:
        f1 = metrics.get("f1_score")
        f1_text = (
            f"{f1 * 100:.1f}%"
            if isinstance(f1, (int, float))
            else "N/A"
        )
        metric_card("Model F1-Score", f1_text)

    st.markdown(
        '<div class="section-heading">Start Your Learning Journey</div>',
        unsafe_allow_html=True
    )

    left, right = st.columns([1.2, 1])

    with left:
        st.markdown(
            """
            <div class="resource-card">
                <h4>🎯 Personalized Recommendations</h4>
                <p>
                    Choose your interests and preferred learning style
                    to discover suitable resources.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

        if st.button("Explore Recommendations", type="primary"):
            st.session_state["main_navigation"] = "Recommendations"
            st.rerun()

    with right:
        st.markdown(
            """
            <div class="resource-card">
                <h4>👩‍🎓 Student Profile</h4>
                <p>
                    Enter your performance score, learning interests,
                    and completed topics.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

        if st.button("Create Student Profile", type="primary"):
            st.session_state["main_navigation"] = "Student Profile"
            st.rerun()

    st.markdown(
        '<div class="section-heading">Featured Learning Resources</div>',
        unsafe_allow_html=True
    )

    if not resources.empty:
        show_resource_cards(resources.head(3))


# --------------------------------------------------
# 7. STUDENT PROFILE PAGE
# --------------------------------------------------

elif page == "Student Profile":

    st.markdown(
        '<div class="section-heading">👩‍🎓 Student Profile</div>',
        unsafe_allow_html=True
    )

    st.write(
        "Tell us about your learning preferences to get suitable resources."
    )

    category_col = get_column(
        ["category", "resource_category"],
        resources.columns
    )

    available_interests = (
        sorted(resources[category_col].dropna().astype(str).unique().tolist())
        if category_col and not resources.empty
        else ["Python", "Data Science", "Machine Learning", "Web Development"]
    )

    type_col = get_column(["resource_type"], resources.columns)

    available_styles = (
        sorted(resources[type_col].dropna().astype(str).unique().tolist())
        if type_col and not resources.empty
        else ["Video", "Article", "Practice", "Interactive"]
    )

    saved_profile = st.session_state.get("student_profile", {})

    with st.form("student_profile_form"):

        name = st.text_input(
            "Student Name (optional)",
            value=saved_profile.get("name", "")
        )

        performance = st.slider(
            "Recent Performance Score",
            min_value=0,
            max_value=100,
            value=int(saved_profile.get("performance_score", 70))
        )

        interest = st.selectbox(
            "Main Learning Interest",
            available_interests
        )

        style = st.selectbox(
            "Preferred Learning Style",
            available_styles
        )

        completed_text = st.text_input(
            "Completed Topics (comma-separated)",
            value=saved_profile.get("completed_text", ""),
            placeholder="Example: Variables, Loops"
        )

        submitted = st.form_submit_button(
            "Save Student Profile",
            type="primary"
        )

    if submitted:
        st.session_state["student_profile"] = {
            "name": name,
            "performance_score": performance,
            "interest": interest,
            "learning_style": style,
            "completed_text": completed_text
        }

        st.success("Your student profile has been saved!")

        st.write("### Profile Summary")
        st.write(f"**Student:** {name or 'Student'}")
        st.write(f"**Performance:** {performance}/100")
        st.write(f"**Interest:** {interest}")
        st.write(f"**Preferred Style:** {style}")
        st.write(f"**Completed Topics:** {completed_text or 'None entered'}")

        if st.button("Get My Recommendations", type="primary"):
            st.session_state["main_navigation"] = "Recommendations"
            st.rerun()

    elif saved_profile:
        st.info("Your previously saved profile is available in this session.")


# --------------------------------------------------
# 8. RECOMMENDATIONS PAGE
# --------------------------------------------------

elif page == "Recommendations":

    st.markdown(
        '<div class="section-heading">🎯 Personalized Recommendations</div>',
        unsafe_allow_html=True
    )

    st.write(
        "Choose your preferences to find learning resources suited to you."
    )

    if resources.empty:
        st.error(
            "The learning resources file could not be found. "
            "Check that data/learning_resources.csv exists."
        )

    else:
        category_col = get_column(
            ["category", "resource_category"],
            resources.columns
        )

        type_col = get_column(["resource_type"], resources.columns)

        available_interests = (
            sorted(resources[category_col].dropna().astype(str).unique().tolist())
            if category_col
            else ["Python", "Data Science", "Machine Learning"]
        )

        available_styles = (
            sorted(resources[type_col].dropna().astype(str).unique().tolist())
            if type_col
            else ["Video", "Article", "Practice"]
        )

        saved_profile = st.session_state.get("student_profile", {})

        with st.form("recommendation_form"):

            interest_default = saved_profile.get("interest")
            if interest_default not in available_interests:
                interest_default = available_interests[0]

            style_default = saved_profile.get("learning_style")
            if style_default not in available_styles:
                style_default = available_styles[0]

            interest = st.selectbox(
                "Choose your interest",
                available_interests,
                index=available_interests.index(interest_default)
            )

            learning_style = st.selectbox(
                "Preferred learning style",
                available_styles,
                index=available_styles.index(style_default)
            )

            performance_score = st.slider(
                "Your performance score",
                0,
                100,
                int(saved_profile.get("performance_score", 70))
            )

            completed_text = st.text_input(
                "Topics you have already completed",
                value=saved_profile.get("completed_text", ""),
                placeholder="Example: Variables, Loops"
            )

            top_n = st.slider(
                "Number of recommendations",
                min_value=1,
                max_value=10,
                value=5
            )

            generate = st.form_submit_button(
                "Get Recommendations",
                type="primary"
            )

        if generate:
            completed_topics = [
                topic.strip()
                for topic in completed_text.split(",")
                if topic.strip()
            ]

            try:
                results = make_recommendations(
                    interest=interest,
                    learning_style=learning_style,
                    performance_score=performance_score,
                    completed_topics=completed_topics,
                    top_n=top_n
                )

                st.session_state["last_recommendations"] = results

                st.success("Your recommendations are ready!")

                st.caption(
                    "Match Score is a simple ranking score, not a probability "
                    "from the trained Random Forest model."
                )

            except (ValueError, KeyError, FileNotFoundError) as error:
                st.error(f"Could not generate recommendations: {error}")

        results = st.session_state.get("last_recommendations")

        if results is not None and not results.empty:

            st.markdown("### Your Recommended Resources")

            for index, row in results.iterrows():

                topic_col = get_column(["topic"], results.columns)
                category_col = get_column(
                    ["category", "resource_category"],
                    results.columns
                )
                type_col = get_column(["resource_type"], results.columns)
                difficulty_col = get_column(["difficulty"], results.columns)
                time_col = get_column(["estimated_minutes"], results.columns)
                description_col = get_column(["description"], results.columns)
                url_col = get_column(["url"], results.columns)

                topic = row.get(topic_col, "Learning Resource") if topic_col else "Learning Resource"
                category = row.get(category_col, "General") if category_col else "General"
                resource_type = row.get(type_col, "Resource") if type_col else "Resource"
                difficulty = row.get(difficulty_col, "Not specified") if difficulty_col else "Not specified"
                duration = row.get(time_col, "Not specified") if time_col else "Not specified"
                description = row.get(description_col, "") if description_col else ""
                match_score = row.get("Match Score", "N/A")
                url = row.get(url_col, "") if url_col else ""

                st.markdown(
                    f"""
                    <div class="resource-card">
                        <h4>{index + 1}. {topic}</h4>
                        <span class="tag">{category}</span>
                        <span class="tag">{resource_type}</span>
                        <span class="tag">{difficulty}</span>
                        <p>{description}</p>
                        <p><b>Estimated time:</b> {duration} minutes</p>
                        <p><b>Match score:</b> {match_score}</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                if isinstance(url, str) and url.startswith(("https://", "http://")):
                    st.link_button(
                        f"Open Resource: {topic}",
                        url,
                        key=f"resource_{index}"
                    )

            csv_data = results.to_csv(index=False).encode("utf-8")

            st.download_button(
                label="📥 Download Recommendations as CSV",
                data=csv_data,
                file_name="learngreen_recommendations.csv",
                mime="text/csv"
            )


# --------------------------------------------------
# 9. MODEL INSIGHTS PAGE
# --------------------------------------------------

elif page == "Model Insights":

    st.markdown(
        '<div class="section-heading">📊 Model Insights</div>',
        unsafe_allow_html=True
    )

    st.write("Review the saved evaluation metrics and project datasets.")

    if metrics:

        st.markdown("### Model Evaluation")

        metric_labels = {
            "accuracy": "Accuracy",
            "precision": "Precision",
            "recall": "Recall",
            "f1_score": "F1-Score"
        }

        metric_keys = [
            key for key in metric_labels if key in metrics
        ]

        if metric_keys:
            cols = st.columns(len(metric_keys))

            for col, key in zip(cols, metric_keys):
                value = metrics[key]

                if isinstance(value, (int, float)):
                    value = f"{value * 100:.2f}%"

                with col:
                    metric_card(metric_labels[key], value)

        if "test_rows" in metrics:
            st.info(f"Number of test records: {metrics['test_rows']}")

    else:
        st.warning(
            "No evaluation metrics file was found. "
            "Train and evaluate your model to generate it."
        )

    st.markdown("### Learning Resources Dataset")

    if not resources.empty:
        st.write(f"Total resources: {len(resources)}")
        st.dataframe(resources, use_container_width=True)

    else:
        st.warning("Learning resources dataset is unavailable.")

    st.markdown("### Student Interactions Dataset")

    if not interactions.empty:
        st.write(f"Total interaction records: {len(interactions)}")
        st.dataframe(interactions.head(100), use_container_width=True)

    else:
        st.info(
            "The student interactions dataset is not available. "
            "Other dashboard features can still work."
        )


# --------------------------------------------------
# 10. FOOTER
# --------------------------------------------------

st.markdown(
    """
    <div class="footer">
        🌿 LearnGreen — Learn Smarter, Grow Better
    </div>
    """,
    unsafe_allow_html=True
)
