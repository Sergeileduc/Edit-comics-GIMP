;Script pour copier l'image originale dans un nouveau calque, au sommet, en non visible, et en vérouillé.

(define (script-fu-copy-layer image)
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
    (gimp-context-push)
    (gimp-image-undo-group-start image)

    ;Resolution
    ; (gimp-image-set-resolution image 72 72)

    ;SCRIPT
    (gimp-item-set-name layer "Edit")
    (define new-layer (car (gimp-layer-copy layer)))
    (gimp-image-insert-layer image new-layer 0 0)
    (gimp-item-set-name new-layer "Original")
    (gimp-image-set-selected-layers image (vector layer))
    (gimp-item-set-lock-position layer TRUE)
    (gimp-item-set-lock-position new-layer TRUE)
    (gimp-item-set-lock-content new-layer TRUE)
    (gimp-item-set-visible new-layer FALSE)
    ;Finish
    (gimp-displays-flush)
    (gimp-image-undo-group-end image)
    (gimp-context-pop)
  );end let
)


(script-fu-register "script-fu-copy-layer"
"0) Dupliquer le calque image pour garder l'original..."
"Duplique le calque image, pour avoir un calque de travail \"Edit\" et une calque de reference \#Original\"\
Le script verouille les calques en deplacement, et verouille le calque original pour le rendre non modifiable"
  "Sergeileduc"	                   ; author
  "2018 Sergeileduc"               ; copyright notice
  "2025-10"                        ;date created
  "RGB* GRAY*"                     ; image types handled by script
  SF-IMAGE "Input Image" 0
  SF-DRAWABLE "Current Layer" 0
)

(script-fu-menu-register
  "script-fu-copy-layer" "<Image>/DC-trad/")
