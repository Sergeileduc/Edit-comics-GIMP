; To use this script, make sure that the selected layer is the one that you want to outline


;Create selection
(define (create-selection-flood image layer thickness feather)
	(gimp-image-select-item image CHANNEL-OP-REPLACE layer)
	(gimp-selection-grow image thickness)
	(gimp-selection-flood image)
	(if (> feather 0) (gimp-selection-feather image feather))
);end define

;Fill selection with colour
(define (fill-selection image layer colour)
	;définit la couleur de premier plan
	(gimp-context-set-foreground colour)
	(if (= (car (gimp-selection-is-empty image)) FALSE)
		(gimp-drawable-edit-fill layer FILL-FOREGROUND)
	);end if
	(gimp-selection-none image)
);end define

; our script
(define (script-fu-double-bordure
	image
	drawable
	first-flag
	colour-1
	thickness-1
	feather-1
	second-flag
	colour-2
	thickness-2
	feather-2)

	;Prep
	(gimp-context-push)
	(gimp-image-undo-group-start image)

	;variable
	(let*	(
		(offset 100)
		(drawable (car (gimp-image-active-drawable image)))
		(layer (car (gimp-image-get-active-layer image)))
		(layer-1 0)
		(layer-2 0)
		(pos (car (gimp-image-get-item-position image layer)))
		(width (+ (car (gimp-drawable-width drawable)) (* 2 offset)))
        (height (+ (car (gimp-drawable-height drawable))(* 2 offset)))
		(old-x (car (gimp-drawable-offsets layer)))
		(old-y (car (cdr (gimp-drawable-offsets layer))))
		(x-coord (- old-x offset))
		(y-coord (- old-y offset))
		(name (car (gimp-drawable-get-name drawable)))
		(group (car (gimp-layer-group-new image)))
	)

	;Creer le groupe de calques
	(set! group (car (gimp-layer-group-new image)))
	(gimp-item-set-name group name)
	(gimp-image-insert-layer image group 0 (+ pos 1))
	(gimp-image-reorder-item image layer group 0)


	;Creer la première bordure
	(if (= first-flag TRUE)
		(begin
		(set! layer-1 (car (gimp-layer-new image width height RGBA-IMAGE "1ere Bordure" 100 NORMAL-MODE)))
		(gimp-image-insert-layer image layer-1 group 1)
		(gimp-layer-translate layer-1 x-coord y-coord)
		(create-selection-flood image layer thickness-1 feather-1)
		(fill-selection image layer-1 colour-1)
		)
	)

	;Creer la deuxième bordure
	(if (= second-flag TRUE)
		(begin
		(set! layer-2 (car (gimp-layer-new image width height RGBA-IMAGE "2eme Bordure" 100 NORMAL-MODE)))
		(gimp-image-insert-layer image layer-2 group 2)
		(gimp-layer-translate layer-2 x-coord y-coord)
		(create-selection-flood image layer (+ thickness-1 thickness-2) feather-2)
		(fill-selection image layer-2 colour-2)
		)
	)


	;Groupe actif
	(if (or first-flag shadow-border)
		(gimp-image-set-active-layer image group)
	)

	;Finish
	(gimp-displays-flush)
	(gimp-image-undo-group-end image)
	(gimp-context-pop)

	);end let
);end define

;This is the plugin registration function
(script-fu-register "script-fu-double-bordure"
	"Double bordure"
	"Dessine une double bordure pour le calque ou le texte actif"
	"Sergeileduc"
	"Sergeileduc"
	"2018-10"
	"*"
	SF-IMAGE "Input Image" 0
	SF-DRAWABLE "Current Layer" 0
	SF-TOGGLE "Première bordure" TRUE
	SF-COLOR "Couleur" '(255 255 255)
	SF-ADJUSTMENT "Epaisseur" '(10 0 50 1 10 0 0)
	SF-ADJUSTMENT "Adoucissement" '(2 0 20 1 10 0 0)
	SF-TOGGLE "Deuxième bordure" TRUE
	SF-COLOR "Couleur" '(0 0 0)
	SF-ADJUSTMENT "Epaisseur" '(2 0 50 1 10 0 0)
	SF-ADJUSTMENT "Adoucissement" '(2 0 20 1 10 0 0)
	)

(script-fu-menu-register
	"script-fu-double-bordure" "<Image>/DC-trad/")
