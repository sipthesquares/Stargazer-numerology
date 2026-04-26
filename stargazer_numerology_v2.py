import streamlit as st
from datetime import datetime, date
from fpdf import FPDF
import io
import os

# ─────────────────────────────────────────
#  VERSION INFO  (update this each release)
# ─────────────────────────────────────────
APP_VERSION = "2.0.0"
RELEASE_DATE = "2026-04-26"
RELEASE_NOTES = """
**What's new in v2.0:**
- ✅ Settings panel with theme & method selection
- ✅ Meanings for every number (1–9, 11, 22, 33)
- ✅ Quit Date / Special Date analysis
- ✅ Save results as PDF
- ✅ Version tracker with release notes
- ✅ Password protected access
"""

# ─────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────
st.set_page_config(page_title="Stargazer Numerology System", layout="centered", page_icon="🔮")

# ─────────────────────────────────────────
#  PASSWORD PROTECTION
# ─────────────────────────────────────────
ACCESS_PASSWORD = "star2025"    # ← your admin password
USER_PASSWORD   = "Mon2025"     # ← her password

def check_password():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if not st.session_state.authenticated:
        st.title("🔮 Stargazer Numerology System")
        st.markdown("---")
        pwd = st.text_input("Enter access password", type="password")
        if st.button("Enter"):
            if pwd == ACCESS_PASSWORD:
                st.session_state.authenticated = True
                st.session_state.role = "admin"
                st.rerun()
            elif pwd == USER_PASSWORD:
                st.session_state.authenticated = True
                st.session_state.role = "user"
                st.rerun()
            else:
                st.error("Incorrect password. Please try again.")
        return False
    return True

if not check_password():
    st.stop()

# ─────────────────────────────────────────
#  HELPER FUNCTIONS
# ─────────────────────────────────────────
def reduce_number(n):
    while n > 9 and n not in (11, 22, 33):
        n = sum(int(d) for d in str(n))
    return n

def pythagorean_value(name):
    chart = {
        **dict.fromkeys(list("AJS"), 1),
        **dict.fromkeys(list("BKT"), 2),
        **dict.fromkeys(list("CLU"), 3),
        **dict.fromkeys(list("DMV"), 4),
        **dict.fromkeys(list("ENW"), 5),
        **dict.fromkeys(list("FOX"), 6),
        **dict.fromkeys(list("GPY"), 7),
        **dict.fromkeys(list("HQZ"), 8),
        **dict.fromkeys(list("IR"),  9),
    }
    return sum(chart.get(c.upper(), 0) for c in name if c.isalpha())

def chaldean_value(name):
    chart = {
        **dict.fromkeys(list("AIJQY"), 1),
        **dict.fromkeys(list("BKR"),   2),
        **dict.fromkeys(list("CGLS"),  3),
        **dict.fromkeys(list("DMT"),   4),
        **dict.fromkeys(list("EHNX"),  5),
        **dict.fromkeys(list("UVW"),   6),
        **dict.fromkeys(list("OZ"),    7),
        **dict.fromkeys(list("FP"),    8),
    }
    return sum(chart.get(c.upper(), 0) for c in name if c.isalpha())

def ordinal_value(name):
    return sum((ord(c.upper()) - 64) for c in name if c.isalpha())

def life_path(dob_str):
    digits = [int(d) for d in dob_str.replace("-", "")]
    return reduce_number(sum(digits))

def date_number(d):
    digits = [int(x) for x in d.strftime("%Y-%m-%d").replace("-", "")]
    return reduce_number(sum(digits))

# ─────────────────────────────────────────
#  NUMBER MEANINGS
# ─────────────────────────────────────────
NUMBER_MEANINGS = {
    1:  ("The Pioneer",    "Independence, leadership, new beginnings, originality, courage."),
    2:  ("The Diplomat",   "Cooperation, harmony, intuition, sensitivity, partnership."),
    3:  ("The Creator",    "Creativity, joy, self-expression, communication, optimism."),
    4:  ("The Builder",    "Stability, hard work, practicality, loyalty, foundation."),
    5:  ("The Adventurer", "Freedom, change, adventure, versatility, liberation."),
    6:  ("The Nurturer",   "Love, family, responsibility, healing, service to others."),
    7:  ("The Seeker",     "Wisdom, introspection, spirituality, analysis, truth."),
    8:  ("The Achiever",   "Abundance, power, ambition, material success, authority."),
    9:  ("The Humanitarian","Compassion, completion, universal love, wisdom, endings."),
    11: ("Master Intuitive","Spiritual illumination, inspiration, psychic sensitivity. Master Number."),
    22: ("Master Builder",  "Large-scale achievement, visionary dreams made real. Master Number."),
    33: ("Master Teacher",  "Unconditional love, upliftment of humanity, divine guidance. Master Number."),
}

def number_card(label, number):
    title, meaning = NUMBER_MEANINGS.get(number, ("", ""))
    st.metric(label=label, value=number)
    if title:
        st.caption(f"**{title}** — {meaning}")

