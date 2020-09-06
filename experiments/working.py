import os
import sys
import pdfkit
import misaka as m

version = "7.x"

brokenPages = []

pagesCount = 0

print(f"\nBuilding the Laravel version {version} docs!\n")

for filename in os.listdir('docs'):

    if filename.endswith(".md") and not filename.startswith('readme') and not filename.startswith('license'):

        print("Building Page: ", filename)

        path = os.path.join('docs', filename)

        md = open(path, 'r')

        try:

            md = md.read()

        except Exception:

            brokenPages.append(filename)

            print('Unable to build page: ', filename)

            continue

        html = m.html(md)

        html = '<!DOCTYPEhtml><htmllang="en"><head><metacharset="UTF-8"><metaname="viewport"content="width=device-width,initial-scale=1.0"><linkrel="stylesheet"href="laravel.css"><linkrel="stylesheet"href="tailwind.css"></head><body><div class="prose prose-xl">' + html + "</div></body></html>"

        options = {
            'page-size': 'Letter',
            'encoding': "UTF-8",
            'no-outline': None,
            'default-header': False,
            'header-left': f"Laravel {version} Documentation",
            'header-spacing': '5',
            'dpi': 600,
            'enable-internal-links': None,
            'header-center': filename.split('.')[0].title(),
            'load-media-error-handling': 'ignore',
            'quiet': ''
        }

        css = ['laravel.css', 'tailwind.css']

        if not os.path.exists(f"builds/{version}"):

            os.makedirs(f"builds/{version}/src")

            os.makedirs(f"builds/{version}/build")

        outputPath = f"builds/{version}/src/{filename.split('.')[0].lower()}.html"

        with open(outputPath, 'w') as document:

            try:
                document.write(str(html))
            except UnicodeEncodeError:
                brokenPages.append(filename)

                print('Unable to build page: ', filename)

                continue

        try:
            pdfkit.from_file(
                outputPath, f"builds/{version}/build/{filename.split('.')[0].lower()}.pdf", css=css, options=options)

            pagesCount = pagesCount + 1

        except Exception:

            brokenPages.append(filename)

            print("Unable to build: ", filename)

            continue

    else:

        continue

print(f"\nDone, built {pagesCount} pages!")

print(f"\nThere were issues building the following pages:")

for page in brokenPages:

    print("- ", page)
