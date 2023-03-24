# A Simple Static Site Generator (SSSG)
This is a basic static-site generator that generates a website using Markdown, HTML, CSS, and Python. The generator reads content from Markdown files in the `content` directory and populates the website with articles based on the content.

## How to use

1. Clone the repository to your local machine.
2. Install any necessary Python dependencies by running `pip install -r requirements.txt`.
3. Create a new Markdown file in the `content` directory for each article you want to publish on the site.
4. Run the site compiler by executing `python app2.py` in a terminal window.
5. Open the `index.html` file in a web browser to view the generated website.

## Content

The content for the website is stored in Markdown files in the `content` directory. Each Markdown file should contain the content for a single article and should be named using the following format: `YYYY-MM-DD-article-title.md`. For example, an article published on June 1st, 2023, with the title "My First Article" would be named `2023-06-01-my-first-article.md`.

Each Markdown file should begin with a metadata section that includes the following information:

- `title`: The title of the article.
- `date`: The date the article was published (in YYYY-MM-DD format).
- `tags`: An array of tags associated with the article.

The metadata section should be followed by the content of the article in Markdown format.

## Appearance

The appearance of the website is controlled by the `style.css` file. The CSS file includes styles for the navigation bar, the grid of articles, and the selected article. You can modify the CSS file to customize the appearance of the website.

## How it works

The static-site generator uses Python to read the content from the Markdown files in the `content` directory and convert them to HTML files. The HTML files are then used to populate the website with articles. The generator also includes event listeners to handle navigation and history management, allowing the user to browse articles and use the back and forward buttons to navigate the site. The generator is designed to be simple and lightweight, and can be easily modified to suit your needs.



