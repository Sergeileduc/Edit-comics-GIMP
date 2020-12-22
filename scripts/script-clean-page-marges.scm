(define (script-fu-clean-page-marges image drawable marge_w marge_h seuil)
(let*
	(
	(drawable (car (gimp-image-get-active-drawable image)))
	(imageWidth (car (gimp-image-width image))) ;largeur de l'image
	(imageHeight (car (gimp-image-height image))) ;hauteur de l'image
	)

	;Prep
	(gimp-context-push)
	(gimp-image-undo-group-start image)

    ;Context
    (gimp-context-set-sample-threshold-int seuil)
    (gimp-context-set-paint-mode LAYER-MODE-NORMAL)
    (gimp-context-set-opacity 100)

	;Sélectionner le centre de la page (sans les marges)
	(gimp-image-select-rectangle image 2 marge_w marge_h (- imageWidth (* 2 marge_w)) (- imageHeight (* 2 marge_h)))

	;Sélection par couleur, dans la zone sans les marges (par intersection)
	(gimp-image-select-color image 3 drawable (car (gimp-context-get-background)))

	;Enlève les trous la sélection
	(gimp-selection-flood image)

	;Test si la sélection est vide
	(if (= (car (gimp-selection-is-empty image)) FALSE)
		(gimp-drawable-edit-fill drawable FILL-BACKGROUND)
		;message d'erreur si selection vide
		(gimp-message "Aucune sélection !\
Vérifiez la couleur d'arrière-plan, ou augmentez le seuil")
	);end if

	; Déselectionne tout
	;(gimp-selection-none image)

	;test
	(gimp-image-select-rectangle image 2 marge_w marge_h (- imageWidth (* 2 marge_w)) (- imageHeight (* 2 marge_h)))
	(gimp-displays-flush)

	;Finish
	(gimp-image-undo-group-end image)
	(gimp-context-pop)
);end let
)

(script-fu-register "script-fu-clean-page-marges"
"4b) Clean page - Marges et seuil variables"
"Clean toutes les bulles de la page de la couleur de l'AP, en excluant les marges de l'algorithme.\
...................\
-Le seuil de tolérance à la couleur est variable (0 = couleur pure).\
-Commencez à zéro et augmentez petit à petit"
"Sergeileduc"
"Sergeileduc"
"2018-08"
"RGB*"
SF-IMAGE "Input Image" 0
SF-DRAWABLE "Current Layer" 0
SF-ADJUSTMENT "Taille de la marge horizontale (en px)" '(90 0 300 1 10 0 0)
SF-ADJUSTMENT "Taille de la marge verticale (en px)" '(90 0 300 1 10 0 0)
SF-ADJUSTMENT "seuil de tolérance à la couleur (pour le blanc cassé par exemple)" '(0 0 30 1 10 0 0)
)
( script-fu-menu-register
	"script-fu-clean-page-marges" "<Image>/DC-trad/")
