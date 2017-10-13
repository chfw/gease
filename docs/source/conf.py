# -*- coding: utf-8 -*-
DESCRIPTION = (
    'simply makes a git release using github api v3' +
    ''
)
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.doctest',
    'sphinx.ext.intersphinx',
    'sphinx.ext.viewcode',
]

templates_path = ['_templates']
source_suffix = '.rst'
master_doc = 'index'

project = u'gease'
copyright = u'2017 Onni Software Ltd.'
version = '0.0.0'
release = '0.0.1'
exclude_patterns = []
pygments_style = 'sphinx'
html_theme = 'default'
html_static_path = ['_static']
htmlhelp_basename = 'geasedoc'
latex_elements = {}
latex_documents = [
    ('index', 'gease.tex',
     'gease Documentation',
     'Onni Software Ltd.', 'manual'),
]
man_pages = [
    ('index', 'gease',
     'gease Documentation',
     [u'Onni Software Ltd.'], 1)
]
texinfo_documents = [
    ('index', 'gease',
     'gease Documentation',
     'Onni Software Ltd.', 'gease',
     DESCRIPTION,
     'Miscellaneous'),
]
