(define (script-fu-clean-transpa image drawable seuil grow-pixel sampling-width sample-from filling-order flou)

	;Prep
	(gimp-context-push)
	(gimp-image-undo-group-start image)
	(gimp-context-set-sample-threshold-int seuil)
	(gimp-image-get-selection image)
	(let* (
		(drawable (car (gimp-image-active-drawable image)))
		(select-bounds (gimp-selection-bounds image))
		(select-x1 (cadr select-bounds))
		(select-y1 (caddr select-bounds))
		(select-x2 (cadr (cddr select-bounds)))
		(select-y2 (caddr (cddr select-bounds)))
		(select-width (- select-x2 select-x1))
		(select-height (- select-y2 select-y1))
		)

	;Test selection vide
	(if (= (car (gimp-selection-is-empty image)) FALSE)
		(begin
		;intersection avec le couleur de PP
		(gimp-image-select-color image CHANNEL-OP-INTERSECT drawable (car (gimp-context-get-foreground)))
		;test si la couleur AP est correcte
		(if (= (car (gimp-selection-is-empty image)) FALSE)
			(begin
			(gimp-selection-grow image grow-pixel)
			;heal selection
			(python-fu-heal-selection 1 image drawable sampling-width sample-from filling-order)
			;flou
			;(gimp-image-select-round-rectangle image CHANNEL-OP-REPLACE select-x1 select-y1 select-width select-height 5 5)
			(plug-in-gauss 0 image drawable flou flou 0)
			(plug-in-gauss 0 image drawable flou flou 0)
			;(plug-in-gauss 0 image drawable flou flou 0)
			(gimp-selection-none image)
			(gimp-displays-flush)
			);message d'erreur sur la couleur de PP
			(gimp-message "La couleur de Premier Plan doit être de la couleur des LETTRES\
Utilisez la PIPETTE\
Ou augmentez le seuil"));end if couleur
		);message d'erreur selection utilisateur
		(gimp-message "Aucune sélection !!!\
Veuillez sélectionner la zone à corriger"));end if selection utilisateur vide

	;Finish
	(gimp-image-undo-group-end image)
	(gimp-context-pop)
	);end let
)

(script-fu-register "script-fu-clean-transpa"
"TEST BETA) Clean zone texturée ou transparente..."
"Il faut que la couleur de PP soit la couleur des lettres\
\(Utilisez la PIPETTE -> le noir des lettres n'est jamais du  vrai \(0 0 0\),\
souvent c'est du gris foncé \(30 30 30\)\),
\alors utilisez la pipette sur les lettres..
......................\
Veuillez d'abord sélectionner une zone \(avec l'outil de sélection RECTANGULAIRE par exemple\)"
"Sergeileduc"
"Sergeileduc"
"2018-06-28"
"RGB*"
SF-IMAGE "Input Image" 0
SF-DRAWABLE "Current Layer" 0
SF-ADJUSTMENT "Seuil de tolérance à la couleur des LETTRES (défault = 30)" '(30 10 70 1 10 0 0)
SF-ADJUSTMENT "Agrandir la sélection autour des lettres de n (pixels)\
1 ou 2 généralement, jouer plutôt sur le seuil si les lettres disparaissent mal" '(1 0 10 1 10 0 0)
SF-ADJUSTMENT "Context sampling width \(pixels\)" '(10 0 100 1 10 0 0)
SF-OPTION "Sample from" '("All around" "Sides" "Above and below")
SF-OPTION "Filling order" '("Random" "Inwards towards center" "Outwards from center")
;SF-TOGGLE "Flouter avec un flou gaussien après la correction ?" FALSE
SF-ADJUSTMENT "Intensité du flou gaussien à appliquer en fin de script pour gommer les défauts\
0 pas de flou / 2 léger flou" '(0 0 10 1 10 0 0)
)

( script-fu-menu-register
	"script-fu-clean-transpa" "<Image>/Dev/")