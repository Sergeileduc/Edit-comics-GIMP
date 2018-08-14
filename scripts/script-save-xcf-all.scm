(define (script-fu-save-xcf-all)
  (let* ((i (car (gimp-image-list)))
         (image))
    (while (> i 0)
      (set! image (vector-ref (cadr (gimp-image-list)) (- i 1)))
      (python-save-to-xcf RUN-NONINTERACTIVE
                      image)
      ;(gimp-image-clean-all image)
      (set! i (- i 1))
    );end while
  );end let
);end define

(script-fu-register "script-fu-save-xcf-all"
"3) Sauver toutes les images ouvertes en .xcf..."
"Sauve toutes les images ouvertes en .xcf dans le dossier _XCF"
"Sergeileduc"
"Sergeileduc"
"2008-06-28"
"RGB*"
)

( script-fu-menu-register
	"script-fu-save-xcf-all" "<Image>/DC-trad Traitement par lot/")
