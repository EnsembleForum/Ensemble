
# Integration Tooling

We also added some tools to make it easier to develop integration between the
backend and the frontend. The main one was a documentation server built using
[Pdoc](https://github.com/mitmproxy/pdoc), which allowed us to write
documentation for all of our API routes using Python docstrings. You can view
this documentation by running the script `python scripts/routes.py`. This tool
made it much easier for our frontend team to develop the frontend confidently
without as much assistance, meaning that the backend team could focus on
implementing more functionality for the backend.
