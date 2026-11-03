# config.py
# Reads settings from Streamlit secrets (deployed app) or a local .env file.

import os

import streamlit as st
from dotenv import load_dotenv

load_dotenv()  # loads .env when running locally; does nothing if there is no .env


def get_setting(name):
    """Return a setting from Streamlit secrets first, then environment variables.
    Returns None if the setting is not configured anywhere."""
    try:
        if name in st.secrets:
            return st.secrets[name]
    except Exception:
        pass  # no secrets.toml file exists (normal when running locally with .env)
    return os.getenv(name)
