(define (script-fu-clean-zone-seuil-variable image drawable seuil)

	;variable
	(let* (
		(drawable (car (gimp-image-active-drawable image)))
		)

	;Prep
	(gimp-context-push)
	(gimp-image-undo-group-start image)
	(gimp-context-set-sample-threshold-int seuil)

	;script
	(gimp-image-get-selection image)
	;(gimp-image-select-color image 3 drawable (car (gimp-context-get-background)))
	(gimp-image-select-color image 3 (car (gimp-image-get-active-drawable image)) (car (gimp-context-get-background)))
	(gimp-selection-flood image)
	(gimp-drawable-edit-fill (car (gimp-image-get-active-drawable image)) FILL-BACKGROUND)

	;Finish
	(gimp-displays-flush)
	(gimp-selection-none image)
	(gimp-image-undo-group-end image)
	(gimp-context-pop)

))

(script-fu-register "script-fu-clean-zone-seuil-variable"
	"<Image>/DCT-trad/3b) Clean zone - seuil variable"
	"Clean toutes les bulles de la zone avec la couleur de AP
	Veuillez d'abord sélectionner une zone \(avec l'outil de sélection réctangulaire par exemple\)
	Le seuil de tolérance à la couleur est variable"
	"Sergeileduc"
	"Sergeileduc"
	"2018-06-28"
	"RGB*"
	SF-IMAGE "Input Image" 0
	SF-DRAWABLE "Current Layer" 0
	SF-ADJUSTMENT "seuil de tolérance à la couleur \(pour le blanc cassé par exemple\)" '(5 0 30 1 10 0 0)
)
