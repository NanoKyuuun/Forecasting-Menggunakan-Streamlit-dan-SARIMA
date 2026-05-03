"""Temporary page shells for upcoming implementation issues."""

from __future__ import annotations

import streamlit as st

from src.page_registry import PAGE_DESCRIPTIONS


def render_placeholder_page(page_name: str) -> None:
    """Render a stable shell for pages implemented in later PRD issues."""
    st.title(page_name)
    st.info("Halaman ini sudah disiapkan sebagai bagian dari struktur dashboard.")

    issue_hint = PAGE_DESCRIPTIONS.get(page_name)
    if issue_hint:
        st.caption(f"Tahap implementasi: {issue_hint}")

    st.divider()
    st.write("Konten utama akan mengikuti acceptance criteria pada issue terkait.")
