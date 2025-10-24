;Script pour enregistrer dans le dossier _XCF
;de TOUTES les images ouvertes dans GIMP


(define (script-fu-save-xcf-all)
  (let* ((images (vector->list (car (gimp-get-images)))))
    (for-each
      (lambda (img)
        (python-fu-save-to-xcf RUN-NONINTERACTIVE img))
      images
    )
  );end let
);end define

(script-fu-register "script-fu-save-xcf-all"
"3) Sauver toutes les images ouvertes en .xcf..."
"Sauve toutes les images ouvertes en .xcf dans le dossier _XCF"
  "Sergeileduc"	                   ; author
  "2018 Sergeileduc"               ; copyright notice
  "2025-10"                        ;date created
  "RGB* GRAY*"                     ; image types handled by script
)

(script-fu-menu-register
    "script-fu-save-xcf-all" "<Image>/DC-trad Traitement par lot/")
