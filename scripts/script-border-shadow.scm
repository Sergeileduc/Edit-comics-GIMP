; To use this script, make sure that the selected layer is the one that you want to outline


;Create selection
(define (create-selection image layer thickness feather)
	(gimp-image-select-item image CHANNEL-OP-REPLACE layer)
	(if (> thickness 0)(gimp-selection-grow image thickness))
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
(define (script-fu-add-text-outline
									image
									drawable
									flag-border
									colour-border
									thickness-border
									feather-border
									flag-shadow
									colour-shadow
									thickness-shadow
									feather-shadow
									shadow-offset-x
									shadow-offset-y)

	;Prep
	(gimp-context-push)
	(gimp-image-undo-group-start image)

	;variable
	(let*	(
		(offset 100)
		(drawable (car (gimp-image-get-active-drawable image)))
		(layer (car (gimp-image-get-active-layer image)))
		(border-layer 0)
		(shadow-layer 0)
		(pos (car (gimp-image-get-item-position image layer)))
		(width (+ (car (gimp-drawable-width drawable)) (* 2 offset)))
        (height (+ (car (gimp-drawable-height drawable))(* 2 offset)))
		(old-x (car (gimp-drawable-offsets layer)))
		(old-y (car (cdr (gimp-drawable-offsets layer))))
		(x-coord (- old-x offset))
		(y-coord (- old-y offset))
		(name (car (gimp-item-get-name drawable)))
		(group (car (gimp-layer-group-new image)))
			)

	;Creer le groupe de calques
	(if (or flag-border flag-shadow)
		(begin
		(set! group (car (gimp-layer-group-new image)))
		(gimp-item-set-name group name)
		(gimp-image-insert-layer image group 0 (+ pos 1))
		(gimp-image-reorder-item image layer group 0)
		)
	)

	;Creer une bordure autour du texte
	(if (= flag-border TRUE)
		(begin
		(set! border-layer (car (gimp-layer-new image width height RGBA-IMAGE "Bordure" 100 LAYER-MODE-NORMAL)))
		(gimp-image-insert-layer image border-layer group 1)
		(gimp-item-transform-translate border-layer x-coord y-coord)
		(create-selection image layer thickness-border feather-border)
		(fill-selection image border-layer colour-border)
		)
	)

	;Creer une ombre du texte
	(if (= flag-shadow TRUE)
		(begin
		(set! shadow-layer (car (gimp-layer-new image width height RGBA-IMAGE "Ombre" 100 LAYER-MODE-NORMAL)))
		(gimp-image-insert-layer image shadow-layer group 2)
		(gimp-item-transform-translate shadow-layer x-coord y-coord)
		(create-selection image layer thickness-shadow feather-shadow)
		(fill-selection image shadow-layer colour-shadow)
		(gimp-item-transform-translate shadow-layer shadow-offset-x shadow-offset-y)
		)
	)



	;Groupe actif
	(if (or flag-border shadow-border)
		(gimp-image-set-active-layer image group)
	)

	;Finish
	(gimp-displays-flush)
	(gimp-image-undo-group-end image)
	(gimp-context-pop)

	);end let
);end define
;This is the plugin registration function
(script-fu-register "script-fu-add-text-outline"
	"Bordures et ombres"
	"Dessine une bordure et/ou une ombre pour le calque ou le texte actif"
	"Sergeileduc"
	"Sergeileduc"
	"2018-08"
	"*"
	SF-IMAGE "Input Image" 0
	SF-DRAWABLE "Current Layer" 0
	SF-TOGGLE "Appliquer une bordure ?" TRUE
	SF-COLOR "Couleur" '(0 0 0)
	SF-ADJUSTMENT "Epaisseur" '(2 0 20 1 10 0 0)
	SF-ADJUSTMENT "Fondu/flou" '(2 0 20 1 10 0 0)
	SF-TOGGLE "Appliquer une ombre ?" FALSE
	SF-COLOR "Couleur" '(0 0 0)
	SF-ADJUSTMENT "Epaisseur" '(2 0 20 1 10 0 0)
	SF-ADJUSTMENT "Fondu/flou" '(2 0 20 1 10 0 0)
	SF-ADJUSTMENT "Décalage en x (positif vers la droite, négatif vers la gauche" '(-5 -50 50 1 10 0 0)
	SF-ADJUSTMENT "Décalage en y (positif vers le bas, négatif vers le haut" '(5 -50 50 1 10 0 0)
	)

( script-fu-menu-register
	"script-fu-add-text-outline" "<Image>/DC-trad/")
