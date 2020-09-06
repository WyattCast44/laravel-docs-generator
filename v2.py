import os
import sys
import pdfkit
import subprocess
from subprocess import Popen, PIPE
import misaka as m
from pygments import highlight
from pygments.formatters import HtmlFormatter, ClassNotFound
from pygments.lexers import get_lexer_by_name, guess_lexer


class HighlighterRenderer(m.HtmlRenderer):

    def blockcode(self, text, lang):

        lexer = get_lexer_by_name('Javascript+Php')

        formatter = HtmlFormatter()

        return highlight(text, lexer, formatter)


def promptVersion(version='7.x'):

    versions = [
        'master',
        '8.x',
        '7.x',
        '6.x',
        '5.8',
        '5.7',
        '5.6',
        '5.5',
        '5.4',
        '5.3',
        '5.2',
        '5.1',
        '5.0',
        '4.2',
    ]

    print(
        f"\nWhat version of the docs would you like to build? (default = {version})")
    print("\nAvailable Versions:", versions, "\n")

    choice = input('> ')

    if not choice in versions and choice != "":

        print("\nYou must select from the available versions.")
        quit()

    return choice if choice != "" else version


def promptSource(source='markdown'):

    sources = [
        'markdown',
        'laravel.com'
    ]

    print(
        f"\nWhat source of the docs would you like to build? (default = {source})")
    print("\nAvailable Sources:", sources, "\n")

    choice = input('> ')

    if not choice in sources and choice != "":

        print("\nYou must select from the available sources.")
        quit()

    return choice if choice != "" else source


def changeDocsBranch(branch):

    cwd = os.getcwd()

    os.chdir('docs')

    print("\n==> Switching branch to version: ", branch, "\n")
    subprocess.Popen(["git", "checkout", branch],
                     stdout=subprocess.PIPE).wait()

    print("\n==> Pulling down the lastest changes\n")
    subprocess.Popen(["git", "pull"], stdout=subprocess.PIPE).wait()

    os.chdir(cwd)


sections = [
    'Prologue',
    'Getting Started',
    'Architecture Concepts',
    'The Basics',
    'Frontend',
    'Security',
    'Digging Deeper',
    'Database',
    'Eloquent ORM',
    'Testing',
    'Official Packages'
]


def buildMarkdownDocs():

    pagesCount = 0

    allHTMLBits = []

    brokenPages = []

    markdownCompiler = m.Markdown(
        HighlighterRenderer(), extensions=('fenced-code',))

    print("==> Compiling Markdown Pages\n")

    for filename in os.listdir('docs'):

        if filename.endswith(".md") and not filename.startswith('readme') and not filename.startswith('license'):

            print("Building Page:", filename)

            path = os.path.join('docs', filename)

            markdownFile = open(path, 'r')

            try:

                markdown = markdownFile.read()

                markdownFile.close()

                pagesCount = pagesCount + 1

            except Exception:

                brokenPages.append(filename)

                print('Unable to Build Page:', filename)

                continue

            html = markdownCompiler(markdown)

            # Add a page break between pages
            html = html + '<div style="page-break-after: always;" ></div>'

            allHTMLBits.append(html)

            continue

        else:

            continue

    html = "".join(allHTMLBits)

    try:

        path = os.path.join('docs', 'license.md')

        licenseFile = open(path, 'r')

        content = licenseFile.read()

        licenseFile.close()

        pagesCount = pagesCount + 1

        content = markdownCompiler(
            content) + '<div style="page-break-after: always;" ></div>'

        html = content + html

    except Exception:

        pass

    html = '<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0"><link rel="stylesheet" href="resources/code.css"><link rel="stylesheet" href="resources/tailwind.css"></head><body><div class="prose prose-xl mx-auto my-10">' + html + "</div></body></html>"

    print(f"\nCompiled {pagesCount} markdown pages!")

    if brokenPages != []:

        print(f"\nThe following pages were skipped due to errors compiling:\n")

        for page in brokenPages:

            print(f"- ", page)

    return html


def saveHtmlToFile(html, filename):

    with open(filename, 'w') as handler:

        handler.write(html)

    return True


def convertHtmlFileToPDF(path):

    print("\nCoverting the final HTML document info a PDF")

    options = {
        'page-size': 'Letter',
        'encoding': "UTF-8",
        'no-outline': None,
        'default-header': False,
        'header-left': f"Laravel {version} Documentation",
        'header-spacing': '5',
        'dpi': 600,
        'enable-internal-links': None,
        'load-media-error-handling': 'skip',
        'quiet': '',
        'enable-local-file-access': '',
    }

    try:
        pdfkit.from_file(
            path, path.replace('.html', '.pdf'), options=options)

    except OSError:

        pass

    print("\nDone! The final PDF can be found here:",
          path.replace('.html', '.pdf'))


source = promptSource()
version = promptVersion()

if source == 'markdown':

    changeDocsBranch(version)
    html = buildMarkdownDocs()
    saveHtmlToFile(html, f"laravel-{version}-documentation-markdown.html")
    convertHtmlFileToPDF(f"laravel-{version}-documentation-markdown.html")
