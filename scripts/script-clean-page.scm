(define (script-fu-clean-page image drawable marge_w marge_h)
 ( let*
		(
		(drawable (car (gimp-image-active-drawable image)))
		(imageWidth (car (gimp-image-width image))) ;largeur de l'image
		(imageHeight (car (gimp-image-height image))) ;hauteur de l'image
		)

	;Prep
	(gimp-context-push)
	(gimp-image-undo-group-start image)
	
	;modifiez cette valeur (0 par défaut) si vous voulez un script avec un seuil plus tolérant
	(gimp-context-set-sample-threshold 0)

    ;Sélectionner le centre de la page (sans les marges)
	(gimp-image-select-rectangle image 2 marge_w marge_h (- imageWidth (* 2 marge_w)) (- imageHeight (* 2 marge_h)))
  
	;Sélection par couleur, dans la zone sans les marges (par intersection)
	(gimp-image-select-color image 3 drawable (car (gimp-context-get-background)))
	
	;Enlève les trous la sélection
	(gimp-selection-flood image)

	;Remplit la sélection de noir (couleur d'avant-plan)
	(gimp-drawable-edit-fill drawable FILL-BACKGROUND)
	
	; Déselectionne tout
	;(gimp-selection-none image)
	
	;test
	(gimp-image-select-rectangle image 2 marge_w marge_h (- imageWidth (* 2 marge_w)) (- imageHeight (* 2 marge_h)))
	(gimp-displays-flush)

	;Finish
	(gimp-image-undo-group-end image)
	(gimp-context-pop)
))

(script-fu-register "script-fu-clean-page"
		    "<Image>/DCT-trad/4) Clean page..."
		    "Clean toutes les bulles de la page de la couleur de l'AP, en excluant les marges de l'algorithme.
			Le seuil de tolérance à la couleur est de 0. Pour un seuil variable, utilisez le script 4b) Clean page - seuil variable"
		    "Sergeileduc"
		    "Sergeileduc"
		    "2008-06-28"
		    "RGB*"
		    SF-IMAGE "Input Image" 0
			SF-DRAWABLE "Current Layer" 0
			SF-ADJUSTMENT _"Taille de la marge horizontale (en px)" '(120 0 300 1 10 0 0)
			SF-ADJUSTMENT _"Taille de la marge verticale (en px)" '(140 0 300 1 10 0 0)
)