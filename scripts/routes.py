"""
# Scripts / Routes

Use PDoc to generate documentation on available routes.

## Usage

* `python scripts/routes.py`: Generate documentation and run a live server. No
  data is written to the disk. The server runs until you kill it with `Ctrl+C`.

* `python scripts/routes.py [directory]`: Generate documentation and save it to
  the given directory. If the directory already exists, it will only be
  overwritten if it contains a `.ensemble_docs` file. Otherwise the script
  fails.
"""
import sys
from pathlib import Path
from pdoc import pdoc, render  # type: ignore
from pdoc.web import DocServer, open_browser


render.configure(
    docformat='markdown',
    footer_text='Ensemble Forum Routes',
    show_source=False,
    # template_directory=Path('./resources/pdoc_templates'),
)

if len(sys.argv) == 1:
    server = DocServer(('localhost', 8080), ['request'])
    with server:
        url = f'http://localhost:{server.server_port}'
        print(f'pdoc server ready at {url}')
        open_browser(url)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print('\nGoodbye!')
            server.server_close()

elif len(sys.argv) == 2:
    out_dir = Path(sys.argv[1])
    if out_dir.exists():
        # Only continue if a `.ensemble_docs` file exists
        if not out_dir.joinpath('.ensemble_docs').exists():
            print(
                "ERROR: Performing this action would overwrite existing data "
                "on the disk. To silence this error, create a "
                "`.ensemble_docs` file in the desired directory."
            )
            sys.exit(1)

    # Now run pdoc
    pdoc(
        'request',
        output_directory=out_dir
    )
    # And create a .ensemble_docs file there so it can be overwritten easily
    open(out_dir.joinpath('.ensemble_docs'), "w").close()
    with open(out_dir.joinpath('.gitignore'), "w") as f:
        f.write('*')
