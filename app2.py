import os
import re
import datetime
import random
import json
import markdown2
import io
from PIL import Image
import base64

def convert_image_to_png_bytes(image_path):
    # Open the image file using Pillow
    with Image.open(image_path) as img:
        # Create an in-memory binary stream to store the PNG bytes
        buffer = io.BytesIO()
        # Save the image to the buffer in PNG format
        img.save(buffer, format="PNG")
        # Return the PNG bytes string
        return buffer.getvalue()


def extract_date(first_line):
    """
    Extracts a date from the first line of a markdown file and returns it as a string in YYYY-MM-DD format.
    """
    # Regular expressions to match various date formats
    date_formats = [
        r'\d{4}',  # Year only
        r'[a-zA-Z]{3}\s+\d{1,2},\s+\d{4}',  # Abbreviated month name, day, year
        r'[a-zA-Z]{3}\s+\d{1,2}\s+\d{4}',  # Abbreviated month name, day, year
        r'\d{1,2}\s+[a-zA-Z]{3},\s+\d{4}',  # Day, abbreviated month name, year
        r'\d{1,2}\s+[a-zA-Z]{3}\s+\d{4}',  # Day, abbreviated month name, year
    ]

    for date_format in date_formats:
        match = re.search(date_format, first_line)
        if match:
            date_str = match.group(0)
            break
    else:
        date_str = 'unknown'

    # Convert the date string to a YYYY-MM-DD format
    if date_str == 'unknown':
        return date_str
    elif len(date_str) == 4:
        return f"{date_str}-01-01"
    else:
        dt = datetime.datetime.strptime(date_str, '%b %d, %Y')
        return dt.strftime('%Y-%m-%d')


def extract_quick_blurb(markdown):
    """
    Extracts the first paragraph or bullet point of the given markdown content and returns it as plain text, truncated to 200 characters with an ellipsis if necessary.
    """
    # Find the first non-header line
    paragraph_text = ''
    for line in markdown.split('\n'):
        line = line.strip()
        if line and not line.startswith('#') and not line.startswith('!'):
            if line.startswith("* "):
                line = line[2:]
            if all(c.isdigit() or c.isspace() for c in line):
                continue
            paragraph_text = line
            break

    # Truncate the paragraph if necessary and add an ellipsis
    if len(paragraph_text) > 200:
        paragraph_text = paragraph_text[:200] + '...'

    return paragraph_text

RES = 20

def convert_image_to_jpeg_base64(image_path, res=RES):
    # Open the image file using Pillow
    with Image.open(image_path) as img:
        basewidth = min(600, img.size[0])
        wpercent = (basewidth/float(img.size[0]))
        hsize = int((float(img.size[1])*float(wpercent)))
        img = img.resize((basewidth,hsize), Image.Resampling.LANCZOS)

        # Create an in-memory binary stream to store the PNG bytes
        buffer = io.BytesIO()
        # Save the image to the buffer in JPEG format
        img = img.convert('RGB')
        img.save(buffer, format="JPEG", quality=90, dpi=(res, res))
        # Return the base64-encoded JPEG data
        return base64.b64encode(buffer.getvalue()).decode('utf-8')

def embed_images_in_html(html):
    # Find all <img> tags in the HTML
    img_tags = re.findall(r'<img.*?src="(.*?)".*?>', html)

    # Replace each <img> tag with a base64-encoded embedded image
    for img_tag in img_tags:
        if img_tag.startswith('http'):
            continue
        encoded_bytes = convert_image_to_jpeg_base64("./static_resources/"+img_tag.split("/")[-1])
        # Replace the <img> tag with the embedded image
        html = html.replace(f'src="{img_tag}"', f'src="data:image/jpeg;base64,{encoded_bytes}"')

    return html

def find_markdown_files(directory):
    """
    Recursively finds all markdown files in the given directory and returns a list of dictionaries containing metadata about each file.
    """
    files = []

    for root, dirs, filenames in os.walk(directory):
        for filename in filenames:
            if filename.endswith('.md'):
                # Read the file contents
                with open(os.path.join(root, filename), 'r', encoding='utf-8') as f:
                    markdown = f.read()

                # Convert the markdown to HTML
                html = markdown2.markdown(
                    markdown,
                    extras=['fenced-code-blocks', 'code-friendly', 'break-on-newline', 'tables']
                ).replace("</p>\n","</p><br>")

                # Extract metadata
                first_line = markdown.split('\n')[0]
                published_date = extract_date(first_line)
                relative_path = "/".join(os.path.relpath(os.path.join(root, filename), directory).split("/")[:-1])
                updated_date = datetime.datetime.fromtimestamp(os.path.getmtime(os.path.join(root, filename))).strftime('%Y-%m-%d')
                title = os.path.splitext(os.path.basename(filename))[0]
                quick_blurb = extract_quick_blurb(markdown)

                html = embed_images_in_html(html)

                # Extract a random image from the markdown, if any
                image_matches = re.findall(r'!\[.*?\]\((.*?)\)', markdown)
                random_image = "data:image/png;base64,"+convert_image_to_jpeg_base64("./static_resources/"+random.choice(image_matches).split("/")[-1], res=5) if image_matches else ''

                # Add the metadata to the file dictionary and append it to the list
                file_data = {
                    'html': html,
                    'published_date': published_date,
                    'relative_path': relative_path,
                    'random_image': random_image,
                    'updated_date': updated_date,
                    'title': title,
                    'quick_blurb': quick_blurb,
                    'tags': ["#" + x for x in relative_path.split("/") if x != ""]
                }
                files.append(file_data)

    return files


def dump_metadata_as_json(metadata_list, output_file):
    """
    Dumps the given metadata list as a JSON string to the given output file.
    """
    with open(output_file, 'w') as f:
        json.dump(metadata_list, f, indent=2)


# Example Usage
files = find_markdown_files('.')
dump_metadata_as_json(files, 'content.json')
