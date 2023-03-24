# A Simple Static Site Generator (SSSG)
This is a basic static-site generator that generates a website using Markdown, HTML, CSS, and Python. The generator reads content from Markdown files in any subdirectory. The first level directories are turned into nav bar links, and any further directories are drop downs. **I have only tested this to depth 2.**

## How to use

1. Clone the repository to your local machine.
2. Install any necessary Python dependencies by running `pip install -r requirements.txt`.
3. Create a new Markdown file in the appropriate path for any page you want
4. Run the site compiler by executing `python app2.py` in a terminal window.
5. Host the website locally with `python -m http.server`

## Content

Each Markdown file should contain the content for a single article and should be named the name of the page. The first line should be a machine interpretable date or year. This should be followed by the content of the article in Markdown format.

## Appearance

The appearance of the website is controlled by the `style.css` file. The CSS file includes styles for the navigation bar, the grid of articles, and the selected article. You can modify the CSS file to customize the appearance of the website.

## How it works

The static-site generator uses Python to read the content from the Markdown files in the all directories from root recursively and converts them to HTML files. The HTML files are then used to populate the website with articles. The javascript also includes event listeners to handle navigation and history management, allowing the user to browse articles and use the back and forward buttons to navigate the site. The generator is designed to be simple and lightweight, and can be easily modified to suit your needs.

## Novelties
The entire site is shipped via content.json to your end-user on the first interaction, including base64 encoding of images. This makes your website super fast and responsive for your end user.


