;Script pour enregistrer dans le dossier _XCF et _EDIT
;TOUTES les images ouvertes dans GIMP

(define (script-fu-save-xcfnjpeg-all)
  (let* ((images (vector->list (car (gimp-get-images)))))
    (for-each
      (lambda (img)
        (python-fu-save-to-edit RUN-NONINTERACTIVE img))
      images
    )
  );end let
);end define

(script-fu-register "script-fu-save-xcfnjpeg-all"
"4) Sauver toutes les images ouvertes en .xcf ET en .jpeg..."
"Sauve toutes les images ouvertes en .xcf dans le dossier _XCF\n et en .jpeg dans le dossier _EDIT"
  "Sergeileduc"	                   ; author
  "2018 Sergeileduc"               ; copyright notice
  "2025-10"                        ;date created
  "RGB* GRAY*"                     ; image types handled by script
)

(script-fu-menu-register
  "script-fu-save-xcfnjpeg-all" "<Image>/DC-trad Traitement par lot/")
