### bibtex-misc: a repository allowing you to fix your bibtex references
I found that a lot of my references had issues from multiple Zotero exports and LaTeX projects.  When putting them into my thesis, I wanted to make sure that I was only including the references I was uing (rather than entire Zotero library).
This program allows you to use your .aux file generated in LaTeX to only select the citations that you actually used and pare down the BibTeX file.
Additionally, since I used IEEE format, I decided to add in a file with IEEE abbreviations to contribute towards journal name abbreviation.
Finally, there is a file that allows you to generate a "year" field from a "date" field.  A lot of style files aren't that flexible or easy to work with; this just uses a simple Pandas parsing to create a year field if it is missing in your BibTex entries but the date is present.

Good luck with your citation endeavors!
