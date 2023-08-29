import re
from nltk.tokenize import word_tokenize
import ebooklib

def load_epub_content(epub_path):
    book = ebooklib.epub.read_epub(epub_path)
    content = []
    for item in book.get_items():
        if item.get_type() == ebooklib.ITEM_DOCUMENT:
            content.append(item.get_content().decode('utf-8'))
    return "\n".join(content)

epub_path = '/Users/xinmingshen/Desktop/nogamenolife/正篇/NO GAME NO LIFE游戏人生 01 听说游戏玩家兄妹要征服幻想世界.epub'
novel_text = load_epub_content(epub_path)

chapter_markers = ["序章", "第一章", "第二章", "第三章", "第四章", "终章"] #lol should use this one but I didnt
title_patterns = re.compile(r"^(?:第[一二三四五六七八九十百千]+章)")
lines = novel_text.splitlines()
current_chapter = ""
current_tokens = []

for line in lines: #ask GPT to do this didnt check
    line = line.strip()  
    if not line:  
        continue
    
    if any(marker in line for marker in chapter_markers):
        if current_chapter:
            num_tokens = len(word_tokenize(" ".join(current_tokens)))
            if num_tokens > 0:
                print(f"{current_chapter} has {num_tokens} tokens.")

        current_chapter = line
        current_tokens = []
    elif title_patterns.match(line):
        if current_chapter:
            num_tokens = len(word_tokenize(" ".join(current_tokens)))
            if num_tokens > 0:
                print(f"{current_chapter} has {num_tokens} tokens.")

        current_chapter = line
        current_tokens = []

    current_tokens.append(line)

num_tokens = len(word_tokenize(" ".join(current_tokens)))
if num_tokens > 0:
    print(f"{current_chapter} has {num_tokens} tokens.")
