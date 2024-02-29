import hashlib
import html2text
from bs4 import BeautifulSoup
from datetime import datetime
from django.utils import timezone
from enum import Enum, unique
from typing import TYPE_CHECKING, Any, Optional, TypeGuard

@unique
class EnumBase(Enum):
    """
    You are supposed to support _label_ like the __new__:
    """

    def __new__(cls, attribs):
        obj = object.__new__(cls)
        obj._value_ = attribs["id"]
        obj._label_ = attribs["label"]
        return obj

    def __int__(self):
        return self.value

    def __str__(self):
        return self.name.lower()

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.value == other.value
        elif isinstance(other, int):
            return self.value == other
        return False

    def __lt__(self, other):
        if isinstance(other, self.__class__):
            return self.value < other.value
        elif isinstance(other, int):
            return self.value < other
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.value)

    @property
    def id(self) -> int:
        return self._value_

    @property
    def label(self) -> str:
        return self._label_

    def json(self) -> dict[str, Any]:
        return {"id": self.id, "name": str(self), "label": self.label}

    @classmethod
    def list(cls: type["EnumBase"]) -> list[dict[str, Any]]:
        return [x.json() for x in cls]

    @classmethod
    def fromStr(cls: type["EnumBase"], string) -> "EnumBase":
        return cls[string.upper()]

    @classmethod
    def fromLabel(cls: type["EnumBase"], label) -> Optional["EnumBase"]:
        for i in cls:
            if i.label == label:
                return i
        return None

def split_to_paragraphs(text):
    lines = text.split('\n')
    paragraphs = []
    buffer = []

    for line in lines:
        line_stripped = line.strip()
        if not line_stripped:
            if buffer:
                paragraphs.append("\n".join(buffer))
                buffer = []
        else:
            buffer.append(line_stripped)

    if buffer:
        paragraphs.append("\n".join(buffer))

    # Process paragraphs according to the length and '#' rule
    processed_paragraphs = []
    for i, paragraph in enumerate(paragraphs):
        # Attach short paragraphs (< 80 chars) to the previous or next paragraph
        if len(paragraph) < 80:
            if paragraph.startswith("#"):
                # If it starts with '#' and is short, attach it to the next paragraph
                if i + 1 < len(paragraphs):
                    paragraphs[i + 1] = paragraph + "\n\n" + paragraphs[i + 1]
                elif processed_paragraphs:
                    # If there's no next paragraph but there is a previous one
                    processed_paragraphs[-1] += "\n\n" + paragraph
            else:
                # If it's short but doesn't start with '#', attach to the previous
                if processed_paragraphs:
                    processed_paragraphs[-1] += "\n\n" + paragraph
                elif i + 1 < len(paragraphs):
                    # If there's no previous paragraph but there is a next one
                    paragraphs[i + 1] = paragraph + "\n\n" + paragraphs[i + 1]
        else:
            # Add long paragraphs or paragraphs starting with '#' that are long enough
            processed_paragraphs.append(paragraph)

    return processed_paragraphs

def convert_html_to_md(html_content):
    h = html2text.HTML2Text()
    h.ignore_links = True
    h.ignore_emphasis = True
    h.ignore_images = True
    h.ignore_mailto_links = True
    markdown_content = h.handle(html_content)
    return markdown_content

def remove_newlines(s):
    s = s.replace('\n', ' ')
    s = s.replace('\\n', ' ')
    s = s.replace('\t', ' ')
    s = s.replace('\\t', ' ')
    s = s.replace('  ', ' ')
    s = s.replace('  ', ' ')
    return s

def now() -> datetime:
    """
    Returns timezone.now() with milliseconds precision as datetime.
    """
    now = timezone.now()
    return now.replace(microsecond=1000 * (now.microsecond // 1000))

def calculate_hash(content):
    hasher = hashlib.sha256()
    hasher.update(content)
    return hasher.hexdigest()

def clean_html(html_content):
    # This function removes header, footer, and navigation menu from the HTML
    # and returns the body of the page.
    soup = BeautifulSoup(html_content, 'html.parser')
    tags = ['header', 'footer', 'nav']
    for tag in tags:
        elems = soup.find_all(tag)
        for elem in elems:
            elem.decompose()

    return soup.prettify()