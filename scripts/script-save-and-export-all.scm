(define (script-fu-save-xcfnjpeg-all)
  (let* ((i (car (gimp-image-list)))
         (image))
    (while (> i 0)
      (set! image (vector-ref (cadr (gimp-image-list)) (- i 1)))
      (python-save-to-edit RUN-NONINTERACTIVE
                      image)
      ;(gimp-image-clean-all image)
      (set! i (- i 1))
    );end while
  );end let
);end define

(script-fu-register "script-fu-save-xcfnjpeg-all"
"4) Sauver toutes les images ouvertes en .xcf ET en .jpeg..."
"Sauve toutes les images ouvertes en .xcf dans le dossier _XCF\n et en .jpeg dans le dossier _EDIT"
"Sergeileduc"
"Sergeileduc"
"2008-06-28"
"RGB*"
)

( script-fu-menu-register
	"script-fu-save-xcfnjpeg-all" "<Image>/DC-trad Traitement par lot/")
