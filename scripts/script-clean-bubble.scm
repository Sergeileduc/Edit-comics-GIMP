#!/usr/bin/env gimp-script-fu-interpreter-3.0
;!# Close comment started on first line. Needed by gettext.

(define (script-fu-clean-bubble image drawable)

  ;Prep
  (gimp-context-push)
  (gimp-image-undo-group-start image)

  ;Context
  (gimp-context-set-paint-mode LAYER-MODE-NORMAL)
  (gimp-context-set-opacity 100)


  ; Enlève les trous (le lettrage VO) de la sélection
  (gimp-selection-flood image)

  ;remplit la sélection avec la couleur de PP
  (if (= (car (gimp-selection-is-empty image)) FALSE)
      (begin
      (gimp-drawable-edit-fill drawable FILL-BACKGROUND)
      (gimp-selection-none image)
      );message d'erreur
      (gimp-message "Aucune sélection !!!\
  Sélectionnez des bulles avec la baguette magique")
  )

    ;Finish
    (gimp-displays-flush)
    (gimp-image-undo-group-end image)
    (gimp-context-pop)
)

(script-fu-register "script-fu-clean-bubble"
"1) Clean bulle..."
"Clean la/les bulle(s) selectionnées avec la couleur AP\
....................\
Sélectionnez vos bulles en les sélectionnant avec la baguette magique avant de lancer le script"
  "Sergeileduc"	                   ; author
  "2018 Sergeileduc"               ; copyright notice
  "2025-10"                        ;date created
  "RGB* GRAY*"                     ; image types handled by script
SF-IMAGE "Input Image" 0
SF-DRAWABLE "Current Layer" 0
)

(script-fu-menu-register
  "script-fu-clean-bubble" "<Image>/DC-trad/")
