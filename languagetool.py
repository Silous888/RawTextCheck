import language_tool_python
# java needed for that

tool = language_tool_python.LanguageTool('fr')


def language_tool_on_text(texts: list[str], specific_words: list[str]) -> list[tuple[int, str]]:
    combined_text: str = "\n".join(texts)

    matches: list[language_tool_python.Match] = tool.check(combined_text)

    output: list[tuple[int, str]] = []
    line_offsets: List[int] = [0]
    for text in texts:
        line_offsets.append(line_offsets[-1] + len(text) + 1)

    for match in matches:
        if match.matchedText in specific_words:
            continue
        line_number: int = next(i for i, offset in enumerate(line_offsets) if offset > int(match.offset)) - 1
        output.append((line_number, str(match.matchedText) + ", " + str(match.message)))

    return output
