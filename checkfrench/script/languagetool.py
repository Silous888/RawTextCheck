"""
File        : languagetool.py
Author      : Silous
Created on  : 2025-02-07
Description : Module for integrating LanguageTool for grammar and style checking.

This module provides functions to initialize and use LanguageTool for analyzing text.
"""


# == Imports ==================================================================

from logging import Logger
import language_tool_python  # type: ignore

from checkfrench.default_parameters import LANGUAGETOOL_SPELLING_CATEGORY, LANGUAGETOOL_MAX_LINES_PER_BATCH
from checkfrench.newtype import ItemResult
from checkfrench.logger import get_logger


# == Global Variables =========================================================

tool: language_tool_python.LanguageTool | None = None
logger: Logger = get_logger(__name__)


# == Functions ================================================================

def initialize_tool(language: str) -> None:
    """Initialize the global LanguageTool for the specified language.

    Args:
        language (str): The language code.
    """
    global tool
    if tool is None:
        tool = language_tool_python.LanguageTool(language)
        logger.info("Loaded languagetool with %s language.", language)
    elif tool.language == language:
        logger.info("Languagetool already loaded with %s language", language)
    else:
        tool = language_tool_python.LanguageTool(language)
        logger.info("Reloaded languagetool with %s language.", language)


def close_tool() -> None:
    """Close the global LanguageTool.
    """
    global tool
    if tool is not None:
        tool.close()
        tool = None


def analyze_text(texts: list[tuple[str, str]], ignored_words: list[str],
                 ignored_rules: list[str]) -> list[ItemResult]:
    output: list[ItemResult] = []

    if tool is None:
        logger.error("LanguageTool not initialized.")
        return output

    for batch_start in range(0, len(texts), LANGUAGETOOL_MAX_LINES_PER_BATCH):
        batch: list[tuple[str, str]] = texts[batch_start:batch_start + LANGUAGETOOL_MAX_LINES_PER_BATCH]
        combined_text: str = "\n".join([x[1] for x in batch])

        # offset position of lines in combined_text
        line_offsets: list[int] = [0]
        for text in [x[1] for x in batch]:
            line_offsets.append(line_offsets[-1] + len(text) + 1)

        try:
            logger.info("Analyzing %d lines (%d characters) (batch %s of %s)",
                        len(batch), len(combined_text),
                        batch_start // LANGUAGETOOL_MAX_LINES_PER_BATCH + 1,
                        (len(texts) + LANGUAGETOOL_MAX_LINES_PER_BATCH - 1) // LANGUAGETOOL_MAX_LINES_PER_BATCH)
            errors: list[language_tool_python.Match] = tool.check(combined_text)
        except Exception as e:
            logger.error("LanguageTool failed on batch %d: %s", batch_start, e)
            continue

        for error in errors:
            if (str(error.matchedText) in ignored_words and str(error.ruleIssueType) == LANGUAGETOOL_SPELLING_CATEGORY):
                continue
            if str(error.ruleId) in ignored_rules:
                continue

            line_number: int = next(
                i for i, offset in enumerate(line_offsets) if offset > int(error.offset)  # type: ignore
            ) - 1

            output.append(
                ItemResult(
                    line_number=batch[line_number][0],
                    line=batch[line_number][1],
                    error=str(error.matchedText),
                    error_type=str(error.ruleId),
                    error_issue_type=error.ruleIssueType,
                    explanation=str(error.message),
                    suggestion=str(error.replacements)
                )
            )
    return output
