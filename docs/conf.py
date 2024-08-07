# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import time

project = "jupyter_scheduler"
copyright = f"2022–{time.localtime().tm_year}, Project Jupyter"
author = "Project Jupyter"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ["myst_parser"]
myst_enable_extensions = ["colon_fence"]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "pydata_sphinx_theme"
html_static_path = ["_static"]

# -- Jupyter theming -------------------------------------------------
html_logo = "_static/jupyter_logo.png"

html_theme_options = {
    "logo": {
        "text": "Jupyter Scheduler",
    },
    "icon_links": [
        {
            # Label for this link
            "name": "GitHub",
            # URL where the link will redirect
            "url": "https://github.com/jupyter-server/jupyter-scheduler",  # required
            # Icon class (if "type": "fontawesome"), or path to local image (if "type": "local")
            "icon": "fab fa-github-square",
            # The type of image to be used (see below for details)
            "type": "fontawesome",
        },
        {
            "name": "jupyter.org",
            "url": "https://jupyter.org",
            "icon": "_static/jupyter_logo.png",
            "type": "local",
        },
    ],
}
