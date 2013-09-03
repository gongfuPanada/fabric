# -*- coding: utf-8 -*-
#
# Fabric documentation build configuration file, created by
# sphinx-quickstart on Sat Apr 25 14:53:36 2009.
#
# This file is execfile()d with the current directory set to its containing dir.
#
# Note that not all possible configuration values are present in this
# autogenerated file.
#
# All configuration values have a default; values that are commented out
# serve to show the default.

from __future__ import with_statement
import os
import re
import sys
import types
from datetime import datetime

# Custom ReST roles.
from docutils.parsers.rst import roles
from docutils import nodes, utils
# Custom ReST nodes
from fabric.changelog import issue, release as release_node

issue_types = ('bug', 'feature', 'support')

def issues_role(name, rawtext, text, lineno, inliner, options={}, content=[]):
    """
    Use: :issue|bug|feature|support:`ticket_number`

    When invoked as :issue:, turns into just a "#NN" hyperlink to Github.

    When invoked otherwise, turns into "[Type] <#NN hyperlink>: ".

    May give a 'ticket number' of '<number> backported' to indicate a
    backported feature or support ticket. This extra info will be stripped out
    prior to parsing.
    """
    # Old-style 'just the issue link' behavior
    issue_no, _, backported = utils.unescape(text).partition(' ')
    ref = "https://github.com/fabric/fabric/issues/" + issue_no
    link = nodes.reference(rawtext, '#' + issue_no, refuri=ref, **options)
    nodelist = [link]
    # Additional 'new-style changelog' stuff
    if name in issue_types:
        which = '[<span class="changelog-%s">%s</span>]' % (
            name, name.capitalize()
        )
        ret = [
            nodes.raw(text=which, format='html'),
            nodes.inline(text=" "),
            link,
            nodes.inline(text=":")
        ]
    # Create temporary node w/ data & final nodes to publish
    node = issue(
        number=issue_no,
        type_=name,
        nodelist=nodelist,
        backported=bool(backported)
    )
    return [node], []

for x in issue_types + ('issue',):
    roles.register_local_role(x, issues_role)


year_arg_re = re.compile(r'^(.+?)\s*(?<!\x00)<(.*?)>$', re.DOTALL)

def release_role(name, rawtext, text, lineno, inliner, options={}, content=[]):
    """
    Invoked as :release:`N.N.N <YYYY-MM-DD>`.

    Turns into: <b>YYYY-MM-DD</b>: released <b><a>Fabric N.N.N</a></b>, with
    the link going to the Github source page for the tag.
    """
    # Make sure year has been specified
    match = year_arg_re.match(text)
    if not match:
        msg = inliner.reporter.error("Must specify release date!")
        return [inliner.problematic(rawtext, rawtext, msg)], [msg]
    number, date = match.group(1), match.group(2)
    nodelist = [
        nodes.strong(text=date),
        nodes.inline(text=": released "),
        nodes.reference(
            text="Fabric %s" % number,
            refuri="https://github.com/fabric/fabric/tree/%s" % number,
            classes=['changelog-release']
        )
    ]
    # Return intermediate node
    node = release_node(number=number, date=date, nodelist=nodelist)
    return [node], []
roles.register_local_role('release', release_role)


# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#sys.path.append(os.path.abspath('.'))

# -- General configuration -----------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be extensions
# coming with Sphinx (named 'sphinx.ext.*') or your custom ones.
extensions = ['sphinx.ext.autodoc', 'fabric.changelog']

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix of source filenames.
source_suffix = '.rst'

# The encoding of source files.
#source_encoding = 'utf-8'

# The master toctree document.
master_doc = 'index'

# General information about the project.
project = u'Fabric'
year = datetime.now().year
copyright = u'%d, Christian Vest Hansen and Jeffrey E. Forcier' % year

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.

# Add this checkout's local Fabric module to sys.path. Allows use of
# fabric.version in here, and ensures that the autodoc stuff also works.
sys.path.insert(0, os.path.abspath(os.path.join(os.getcwd(), '..')))
from fabric.version import get_version

# Get version info
#
# Branch-only name
version = get_version('branch')
# The full human readable version, including alpha/beta/rc tags.
release = get_version('normal')


# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#language = None

# There are two options for replacing |today|: either, you set today to some
# non-false value, then it is used:
#today = ''
# Else, today_fmt is used as the format for a strftime call.
#today_fmt = '%B %d, %Y'

