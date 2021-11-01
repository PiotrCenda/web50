import re
from markdown2 import Markdown
import random

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage


def list_entries():
    """
    Returns a list of all names of encyclopedia entries.
    """
    _, filenames = default_storage.listdir("entries")
    return list(sorted(re.sub(r"\.md$", "", filename)
                for filename in filenames if filename.endswith(".md")))


def save_entry(title, content):
    """
    Saves an encyclopedia entry, given its title and Markdown
    content. If an existing entry with the same title already exists,
    it is replaced.
    """
    filename = f"entries/{title}.md"
    if default_storage.exists(filename):
        default_storage.delete(filename)
    
    default_storage.save(filename, ContentFile(re.sub(r"\r\n", "\n", content)))


def get_entry(title):
    """
    Retrieves an encyclopedia entry by its title. If no such
    entry exists, the function returns None.
    """
    try:
        f = default_storage.open(f"entries/{title}.md")
        return f.read().decode("utf-8")
    except FileNotFoundError:
        return None


def view_entry(title):
    file = get_entry(title)
    
    if file is None:
        return None
    
    markdowner = Markdown()

    return markdowner.convert(file)


def search_entries(entry_name):
    matched_entries = list()
    filelist = list_entries()

    for entry in filelist:
        if entry_name.lower() in entry.lower():
            matched_entries.append(entry)
    
    return matched_entries


def random_entry():
    return random.choice(list_entries())