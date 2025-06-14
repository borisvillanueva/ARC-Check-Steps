import streamlit as st
import re

st.set_page_config(page_title="CX Asset Onboarding Checklist", layout="centered")
st.title("✅ CX Utilities - Asset Onboarding Checklist")

steps = [
    "Be on the path `cx utilities` (`pwd`)",
    "Run `poetry shell`",
    "Run `aws configure sso`",
    "Enter `production` for the SSO session name",
    "Run `git branch` to confirm branch is `main`",
    "Run `git pull origin main` to update files",
    "Run `./arc_create_update_branch.sh`",
    "Run `pyx packages/arc/core/add_new_assets.py`",
    "Select `cx_production-241887966600` and click OK in Page Crawler",
    "Collect metadata and select exchanges to work on",
    "Allow crawling when prompted",
    "Wait for crawl summary (e.g., 0/16 added)",
    "Run `pyx packages/arc_admin_app/src/launch.py`",
    "Open browser to `http://0.0.0.0:10450/review-asset`",
    "If no assets to review, run `./arc_commit_editable_files.sh`",
    "If assets exist, click red button: `Review # Assets`",
    "Sort by good scores and begin reviewing",
    "Review price comparisons and asset cycling",
    "Once done, press `Ctrl+C` in terminal",
    "Run `./arc_commit_editable_files.sh` again",
    "Run `pyx packages/arc/src/post_processing/clean_arc_pairs.py` and select `Clean ALL`",
    "Run `./arc_commit_generated_files.sh`",
    "Click on the the PR link and create a Pull Request"
]

def extract_command(step):
    return re.findall(r'`([^`]+)`', step)

# Initialize session state
if "progress" not in st.session_state:
    st.session_state.progress = [False] * len(steps)

st.markdown("#### Click each box to mark the step as completed. Commands will hide once marked:")

for i, step in enumerate(steps):
    enabled = i == 0 or st.session_state.progress[i - 1]

    # Only allow interaction if enabled
    st.session_state.progress[i] = st.checkbox(step, key=i, value=st.session_state.progress[i], disabled=not enabled)

    # Show command(s) if step is enabled but not yet completed
    if enabled and not st.session_state.progress[i]:
        commands = extract_command(step)
        for cmd in commands:
            st.code(cmd, language="bash")

# Final message
if all(st.session_state.progress):
    st.success("🎉 All steps completed! Great job, Boris!")
