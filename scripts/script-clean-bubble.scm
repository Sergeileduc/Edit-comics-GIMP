(define (script-fu-clean-bubble image drawable)

	;variable
	(let*	(
		(drawable (car (gimp-image-active-drawable image)))
			)


	;Prep
	(gimp-context-push)
	(gimp-image-undo-group-start image)

    ;Context
    (gimp-context-set-paint-mode LAYER-MODE-NORMAL)
    (gimp-context-set-opacity 100)


	; Enlève les trous (le lettrage VO) de la sélection
	(gimp-selection-flood image)

	;remplit la sélection avec la couleur de PP
	(if (= (car (gimp-selection-is-empty image)) FALSE)
		(begin
		(gimp-drawable-edit-fill drawable FILL-BACKGROUND)
		(gimp-selection-none image)
		);message d'erreur
		(gimp-message "Aucune sélection !!!\
Sélectionnez des bulles avec la baguette magique")
	)

	;Finish
	(gimp-displays-flush)
	(gimp-image-undo-group-end image)
	(gimp-context-pop)
	);end let
)

(script-fu-register "script-fu-clean-bubble"
"1) Clean bulle..."
"Clean la/les bulle(s) selectionnées avec la couleur AP\
....................\
Sélectionnez vos bulles en les sélectionnant avec la baguette magique avant de lancer le script"
"Sergeileduc"
"Sergeileduc"
"2018-08"
"RGB*"
SF-IMAGE "Input Image" 0
SF-DRAWABLE "Current Layer" 0
)

( script-fu-menu-register
	"script-fu-clean-bubble" "<Image>/DC-trad/")
