(define (script-fu-clean-zone image drawable)

	;variable
	(let* (
		(drawable (car (gimp-image-active-drawable image))))

	;Prep
	(gimp-context-push)
	(gimp-image-undo-group-start image)

	;modifiez cette valeur (0 par défaut) si vous voulez un script avec un seuil plus tolérant
	(gimp-context-set-sample-threshold 0)

	;script
	(gimp-image-get-selection image)
	;(gimp-image-select-color image 3 drawable (car (gimp-context-get-backgroud)))
	(gimp-image-select-color image 3 (car (gimp-image-get-active-drawable image)) (car (gimp-context-get-background)))
	(gimp-selection-flood image)
	(gimp-drawable-edit-fill (car (gimp-image-get-active-drawable image)) FILL-BACKGROUND)

	;Finish
	(gimp-displays-flush)
	(gimp-selection-none image)
	(gimp-image-undo-group-end image)
	(gimp-context-pop)

);end let
)

(script-fu-register "script-fu-clean-zone"
	"<Image>/DCT-trad/3) Clean zone..."
	"Clean toutes les bulles de la zone avec la couleur de AP
	Veuillez d'abord sélectionner une zone (avec l'outil de sélection réctangulaire par exemple)
	Le seuil de tolérance à la couleur est de 0. Pour un seuil variable, utilisez le script 3b) Clean zone - seuil variable"
	"Sergeileduc"
	"Sergeileduc"
	"2018-06-28"
	"RGB*"
	SF-IMAGE "Input Image" 0
	SF-DRAWABLE "Current Layer" 0
)