# ─────────────────────────────────────────
#  PDF EXPORT
# ─────────────────────────────────────────
def generate_pdf(name, dob_str, results: dict, special_date=None, special_label=None):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 20)
    pdf.cell(0, 12, "Stargazer Numerology System", ln=True, align="C")
    pdf.set_font("Helvetica", "", 11)
    pdf.cell(0, 8, f"Generated: {datetime.now().strftime('%B %d, %Y')}", ln=True, align="C")
    pdf.ln(6)

    pdf.set_font("Helvetica", "B", 13)
    pdf.cell(0, 9, f"Profile for: {name}", ln=True)
    pdf.set_font("Helvetica", "", 11)
    pdf.cell(0, 7, f"Date of Birth: {dob_str}", ln=True)
    pdf.ln(4)

    pdf.set_draw_color(180, 150, 220)
    pdf.set_line_width(0.5)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(4)

    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, "Numerology Results", ln=True)
    pdf.set_font("Helvetica", "", 11)
    for label, number in results.items():
        title, meaning = NUMBER_MEANINGS.get(number, ("", ""))
        pdf.set_font("Helvetica", "B", 11)
        pdf.cell(0, 7, f"{label}: {number} — {title}", ln=True)
        pdf.set_font("Helvetica", "", 10)
        pdf.multi_cell(0, 6, meaning)
        pdf.ln(2)

    if special_date and special_label:
        pdf.ln(2)
        pdf.set_font("Helvetica", "B", 12)
        pdf.cell(0, 8, f"Special Date: {special_label}", ln=True)
        pdf.set_font("Helvetica", "", 11)
        num = date_number(special_date)
        title, meaning = NUMBER_MEANINGS.get(num, ("", ""))
        pdf.cell(0, 7, f"Date Number: {num} — {title}", ln=True)
        pdf.set_font("Helvetica", "", 10)
        pdf.multi_cell(0, 6, meaning)

    pdf.ln(6)
    pdf.set_font("Helvetica", "I", 9)
    pdf.cell(0, 6, f"Stargazer Numerology System v{APP_VERSION} | {RELEASE_DATE}", ln=True, align="C")

    return bytes(pdf.output())

# ─────────────────────────────────────────
#  SIDEBAR — SETTINGS & VERSION
# ─────────────────────────────────────────
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/8/8e/Milky_Way_Night_Sky_Black_Rock_Desert_Nevada.jpg/320px-Milky_Way_Night_Sky_Black_Rock_Desert_Nevada.jpg",
             use_container_width=True)
    st.markdown("## ⚙️ Settings")

    st.markdown("### Calculation Methods")
    show_pyth  = st.checkbox("Pythagorean", value=True)
    show_chald = st.checkbox("Chaldean",    value=True)
    show_ordn  = st.checkbox("Ordinal",     value=False)

    st.markdown("### Special Date Analysis")
    enable_special = st.checkbox("Add a special date", value=False)
    special_label  = ""
    special_date   = None
    if enable_special:
        special_label = st.text_input("Label (e.g. Quit Date, Wedding)", value="Quit Date")
        special_date  = st.date_input("Date", value=date(2026, 6, 5), key="special")

    st.markdown("---")
    st.markdown("### 🔒 Access Password")
    new_pwd = st.text_input("Change password", type="password", placeholder="Leave blank to keep current")
    if st.button("Update Password"):
        if new_pwd:
            ACCESS_PASSWORD = new_pwd
            st.success("Password updated! Share the new one with your user.")
        else:
            st.warning("Enter a new password first.")

    st.markdown("---")
    st.markdown(f"### 📦 Version {APP_VERSION}")
    st.caption(f"Released: {RELEASE_DATE}")
    with st.expander("Release Notes"):
        st.markdown(RELEASE_NOTES)

    if st.button("🚪 Log Out"):
        st.session_state.authenticated = False
        st.rerun()

# ─────────────────────────────────────────
#  MAIN APP
# ─────────────────────────────────────────
st.title("🔮 Stargazer Numerology System")
st.caption(f"v{APP_VERSION}")
st.markdown("---")

name = st.text_input("Enter Full Name", placeholder="e.g. Jane Marie Smith")
dob  = st.date_input("Enter Date of Birth", value=date(1970, 1, 1))

if st.button("✨ Calculate", use_container_width=True):
    if name and dob:
        dob_str = dob.strftime("%Y-%m-%d")
        life    = life_path(dob_str)
        pyth    = reduce_number(pythagorean_value(name))
        chald   = reduce_number(chaldean_value(name))
        ordn    = reduce_number(ordinal_value(name))

        st.markdown("---")
        st.subheader("✨ Your Numerology Profile")

        # Life Path always shown
        st.markdown("#### Life Path Number")
        number_card("Life Path", life)

        # Name numbers based on settings
        if show_pyth or show_chald or show_ordn:
            st.markdown("#### Name Numbers")
            cols = st.columns(sum([show_pyth, show_chald, show_ordn]))
            i = 0
            results = {"Life Path": life}
            if show_pyth:
                with cols[i]: number_card("Pythagorean", pyth)
                results["Pythagorean"] = pyth
                i += 1
            if show_chald:
                with cols[i]: number_card("Chaldean", chald)
                results["Chaldean"] = chald
                i += 1
            if show_ordn:
                with cols[i]: number_card("Ordinal", ordn)
                results["Ordinal"] = ordn
                i += 1

        # Special date
        if enable_special and special_date and special_label:
            st.markdown(f"#### {special_label} Analysis")
            snum = date_number(special_date)
            number_card(f"{special_label} ({special_date.strftime('%B %d, %Y')})", snum)

        st.success("Numerology profile generated successfully!")
        st.markdown("---")

        # PDF Download
        st.markdown("#### 📄 Save as PDF")
        try:
            pdf_bytes = generate_pdf(
                name, dob_str, results,
                special_date if enable_special else None,
                special_label if enable_special else None
            )
            st.download_button(
                label="Download PDF Report",
                data=pdf_bytes,
                file_name=f"stargazer_{name.replace(' ','_')}.pdf",
                mime="application/pdf",
                use_container_width=True
            )
        except Exception as e:
            st.info("Install fpdf2 to enable PDF export: `pip install fpdf2`")

    else:
        st.warning("Please enter both a name and date of birth.")
