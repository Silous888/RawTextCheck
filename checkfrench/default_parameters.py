"""
File        : default_parameters.py
Author      : Silous
Created on  : 2025-04-6
Description : Various parameters used in the application.

This file contains default parameters such as file paths, valid letters,
punctuation, and a list of languages supported by LanguageTool.
It is used to centralize configuration settings for easier management and
maintenance.
"""


# == Imports ==================================================================

from typing import Tuple, Callable

from PyQt5.QtCore import QCoreApplication as QCA


# == Constants ================================================================

CONFIG_FOLDER = "config"
"""Folder where config files are stored"""

# ------- App Config ----------

JSON_CONFIG_PATH = CONFIG_FOLDER + "/config.json"
"""Path to the JSON file containing app configuration"""

LANGUAGES: list[Tuple[str, str]] = [
    ("english", "English"),
    ("french", "French")
    ]
"""Avalaible language for the app interface, first value
is default value"""

THEMES: list[Tuple[str, str]] = [
    ("light", QCA.translate("color theme", "Light"))
    ]
"""Avalaible theme for the app interface, first value is
default value"""


# ------- Project Config ----------

JSON_PROJECT_PATH = CONFIG_FOLDER + "/data_projects.json"
"""Path to the JSON file containing projects data"""

DEFAULT_VALID_ALPHANUMERIC = "0123456789" \
                             "abcdefghijklmnopqrstuvwxyz" \
                             "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
"""Default valid alphanumeric proposed in a project configuration"""

DEFAULT_VALID_PUNCTUATION = ".,;:!?" \
                            "()[]\"'"
"""Default valid punctuation proposed in a project configuration"""

DEFAULT_VALID_SPACE = " "  # basic Space
"""Default valid space proposed in a project configuration"""

NARROW_NOBREAK_SPACE = " "
"""Narrow No-Break Space, used as a space before punctuation in French"""

NOBREAK_SPACE = " "
"""No-Break Space, used as a space before punctuation"""

DEFAULT_LANGUAGE = "en"
"""Default language when creating a project"""

DEFAULT_PARSER = "textfile"
"""Default parser when creating a project"""

PLUGIN_PARSER_FOLDER = "parsers"
"""Directory where plugin parsers are stored"""

PARSERFUNCTIONTYPE = Callable[[str, str], list[tuple[str, str]]]
"""Type alias for a parser function: it takes (pathfile, argument)
and returns a list of (str, str) tuples"""

