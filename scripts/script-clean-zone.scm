(define (script-fu-clean-zone image drawable)

	;Prep
	(gimp-context-push)
	(gimp-image-undo-group-start image)
	;modifiez cette valeur (2 par défaut) si vous voulez un script avec un seuil plus tolérant
	(gimp-context-set-sample-threshold-int 2)
	
	;Recupere la selection utilisateur
	(gimp-image-get-selection image)
	
	;test la sélection utilisateur est vide
	(if (= (car (gimp-selection-is-empty image)) FALSE)
	(begin
	;intersection avec la couleur de PP
	(gimp-image-select-color image 3 drawable (car (gimp-context-get-background)))
		;test si la couleur AP est correcte
		(if (= (car (gimp-selection-is-empty image)) FALSE)
			(begin
			(let* ((drawable (car (gimp-image-active-drawable image))))
			;ACTIONS DU SCRIPT
			(gimp-selection-flood image)
			(gimp-drawable-edit-fill drawable FILL-BACKGROUND));end let
			);sinon, message sur la couleur de AP
			(gimp-message "Vérifiez votre couleur d'arrière-plan, ou augmentez le seuil !!!"));end if couleur
	);si non, message "pas de selection"
	(gimp-message "Aucune sélection !\
Veuillez d'abord sélectionner une zone \(rectangulaire par exemple\) !!!")
	);end if selection utilisateur
	
	;Finish
	(gimp-displays-flush)
	(gimp-selection-none image)
	(gimp-image-undo-group-end image)
	(gimp-context-pop)

)

(script-fu-register "script-fu-clean-zone"
	"3) Clean zone \(seuil=2)..."
	"Clean toutes les bulles de la zone avec la couleur de AP\
...................\
-Veuillez d'abord sélectionner une zone (avec l'outil de sélection réctangulaire par exemple)\
-Le seuil de tolérance à la couleur est de 2. Pour un seuil variable, utilisez le script 3b) Clean zone - seuil variable"
	"Sergeileduc"
	"Sergeileduc"
	"2018-06-28"
	"RGB*"
	SF-IMAGE "Input Image" 0
	SF-DRAWABLE "Current Layer" 0
)

( script-fu-menu-register
	"script-fu-clean-zone" "<Image>/DC-trad/")
