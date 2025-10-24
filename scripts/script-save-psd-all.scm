;Script pour enregistrer dans le dossier _PSD
;de TOUTES les images ouvertes dans GIMP

(define (script-fu-save-psd-all)
  (let* ((images (vector->list (car (gimp-get-images)))))
    (for-each
      (lambda (img)
        (python-fu-save-to-psd RUN-NONINTERACTIVE img))
      images
    )
  );end let
);end define

(script-fu-register "script-fu-save-psd-all"
"5) [PHOTOSHOP] Sauver toutes les images ouvertes en projets .psd"
"Sauve toutes les images ouvertes en .psd dans le dossier _PSD"
  "Sergeileduc"	                   ; author
  "2018 Sergeileduc"               ; copyright notice
  "2025-10"                        ;date created
  "RGB* GRAY*"                     ; image types handled by script
)

(script-fu-menu-register
  "script-fu-save-psd-all" "<Image>/DC-trad Traitement par lot/")
