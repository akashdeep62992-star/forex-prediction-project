import streamlit as st

# Set page config must be the first Streamlit command
st.set_page_config(
    layout="wide",
    page_title="Forex Price Predictor",
    page_icon="📈",
    initial_sidebar_state="auto"
)

AUTHOR = "Akashdeep"

# Initialize session state for dark mode
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = False

# Unified Professional Color Theme
COLOR_THEME = {
    'light': {
        'primary': '#2563EB',      # Professional Blue
        'secondary': '#7C3AED',    # Purple Accent
        'accent': '#059669',       # Emerald Green
        'background': '#F8FAFC',   # Light Gray
        'card': '#FFFFFF',         # White
        'text': '#1E293B',         # Dark Gray
        'muted': '#64748B',        # Secondary text
        'border': '#E2E8F0',       # Light Border
        'sidebar': '#FFFFFF',      # Sidebar background
        'shadow': 'rgba(15, 23, 42, 0.08)',
        'shadow_hover': 'rgba(15, 23, 42, 0.14)'
    },
    'dark': {
        'primary': '#3B82F6',      # Bright Blue
        'secondary': '#8B5CF6',    # Light Purple
        'accent': '#10B981',       # Bright Green
        'background': '#0F172A',   # Dark Blue
        'card': '#1E293B',         # Dark Card
        'text': '#F1F5F9',         # Light Text
        'muted': '#94A3B8',        # Secondary text
        'border': '#334155',       # Dark Border
        'sidebar': '#111827',      # Sidebar background
        'shadow': 'rgba(0, 0, 0, 0.35)',
        'shadow_hover': 'rgba(0, 0, 0, 0.5)'
    }
}

# Get current colors based on dark mode
colors = COLOR_THEME['dark' if st.session_state.dark_mode else 'light']

# Responsive, theme-aware CSS shared by every page
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

/* ===== THEME TOKENS ===== */
:root {{
    --primary-color: {colors['primary']};
    --secondary-color: {colors['secondary']};
    --accent-color: {colors['accent']};
    --bg-primary: {colors['background']};
    --bg-secondary: {colors['card']};
    --bg-sidebar: {colors['sidebar']};
    --text-primary: {colors['text']};
    --text-secondary: {colors['muted']};
    --border-color: {colors['border']};
    --gradient-primary: linear-gradient(135deg, {colors['primary']} 0%, {colors['secondary']} 100%);
    --gradient-accent: linear-gradient(135deg, {colors['accent']} 0%, {colors['primary']} 100%);
    --shadow: 0 8px 24px {colors['shadow']};
    --shadow-hover: 0 16px 36px {colors['shadow_hover']};
    --radius-lg: clamp(14px, 2vw, 20px);
    --radius-md: 12px;
    --space-card: clamp(1rem, 2.5vw, 2rem);
}}

/* ===== GLOBAL ===== */
html {{
    -webkit-text-size-adjust: 100%;
}}

.stApp {{
    background: var(--bg-primary);
    color: var(--text-primary);
    font-family: 'Inter', 'Segoe UI', system-ui, -apple-system, sans-serif;
}}

.stApp, .stApp p, .stApp li, .stApp label, .stApp span,
[data-testid="stMarkdownContainer"],
[data-testid="stWidgetLabel"],
[data-testid="stCaptionContainer"] {{
    color: var(--text-primary);
}}

[data-testid="stCaptionContainer"] {{
    color: var(--text-secondary) !important;
}}

[data-testid="stHeader"] {{
    background: var(--bg-primary);
}}

/* Main content width + fluid gutters */
.block-container, [data-testid="stMainBlockContainer"] {{
    max-width: 1320px;
    padding-top: clamp(2.5rem, 5vw, 4rem) !important;
    padding-left: clamp(1rem, 4vw, 3rem) !important;
    padding-right: clamp(1rem, 4vw, 3rem) !important;
    padding-bottom: 3rem !important;
}}

/* Media never overflows its column */
[data-testid="stImage"] img,
[data-testid="stMarkdownContainer"] img,
[data-testid="stPyplot"] img,
.stApp video {{
    max-width: 100%;
    height: auto;
}}

/* Keep the app's root from scrolling sideways on narrow screens */
[data-testid="stAppViewContainer"], [data-testid="stMain"] {{
    overflow-x: hidden;
}}

[data-testid="stImage"] img {{
    border-radius: var(--radius-md);
}}

[data-testid="stPlotlyChart"], .stPlotlyChart, .js-plotly-plot {{
    width: 100% !important;
}}

