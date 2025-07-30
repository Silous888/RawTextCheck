"""
File        : startup.py
Author      : Silous
Created on  : 2025-07-26
Description : Startup module for the CheckFrench application.

This module handles the initialization of the application,
including creating necessary folders, creating JSON configuration.
"""


# == Imports ==================================================================

import os

from rawtextcheck.api import google_sheet_api
from rawtextcheck.default_parameters import RESULTS_FOLDER, PLUGIN_PARSER_FOLDER
from rawtextcheck.newtype import ItemConfig
from rawtextcheck.script import json_config, json_projects


# == Functions ================================================================

def create_json_config() -> None:
    """Create the JSON configuration file if it does not exist."""
    json_config.create_json()


def create_json_projects() -> None:
    """Create the JSON projects file if it does not exist."""
    json_projects.create_json()


def create_folders() -> None:
    """Create necessary folders for the application."""
    if not os.path.exists(RESULTS_FOLDER):
        os.makedirs(RESULTS_FOLDER)
    if not os.path.exists(PLUGIN_PARSER_FOLDER):
        os.makedirs(PLUGIN_PARSER_FOLDER)


def set_google_credentials() -> None:
    """Set Google API credentials."""
    config: ItemConfig = json_config.load_data()
    if config["credentials_google"]:
        google_sheet_api.set_credentials_info(config["credentials_google"])


def startup_everything() -> None:
    """Call every function of startup.py"""
    create_folders()
    create_json_config()
    create_json_projects()
    set_google_credentials()
