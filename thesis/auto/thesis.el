(TeX-add-style-hook
 "thesis"
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
    "minted"
    "framed"
    "algorithm2e"
    "caption"
    "subcaption"
    "cleveref"
    "soul"
    "float"
    "wrapfig")
   (LaTeX-add-labels
    "fig:architecture"
    "sec:application_scenario"
    "sec:wapi"
    "ex:cas_query"
    "fig:hierarchical_db"
    "def:matching_node"
    "def:vol_count"
    "def:volatile_node"
    "ex:volatile_node"
    "fig:unproductive_nodes"
    "fig:query_runtime_synthetic"
    "fig:query_runtime_real"
    "fig:query_runtime"
    "fig:trav_nodes_synthetic"
    "fig:trav_nodes_real"
    "fig:trav_nodes"
    "fig:trav_node_ratio_synthetic"
    "fig:trav_node_ratio_real"
    "fig:trav_node_ratio"
    "algo:periodic_gc_wapi"
    "fig:periodic_gc"
    "fig:java_periodic_gc"
    "algo:query_qtp_wapi"
    "fig:qtp"
    "fig:java_qtp"
    "sec:experimental-evaluation"
    "fig:query_runtime_taus_synthetic"
    "fig:query_runtime_taus_real"
    "fig:tau_query_runtime_synthetic"
    "fig:tau_query_runtime_real"
    "fig:trav_unprod_nodes_taus_synthetic"
    "fig:trav_unprod_nodes_taus_real"
    "fig:tau_trav_unprod_nodes_synthetic"
    "fig:tau_trav_unprod_nodes_real"
    "fig:query_runtime_Ls_synthetic"
    "fig:query_runtime_Ls_real"
    "fig:L_query_runtime_synthetic"
    "fig:L_query_runtime_real"
    "fig:trav_unprod_nodes_Ls_synthetic"
    "fig:trav_unprod_nodes_Ls_real"
    "fig:L_trav_unprod_nodes_synthetic"
    "fig:L_trav_unprod_nodes_real"
    "fig:java_dfs"
    "fig:java_map"
    "fig:java_filter")
   (LaTeX-add-bibliographies)
   (LaTeX-add-amsthm-newtheorems
    "definition"
    "example"))
 :latex)

