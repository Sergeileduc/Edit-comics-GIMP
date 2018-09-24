(define (script-fu-clean-page-auto-0 image)

	;Prep
	(gimp-context-push)

	;On fixe le seuil de détection à 0
	(gimp-context-set-sample-threshold-int 0)

	;on lance le script clean page
	(script-fu-clean-page image)

	;Finish
	(gimp-context-pop)

);end define

;Gimp register
(script-fu-register
"script-fu-clean-page-auto-0"
"4) Clean page - Auto - seuil 0"
"Clean toutes les bulles de la page de la couleur de l'AP, en excluant les marges de l'algorithme.\
...................\
-Le seuil de tolérance à la couleur est fixée à 0.\
Utilisez les scripts avec d'autres seuils en cas de problème"
"Sergeileduc"
"Sergeileduc"
"2018-08"
"RGB*"
SF-IMAGE "Input Image" 0
)
;Gimp menu register
( script-fu-menu-register
	"script-fu-clean-page-auto-0" "<Image>/DC-trad/")
