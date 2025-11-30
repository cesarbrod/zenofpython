import sys
import io
import argparse
from contextlib import redirect_stdout
from deep_translator import GoogleTranslator

def get_zen_of_python():
    """Captures the output of 'import this'."""
    f = io.StringIO()
    with redirect_stdout(f):
        import this
    return f.getvalue()

def get_available_languages():
    """Returns a dictionary of supported languages."""
    # GoogleTranslator().get_supported_languages(as_dict=True) returns {name: code}
    return GoogleTranslator().get_supported_languages(as_dict=True)

def display_pager(items):
    """
    Displays items page by page.
    items: list of strings to display.
    """
    page_size = 20
    total_items = len(items)
    
    for i in range(0, total_items, page_size):
        chunk = items[i:i + page_size]
        for item in chunk:
            print(item)
        
        if i + page_size < total_items:
            try:
                user_input = input(f"\n--- Press Enter for more ({i + len(chunk)}/{total_items}), or type a language name to select: --- ").strip()
                if user_input:
                    return user_input
            except KeyboardInterrupt:
                print("\nAborted.")
                sys.exit(0)
    return None

def main():
    parser = argparse.ArgumentParser(description="Print the Zen of Python in a specified language.")
    parser.add_argument("language", nargs="?", help="The language to translate to.")
    args = parser.parse_args()

    translator = GoogleTranslator(source='auto', target='en') # Init with dummy
    supported_langs = get_available_languages()
    # supported_langs is {name: code}
    # We want to be able to search by name.
    
    target_lang_code = None
    target_lang_name = None

    if args.language:
        query = args.language.lower()
        if query in supported_langs:
            target_lang_code = supported_langs[query]
            target_lang_name = query
        elif query in supported_langs.values():
             # User provided a code directly
             target_lang_code = query
             # find name
             for name, code in supported_langs.items():
                 if code == query:
                     target_lang_name = name
                     break
        else:
            print(f"Language '{args.language}' not found in supported languages.")
            # Fall through to list? Or exit? The prompt implies if *not provided*.
            # But if provided and invalid, maybe helpful to list.
            # For now, let's exit to be strict about "If the user does not provide..."
            sys.exit(1)
    else:
        # No language provided. List them.
        print("No language specified. Available languages:\n")
        sorted_names = sorted(supported_langs.keys())
        
        # We need to handle the selection from the pager.
        # The pager prints, and optionally returns a selection if typed.
        # If the pager finishes without selection, we prompt at the end.
        
        selection = display_pager(sorted_names)
        
        if not selection:
            try:
                selection = input("\nPlease enter the name of the language: ").strip()
            except KeyboardInterrupt:
                sys.exit(0)
        
        if selection:
            query = selection.lower()
            if query in supported_langs:
                target_lang_code = supported_langs[query]
                target_lang_name = query
            else:
                print(f"Invalid language selected: {selection}")
                sys.exit(1)
        else:
            print("No language selected.")
            sys.exit(1)

    # Perform translation
    zen_text = get_zen_of_python()
    
    print(f"\nTranslating Zen of Python to {target_lang_name.title()}...\n")
    
    try:
        # Translate line by line to preserve structure, or whole block?
        # Whole block might lose newlines or formatting if not careful.
        # deep-translator usually handles text well.
        # Let's try translating the whole block.
        translator = GoogleTranslator(source='en', target=target_lang_code)
        translated = translator.translate(zen_text)
        print(translated)
    except Exception as e:
        print(f"Error during translation: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
