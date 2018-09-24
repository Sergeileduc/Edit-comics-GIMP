;Script pour copier l'image originale dans un nouveau calque, au sommet, en non visible, et en vérouillé,
;de TOUTES les images ouvertes dans GIMP


(define (script-fu-clean-page-all seuil)
	;Prep
	(gimp-context-push)
	;On fixe le seuil de détection
	(gimp-context-set-sample-threshold-int seuil)

	(define images (vector->list (cadr (gimp-image-list))))
	(map script-fu-clean-page images)
	(gimp-displays-flush)

	;Finish
	(gimp-context-pop)
)

(script-fu-register "script-fu-clean-page-all"
"2) Cleaner toutes les images ouvertes..."
"Clean toutes les bulles de TOUTES les images ouvertes (de la couleur de l'AP)"
"Sergeileduc"
"Sergeileduc"
"2018-08"
"RGB*"
;SF-IMAGE "Input Image" 0
;SF-DRAWABLE "Current Layer" 0
SF-ADJUSTMENT "Seuil de tolérance à la couleur d'AP" '(0 0 5 1 1 0 0)
)

( script-fu-menu-register
	"script-fu-clean-page-all" "<Image>/DC-trad Traitement par lot/")
