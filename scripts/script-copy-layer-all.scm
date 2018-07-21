;Script pour copier l'image originale dans un nouveau calque, au sommet, en non visible, et en vérouillé,
;de TOUTES les images ouvertes dans GIMP


(define (script-fu-copy-layer-all)
  (define images (vector->list (cadr (gimp-image-list))))
  (map script-fu-copy-layer images)
  (gimp-displays-flush)
)

(script-fu-register "script-fu-copy-layer-all"
"1) Dupliquer toutes les images ouvertes garder l'original..."
"Duplique le calque de TOUTES les images ouvertes, pour avoir un calque de travail \"Edit\" et une calque de reference \#Original\"\
Le script verouille les calques en deplacement, et verouille le calque original pour le rendre non modifiable"
"Sergeileduc"
"Sergeileduc"
"2008-06-28"
"RGB*"
;SF-IMAGE "Input Image" 0
;SF-DRAWABLE "Current Layer" 0
)

( script-fu-menu-register
	"script-fu-copy-layer-all" "<Image>/DC-trad Traitement par lot/")
