import streamlit as st
from datetime import datetime, date
from fpdf import FPDF

# ─────────────────────────────────────────
#  VERSION INFO
# ─────────────────────────────────────────
APP_VERSION  = "3.0.0"
RELEASE_DATE = "2026-04-26"
RELEASE_NOTES = """
**What's new in v3.0:**
- ✅ Beautiful deep-space purple theme
- ✅ Rich styled number cards with meanings
- ✅ Admin (star2025) & User (Mon2025) passwords
- ✅ Settings panel — toggle calculation methods
- ✅ Special Date analysis (Quit Date etc.)
- ✅ PDF export with full profile
- ✅ Version tracker & release notes
- ✅ Mobile friendly layout
"""

# ─────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────
st.set_page_config(
    page_title="Stargazer Numerology",
    page_icon="🔮",
    layout="centered"
)

# ─────────────────────────────────────────
#  GLOBAL STYLES
# ─────────────────────────────────────────
st.markdown("""
<style>
  .stApp { background: linear-gradient(160deg, #0d0d2b 0%, #1a0533 50%, #0d1a2b 100%); }
  section[data-testid="stSidebar"] { background: #110d2a !important; border-right: 1px solid #2e1f5e; }
  header[data-testid="stHeader"] { background: transparent; }
  input, .stDateInput input { background: #1c1040 !important; color: #e8d5ff !important; border: 1px solid #4a2f8a !important; border-radius: 8px !important; }
  label { color: #c4a8f5 !important; font-size: 14px !important; }
  .stButton > button {
    background: linear-gradient(135deg, #6b21e8, #9333ea) !important;
    color: white !important; border: none !important;
    border-radius: 10px !important; font-size: 16px !important;
    font-weight: 600 !important; padding: 0.6rem 1.5rem !important;
    box-shadow: 0 4px 20px rgba(147,51,234,0.4) !important;
  }
  .stDownloadButton > button {
    background: linear-gradient(135deg, #0f4c8a, #1a6fc4) !important;
    color: white !important; border: none !important;
    border-radius: 10px !important; font-weight: 600 !important;
  }
  [data-testid="stMetric"] { background: linear-gradient(135deg, #1c1040, #2a1060) !important; border: 1px solid #4a2f8a !important; border-radius: 12px !important; padding: 1rem !important; }
  [data-testid="stMetricValue"] { color: #e0b0ff !important; font-size: 2.5rem !important; font-weight: 700 !important; }
  [data-testid="stMetricLabel"] { color: #a78bca !important; font-size: 13px !important; text-transform: uppercase !important; letter-spacing: 0.05em !important; }
  .stSuccess { background: #0d2b1a !important; border: 1px solid #1a5c35 !important; color: #4ade80 !important; border-radius: 10px !important; }
  .stWarning { background: #2b1a0d !important; border: 1px solid #5c3a1a !important; color: #fbbf24 !important; border-radius: 10px !important; }
  .stError   { background: #2b0d0d !important; border: 1px solid #5c1a1a !important; color: #f87171 !important; border-radius: 10px !important; }
  .stSidebar h2, .stSidebar h3, .stSidebar p, .stSidebar label { color: #c4a8f5 !important; }
  .stCheckbox label { color: #c4a8f5 !important; }
  .num-card {
    background: linear-gradient(135deg, #1c1040 0%, #2d1060 100%);
    border: 1px solid #5b3fa0; border-radius: 16px;
    padding: 1.2rem 1.4rem; margin-bottom: 1rem;
    box-shadow: 0 4px 20px rgba(91,63,160,0.3);
  }
  .num-card .num-big { font-size: 3rem; font-weight: 800; color: #e0b0ff; line-height: 1; }
  .num-card .num-label { font-size: 12px; text-transform: uppercase; letter-spacing: 0.08em; color: #9b7cc8; margin-bottom: 6px; }
  .num-card .num-title { font-size: 16px; font-weight: 700; color: #d4aaff; margin: 6px 0 4px; }
  .num-card .num-meaning { font-size: 13px; color: #b89de0; line-height: 1.6; }
  .num-card.master { border-color: #f59e0b; box-shadow: 0 4px 25px rgba(245,158,11,0.3); }
  .num-card.master .num-big { color: #fcd34d; }
  .hero {
    text-align: center; padding: 2rem 1rem 1.5rem;
    background: linear-gradient(135deg, #1a0533 0%, #0d1a2b 100%);
    border-radius: 20px; border: 1px solid #2e1f5e; margin-bottom: 2rem;
  }
  .hero h1 { font-size: 2.2rem; font-weight: 800; color: #e0b0ff; margin: 0; text-shadow: 0 0 30px rgba(224,176,255,0.5); }
  .hero p  { color: #9b7cc8; font-size: 14px; margin: 8px 0 0; }
  .section-hdr { font-size: 11px; font-weight: 600; letter-spacing: 0.1em; text-transform: uppercase; color: #7c5cbf; margin: 1.5rem 0 0.75rem; padding-bottom: 6px; border-bottom: 1px solid #2e1f5e; }
  .login-box { max-width: 380px; margin: 4rem auto; text-align: center; }
  .login-box h1 { color: #e0b0ff; font-size: 2rem; margin-bottom: 0.5rem; }
  .login-box p  { color: #9b7cc8; font-size: 14px; margin-bottom: 2rem; }
  .stars { font-size: 22px; letter-spacing: 8px; color: #e0b0ff; opacity: 0.6; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────
#  PASSWORDS
# ─────────────────────────────────────────
ADMIN_PASSWORD = "star2025"
USER_PASSWORD  = "moon2025"

# ─────────────────────────────────────────
#  PASSWORD GATE
# ─────────────────────────────────────────
def check_password():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
        st.session_state.role = None

    if not st.session_state.authenticated:
        st.markdown("""
        <div class="login-box">
          <div class="stars">✦ ✦ ✦</div>
          <h1>🔮 Stargazer</h1>
          <p>Numerology System — Enter your access password</p>
        </div>
        """, unsafe_allow_html=True)

        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            pwd = st.text_input("Password", type="password", label_visibility="collapsed", placeholder="Enter password...")
            if st.button("✨ Enter the Portal", use_container_width=True):
                if pwd == ADMIN_PASSWORD:
                    st.session_state.authenticated = True
                    st.session_state.role = "admin"
                    st.rerun()
                elif pwd == USER_PASSWORD:
                    st.session_state.authenticated = True
                    st.session_state.role = "user"
                    st.rerun()
                else:
                    st.error("✗ Incorrect password. Please try again.")
        return False
    return True

if not check_password():
    st.stop()

# ─────────────────────────────────────────
#  HELPERS
# ─────────────────────────────────────────
def reduce_number(n):
    while n > 9 and n not in (11, 22, 33):
        n = sum(int(d) for d in str(n))
    return n

def pythagorean_value(name):
    chart = {
        **dict.fromkeys("AJS", 1), **dict.fromkeys("BKT", 2),
        **dict.fromkeys("CLU", 3), **dict.fromkeys("DMV", 4),
        **dict.fromkeys("ENW", 5), **dict.fromkeys("FOX", 6),
        **dict.fromkeys("GPY", 7), **dict.fromkeys("HQZ", 8),
        **dict.fromkeys("IR",  9),
    }
    return sum(chart.get(c.upper(), 0) for c in name if c.isalpha())

def chaldean_value(name):
    chart = {
        **dict.fromkeys("AIJQY", 1), **dict.fromkeys("BKR",  2),
        **dict.fromkeys("CGLS",  3), **dict.fromkeys("DMT",  4),
        **dict.fromkeys("EHNX",  5), **dict.fromkeys("UVW",  6),
        **dict.fromkeys("OZ",    7), **dict.fromkeys("FP",   8),
    }
    return sum(chart.get(c.upper(), 0) for c in name if c.isalpha())

def ordinal_value(name):
    return sum((ord(c.upper()) - 64) for c in name if c.isalpha())

def life_path(dob_str):
    return reduce_number(sum(int(d) for d in dob_str.replace("-", "")))

def date_number(d):
    return reduce_number(sum(int(x) for x in d.strftime("%Y%m%d")))

# ─────────────────────────────────────────
#  NUMBER MEANINGS
# ─────────────────────────────────────────
MEANINGS = {
    1:  ("The Pioneer",      "Independence, leadership, new beginnings, originality, courage."),
    2:  ("The Diplomat",     "Cooperation, harmony, intuition, sensitivity, partnership."),
    3:  ("The Creator",      "Creativity, joy, self-expression, communication, optimism."),
    4:  ("The Builder",      "Stability, hard work, practicality, loyalty, foundation."),
    5:  ("The Adventurer",   "Freedom, change, adventure, versatility, liberation."),
    6:  ("The Nurturer",     "Love, family, responsibility, healing, service to others."),
    7:  ("The Seeker",       "Wisdom, introspection, spirituality, analysis, truth."),
    8:  ("The Achiever",     "Abundance, power, ambition, material success, authority."),
    9:  ("The Humanitarian", "Compassion, completion, universal love, wisdom, endings."),
    11: ("Master Intuitive", "Spiritual illumination, inspiration, psychic sensitivity."),
    22: ("Master Builder",   "Large-scale achievement, visionary dreams made real."),
    33: ("Master Teacher",   "Unconditional love, upliftment of humanity, divine guidance."),
}

def render_number_card(label, number):
    title, meaning = MEANINGS.get(number, ("", ""))
    is_master = number in (11, 22, 33)
    cls = "num-card master" if is_master else "num-card"
    badge = " 🌟 Master Number" if is_master else ""
    st.markdown(f"""
    <div class="{cls}">
      <div class="num-label">{label}{badge}</div>
      <div class="num-big">{number}</div>
      <div class="num-title">{title}</div>
      <div class="num-meaning">{meaning}</div>
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────
#  PDF EXPORT
# ─────────────────────────────────────────
def generate_pdf(name, dob_str, results, special_date=None, special_label=None):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 22)
    pdf.set_text_color(200, 160, 255)
    pdf.cell(0, 14, "Stargazer Numerology System", ln=True, align="C")
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(155, 124, 200)
    pdf.cell(0, 7, f"Generated: {datetime.now().strftime('%B %d, %Y')}  |  v{APP_VERSION}", ln=True, align="C")
    pdf.ln(4)
    pdf.set_draw_color(91, 63, 160)
    pdf.set_line_width(0.6)
    pdf.line(15, pdf.get_y(), 195, pdf.get_y())
    pdf.ln(5)
    pdf.set_font("Helvetica", "B", 13)
    pdf.set_text_color(220, 190, 255)
    pdf.cell(0, 9, f"Profile: {name}", ln=True)
    pdf.set_font("Helvetica", "", 11)
    pdf.set_text_color(180, 157, 224)
    pdf.cell(0, 7, f"Date of Birth: {dob_str}", ln=True)
    pdf.ln(5)
    for label, number in results.items():
        title, meaning = MEANINGS.get(number, ("", ""))
        pdf.set_font("Helvetica", "B", 12)
        pdf.set_text_color(224, 176, 255)
        pdf.cell(0, 8, f"{label}: {number}  -  {title}", ln=True)
        pdf.set_font("Helvetica", "", 10)
        pdf.set_text_color(184, 157, 224)
        pdf.multi_cell(0, 6, meaning)
        pdf.ln(2)
    if special_date and special_label:
        pdf.ln(3)
        pdf.line(15, pdf.get_y(), 195, pdf.get_y())
        pdf.ln(4)
        snum = date_number(special_date)
        stitle, smeaning = MEANINGS.get(snum, ("", ""))
        pdf.set_font("Helvetica", "B", 12)
        pdf.set_text_color(224, 176, 255)
        pdf.cell(0, 8, f"{special_label} ({special_date.strftime('%B %d, %Y')}): {snum}  -  {stitle}", ln=True)
        pdf.set_font("Helvetica", "", 10)
        pdf.set_text_color(184, 157, 224)
        pdf.multi_cell(0, 6, smeaning)
    pdf.ln(8)
    pdf.set_font("Helvetica", "I", 9)
    pdf.set_text_color(120, 90, 170)
    pdf.cell(0, 6, f"Stargazer Numerology System v{APP_VERSION}  |  {RELEASE_DATE}", ln=True, align="C")
    return bytes(pdf.output())