[data-testid="stDataFrame"], .stDataFrame, [data-testid="stTable"] {{
    max-width: 100%;
    overflow-x: auto;
    border: 1px solid var(--border-color);
    border-radius: var(--radius-md);
}}

pre, code {{
    white-space: pre-wrap;
    word-break: break-word;
}}

/* ===== TYPOGRAPHY (fluid) ===== */
h1 {{
    background: var(--gradient-primary);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    font-size: clamp(2rem, 4.5vw + 0.5rem, 3.5rem) !important;
    font-weight: 800 !important;
    line-height: 1.15 !important;
    text-align: center;
    margin-bottom: 0.75rem;
    letter-spacing: -0.02em;
    animation: fadeInUp 0.6s ease-out;
    overflow-wrap: anywhere;
}}

h2 {{
    font-size: clamp(1.4rem, 2.5vw + 0.6rem, 2.3rem) !important;
    font-weight: 700 !important;
    line-height: 1.25 !important;
    color: var(--text-primary) !important;
    text-align: center;
    margin: clamp(1.5rem, 4vw, 2.5rem) 0 clamp(1rem, 2.5vw, 1.75rem) 0;
    position: relative;
    overflow-wrap: anywhere;
}}

h2:after {{
    content: "";
    position: absolute;
    bottom: -10px;
    left: 50%;
    transform: translateX(-50%);
    width: 72px;
    height: 4px;
    background: var(--gradient-primary);
    border-radius: 2px;
}}

h2[style*="left"]:after {{
    left: 0;
    transform: none;
}}

/* Streamlit's own st.header / st.subheader */
[data-testid="stHeadingWithActionElements"] h2:after,
[data-testid="stDialog"] h2:after {{
    display: none;
}}

h3 {{
    font-size: clamp(1.1rem, 1.2vw + 0.8rem, 1.5rem) !important;
    font-weight: 600 !important;
    color: var(--primary-color) !important;
    margin-bottom: 0.75rem;
}}

p, li {{
    line-height: 1.7;
    font-size: clamp(0.95rem, 0.3vw + 0.88rem, 1.05rem);
}}

.page-lead {{
    text-align: center;
    font-size: clamp(1rem, 0.8vw + 0.85rem, 1.25rem) !important;
    max-width: 780px;
    margin: 0 auto 1.5rem auto;
    color: var(--text-secondary) !important;
}}

/* ===== CARDS ===== */
/* Empty wrapper divs left behind by st.markdown('<div ...>') render as blank boxes, so hide them */
.main-container:empty, .info-container:empty {{
    display: none;
}}

.info-card {{
    background: var(--bg-secondary);
    border-radius: var(--radius-lg);
    padding: var(--space-card);
    border: 1px solid var(--border-color);
    border-left: 4px solid var(--primary-color);
    box-shadow: var(--shadow);
    transition: transform 0.25s ease, box-shadow 0.25s ease, border-color 0.25s ease;
    height: 100%;
}}

.info-card ul {{
    padding-left: 1.25rem;
    margin: 0;
}}

.highlight-card {{
    background: var(--gradient-primary);
    border: none;
    border-left: 4px solid var(--accent-color);
}}

.highlight-card h3,
.highlight-card p,
.highlight-card li,
.highlight-card b {{
    color: #FFFFFF !important;
}}

@media (hover: hover) {{
    .info-card:hover {{
        transform: translateY(-4px);
        border-left-color: var(--accent-color);
        box-shadow: var(--shadow-hover);
    }}
}}

/* ===== BUTTONS ===== */
div[data-testid="stButton"] > button,
div[data-testid="stDownloadButton"] > button,
div[data-testid="stFormSubmitButton"] > button {{
    border-radius: var(--radius-md) !important;
    border: none !important;
    background: var(--gradient-primary) !important;
    color: #FFFFFF !important;
    padding: 0.65rem 1.5rem !important;
    min-height: 44px;
    font-weight: 600 !important;
    box-shadow: 0 4px 14px {colors['primary']}40 !important;
    transition: transform 0.2s ease, box-shadow 0.2s ease !important;
}}

div[data-testid="stButton"] > button p,
div[data-testid="stDownloadButton"] > button p {{
    color: #FFFFFF !important;
}}

@media (hover: hover) {{
    div[data-testid="stButton"] > button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 8px 22px {colors['primary']}60 !important;
    }}
}}

/* ===== FORM ELEMENTS ===== */
.stSelectbox div[data-baseweb="select"] > div,
.stMultiSelect div[data-baseweb="select"] > div,
.stTextInput input,
.stNumberInput input,
.stDateInput input,
.stTextArea textarea {{
    background: var(--bg-secondary) !important;
    color: var(--text-primary) !important;
    border-color: var(--border-color) !important;
    border-radius: var(--radius-md) !important;
}}

