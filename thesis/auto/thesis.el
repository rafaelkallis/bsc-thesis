(TeX-add-style-hook
 "thesis"
 (lambda ()
   (TeX-add-to-alist 'LaTeX-provided-class-options
                     '(("scrartcl" "abstracton" "12pt")))
   (TeX-add-to-alist 'LaTeX-provided-package-options
                     '(("inputenc" "utf8") ("algorithm2e" "ruled" "vlined")))
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
    "framed"
    "algorithm2e"
    "caption"
    "subcaption"
    "cleveref"
    "soul")
   (LaTeX-add-labels
    "fig:architecture"
    "sec:wapi"
    "def:vol_count"
    "fig:unproductive_nodes"
    "fig:query_runtime_synthetic_millis"
    "fig:query_runtime_aem_millis"
    "fig:query_runtime_synthetic_updates"
    "fig:query_runtime_aem_updates"
    "fig:query_runtime"
    "fig:trav_nodes_synthetic_millis"
    "fig:trav_nodes_aem_millis"
    "fig:trav_nodes_synthetic_updates"
    "fig:trav_nodes_aem_updates"
    "fig:trav_node_density_synthetic_millis"
    "fig:trav_node_density_aem_millis"
    "fig:trav_node_density_synthetic_updates"
    "fig:trav_node_density_aem_updates")
   (LaTeX-add-environments
    "centerverbatim")
   (LaTeX-add-bibliographies)
   (LaTeX-add-amsthm-newtheorems
    "definition"
    "example"))
 :latex)

