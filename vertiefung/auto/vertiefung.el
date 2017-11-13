(TeX-add-style-hook
 "vertiefung"
 (lambda ()
   (TeX-add-to-alist 'LaTeX-provided-class-options
                     '(("scrartcl" "abstracton" "12pt")))
   (TeX-add-to-alist 'LaTeX-provided-package-options
                     '(("inputenc" "utf8") ("algorithm2e" "ruled" "vlined")))
   (add-to-list 'LaTeX-verbatim-environments-local "minted")
   (add-to-list 'LaTeX-verbatim-environments-local "lstlisting")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "lstinline")
   (add-to-list 'LaTeX-verbatim-macros-with-delims-local "lstinline")
   (TeX-run-style-hooks
    "latex2e"
    "scrartcl"
    "scrartcl12"
    "inputenc"
    "fancyhdr"
    "graphicx"
    "tikz"
    "listings"
    "amssymb"
    "amsfonts"
    "amsmath"
    "amsthm"
    "pdfpages"
    "forest"
    "multicol"
    "varwidth"
    "verbatim"
    "cleveref"
    "minted"
    "framed"
    "algorithm2e"
    "caption"
    "subcaption"
    "soul")
   (TeX-add-symbols
    "bbbr"
    "bbbm"
    "bbbn"
    "bbbz")
   (LaTeX-add-labels
    "fig:architecture"
    "sec:wapi"
    "algo:add_triple_wapi"
    "fig:add_wapi"
    "algo:query_wapi"
    "fig:cas_query"
    "fig:remove_wapi"
    "algo:remove_triple_wapi"
    "sec:volatility"
    "def:vol_count"
    "fig:vol_example"
    "sec:implementation"
    "fig:json_simple"
    "fig:is_volatile"
    "ex:split_doc"
    "fig:split_document"
    "fig:split_doc_mongo"
    "fig:split_doc_debug"
    "fig:helper^functions")
   (LaTeX-add-environments
    "centerverbatim")
   (LaTeX-add-bibliographies)
   (LaTeX-add-amsthm-newtheorems
    "definition"
    "example"))
 :latex)

