
from pathlib import Path
from typing import Tuple

from PyQt5.QtCore import QCoreApplication as QCA

JSON_FILE_PATH: Path = Path(__file__).parent / "json_data_projects.json"

RESULTS_FOLDER_PATH: Path = Path(__file__).parent / "results"


DEFAULT_VALID_LETTERS: str = "0123456789" \
                             "abcdefghijklmnopqrstuvwxyz" \
                             "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

DEFAULT_VALID_PUNCTUATION: str = ".,;:!?" \
                                 "()[]<>\"'" \
                                 "-+=" \
                                 " "  # Space

# Default valid characters for the language
LANGUAGES_LANGUAGETOOL: list[Tuple[str, str]] = [
    ("ast", QCA.translate("Languages", "Asturian")),
    ("da", QCA.translate("Language", "Danish")),
    ("pt-MZ", QCA.translate("Language", "Portuguese (Mozambique)")),
    ("eo", QCA.translate("Language", "Esperanto")),
    ("fa-IR", QCA.translate("Language", "Persian (Iran)")),
    ("sv", QCA.translate("Language", "Swedish")),
    ("pt-AO", QCA.translate("Language", "Portuguese (Angola)")),
    ("tl", QCA.translate("Language", "Tagalog")),
    ("zh-CN", QCA.translate("Language", "Chinese (Simplified)")),
    ("sk-SK", QCA.translate("Language", "Slovak")),
    ("zh", QCA.translate("Language", "Chinese")),
    ("pl-PL", QCA.translate("Language", "Polish")),
    ("ja-JP", QCA.translate("Language", "Japanese")),
    ("be-BY", QCA.translate("Language", "Belarusian")),
    ("km", QCA.translate("Language", "Khmer")),
    ("sv-SE", QCA.translate("Language", "Swedish (Sweden)")),
    ("fr-FR", QCA.translate("Language", "French (France)")),
    ("ga-IE", QCA.translate("Language", "Irish (Ireland)")),
    ("it-IT", QCA.translate("Language", "Italian (Italy)")),
    ("ast-ES", QCA.translate("Language", "Asturian (Spain)")),
    ("de-DE", QCA.translate("Language", "German (Germany)")),
    ("de", QCA.translate("Language", "German")),
    ("nl-NL", QCA.translate("Language", "Dutch (Netherlands)")),
    ("km-KH", QCA.translate("Language", "Khmer (Cambodia)")),
    ("pt-BR", QCA.translate("Language", "Portuguese (Brazil)")),
    ("es", QCA.translate("Language", "Spanish")),
    ("fr-CA", QCA.translate("Language", "French (Canada)")),
    ("be", QCA.translate("Language", "Belarusian")),
    ("ca-ES", QCA.translate("Language", "Catalan (Spain)")),
    ("br", QCA.translate("Language", "Breton")),
    ("de-CH", QCA.translate("Language", "German (Switzerland)")),
    ("gl", QCA.translate("Language", "Galician")),
    ("uk", QCA.translate("Language", "Ukrainian")),
    ("en-NZ", QCA.translate("Language", "English (New Zealand)")),
    ("el", QCA.translate("Language", "Greek")),
    ("en-AU", QCA.translate("Language", "English (Australia)")),
    ("ja", QCA.translate("Language", "Japanese")),
    ("pt-PT", QCA.translate("Language", "Portuguese (Portugal)")),
    ("fa", QCA.translate("Language", "Persian")),
    ("ru-RU", QCA.translate("Language", "Russian")),
    ("de-LU", QCA.translate("Language", "German (Luxembourg)")),
    ("ca-ES-valencia", QCA.translate("Language", "Catalan (Valencian)")),
    ("de-AT", QCA.translate("Language", "German (Austria)")),
    ("auto", QCA.translate("Language", "Auto-detect")),
    ("ga", QCA.translate("Language", "Irish")),
    ("ro-RO", QCA.translate("Language", "Romanian (Romania)")),
    ("en-US", QCA.translate("Language", "English (US)")),
    ("da-DK", QCA.translate("Language", "Danish (Denmark)")),
    ("es-ES", QCA.translate("Language", "Spanish (Spain)")),
    ("de-DE-x-simple-language", QCA.translate("Language", "Simple German")),
    ("uk-UA", QCA.translate("Language", "Ukrainian (Ukraine)")),
    ("ro", QCA.translate("Language", "Romanian")),
    ("en-ZA", QCA.translate("Language", "English (South Africa)")),
    ("nl-BE", QCA.translate("Language", "Dutch (Belgium)")),
    ("crh", QCA.translate("Language", "Crimean Tatar")),
    ("crh-UA", QCA.translate("Language", "Crimean Tatar (Ukraine)")),
    ("br-FR", QCA.translate("Language", "Breton (France)")),
    ("el-GR", QCA.translate("Language", "Greek (Greece)")),
    ("en-CA", QCA.translate("Language", "English (Canada)")),
    ("fr", QCA.translate("Language", "French")),
    ("ru", QCA.translate("Language", "Russian")),
    ("en-GB", QCA.translate("Language", "English (UK)")),
    ("sl-SI", QCA.translate("Language", "Slovenian (Slovenia)")),
    ("ca", QCA.translate("Language", "Catalan")),
    ("sk", QCA.translate("Language", "Slovak")),
    ("ar", QCA.translate("Language", "Arabic")),
    ("ca-ES-balear", QCA.translate("Language", "Catalan (Balearic)")),
    ("it", QCA.translate("Language", "Italian")),
    ("fr-BE", QCA.translate("Language", "French (Belgium)")),
    ("pl", QCA.translate("Language", "Polish")),
    ("tl-PH", QCA.translate("Language", "Tagalog (Philippines)")),
    ("sl", QCA.translate("Language", "Slovenian")),
    ("ta-IN", QCA.translate("Language", "Tamil (India)")),
    ("es-AR", QCA.translate("Language", "Spanish (Argentina)")),
    ("nl", QCA.translate("Language", "Dutch")),
    ("fr-CH", QCA.translate("Language", "French (Switzerland)")),
    ("ta", QCA.translate("Language", "Tamil")),
    ("en", QCA.translate("Language", "English")),
    ("pt", QCA.translate("Language", "Portuguese")),
    ("de-DE-x-simple-language-DE", QCA.translate("Language", "Simple German (Germany)")),
    ("gl-ES", QCA.translate("Language", "Galician (Spain)")),
]
