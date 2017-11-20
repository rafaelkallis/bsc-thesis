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
    "def:matching_node"
    "fig:hierarchical_db"
    "def:vol_count"
    "def:volatile_node"
    "fig:unproductive_nodes"
    "fig:query_runtime_synthetic_updates"
    "fig:query_runtime_aem_updates"
    "fig:query_runtime"
    "fig:trav_nodes_synthetic_updates"
    "fig:trav_nodes_aem_updates"
    "fig:trav_node_density_synthetic_updates"
    "fig:trav_node_density_aem_updates"
    "fig:query_runtime_taus_synthetic"
    "fig:query_runtime_taus_aem"
    "fig:tau_query_runtime_synthetic"
    "fig:tau_query_runtime_aem"
    "fig:trav_unprod_nodes_taus_synthetic"
    "fig:trav_unprod_nodes_taus_aem"
    "fig:tau_unprod_nodes_synthetic"
    "fig:tau_unprod_nodes_aem"
    "fig:volatility_threshold"
    "fig:query_runtime_Ls_synthetic"
    "fig:query_runtime_Ls_aem"
    "fig:L_query_runtime_synthetic"
    "fig:L_query_runtime_aem"
    "fig:trav_unprod_nodes_Ls_synthetic"
    "fig:trav_unprod_nodes_Ls_aem"
    "fig:L_unprod_nodes_synthetic"
    "fig:L_unprod_nodes_aem"
    "fig:sliding_window_length")
   (LaTeX-add-environments
    "centerverbatim")
   (LaTeX-add-bibliographies)
   (LaTeX-add-amsthm-newtheorems
    "definition"
    "example"))
 :latex)

