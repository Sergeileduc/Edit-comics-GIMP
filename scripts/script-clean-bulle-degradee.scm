(define (script-fu-clean-degrade image drawable)

	;Prep
	(gimp-context-push)
	(gimp-image-undo-group-start image)

	(let* (
		(drawable (car (gimp-image-active-drawable image)))
		)

	;Test selection vide
	(if (= (car (gimp-selection-is-empty image)) FALSE)
		(begin
		;Selectionne la bulle entière
		(gimp-selection-flood image)
		;Selectionne les lettres de couleur de PP
		(gimp-image-select-color image CHANNEL-OP-INTERSECT drawable (car (gimp-context-get-foreground)))
		;agrandis la sélection pour éviter les liserés
		(gimp-selection-grow image 2)
		(python-fu-heal-selection 0 image drawable 10 0 0)
		);message d'erreur si selection vide
		(gimp-message "Aucune sélection !!!\
Veuillez sélectionner la zone à corriger\
La couleur de Premier Plan doit être de la couleur des LETTRES\
Utilisez la PIPETTE")
	);end if

	;Finish
	(gimp-displays-flush)
	(gimp-selection-none image)
	(gimp-image-undo-group-end image)
	(gimp-context-pop)
	);end let
)

(script-fu-register "script-fu-clean-degrade"
	"1b) Clean bulle dégradée..."
	"Il faut que la couleur de PP soit la couleur des LETTRES\
(Utilisez la PIPETTE -> le noir des lettres n'est jamais du  vrai \(0 0 0\),\
souvent c'est du gris foncé \(30 30 30\)\),\
alors utilisez la pipette sur les lettres..
.......................\
Veuillez d'abord sélectionner une (ou plusieurs bulles) \(avec l'outil baguette magique par exemple\)"
	"Sergeileduc"
	"Sergeileduc"
	"2018-06-28"
	"RGB*"
	SF-IMAGE "Input Image" 0
	SF-DRAWABLE "Current Layer" 0
)

( script-fu-menu-register
	"script-fu-clean-degrade" "<Image>/DC-trad/")
