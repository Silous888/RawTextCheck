
from logging import Logger
import language_tool_python  # type: ignore

from checkfrench.newtype import ItemResult
from checkfrench.logger import get_logger

tool: language_tool_python.LanguageTool | None = None

logger: Logger = get_logger(__name__)


def initialize_tool(language: str) -> None:
    """Initialize the global LanguageTool for the specified language.

    Args:
        language (str): The language code (default is 'fr' for French).
    """
    global tool
    tool = language_tool_python.LanguageTool(language)
    logger.info("Loaded languagetool with %s language.", language)


def close_tool() -> None:
    """Close the global LanguageTool.
    """
    global tool
    if tool is not None:
        tool.close()
        tool = None


def analyze_text(texts: list[tuple[str, str]], ignored_words: list[str],
                 ignored_rules: list[str]) -> list[ItemResult]:
    """
    Analyse une liste de textes avec LanguageTool et retourne les erreurs détectées.

    Args:
        texts (list[str, str]): Liste des phrases à vérifier.
        ignored_words (list[str]): Liste de mots à ignorer dans la détection d'erreurs.
        rules_ignored (list[str]): Liste d'identifiants de règles à ignorer.

    Returns:

    """
    combined_text: str = "\n".join([x[1] for x in texts])

    output: list[ItemResult] = []

    # offset position of lines in combined_text
    line_offsets: list[int] = [0]
    for text in [x[1] for x in texts]:
        line_offsets.append(line_offsets[-1] + len(text) + 1)

    if tool is None:
        logger.error("LanguageTool not initialized.")
        return output

    errors: list[language_tool_python.Match] = tool.check(combined_text)

    for error in errors:
        if str(error.matchedText) in ignored_words or str(error.ruleId) in ignored_rules:
            continue

        line_number: int = next(
            i for i, offset in enumerate(line_offsets) if offset > int(error.offset)  # type: ignore
        ) - 1

        output.append(
            ItemResult(line_number=[x[0] for x in texts][line_number],
                       line=[x[1] for x in texts][line_number],
                       error=str(error.matchedText),
                       error_type=str(error.message),
                       explanation=str(error.ruleId),
                       suggestion=str(error.replacements))
        )
    return output
