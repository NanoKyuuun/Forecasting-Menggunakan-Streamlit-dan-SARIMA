"""Reusable Streamlit UI components for a guided dashboard flow."""

from __future__ import annotations

from typing import Any, Mapping

import streamlit as st

from src.workflow import WorkflowStep, get_step_for_page, get_step_status


def render_page_header(page_name: str, caption: str | None = None) -> None:
    """Render a consistent page title and workflow guide."""
    step = get_step_for_page(page_name)
    if step is None:
        st.title(page_name)
        if caption:
            st.caption(caption)
        return

    st.caption(f"Tahap {step.number} dari 7")
    st.title(step.title)
    st.write(step.goal)

    columns = st.columns(3)
    columns[0].info(f"Input: {step.required_input}")
    columns[1].success(f"Output: {step.output}")
    columns[2].warning(f"Lanjut: {step.next_step}")

    if caption:
        st.caption(caption)


def render_not_ready_message(page_name: str, detail: str) -> None:
    """Render a friendly blocked-state message."""
    step = get_step_for_page(page_name)
    title = "Tahap belum siap" if step is None else f"{step.title} belum siap"
    st.info(title)
    st.write(detail)
    if step is not None:
        st.write(f"Input yang dibutuhkan: {step.required_input}")


def render_sidebar_workflow(state: Mapping[str, Any], steps: list[WorkflowStep]) -> None:
    """Render compact workflow progress in the sidebar."""
    completed = sum(1 for step in steps if get_step_status(state, step.page) == "Selesai")
    total = len(steps)
    st.sidebar.subheader("Progress Alur")
    st.sidebar.progress(0 if total == 0 else completed / total)
    st.sidebar.caption(f"{completed} dari {total} tahap selesai.")

    for step in steps:
        status = get_step_status(state, step.page)
        st.sidebar.write(f"{step.number}. {step.short_label}: {status}")


def render_recommended_action(page_name: str) -> None:
    """Render the next-step hint for the current page."""
    step = get_step_for_page(page_name)
    if step is None:
        return
    st.info(f"Langkah berikutnya: buka menu {step.next_step} setelah output tahap ini sudah valid.")