.stNumberInput input:focus, .stTextInput input:focus {{
    box-shadow: 0 0 0 3px {colors['primary']}33 !important;
}}

[data-testid="stFileUploaderDropzone"] {{
    background: var(--bg-secondary) !important;
    border: 2px dashed var(--border-color) !important;
    border-radius: var(--radius-lg) !important;
}}

/* ===== METRICS ===== */
[data-testid="stMetric"], [data-testid="metric-container"] {{
    background: var(--bg-secondary);
    border: 1px solid var(--border-color);
    border-radius: var(--radius-md);
    padding: clamp(0.75rem, 1.5vw, 1rem);
    box-shadow: var(--shadow);
    height: 100%;
}}

[data-testid="stMetricValue"] {{
    font-size: clamp(1.15rem, 1.5vw + 0.7rem, 1.9rem) !important;
    color: var(--text-primary) !important;
    overflow-wrap: anywhere;
    white-space: normal !important;
}}

[data-testid="stMetricValue"] * {{
    white-space: normal !important;
    overflow: visible !important;
    text-overflow: clip !important;
}}

[data-testid="stMetricLabel"] p {{
    color: var(--text-secondary) !important;
    white-space: normal !important;
}}

/* ===== EXPANDERS ===== */
[data-testid="stExpander"] details {{
    background: var(--bg-secondary);
    border: 1px solid var(--border-color) !important;
    border-radius: var(--radius-md) !important;
}}

[data-testid="stExpander"] summary:hover p {{
    color: var(--primary-color) !important;
}}

/* ===== TABS (scroll horizontally instead of squashing) ===== */
.stTabs [data-baseweb="tab-list"] {{
    gap: 6px;
    overflow-x: auto;
    overflow-y: hidden;
    flex-wrap: nowrap;
    scrollbar-width: thin;
    -webkit-overflow-scrolling: touch;
    padding-bottom: 4px;
}}

.stTabs [data-baseweb="tab"] {{
    flex: 0 0 auto;
    white-space: nowrap;
    background: var(--bg-secondary) !important;
    border: 1px solid var(--border-color) !important;
    border-radius: 10px !important;
    padding: 0.4rem 0.9rem !important;
    height: auto !important;
}}

.stTabs [aria-selected="true"] {{
    background: var(--gradient-primary) !important;
}}

.stTabs [aria-selected="true"] p {{
    color: #FFFFFF !important;
}}

.stTabs [data-baseweb="tab-highlight"],
.stTabs [data-baseweb="tab-border"] {{
    display: none;
}}

/* ===== DIALOG ===== */
[data-testid="stDialog"] > div > div, div[role="dialog"] {{
    background: var(--bg-secondary) !important;
    color: var(--text-primary) !important;
    border-radius: var(--radius-lg) !important;
    max-width: min(640px, 94vw) !important;
}}

/* ===== SIDEBAR ===== */
section[data-testid="stSidebar"] {{
    background: var(--bg-sidebar) !important;
    border-right: 1px solid var(--border-color);
}}

section[data-testid="stSidebar"] * {{
    color: var(--text-primary);
}}

section[data-testid="stSidebar"] h3 {{
    color: var(--primary-color) !important;
    font-size: 1rem !important;
    border-bottom: 2px solid var(--border-color);
    padding-bottom: 8px;
}}

section[data-testid="stSidebar"] [data-testid="stSidebarNavLink"] {{
    border-radius: 8px;
}}

section[data-testid="stSidebar"] [data-testid="stSidebarNavLink"][aria-current="page"] {{
    background: {colors['primary']}22 !important;
}}

section[data-testid="stSidebar"] [data-testid="stSidebarNavLink"][aria-current="page"] span {{
    color: var(--primary-color) !important;
    font-weight: 600;
}}

.sidebar-credit {{
    margin-top: 1rem;
    padding: 0.75rem 1rem;
    border-radius: var(--radius-md);
    background: var(--gradient-primary);
    text-align: center;
    font-weight: 600;
}}

.sidebar-credit, .sidebar-credit * {{
    color: #FFFFFF !important;
}}

/* ===== TAGLINE + FOOTER ===== */
.company-tagline {{
    text-align: center;
    padding: 0.25rem 0 1rem 0;
}}

.company-tagline .tagline-text {{
    color: var(--text-primary);
    font-size: clamp(1rem, 1.5vw + 0.6rem, 1.6rem);
    font-weight: 700;
    margin: 0;
    line-height: 1.3;
}}

