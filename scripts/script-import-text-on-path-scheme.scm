(define (script-fu-import-text-on-path
          image drawable
          source-path
          page-index
          font
          font-size
          font-color
          justification-index
          line-spacing
          letter-spacing)

  ;; Appelle ton plugin Python via son nom PDB
  (sl-gimp-import-text-on-path
    RUN-NONINTERACTIVE
    image
    drawable
    source-path
    page-index
    font
    font-size
    font-color
    justification-index
    line-spacing
    letter-spacing))

(script-fu-register
  "script-fu-import-text-on-path"
  "Importe le texte"
  "Importe le texte depuis un fichier et le place le long d'un chemin"
  "Sergeileduc"
  "2025 Sergeileduc"
  "2025-11"                        ;date created
  "RGB*, GRAY*"
  SF-IMAGE "Image" 0
  SF-DRAWABLE "Calque" 0
;   SF-FILE "Fichier texte" ""
;   SF-SPINNER "Numéro de page" 1 1 50 1
  SF-FONT "Police" "Sans"
;   SF-SPINNER "Taille de police" 27 1 200 1
  SF-COLOR "Couleur texte" '(0 0 0)
;   SF-OPTION "Justification" 2 '("Gauche" "Centre" "Droite" "Justifié")
;   SF-ADJUSTMENT "Espacement lignes" 0.0 -200.0 200.0 0.1 1 0
;   SF-ADJUSTMENT "Espacement lettres" 0.0 -200.0 200.0 0.1 1 0
)

(script-fu-menu-register "script-fu-import-text-on-path" "<Image>/DC-trad/")
