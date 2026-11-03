from pathlib import Path
import json

import pandas as pd
import streamlit as st


# =========================================================
# 1. CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="LearnGreen | Personalized Learning",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
)

PROJECT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_DIR / "data"
OUTPUT_DIR = PROJECT_DIR / "outputs"

RESOURCES_PATH = DATA_DIR / "learning_resources.csv"
INTERACTIONS_PATH = DATA_DIR / "student_learning_interactions.csv"
METRICS_PATH = OUTPUT_DIR / "evaluation_metrics.json"


# =========================================================
# 2. GREEN DASHBOARD DESIGN
# =========================================================

st.markdown(
    """
    <style>
    .stApp {
        background-color: #f4f8f4;
        color: #20352b;
    }

    [data-testid="stSidebar"] {
        background-color: #e5f2e8;
        border-right: 1px solid #d2e5d7;
    }

    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: #14583f;
    }

    .brand {
        color: #14583f;
        font-size: 29px;
        font-weight: 800;
        margin-bottom: 4px;
    }

    .subtitle {
        color: #526e5c;
        font-size: 14px;
    }

    .hero {
        background: linear-gradient(115deg, #e0f3e6, #f5fbf6);
        border: 1px solid #d4e9d9;
        border-radius: 18px;
        padding: 28px;
        margin-bottom: 25px;
    }

    .hero h1 {
        color: #14583f;
        font-size: 30px;
        margin: 0 0 12px 0;
    }

    .hero p {
        color: #456b55;
        font-size: 15px;
        margin-bottom: 0;
    }

    .section-heading {
        color: #174f38;
        font-size: 23px;
        font-weight: 750;
        margin-top: 25px;
        margin-bottom: 14px;
    }

    .metric-card {
        background: white;
        padding: 20px;
        border-radius: 15px;
        border: 1px solid #dce9df;
        min-height: 105px;
    }

    .metric-label {
        color: #64776a;
        font-size: 13px;
    }

    .metric-value {
        color: #1b6a49;
        font-size: 25px;
        font-weight: 800;
        margin-top: 10px;
    }

    .resource-title {
        color: #1b704b;
        font-size: 20px;
        font-weight: 750;
    }

    .tag {
        background-color: #e6f5eb;
        color: #1c704b;
        border-radius: 20px;
        padding: 5px 10px;
        font-size: 12px;
        font-weight: 700;
    }

    div[data-testid="stForm"] {
        background: white;
        border: 1px solid #d5e6d9;
        border-radius: 16px;
        padding: 22px;
    }

    div[data-testid="stForm"] label,
    div[data-testid="stForm"] label p {
        color: #24563e;
    }

    div[data-testid="stForm"] input {
        background-color: white;
        color: #20352b;
    }

    div[data-testid="stForm"] [data-baseweb="select"] > div {
        background-color: white;
        color: #20352b;
    }

    div.stButton > button[kind="primary"],
    div.stFormSubmitButton > button[kind="primary"] {
        background-color: #21845b;
        color: white;
        border: none;
        border-radius: 9px;
        min-height: 44px;
        font-weight: 700;
    }

    div.stButton > button[kind="primary"]:hover,
    div.stFormSubmitButton > button[kind="primary"]:hover {
        background-color: #14583f;
        color: white;
    }

    div[data-testid="stVerticalBlockBorderWrapper"] {
        border-color: #dce9df;
        border-radius: 15px;
    }

    .footer {
        color: #718176;
        font-size: 12px;
        text-align: center;
        padding: 12px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# 3. LOAD DATA
# =========================================================

@st.cache_data
def load_csv(path):
    if not path.exists():
        return pd.DataFrame()

    try:
        return pd.read_csv(path)
    except Exception:
        return pd.DataFrame()


@st.cache_data
def load_json(path):
    if not path.exists():
        return {}

    try:
        with open(path, "r", encoding="utf-8") as file:
            return json.load(file)
    except Exception:
        return {}


resources = load_csv(RESOURCES_PATH)
interactions = load_csv(INTERACTIONS_PATH)
metrics = load_json(METRICS_PATH)


# =========================================================
# 4. HELPER FUNCTIONS
# =========================================================

def find_column(dataframe, possible_names):
    """Find a column using alternative names."""

    lookup = {
        str(column).strip().lower().replace(" ", "_"): column
        for column in dataframe.columns
    }

    for name in possible_names:
        normalized = name.strip().lower().replace(" ", "_")

        if normalized in lookup:
            return lookup[normalized]

    return None


def get_value(row, possible_names, default="Not specified"):
    for name in possible_names:
        if name in row.index:
            value = row[name]

            if pd.notna(value) and str(value).strip():
                return str(value).strip()

    return default


def get_metric(possible_names):
    """Read an evaluation metric from the JSON file."""

    if not isinstance(metrics, dict):
        return None

    for key, value in metrics.items():
        normalized_key = (
            str(key).lower().replace("_", " ").replace("-", " ")
        )

        if any(name in normalized_key for name in possible_names):
            if isinstance(value, (int, float)):
                return float(value)

            if isinstance(value, dict):
                for nested_key, nested_value in value.items():
                    if (
                        any(
                            name in str(nested_key).lower()
                            for name in possible_names
                        )
                        and isinstance(nested_value, (int, float))
                    ):
                        return float(nested_value)

    return None


def show_metric(label, value, percentage=False):
    if value is None:
        display_value = "Not available"

    elif percentage:
        if value <= 1:
            display_value = f"{value * 100:.2f}%"
        else:
            display_value = f"{value:.2f}%"

    else:
        display_value = f"{value:,}"

    with st.container(border=True):
        st.caption(label)
        st.markdown(
            f'<div class="metric-value">{display_value}</div>',
            unsafe_allow_html=True,
        )


# =========================================================
# 5. PERSONALIZED RECOMMENDATION ENGINE
# =========================================================

def get_recommendations(
    dataframe,
    interest,
    learning_style,
    performance,
    completed_topics,
    number_of_results,
):
    """
    Rank resources using student preferences.

    Note: this function performs preference-based ranking.
    It does not run a trained Random Forest model.
    """

    if dataframe.empty:
        return pd.DataFrame()

    result = dataframe.copy()
    result["_score"] = 0

    category_col = find_column(
        result,
        [
            "category",
            "subject",
            "resource_category",
            "interest",
            "topic",
        ],
    )

    title_col = find_column(
        result,
        [
            "title",
            "resource_name",
            "name",
            "topic",
        ],
    )

    type_col = find_column(
        result,
        [
            "format",
            "learning_style",
            "resource_type",
            "type",
        ],
    )

    difficulty_col = find_column(
        result,
        [
            "difficulty",
            "difficulty_level",
            "level",
        ],
    )

    description_col = find_column(
        result,
        [
            "description",
            "summary",
            "resource_description",
        ],
    )

    # Match the student's interest.
    if category_col:
        result["_score"] += (
            result[category_col]
            .astype(str)
            .str.contains(interest, case=False, na=False)
            .astype(int) * 4
        )

    # Match the interest against titles and descriptions.
    for column in [title_col, description_col]:
        if column:
            result["_score"] += (
                result[column]
                .astype(str)
                .str.contains(interest, case=False, na=False)
                .astype(int) * 3
            )

    # Match the preferred learning format.
    if type_col:
        result["_score"] += (
            result[type_col]
            .astype(str)
            .str.contains(learning_style, case=False, na=False)
            .astype(int) * 3
        )

    # Rank resources by difficulty.
    if difficulty_col:

        if performance < 50:
            preferred_levels = ["beginner", "easy", "basic"]

        elif performance < 80:
            preferred_levels = ["intermediate", "medium"]

        else:
            preferred_levels = ["advanced", "intermediate"]

        def difficulty_score(value):
            value = str(value).lower()

            if any(level in value for level in preferred_levels):
                return 2

            return 0

        result["_score"] += result[difficulty_col].apply(
            difficulty_score
        )

    # Exclude completed topics where a matching title is available.
    completed = [
        topic.strip().lower()
        for topic in completed_topics.split(",")
        if topic.strip()
    ]

    if title_col and completed:

        def already_completed(title):
            title = str(title).lower()

            return any(
                topic in title or title in topic
                for topic in completed
            )

        result = result[
            ~result[title_col].apply(already_completed)
        ]

    if result.empty:
        return result

    result = result.sort_values(
        by="_score",
        ascending=False,
        kind="stable",
    )

    result = result.head(number_of_results).copy()

    result.insert(
        0,
        "Recommendation Score",
        result["_score"],
    )

    result.drop(columns=["_score"], inplace=True)

    return result


# =========================================================
# 6. DISPLAY ONE RECOMMENDATION CARD
# =========================================================

def show_resource_card(row, rank):
    title = get_value(
        row,
        ["title", "resource_name", "name", "topic"],
        "Learning Resource",
    )

    category = get_value(
        row,
        ["category", "subject", "resource_category"],
        "Learning",
    )

    resource_type = get_value(
        row,
        ["format", "learning_style", "resource_type", "type"],
        "Resource",
    )

    difficulty = get_value(
        row,
        ["difficulty", "difficulty_level", "level"],
    )

    description = get_value(
        row,
        ["description", "summary", "resource_description"],
        "",
    )

    link = get_value(
        row,
        ["url", "link", "resource_url"],
        "",
    )

    # Native Streamlit components: no HTML card code.
    with st.container(border=True):

        st.caption(f"RECOMMENDATION #{rank}")

        st.markdown(
            f'<div class="resource-title">{title}</div>',
            unsafe_allow_html=True,
        )

        tag1, tag2 = st.columns(2)

        with tag1:
            st.markdown(
                f'<span class="tag">{category}</span>',
                unsafe_allow_html=True,
            )

        with tag2:
            st.markdown(
                f'<span class="tag">{resource_type}</span>',
                unsafe_allow_html=True,
            )

        st.write("")

        st.write(f"**Difficulty:** {difficulty}")

        if description:
            st.write(description)

        if link.startswith(("https://", "http://")):
            st.link_button("Open learning resource ↗", link)


# =========================================================
# 7. SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown(
        '<div class="brand">🌿 LearnGreen</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="subtitle">Personalized Learning Platform</div>',
        unsafe_allow_html=True,
    )

    st.divider()

    st.markdown("### 🌱 Your learning space")

    st.write(
        "Create your learning profile and discover resources "
        "that match your preferences."
    )

    st.divider()

    st.caption("MACHINE LEARNING PROJECT")

    st.write("Personalized Learning Recommendation System")


# =========================================================
# 8. DASHBOARD HEADER
# =========================================================

st.markdown(
    """
    <div class="hero">
        <h1>Your learning journey, personalized 🌱</h1>
        <p>
            Choose your learning interests and preferred format.
            LearnGreen will rank suitable learning resources for you.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# 9. LEARNING OVERVIEW
# =========================================================

st.markdown(
    '<div class="section-heading">Learning overview</div>',
    unsafe_allow_html=True,
)

c1, c2, c3, c4 = st.columns(4)

with c1:
    show_metric("Learning Resources", len(resources))

with c2:
    show_metric("Interaction Records", len(interactions))

with c3:
    show_metric(
        "Model Accuracy",
        get_metric(["accuracy"]),
        percentage=True,
    )

with c4:
    show_metric(
        "F1-score",
        get_metric(["f1 score", "f1"]),
        percentage=True,
    )


# =========================================================
# 10. STUDENT PROFILE FORM
# =========================================================

st.markdown(
    '<div class="section-heading">🎯 Personalize your learning</div>',
    unsafe_allow_html=True,
)

st.write(
    "Tell us what you want to learn. Your personalized "
    "recommendations will appear below the form."
)

if resources.empty:

    st.error(
        "Learning resources could not be loaded. Check that "
        "data/learning_resources.csv exists in your project."
    )

else:

    category_col = find_column(
        resources,
        [
            "category",
            "subject",
            "resource_category",
            "interest",
            "topic",
        ],
    )

    type_col = find_column(
        resources,
        [
            "format",
            "learning_style",
            "resource_type",
            "type",
        ],
    )

    if category_col:
        interests = sorted(
            resources[category_col]
            .dropna()
            .astype(str)
            .unique()
            .tolist(),
            key=str.lower,
        )
    else:
        interests = []

    if type_col:
        learning_styles = sorted(
            resources[type_col]
            .dropna()
            .astype(str)
            .unique()
            .tolist(),
            key=str.lower,
        )
    else:
        learning_styles = []

    if not interests:
        interests = [
            "Python",
            "Data Science",
            "Web Development",
            "Machine Learning",
            "Database",
        ]

    if not learning_styles:
        learning_styles = [
            "Video",
            "Article",
            "Quiz",
            "Practice",
            "Course",
        ]

    with st.form("learning_profile_form"):

        left, right = st.columns(2)

        with left:

            student_name = st.text_input(
                "Student name (optional)",
                placeholder="Enter your name",
            )

            interest = st.selectbox(
                "Main learning interest",
                interests,
            )

            performance = st.slider(
                "Current performance score",
                min_value=0,
                max_value=100,
                value=75,
                help="Used to rank resources by difficulty.",
            )

        with right:

            learning_style = st.selectbox(
                "Preferred learning format",
                learning_styles,
            )

            completed_topics = st.text_input(
                "Topics already completed",
                placeholder="e.g. Python Basics, Variables",
                help="Separate multiple topics with commas.",
            )

            number_of_results = st.slider(
                "Number of recommendations",
                min_value=1,
                max_value=10,
                value=5,
            )

        submitted = st.form_submit_button(
            "🌿 Get My Recommendations",
            type="primary",
            use_container_width=True,
        )

    if submitted:

        st.session_state["learning_profile"] = {
            "name": student_name,
            "interest": interest,
            "learning_style": learning_style,
            "performance": performance,
            "completed_topics": completed_topics,
            "number_of_results": number_of_results,
        }

        st.session_state["recommendations"] = get_recommendations(
            resources,
            interest,
            learning_style,
            performance,
            completed_topics,
            number_of_results,
        )


# =========================================================
# 11. PERSONALIZED RECOMMENDATIONS
# =========================================================

st.markdown(
    '<div class="section-heading">✨ Your recommended learning resources</div>',
    unsafe_allow_html=True,
)

profile = st.session_state.get("learning_profile")
recommendations = st.session_state.get("recommendations")

if recommendations is None:

    st.info(
        "Complete your learning profile above and click "
        "**Get My Recommendations** to see your results here."
    )

elif recommendations.empty:

    st.warning(
        "No resources matched your preferences after excluding "
        "completed topics. Try changing your interest or clearing "
        "the completed-topics field."
    )

else:

    if profile:

        name = profile.get("name", "").strip()

        if name:
            st.success(f"Your recommendations are ready, {name}!")

        else:
            st.success(
                f"{len(recommendations)} personalized resources found."
            )

        st.caption(
            f"Interest: {profile['interest']} · "
            f"Format: {profile['learning_style']}"
        )

    for rank, (_, row) in enumerate(
        recommendations.iterrows(),
        start=1,
    ):
        show_resource_card(row, rank)

    st.download_button(
        label="⬇️ Download Recommendations as CSV",
        data=recommendations.to_csv(index=False).encode("utf-8"),
        file_name="learngreen_recommendations.csv",
        mime="text/csv",
        use_container_width=True,
    )


# =========================================================
# 12. MODEL AND DATASET INFORMATION
# =========================================================

with st.expander("📊 Model evaluation and dataset information"):

    st.subheader("Model evaluation")

    if metrics:
        st.json(metrics)
    else:
        st.info(
            "Evaluation metrics are not available. "
            "Check outputs/evaluation_metrics.json."
        )

    st.divider()

    st.subheader("Student interaction dataset")

    if not interactions.empty:

        st.write(f"Records: {len(interactions):,}")
        st.write(f"Columns: {len(interactions.columns)}")

        st.dataframe(
            interactions.head(10),
            use_container_width=True,
        )

    else:
        st.info("Student interaction dataset was not found.")

    st.divider()

    st.subheader("Learning resources dataset")

    if not resources.empty:

        st.write(f"Resources: {len(resources):,}")
        st.write(f"Columns: {len(resources.columns)}")

        st.dataframe(
            resources.head(10),
            use_container_width=True,
        )

    else:
        st.info("Learning resources dataset was not found.")


# =========================================================
# 13. FOOTER
# =========================================================

st.divider()

st.markdown(
    """
    <div class="footer">
        LearnGreen · Personalized Learning Recommendation System
        <br>
        Machine Learning Project
    </div>
    """,
    unsafe_allow_html=True,
)