# The list is sorted by language code for easier readability.
LANGUAGES_LANGUAGETOOL: list[Tuple[str, str]] = [
    ("ar", QCA.translate("Language", "Arabic")),
    ("ast", QCA.translate("Language", "Asturian")),
    ("ast-ES", QCA.translate("Language", "Asturian (Spain)")),
    ("auto", QCA.translate("Language", "Auto-detect")),
    ("be", QCA.translate("Language", "Belarusian")),
    ("be-BY", QCA.translate("Language", "Belarusian")),
    ("br", QCA.translate("Language", "Breton")),
    ("br-FR", QCA.translate("Language", "Breton (France)")),
    ("ca", QCA.translate("Language", "Catalan")),
    ("ca-ES", QCA.translate("Language", "Catalan (Spain)")),
    ("ca-ES-balear", QCA.translate("Language", "Catalan (Balearic)")),
    ("ca-ES-valencia", QCA.translate("Language", "Catalan (Valencian)")),
    ("crh", QCA.translate("Language", "Crimean Tatar")),
    ("crh-UA", QCA.translate("Language", "Crimean Tatar (Ukraine)")),
    ("da", QCA.translate("Language", "Danish")),
    ("da-DK", QCA.translate("Language", "Danish (Denmark)")),
    ("de", QCA.translate("Language", "German")),
    ("de-AT", QCA.translate("Language", "German (Austria)")),
    ("de-CH", QCA.translate("Language", "German (Switzerland)")),
    ("de-DE", QCA.translate("Language", "German (Germany)")),
    ("de-DE-x-simple-language", QCA.translate("Language", "Simple German")),
    ("de-DE-x-simple-language-DE", QCA.translate("Language", "Simple German (Germany)")),
    ("de-LU", QCA.translate("Language", "German (Luxembourg)")),
    ("el", QCA.translate("Language", "Greek")),
    ("el-GR", QCA.translate("Language", "Greek (Greece)")),
    ("en", QCA.translate("Language", "English")),
    ("en-AU", QCA.translate("Language", "English (Australia)")),
    ("en-CA", QCA.translate("Language", "English (Canada)")),
    ("en-GB", QCA.translate("Language", "English (UK)")),
    ("en-NZ", QCA.translate("Language", "English (New Zealand)")),
    ("en-US", QCA.translate("Language", "English (US)")),
    ("en-ZA", QCA.translate("Language", "English (South Africa)")),
    ("eo", QCA.translate("Language", "Esperanto")),
    ("es", QCA.translate("Language", "Spanish")),
    ("es-AR", QCA.translate("Language", "Spanish (Argentina)")),
    ("es-ES", QCA.translate("Language", "Spanish (Spain)")),
    ("fa", QCA.translate("Language", "Persian")),
    ("fa-IR", QCA.translate("Language", "Persian (Iran)")),
    ("fr", QCA.translate("Language", "French")),
    ("fr-BE", QCA.translate("Language", "French (Belgium)")),
    ("fr-CA", QCA.translate("Language", "French (Canada)")),
    ("fr-CH", QCA.translate("Language", "French (Switzerland)")),
    ("fr-FR", QCA.translate("Language", "French (France)")),
    ("ga", QCA.translate("Language", "Irish")),
    ("ga-IE", QCA.translate("Language", "Irish (Ireland)")),
    ("gl", QCA.translate("Language", "Galician")),
    ("gl-ES", QCA.translate("Language", "Galician (Spain)")),
    ("it", QCA.translate("Language", "Italian")),
    ("it-IT", QCA.translate("Language", "Italian (Italy)")),
    ("ja", QCA.translate("Language", "Japanese")),
    ("ja-JP", QCA.translate("Language", "Japanese")),
    ("km", QCA.translate("Language", "Khmer")),
    ("km-KH", QCA.translate("Language", "Khmer (Cambodia)")),
    ("nl", QCA.translate("Language", "Dutch")),
    ("nl-BE", QCA.translate("Language", "Dutch (Belgium)")),
    ("nl-NL", QCA.translate("Language", "Dutch (Netherlands)")),
    ("pl", QCA.translate("Language", "Polish")),
    ("pl-PL", QCA.translate("Language", "Polish")),
    ("pt", QCA.translate("Language", "Portuguese")),
    ("pt-AO", QCA.translate("Language", "Portuguese (Angola)")),
    ("pt-BR", QCA.translate("Language", "Portuguese (Brazil)")),
    ("pt-MZ", QCA.translate("Language", "Portuguese (Mozambique)")),
    ("pt-PT", QCA.translate("Language", "Portuguese (Portugal)")),
    ("ro", QCA.translate("Language", "Romanian")),
    ("ro-RO", QCA.translate("Language", "Romanian (Romania)")),
    ("ru", QCA.translate("Language", "Russian")),
    ("ru-RU", QCA.translate("Language", "Russian")),
    ("sl", QCA.translate("Language", "Slovenian")),
    ("sl-SI", QCA.translate("Language", "Slovenian (Slovenia)")),
    ("sk", QCA.translate("Language", "Slovak")),
    ("sk-SK", QCA.translate("Language", "Slovak")),
    ("sv", QCA.translate("Language", "Swedish")),
    ("sv-SE", QCA.translate("Language", "Swedish (Sweden)")),
    ("ta", QCA.translate("Language", "Tamil")),
    ("ta-IN", QCA.translate("Language", "Tamil (India)")),
    ("tl", QCA.translate("Language", "Tagalog")),
    ("tl-PH", QCA.translate("Language", "Tagalog (Philippines)")),
    ("uk", QCA.translate("Language", "Ukrainian")),
    ("uk-UA", QCA.translate("Language", "Ukrainian (Ukraine)")),
    ("zh", QCA.translate("Language", "Chinese")),
    ("zh-CN", QCA.translate("Language", "Chinese (Simplified)")),
]
"""List of languages supported by LanguageTool with their codes and names"""


# ------- Result Config ----------

RESULTS_FOLDER = "results"
"""Path to the folder containing results"""

INVALID_CHAR_TEXT_ERROR: str = QCA.translate("error text", "This character in not accepted.")
"""Text used in result for invalid character error"""

INVALID_CHAR_TEXT_ERROR_TYPE = "INVALID CHARACTER"
"""Type used in result for invalid character error"""


BANWORD_TEXT_ERROR: str = QCA.translate("error text", "This word is not authorized in this project.")
"""Text used in result for banword error"""

BANWORD_TEXT_ERROR_TYPE = "BANWORD"
"""Type uesd in result for banword error"""

LANGUAGETOOL_SPELLING_CATEGORY = "misspelling"
"""LanguageTool category used to detect errors as spelling errors"""
