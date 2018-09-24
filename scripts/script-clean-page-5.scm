(define (script-fu-clean-page-auto-5 image)

	;Prep
	(gimp-context-push)

	;On fixe le seuil de détection à 5
	(gimp-context-set-sample-threshold-int 5)

	;on lance le script clean page
	(script-fu-clean-page image)

	;Finish
	(gimp-context-pop)
)

;Gimp register
(script-fu-register "script-fu-clean-page-auto-5"
"4) Clean page - Auto - seuil 5"
"Clean toutes les bulles de la page de la couleur de l'AP, en excluant les marges de l'algorithme.\
...................\
-Le seuil de tolérance à la couleur est fixée à 5.\
Utilisez les scripts avec d'autres seuils en cas de problème"
"Sergeileduc"
"Sergeileduc"
"2018-08"
"RGB*"
SF-IMAGE "Input Image" 0
)
;Gimp menu register
(script-fu-menu-register
	"script-fu-clean-page-auto-5" "<Image>/DC-trad/"
)
