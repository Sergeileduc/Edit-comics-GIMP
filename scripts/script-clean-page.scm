(define (script-fu-clean-page-seuil-variable image drawable marge_w marge_h seuil)
 ( let*
		(
		(drawable (car (gimp-image-active-drawable image)))
		(imageWidth (car (gimp-image-width image))) ;largeur de l'image
		(imageHeight (car (gimp-image-height image))) ;hauteur de l'image
		)

	;Prep
	(gimp-context-push)
	(gimp-image-undo-group-start image)
	(gimp-context-set-sample-threshold-int seuil)

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

(script-fu-register "script-fu-clean-page-seuil-variable"
		    "<Image>/DCT-trad/4b) Clean page - seuil variable"
		    "Clean toutes les bulles de la page de la couleur de l'AP, en excluant les marges de l'algorithme.
			Le seuil de tolérance à la couleur est variable. Commencez à zéro et augmentez petit à petit"
		    "Sergeileduc"
		    "Sergeileduc"
		    "2008-06-28"
		    "RGB*"
		    SF-IMAGE "Input Image" 0
			SF-DRAWABLE "Current Layer" 0
			SF-ADJUSTMENT _"Taille de la marge horizontale (en px)" '(120 0 300 1 10 0 0)
			SF-ADJUSTMENT _"Taille de la marge verticale (en px)" '(140 0 300 1 10 0 0)
			SF-ADJUSTMENT _"seuil de tolérance à la couleur (pour le blanc cassé par exemple)" '(5 0 30 1 10 0 0)
)