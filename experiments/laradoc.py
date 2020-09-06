import os
import sys
import pdfkit
import misaka as m

version = "7.x"

brokenPages = []

pagesCount = 0

allHTMLBits = []

print(f"\nBuilding the Laravel version {version} docs!\n")

for filename in os.listdir('docs'):

    if filename.endswith(".md") and not filename.startswith('readme') and not filename.startswith('license'):

        print("Building Page: ", filename)

        path = os.path.join('docs', filename)

        md = open(path, 'r')

        try:

            md = md.read()

            pagesCount = pagesCount + 1

        except Exception:

            brokenPages.append(filename)

            print('Unable to build page: ', filename)

            continue

        html = m.html(md)

        html = html + '<div style="page-break-after: always;" ></div>'

        allHTMLBits.append(html)

print(f"\nDone compiling markdown, built {pagesCount} pages!")

print(f"\nThere were issues building the following pages:")

for page in brokenPages:

    print("- ", page)

html = "".join(allHTMLBits)

html = '<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0"><link rel="stylesheet" href="tailwind.css"></head><body><div class="prose">' + html + "</div></body></html>"

with open(f"builds/{version}/final.html", 'w') as result:
    result.write(html)

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

pdfkit.from_file(
    f"builds/{version}/final.html", f"builds/{version}/laravel-{version}-documentation.pdf", options=options)

print("\nDone! The final PDF can be found here: ",
      f"builds/{version}/laravel-{version}-documentation.pdf")
