import language_tool_python  # type: ignore
# java needed for that


tool: language_tool_python.LanguageTool | None = None


def initialize_tool(language: str = 'fr') -> None:
    """Initialize the global LanguageTool for the specified language.

    Args:
        language (str): The language code (default is 'fr' for French).
    """
    global tool
    tool = language_tool_python.LanguageTool(language)


def close_tool() -> None:
    """Close the global LanguageTool.
    """
    global tool
    if tool is not None:
        tool.close()
        tool = None


def language_tool_on_text(texts: list[str], specific_words: list[str],
                          rules_ignored: list[str]) -> list[tuple[int, str, str]]:

    combined_text: str = "\n".join(texts)

    matches: list[language_tool_python.Match] = tool.check(combined_text)

    output: list[tuple[int, str]] = []
    line_offsets: list[int] = [0]
    for text in texts:
        line_offsets.append(line_offsets[-1] + len(text) + 1)

    for match in matches:
        if match.matchedText in specific_words:
            continue
        line_number: int = next(i for i, offset in enumerate(line_offsets) if offset > int(match.offset)) - 1
        output.append((line_number, str(match.matchedText) + ", " + str(match.message)))

    return output
