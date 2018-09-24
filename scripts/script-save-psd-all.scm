(define (script-fu-save-psd-all)
  (let* ((i (car (gimp-image-list)))
         (image))
    (while (> i 0)
      (set! image (vector-ref (cadr (gimp-image-list)) (- i 1)))
      (python-save-to-psd RUN-NONINTERACTIVE
                      image)
      ;(gimp-image-clean-all image)
      (set! i (- i 1))
    );end while
  );end let
);end define

(script-fu-register "script-fu-save-psd-all"
"5) [PHOTOSHOP] Sauver toutes les images ouvertes en projets .psd"
"Sauve toutes les images ouvertes en .psd dans le dossier _PSD"
"Sergeileduc"
"Sergeileduc"
"2018-09-20"
"RGB*"
)

( script-fu-menu-register
	"script-fu-save-psd-all" "<Image>/DC-trad Traitement par lot/")
