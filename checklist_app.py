import streamlit as st
import re

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="CX Asset Onboarding Checklist",
    page_icon="✅",
    layout="centered"
)

# ---------------------------------------------------
# CUSTOM CSS
# ---------------------------------------------------

st.markdown("""
<style>

html, body, [class*="css"] {
    font-family: "Inter", sans-serif;
}

.main {
    background: linear-gradient(
        180deg,
        #0f172a 0%,
        #111827 45%,
        #0b1120 100%
    );
    color: white;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 4rem;
    max-width: 900px;
}

.title-box {
    background: linear-gradient(135deg, #2563eb, #7c3aed);
    padding: 2rem;
    border-radius: 22px;
    margin-bottom: 2rem;
    box-shadow: 0 10px 30px rgba(0,0,0,0.35);
}

.title-text {
    font-size: 2.2rem;
    font-weight: 800;
    color: white;
    margin-bottom: 0.5rem;
}

.subtitle-text {
    color: #dbeafe;
    font-size: 1rem;
}

.step-card {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    padding: 1rem 1rem 0.5rem 1rem;
    border-radius: 18px;
    margin-bottom: 1rem;
    transition: 0.25s ease;
    backdrop-filter: blur(8px);
}

.step-card:hover {
    border: 1px solid rgba(96,165,250,0.5);
    transform: translateY(-2px);
}

.progress-wrapper {
    margin-top: 1rem;
    margin-bottom: 2rem;
}

.command-title {
    color: #93c5fd;
    font-size: 0.85rem;
    margin-top: 0.7rem;
    margin-bottom: 0.2rem;
    font-weight: 600;
}

.stCodeBlock {
    border-radius: 12px;
}

.success-box {
    background: linear-gradient(135deg, #059669, #10b981);
    padding: 1.5rem;
    border-radius: 18px;
    text-align: center;
    color: white;
    font-size: 1.2rem;
    font-weight: 700;
    margin-top: 2rem;
    box-shadow: 0 10px 25px rgba(16,185,129,0.25);
}

</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# HEADER
# ---------------------------------------------------

st.markdown("""
<div class="title-box">
    <div class="title-text">
        ✅ CX Utilities Asset Onboarding
    </div>
    <div class="subtitle-text">
        2025 ARC Process Checklist • Progressive Workflow • Streamlit UI
    </div>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# STEPS
# ---------------------------------------------------

steps = [
    "Go to the product CX utilities folder in Your Local ARC Directory",
    "Be sure you are on MAIN BRANCH with `git branch`",
    "If not, run `git checkout main`",
    "Confirm again with `git branch` that you are now on main",
    "Run `git pull origin main` to ensure new bug fixes are applied before everything else",
    "Run `./scripts/arc_setup.sh` to start the process — this initializes everything before continuing",
    "Enter in SSO session name to get AWS Permissions",
    "Enter in Default client Region [us-east-1]",
    "Enter to Default to JSON Format",
    "Verify a new branch was created with the current date using `git branch`",
    "Proceed with `pyx packages/arc/core/add_new_assets.py`",
    "Select `cx-production-24188796600` and click OK",
    'Select "All Non-restricted Exchanges" box from the Exchange selection screen',
    "After review, run `pyx packages/arc_admin_app/src/launch.py`",
    "In your browser, go to `http://0.0.0.0:10450/review-asset` and click on the red **Review Assets** button",
    "If there are **0 (zero)** assets to review, run `./scripts/arc_commit_editable_files.sh`",
    "After reviewing assets, click on the **Errors Page** and then **Find Error** button",
    "Correct error names or run the script in a different window as needed",
    "Be sure to re-enable the environment in new window with `source .venv/bin/activate`",
    "Run `./scripts/arc_commit_editable_files.sh` again",
    "Run `pyx packages/arc/src/post_processing/clean_arc_pairs.py`",
    "Select **Clean ALL** when prompted",
    "Run `./scripts/arc_commit_generated_files.sh`",
    "Create the Pull Request 🎉"
]

# ---------------------------------------------------
# HELPERS
# ---------------------------------------------------

def extract_command(step):
    return re.findall(r'`([^`]+)`', step)

# ---------------------------------------------------
# SESSION STATE
# ---------------------------------------------------

if "progress" not in st.session_state:
    st.session_state.progress = [False] * len(steps)

# ---------------------------------------------------
# PROGRESS BAR
# ---------------------------------------------------

completed_steps = sum(st.session_state.progress)
progress_percent = completed_steps / len(steps)

st.markdown('<div class="progress-wrapper">', unsafe_allow_html=True)

st.progress(progress_percent)

st.caption(
    f"Completed {completed_steps} of {len(steps)} steps "
    f"({int(progress_percent * 100)}%)"
)

st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------
# INTRO TEXT
# ---------------------------------------------------

st.markdown("""
### Workflow Instructions

Click each step in order to unlock the next one.  
Commands will appear automatically for the current active step.
""")

# ---------------------------------------------------
# CHECKLIST UI
# ---------------------------------------------------

for i, step in enumerate(steps):

    enabled = i == 0 or st.session_state.progress[i - 1]

    st.markdown('<div class="step-card">', unsafe_allow_html=True)

    st.session_state.progress[i] = st.checkbox(
        f"Step {i + 1}: {step}",
        key=i,
        value=st.session_state.progress[i],
        disabled=not enabled
    )

    # Show commands only for active incomplete step
    if enabled and not st.session_state.progress[i]:

        commands = extract_command(step)

        for cmd in commands:
            st.markdown(
                '<div class="command-title">Command</div>',
                unsafe_allow_html=True
            )

            st.code(cmd, language="bash")

    st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------
# COMPLETION
# ---------------------------------------------------

if all(st.session_state.progress):

    st.balloons()

    st.markdown("""
    <div class="success-box">
        🎉 All 2025 ARC Steps Completed Successfully
        <br><br>
        Ready to Create the Pull Request 🚀
    </div>
    """, unsafe_allow_html=True)
