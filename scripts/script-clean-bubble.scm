(define (script-fu-clean-bubble image drawable)

	;variable
	(let* (
		(drawable (car (gimp-image-active-drawable image)))
		)


	;Prep
	(gimp-context-push)
	(gimp-image-undo-group-start image)

	; Enlève les trous (le lettrage VO) de la sélection
	(gimp-selection-flood image)

	;remplit la sélection avec la couleur de PP
	(gimp-drawable-edit-fill drawable FILL-BACKGROUND)

	;Finish
	(gimp-displays-flush)
	(gimp-selection-none image)
	(gimp-image-undo-group-end image)
	(gimp-context-pop)
	);end let
	)

(script-fu-register "script-fu-clean-bubble"
	"<Image>/DCT-trad/1) Clean bulle..."
	"Clean la/les bulle(s) selectionnées avec la couleur AP
	Sélectionnez vos bulles en les sélectionnant avec la baguette magique avant de lancer le script"
	"Sergeileduc"
	"Sergeileduc"
	"2008-06-28"
	"RGB*"
	SF-IMAGE "Input Image" 0
	SF-DRAWABLE "Current Layer" 0
)
