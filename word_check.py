import win32com.client
from win32com.client.dynamic import CDispatch
import pythoncom


def check_spelling_with_word(text: str) -> tuple[list[str], list[str]]:
    pythoncom.CoInitialize()

    word_app: CDispatch = win32com.client.Dispatch("Word.Application")
    word_app.Visible = False  # Optionnel : Word invisible
    document: CDispatch = word_app.Documents.Add()

    document.Content.Text = text

    spelling_errors = document.SpellingErrors
    grammar_errors = document.GrammaticalErrors

    errors: list[str] = []
    for error in spelling_errors:
        errors.append(error.Text)

    grammar: list[str] = []
    for error in grammar_errors:
        grammar.append(error.Text)

    document.Close(SaveChanges=False)
    word_app.Quit()

    pythoncom.CoUninitialize()
    return errors, grammar


def word_on_text(texts: list[str], specific_words: list[str]) -> list[tuple[int, str]]:
    combined_text: str = "\n".join(texts)

    errors: list[str]
    grammar: list[str]
    errors, grammar = check_spelling_with_word(combined_text)

    output: list[tuple[int, str]] = []
    line_offsets: list[int] = [0]
    for text in texts:
        line_offsets.append(line_offsets[-1] + len(text) + 1)

    all_errors: list[str] = errors + grammar

    for error, suggestions in all_errors:
        if error in specific_words:
            continue
        line_number: int = next(i for i, offset in enumerate(line_offsets) if offset > combined_text.find(error)) - 1
        output.append((line_number + 1, f"{error}, {'; '.join(suggestions)}"))

    output = sorted(output, key=lambda x: x[0])
    return output
