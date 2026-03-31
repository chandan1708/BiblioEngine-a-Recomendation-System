import os
import sys
import pickle
import streamlit as st
import numpy as np
import pandas as pd
from Recomendation_System.logger.log import logging
from Recomendation_System.exception.exception_handler import AppException
from Recomendation_System.config.configuration import AppConfiguration
from Recomendation_System.pipeline.training_pipeline import TrainingPipeline


# ─── Page Config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="BiblioEngine · Book Recommender",
    page_icon="B",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Premium Dark Theme CSS ─────────────────────────────────────────────────────
st.markdown("""
<style>
/* ── Import Google Fonts ── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Playfair+Display:wght@700&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200');

.material-symbols-outlined {
    font-family: 'Material Symbols Outlined';
    font-weight: normal;
    font-style: normal;
    font-size: 24px;
    display: inline-block;
    line-height: 1;
    text-transform: none;
    letter-spacing: normal;
    word-wrap: normal;
    white-space: nowrap;
    direction: ltr;
    vertical-align: middle;
    -webkit-font-smoothing: antialiased;
}

/* ── Global Overrides ── */
#MainMenu, footer, header {visibility: hidden;}

.stApp {
    background: linear-gradient(160deg, #0f0c29 0%, #1a1a2e 40%, #16213e 100%);
    font-family: 'Inter', sans-serif;
}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: rgba(15, 12, 41, 0.95);
    border-right: 1px solid rgba(255,255,255,0.06);
}
section[data-testid="stSidebar"] .stMarkdown p,
section[data-testid="stSidebar"] .stMarkdown li {
    color: #a0aec0;
    font-size: 0.88rem;
}

/* ── Hero Title ── */
.hero-title {
    font-family: 'Playfair Display', serif;
    font-size: 3.2rem;
    font-weight: 700;
    background: linear-gradient(135deg, #e0c3fc 0%, #8ec5fc 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-align: center;
    margin-bottom: 0.2rem;
    letter-spacing: -0.5px;
}
.hero-subtitle {
    text-align: center;
    color: #718096;
    font-size: 1.05rem;
    font-weight: 300;
    margin-bottom: 2.5rem;
    letter-spacing: 0.3px;
}

/* ── Divider ── */
.section-divider {
    border: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.08), transparent);
    margin: 2rem 0;
}

/* ── Search Area ── */
.search-label {
    color: #cbd5e0;
    font-size: 0.9rem;
    font-weight: 500;
    margin-bottom: 0.5rem;
    letter-spacing: 0.5px;
    text-transform: uppercase;
}

/* Selectbox styling */
div[data-baseweb="select"] > div {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 12px !important;
    color: #e2e8f0 !important;
    font-size: 0.95rem !important;
    padding: 2px 8px !important;
    transition: border-color 0.3s ease, box-shadow 0.3s ease;
}
div[data-baseweb="select"] > div:hover {
    border-color: rgba(142, 197, 252, 0.4) !important;
    box-shadow: 0 0 0 3px rgba(142, 197, 252, 0.08) !important;
}

/* ── Primary Button ── */
.stButton > button[kind="primary"],
.stButton > button {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.65rem 2rem !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
    letter-spacing: 0.3px !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 15px rgba(102, 126, 234, 0.25) !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 7px 20px rgba(102, 126, 234, 0.4) !important;
}

/* ── Sidebar Button ── */
section[data-testid="stSidebar"] .stButton > button {
    background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%) !important;
    box-shadow: 0 4px 15px rgba(245, 87, 108, 0.25) !important;
}
section[data-testid="stSidebar"] .stButton > button:hover {
    box-shadow: 0 7px 20px rgba(245, 87, 108, 0.4) !important;
}

/* ── Recommendation Section Title ── */
.rec-section-title {
    text-align: center;
    font-size: 1.3rem;
    font-weight: 600;
    color: #e2e8f0;
    margin: 2rem 0 1.5rem 0;
    letter-spacing: 0.3px;
}

/* ── Book Card ── */
.book-card {
    background: rgba(255, 255, 255, 0.04);
    border: 1px solid rgba(255, 255, 255, 0.07);
    border-radius: 16px;
    padding: 1.2rem 1rem;
    text-align: center;
    transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
}
.book-card:hover {
    transform: translateY(-6px);
    border-color: rgba(142, 197, 252, 0.25);
    box-shadow: 0 12px 40px rgba(0, 0, 0, 0.3), 0 0 0 1px rgba(142, 197, 252, 0.1);
    background: rgba(255, 255, 255, 0.07);
}

.book-cover {
    width: 140px;
    height: 200px;
    object-fit: cover;
    border-radius: 10px;
    margin-bottom: 1rem;
    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.4);
    transition: transform 0.3s ease;
}
.book-card:hover .book-cover {
    transform: scale(1.03);
}

.book-title {
    font-size: 0.88rem;
    font-weight: 500;
    color: #e2e8f0;
    margin: 0;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
    text-overflow: ellipsis;
    line-height: 1.45;
    min-height: 2.5em;
}

/* ── Info / Success / Error Boxes ── */
.stAlert > div {
    border-radius: 12px !important;
    font-size: 0.9rem !important;
}

/* ── Sidebar Branding ── */
.sidebar-brand {
    text-align: center;
    padding: 1rem 0 0.5rem 0;
}
.sidebar-brand-title {
    font-family: 'Playfair Display', serif;
    font-size: 1.5rem;
    font-weight: 700;
    background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0.5rem 0 0.2rem 0;
}
.sidebar-brand-sub {
    color: #718096;
    font-size: 0.78rem;
    letter-spacing: 2px;
    text-transform: uppercase;
}
.sidebar-divider {
    border: 0;
    height: 1px;
    background: rgba(255,255,255,0.08);
    margin: 1.2rem 0;
}
.sidebar-section-title {
    color: #a0aec0;
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    margin-bottom: 0.8rem;
}
.sidebar-stat {
    background: rgba(255,255,255,0.04);
    border-radius: 10px;
    padding: 0.8rem;
    margin-bottom: 0.6rem;
}
.sidebar-stat-label {
    color: #718096;
    font-size: 0.72rem;
    text-transform: uppercase;
    letter-spacing: 1px;
}
.sidebar-stat-value {
    color: #e2e8f0;
    font-size: 1.1rem;
    font-weight: 600;
}

/* ── Spinner ── */
.stSpinner > div > div {
    border-top-color: #667eea !important;
}

/* ── Footer ── */
.app-footer {
    text-align: center;
    color: #4a5568;
    font-size: 0.75rem;
    margin-top: 4rem;
    padding-bottom: 2rem;
    letter-spacing: 0.3px;
}
</style>
""", unsafe_allow_html=True)


