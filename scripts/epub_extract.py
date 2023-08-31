import os
from ebooklib import epub
import ebooklib
import html2text

class HTML2TextNoImages(html2text.HTML2Text):
    def handle_img(self, starttag, attrs):
        # Override the default image handling to do nothing
        pass

def epub_to_html(epub_path, output_dir):
    # Read the EPUB
    book = epub.read_epub(epub_path)

    # Make sure output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for item in book.items:
        # Check if the item is of type 'text' (i.e., XHTML)
        if item.get_type() != ebooklib.ITEM_DOCUMENT:
            continue

        # item docs:
        # https://docs.sourcefabric.org/projects/ebooklib/en/latest/ebooklib.html#ebooklib.epub.EpubHtml

        # Get the HTML content
        html_content = item.get_body_content().decode('utf-8')

        # HTML to markdown with html2text
        converter = HTML2TextNoImages()
        markdown = converter.handle(html_content)

        # Write the markdown content to file
        output_path = os.path.join(output_dir, f"{item.id}.md")
        with open(output_path, 'w', encoding='utf-8') as markdown_file:
            markdown_file.write(markdown)

os.mkdir('ngnl1_en')
os.mkdir('ngnl1_jp')

epub_to_html('ngnl1_en.epub', 'ngnl1_en')
epub_to_html('ngnl1_jp.epub', 'ngnl1_jp')