.company-tagline .tagline-subtitle {{
    color: var(--text-secondary);
    font-size: clamp(0.85rem, 0.5vw + 0.75rem, 1.05rem);
    margin: 4px 0 0 0;
}}

.app-footer {{
    margin-top: 3rem;
    padding: 1.25rem 0 0.5rem 0;
    border-top: 1px solid var(--border-color);
    text-align: center;
    font-size: 0.875rem;
    color: var(--text-secondary);
}}

.app-footer b {{
    color: var(--text-primary);
}}

/* ===== RESPONSIVE LAYOUT ===== */

/* Tablets / small laptops: let column rows wrap instead of squeezing */
@media (max-width: 1024px) {{
    [data-testid="stHorizontalBlock"] {{
        flex-wrap: wrap !important;
        row-gap: 1rem;
    }}
    [data-testid="stHorizontalBlock"] > [data-testid="stColumn"],
    [data-testid="stHorizontalBlock"] > [data-testid="column"] {{
        flex: 1 1 calc(50% - 1rem) !important;
        min-width: min(240px, 100%) !important;
    }}
    /* Spacer columns (used only for centering) just waste space on small screens */
    [data-testid="stHorizontalBlock"] > [data-testid="stColumn"]:not(:has([data-testid="stElementContainer"])),
    [data-testid="stHorizontalBlock"] > [data-testid="column"]:not(:has([data-testid="element-container"])) {{
        display: none !important;
    }}
}}

/* Phones: single column, full-width controls */
@media (max-width: 640px) {{
    [data-testid="stHorizontalBlock"] > [data-testid="stColumn"],
    [data-testid="stHorizontalBlock"] > [data-testid="column"] {{
        flex: 1 1 100% !important;
        width: 100% !important;
        min-width: 100% !important;
    }}
    div[data-testid="stButton"] > button,
    div[data-testid="stDownloadButton"] > button {{
        width: 100% !important;
    }}
    h2:after {{
        width: 56px;
        height: 3px;
    }}
    .info-card {{
        border-left-width: 3px;
    }}
}}

/* ===== MOTION ===== */
@keyframes fadeInUp {{
    from {{ opacity: 0; transform: translateY(20px); }}
    to {{ opacity: 1; transform: translateY(0); }}
}}

@media (prefers-reduced-motion: reduce) {{
    *, *::before, *::after {{
        animation: none !important;
        transition: none !important;
    }}
}}

/* ===== SCROLLBAR ===== */
::-webkit-scrollbar {{
    width: 8px;
    height: 8px;
}}

::-webkit-scrollbar-track {{
    background: var(--bg-primary);
}}

::-webkit-scrollbar-thumb {{
    background: var(--primary-color);
    border-radius: 4px;
}}

::-webkit-scrollbar-thumb:hover {{
    background: var(--secondary-color);
}}
</style>
""", unsafe_allow_html=True)

# Company tagline shown above every page
st.markdown("""
<div class="company-tagline">
    <p class="tagline-text">Driven By Integrity, Powered by Progress</p>
    <p class="tagline-subtitle">Professional Forex Analysis &amp; Prediction Solutions</p>
</div>
""", unsafe_allow_html=True)


# Dark Mode Toggle in Sidebar
with st.sidebar:
    st.markdown("### ⚙️ Settings")

    def toggle_dark_mode():
        st.session_state.dark_mode = st.session_state.dark_mode_toggle

    st.toggle(
        "🌙 Dark Mode",
        value=st.session_state.dark_mode,
        key="dark_mode_toggle",
        on_change=toggle_dark_mode
    )

# Main about page
Main_page = st.Page(
    page="views/About.py",
    title="About",
    icon="😉",
    default=True
)

# Backtesting Strategy page
Backtest_page = st.Page(
    page="views/Backtest.py",
    title="Backtesting",
    icon="📊"
)

# Future Price prediction
Predication_page = st.Page(
    page="views/Prediction.py",
    title="Prediction",
    icon="📈"
)

# Navigation
pg = st.navigation({
    "Info": [Main_page],
    "Model": [Backtest_page, Predication_page]
})

# Logo and branding
st.logo("Asset/Sidebar.png")
st.sidebar.markdown(
    f"<div class='sidebar-credit'>📈 Analysis with {AUTHOR}!</div>",
    unsafe_allow_html=True
)

try:
    pg.run()
except Exception as e:
    st.error(f"An error occurred: {str(e)}")
    st.info("Please refresh the page or check the console for more details.")

st.markdown(
    f"""
    <div class="app-footer">
        Built by <b>{AUTHOR}</b> · Forex Price Predictor<br>
        <span>For educational purposes only. Not financial advice.</span>
    </div>
    """,
    unsafe_allow_html=True
)