# ─────────────────────────────────────────
#  SIDEBAR
# ─────────────────────────────────────────
with st.sidebar:
    st.markdown("## ⚙️ Settings")
    st.markdown("---")
    st.markdown("**Calculation Methods**")
    show_pyth  = st.checkbox("Pythagorean", value=True)
    show_chald = st.checkbox("Chaldean",    value=True)
    show_ordn  = st.checkbox("Ordinal",     value=False)
    st.markdown("---")
    st.markdown("**Special Date Analysis**")
    enable_special = st.checkbox("Add a special date", value=False)
    special_label  = ""
    special_date   = None
    if enable_special:
        special_label = st.text_input("Label (e.g. Quit Date)", value="Quit Date")
        special_date  = st.date_input("Date", value=date(2026, 6, 5), key="special")
    st.markdown("---")
    st.markdown(f"**📦 Version {APP_VERSION}**")
    st.caption(f"Released: {RELEASE_DATE}")
    with st.expander("Release Notes"):
        st.markdown(RELEASE_NOTES)
    st.markdown("---")
    if st.button("🚪 Log Out", use_container_width=True):
        st.session_state.authenticated = False
        st.session_state.role = None
        st.rerun()

# ─────────────────────────────────────────
#  MAIN APP
# ─────────────────────────────────────────
st.markdown("""
<div class="hero">
  <div class="stars">✦ ✦ ✦ ✦ ✦</div>
  <h1>🔮 Stargazer Numerology</h1>
  <p>Discover the sacred numbers woven into your life</p>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    name = st.text_input("Full Name", placeholder="e.g. Jane Marie Smith")
with col2:
    dob = st.date_input("Date of Birth", value=date(1970, 1, 1))

st.markdown("<br>", unsafe_allow_html=True)

if st.button("✨ Reveal My Numbers", use_container_width=True):
    if name and dob:
        dob_str = dob.strftime("%Y-%m-%d")
        life  = life_path(dob_str)
        pyth  = reduce_number(pythagorean_value(name))
        chald = reduce_number(chaldean_value(name))
        ordn  = reduce_number(ordinal_value(name))
        results = {"Life Path": life}

        st.markdown('<div class="section-hdr">Life Path</div>', unsafe_allow_html=True)
        render_number_card("Life Path Number", life)

        active = [(show_pyth, "Pythagorean", pyth),
                  (show_chald, "Chaldean", chald),
                  (show_ordn, "Ordinal", ordn)]
        active = [x for x in active if x[0]]
        if active:
            st.markdown('<div class="section-hdr">Name Numbers</div>', unsafe_allow_html=True)
            cols = st.columns(len(active))
            for i, (_, lbl, val) in enumerate(active):
                with cols[i]:
                    render_number_card(lbl, val)
                results[lbl] = val

        if enable_special and special_date and special_label:
            st.markdown(f'<div class="section-hdr">{special_label} Analysis</div>', unsafe_allow_html=True)
            snum = date_number(special_date)
            render_number_card(f"{special_label} — {special_date.strftime('%B %d, %Y')}", snum)

        st.success(f"✨ Numerology profile for **{name}** generated successfully!")
        st.markdown("---")
        st.markdown('<div class="section-hdr">Save Your Report</div>', unsafe_allow_html=True)
        try:
            pdf_bytes = generate_pdf(
                name, dob_str, results,
                special_date if enable_special else None,
                special_label if enable_special else None
            )
            st.download_button(
                label="📄 Download PDF Report",
                data=pdf_bytes,
                file_name=f"stargazer_{name.replace(' ', '_')}.pdf",
                mime="application/pdf",
                use_container_width=True
            )
        except Exception:
            st.info("PDF export requires fpdf2. Run: `pip install fpdf2`")
    else:
        st.warning("Please enter both a full name and date of birth.")
