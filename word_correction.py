from typing import Any
import win32com.client
from win32com.client.dynamic import CDispatch


def check_spelling_with_word(text: str) -> tuple[list[Any], list[Any]]:
    # Crée une instance de Word
    word_app: CDispatch = win32com.client.Dispatch("Word.Application")
    word_app.Visible = False  # Optionnel : Garde Word invisible
    document = word_app.Documents.Add()

    # Ajoute le texte dans le document
    document.Content.Text = text

    # Vérifie l'orthographe et la grammaire
    spelling_errors = document.SpellingErrors
    grammar_errors = document.GrammaticalErrors

    # Liste les fautes
    errors = [error.Text for error in spelling_errors]
    grammar = [error.Text for error in grammar_errors]

    # Ferme le document sans sauvegarder
    document.Close(SaveChanges=False)
    word_app.Quit()

    return errors, grammar


