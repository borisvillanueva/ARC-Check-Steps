import streamlit as st

st.set_page_config(page_title="CX Asset Onboarding Checklist", layout="centered")

st.title("✅ CX Utilities - Asset Onboarding Checklist (2025 ARC Steps)")

steps = [
    "Go to the product CX utilities folder in Desktop",
    "Be sure you are on MAIN BRANCH with `git branch`",
    "If not, run `git checkout main`",
    "Confirm again with `git branch` that you are now on main",
    "Run `git pull origin main` to ensure new bug fixes are applied before everything else",
    "Run `./scripts/arc_setup.sh` to start the process — this initializes everything before continuing",
    "Verify a new branch was created with the current date using `git branch`",
    "Proceed with `pyx packages/arc/core/add_new_assets.py`",
    "Select `cx-production-24188796600` and click OK",
    "Skip the following exchanges from the list: **phemex**, **upbit**, **kucoin**, **bitget**, and **gateio**",
    "After review, run `pyx packages/arc_admin_app/src/launch.py`",
    "In your browser, go to `http://0.0.0.0:10450/review-asset` and click on the red **Review * Assets** button",
    "If there are **0 (zero)** assets to review, run `./arc_commit_editable_files.sh`",
    "After reviewing assets, click on the **Errors Page** and then **Find Error** button",
    "Correct error names or run the script in a different window as needed",
    "Run `./scripts/arc_commit_editable_files.sh` again",
    "Run `pyx packages/arc/src/post_processing/clean_arc_pairs.py`",
    "Select **Clean ALL** when prompted",
    "Run `./scripts/arc_commit_generated_files.sh`",
    "Create the Pull Request 🎉"
]

# Initialize session state
if "progress" not in st.session_state:
    st.session_state.progress = [False] * len(steps)

st.markdown("#### Click each box to unlock the next step:")

# Display the steps with progressive checkboxes
for i, step in enumerate(steps):
    if i == 0 or st.session_state.progress[i - 1]:
        st.session_state.progress[i] = st.checkbox(step, key=i, value=st.session_state.progress[i])
    else:
        st.checkbox(step, key=i, value=False, disabled=True)

# Completion message
if all(st.session_state.progress):
    st.success("🎉 All 2025 ARC Steps completed! Great job, Boris!")