# List of documents that shouldn't be included in the build.
#unused_docs = []

# List of directories, relative to source directory, that shouldn't be searched
# for source files.
exclude_trees = ['_build']

# The reST default role (used for this markup: `text`) to use for all documents.
default_role = 'obj'

# If true, '()' will be appended to :func: etc. cross-reference text.
#add_function_parentheses = True

# If true, the current module name will be prepended to all description
# unit titles (such as .. function::).
#add_module_names = True

# If true, sectionauthor and moduleauthor directives will be shown in the
# output. They are ignored by default.
#show_authors = False

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# A list of ignored prefixes for module index sorting.
#modindex_common_prefix = []


# -- Options for HTML output ---------------------------------------------------

# The theme to use for HTML and HTML Help pages.  Major themes that come with
# Sphinx are currently 'default' and 'sphinxdoc'.
html_theme = 'default'
html_style = 'rtd.css'
html_context = {}

from fabric.api import local, hide, settings
with settings(hide('everything'), warn_only=True):
    get_tags = 'git tag | sort -r | egrep "(1\.[^0]+)\.."'
    tag_result = local(get_tags, True)
    if tag_result.succeeded:
        html_context['fabric_tags'] = tag_result.split()


# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
#html_theme_options = {}

# Add any paths that contain custom themes here, relative to this directory.
#html_theme_path = []

# The name for this set of Sphinx documents.  If None, it defaults to
# "<project> v<release> documentation".
#html_title = None

# A shorter title for the navigation bar.  Default is the same as html_title.
#html_short_title = None

# The name of an image file (relative to this directory) to place at the top
# of the sidebar.
#html_logo = None

# The name of an image file (within the static path) to use as favicon of the
# docs.  This file should be a Windows icon file (.ico) being 16x16 or 32x32
# pixels large.
#html_favicon = None

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# If not '', a 'Last updated on:' timestamp is inserted at every page bottom,
# using the given strftime format.
#html_last_updated_fmt = '%b %d, %Y'

# If true, SmartyPants will be used to convert quotes and dashes to
# typographically correct entities.
#html_use_smartypants = True

# Custom sidebar templates, maps document names to template names.
#html_sidebars = {}

# Additional templates that should be rendered to pages, maps page names to
# template names.
#html_additional_pages = {}

# If false, no module index is generated.
#html_use_modindex = True

# If false, no index is generated.
#html_use_index = True

# If true, the index is split into individual pages for each letter.
#html_split_index = False

# If true, links to the reST sources are added to the pages.
#html_show_sourcelink = True

# If true, an OpenSearch description file will be output, and all pages will
# contain a <link> tag referring to it.  The value of this option must be the
# base URL from which the finished HTML is served.
#html_use_opensearch = ''

# If nonempty, this is the file name suffix for HTML files (e.g. ".xhtml").
#html_file_suffix = ''

# Output file base name for HTML help builder.
htmlhelp_basename = 'Fabricdoc'


# -- Options for LaTeX output --------------------------------------------------

# The paper size ('letter' or 'a4').
#latex_paper_size = 'letter'

# The font size ('10pt', '11pt' or '12pt').
#latex_font_size = '10pt'

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title, author, documentclass [howto/manual]).
latex_documents = [
  ('index', 'Fabric.tex', u'Fabric Documentation',
   u'Jeff Forcier', 'manual'),
]

# The name of an image file (relative to this directory) to place at the top of
# the title page.
#latex_logo = None

# For "manual" documents, if this is true, then toplevel headings are parts,
# not chapters.
#latex_use_parts = False

# Additional stuff for the LaTeX preamble.
#latex_preamble = ''

# Documents to append as an appendix to all manuals.
#latex_appendices = []

# If false, no module index is generated.
#latex_use_modindex = True


# Restore decorated functions so that autodoc inspects the right arguments
def unwrap_decorated_functions():
    from fabric import operations, context_managers
    for module in [context_managers, operations]:
        for name, obj in vars(module).iteritems():
            if (
                # Only function objects - just in case some real object showed
                # up that had .undecorated
                isinstance(obj, types.FunctionType)
                # Has our .undecorated 'cache' of the real object
                and hasattr(obj, 'undecorated')
            ):
                setattr(module, name, obj.undecorated)

unwrap_decorated_functions()
