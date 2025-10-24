(define (script-fu-clean-page image)

  ;variable
  (let*	(
    ;get-selected-layers renvoie une liste, car l'utilisateur peut
    ;sélectionner plusieurs layers. On prend donc le "car" de cette liste,
    ;pour ne garder qu'un élément (raw-layer)
    ;Ensuite, ce raw-layer est un vector. On le convertit en liste,
    ;et on en prend le car, pour enfin n'avoir qu'une valeur numérique. (layer)
    (raw-layer (car (gimp-image-get-selected-layers image)))
    (layer (car (vector->list raw-layer)))
      )
    ;Prep
    ;(gimp-context-push)
    (gimp-image-undo-group-start image)

    ;Context
    (gimp-context-set-paint-mode LAYER-MODE-NORMAL)
    (gimp-context-set-opacity 100)

    (gimp-image-select-color image CHANNEL-OP-REPLACE layer (car (gimp-context-get-background)))
    (gimp-selection-invert image)
    (gimp-selection-flood image)
    (gimp-image-select-color image CHANNEL-OP-INTERSECT layer (car (gimp-context-get-background)))

    ;Test si la sélection est vide
    (if (= (car (gimp-selection-is-empty image)) FALSE)
        (begin
            ;Enlève les trous la sélection
            (gimp-selection-flood image)
            (gimp-drawable-edit-fill layer FILL-BACKGROUND)
            (gimp-selection-none image)
            (gimp-displays-flush)
        );message d'erreur si selection vide
        (gimp-message "Aucune sélection !\
  Vérifiez la couleur d'arrière-plan ou utilisez des scripts avec un seuil plus grand (ou réglable)")
    );end if

    ;Finish
    (gimp-image-undo-group-end image)
    ;(gimp-context-pop)
  );end let
)

(script-fu-register "script-fu-clean-page"
"TEST) Clean page"
"Clean toutes les bulles de la page de la couleur de l'AP, en excluant les marges de l'algorithme."
  "Sergeileduc"	                   ; author
  "2018 Sergeileduc"               ; copyright notice
  "2025-10"                        ;date created
  "RGB* GRAY*"                     ; image types handled by script
  SF-IMAGE "Input Image" 0
  SF-DRAWABLE "Current Layer" 0
)