# ─── Backend Logic ───────────────────────────────────────────────────────────────
class Recommendation:
    def __init__(self, app_config=AppConfiguration()):
        try:
            self.recommendation_config = app_config.get_recommendation_config()
        except Exception as e:
            raise AppException(e, sys) from e

    def fetch_poster(self, suggestion):
        try:
            book_name = []
            ids_index = []
            poster_url = []
            book_pivot = pickle.load(open(self.recommendation_config.book_pivot_serialized_objects, 'rb'))
            final_rating = pickle.load(open(self.recommendation_config.final_rating_serialized_objects, 'rb'))

            for book_id in suggestion:
                book_name.append(book_pivot.index[book_id])

            for name in book_name[0]:
                ids = np.where(final_rating['title'] == name)[0]
                if len(ids) > 0:
                    ids_index.append(ids[0])

            for idx in ids_index:
                url = final_rating.iloc[idx]['image_url']
                if pd.isna(url) or not str(url).startswith('http'):
                    url = "https://via.placeholder.com/140x200/1a1a2e/667eea?text=No+Cover"
                poster_url.append(url)
            return poster_url
        except Exception as e:
            logging.error(f"Error fetching posters: {e}")
            raise AppException(e, sys) from e

    def recommend_books(self, book_name):
        try:
            books_list = []
            model = pickle.load(open(self.recommendation_config.trained_model_path, 'rb'))
            book_pivot = pickle.load(open(self.recommendation_config.book_pivot_serialized_objects, 'rb'))
            book_id = np.where(book_pivot.index == book_name)[0][0]
            distances, suggestions = model.kneighbors(
                book_pivot.iloc[book_id, :].values.reshape(1, -1), n_neighbors=6
            )
            poster_url = self.fetch_poster(suggestions)

            for i in range(len(suggestions)):
                books = book_pivot.index[suggestions[i]]
                for j in books:
                    books_list.append(j)
            return books_list, poster_url
        except Exception as e:
            logging.error(f"Error in recommending books: {e}")
            raise AppException(e, sys) from e

    def train_engine(self):
        try:
            with st.spinner("Training the recommendation model — this may take a few minutes..."):
                obj = TrainingPipeline()
                obj.start_training_pipeline()
                logging.info("Training completed successfully")
            st.success("Model trained successfully. The system is ready to make recommendations.")
        except Exception as e:
            st.error(f"Training failed: {str(e)}")
            raise AppException(e, sys) from e

    def recommendations_engine(self, selected_books):
        try:
            with st.spinner(f"Finding books similar to \"{selected_books}\"..."):
                recommended_books, poster_url = self.recommend_books(selected_books)

            st.markdown('<p class="rec-section-title"><span class="material-symbols-outlined" style="font-size:1.3rem; margin-right:6px;">auto_stories</span>You Might Also Enjoy</p>', unsafe_allow_html=True)

            cols = st.columns(5, gap="medium")
            for idx, col in enumerate(cols):
                book_idx = idx + 1
                if book_idx < len(recommended_books) and book_idx < len(poster_url):
                    with col:
                        st.markdown(f"""
                        <div class="book-card">
                            <img src="{poster_url[book_idx]}" class="book-cover"
                                 onerror="this.src='https://via.placeholder.com/140x200/1a1a2e/667eea?text=No+Cover'"
                                 alt="{recommended_books[book_idx]}">
                            <p class="book-title">{recommended_books[book_idx]}</p>
                        </div>
                        """, unsafe_allow_html=True)
        except Exception as e:
            st.error("Something went wrong while generating recommendations. Please try again.")
            logging.error(f"Recommendation engine error: {e}")


