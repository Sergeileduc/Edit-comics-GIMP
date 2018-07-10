(define (script-fu-clean-page-auto-0 image drawable)
(let*
	(
	(drawable (car (gimp-image-active-drawable image)))
	)

	;Prep
	(gimp-context-push)
	(gimp-image-undo-group-start image)
	;On fixe le seuil de détection à 0
	(gimp-context-set-sample-threshold-int 0)
	
	(gimp-image-select-color image CHANNEL-OP-REPLACE drawable (car (gimp-context-get-background)))
	(gimp-selection-invert image)
	(gimp-selection-flood image)
	(gimp-image-select-color image CHANNEL-OP-INTERSECT drawable (car (gimp-context-get-background)))

	;Test si la sélection est vide
	(if (= (car (gimp-selection-is-empty image)) FALSE)
		(begin
			;Enlève les trous la sélection
			(gimp-selection-flood image)
			(gimp-drawable-edit-fill drawable FILL-BACKGROUND)
			(gimp-selection-none image)
			(gimp-displays-flush)
		);message d'erreur si selection vide
		(gimp-message "Aucune sélection !\
Vérifiez la couleur d'arrière-plan ou utilisez des scripts avec un seuil plus grand (ou réglable)")
	);end if

	;Finish
	(gimp-image-undo-group-end image)
	(gimp-context-pop)
);end let
)

(script-fu-register "script-fu-clean-page-auto-0"
"4) Clean page - Auto - seuil 0"
"Clean toutes les bulles de la page de la couleur de l'AP, en excluant les marges de l'algorithme.\
...................\
-Le seuil de tolérance à la couleur est fixée à 0.\
Utilisez les scripts avec d'autres seuils en cas de problème"
"Sergeileduc"
"Sergeileduc"
"2008-06-28"
"RGB*"
SF-IMAGE "Input Image" 0
SF-DRAWABLE "Current Layer" 0
)
( script-fu-menu-register
	"script-fu-clean-page-auto-0" "<Image>/DC-trad/")