# ─── Sidebar ─────────────────────────────────────────────────────────────────────
def render_sidebar():
    with st.sidebar:
        st.markdown("""
        <div class="sidebar-brand">
            <div><span class="material-symbols-outlined" style="font-size: 2.5rem; color: #f093fb;">menu_book</span></div>
            <div class="sidebar-brand-title">BiblioEngine</div>
            <div class="sidebar-brand-sub">Recommendation System</div>
        </div>
        <hr class="sidebar-divider">
        """, unsafe_allow_html=True)

        # System Info
        st.markdown('<p class="sidebar-section-title">System Status</p>', unsafe_allow_html=True)

        model_path = os.path.join('artifacts', 'trained_model', 'model.pkl')
        books_path = os.path.join('artifacts', 'serialized_objects', 'books_name.pkl')
        model_ready = os.path.exists(model_path)
        books_ready = os.path.exists(books_path)

        status_color = "#48bb78" if model_ready else "#f6ad55"
        status_text = "Trained" if model_ready else "Not Trained"
        st.markdown(f"""
        <div class="sidebar-stat">
            <div class="sidebar-stat-label">Model Status</div>
            <div class="sidebar-stat-value" style="color: {status_color};">● {status_text}</div>
        </div>
        """, unsafe_allow_html=True)

        if books_ready:
            book_names = pickle.load(open(books_path, 'rb'))
            st.markdown(f"""
            <div class="sidebar-stat">
                <div class="sidebar-stat-label">Books Indexed</div>
                <div class="sidebar-stat-value">{len(book_names):,}</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown('<hr class="sidebar-divider">', unsafe_allow_html=True)

        # Training Controls
        st.markdown('<p class="sidebar-section-title">Model Training</p>', unsafe_allow_html=True)
        st.markdown(
            "<p style='color: #718096; font-size: 0.82rem; margin-bottom: 1rem;'>"
            "Re-train the model to update recommendations with the latest data.</p>",
            unsafe_allow_html=True
        )

        if st.button('Train Model', use_container_width=True):
            obj = Recommendation()
            obj.train_engine()

        st.markdown('<hr class="sidebar-divider">', unsafe_allow_html=True)
        st.markdown(
            "<p style='color: #4a5568; font-size: 0.72rem; text-align: center;'>"
            "Built with Streamlit · v1.0</p>",
            unsafe_allow_html=True
        )


# ─── Main Page ───────────────────────────────────────────────────────────────────
def main():
    render_sidebar()

    # Hero
    st.markdown('<h1 class="hero-title">Discover Your Next Great Read</h1>', unsafe_allow_html=True)
    st.markdown(
        '<p class="hero-subtitle">Powered by collaborative filtering — find books loved by readers with similar taste.</p>',
        unsafe_allow_html=True
    )

    # Check readiness
    books_path = os.path.join('artifacts', 'serialized_objects', 'books_name.pkl')
    if not os.path.exists(books_path):
        st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
        st.info("**Welcome!** The recommendation engine hasn't been trained yet. "
                "Use the **Train Model** button in the sidebar to get started.")
        return

    book_names = pickle.load(open(books_path, 'rb'))

    # Search Section
    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

    col_left, col_center, col_right = st.columns([1, 2.5, 1])
    with col_center:
        st.markdown('<p class="search-label">Select a book you enjoyed</p>', unsafe_allow_html=True)
        selected_books = st.selectbox(
            "Select a book you enjoyed",
            book_names,
            index=0,
            label_visibility="collapsed",
            placeholder="Start typing a book name..."
        )

        recommend_btn = st.button("Get Recommendations", use_container_width=True, type="primary")

    # Results
    if recommend_btn:
        st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
        obj = Recommendation()
        obj.recommendations_engine(selected_books)

    # Footer
    st.markdown(
        '<p class="app-footer">BiblioEngine © 2026 · Collaborative Filtering Recommendation System</p>',
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()
