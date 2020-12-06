(define (script-fu-clean-texture image drawable seuil grow-pixel sampling-width sample-from filling-order flou_bool flou feather delta)

	;Prep
	(gimp-context-push)
	(gimp-image-undo-group-start image)
	(gimp-context-set-sample-threshold-int seuil)
	(gimp-image-get-selection image)

	;Test selection vide
	(if (= (car (gimp-selection-is-empty image)) FALSE)
		(begin
		;intersection avec le couleur de PP
		(gimp-image-select-color image CHANNEL-OP-INTERSECT drawable (car (gimp-context-get-foreground)))
		;test si la couleur AP est correcte
		(if (= (car (gimp-selection-is-empty image)) FALSE)
			(begin
			(gimp-selection-grow image grow-pixel)
			;Resynthesizer heal selection
			(python-fu-heal-selection 1 image drawable sampling-width sample-from filling-order)
			;flou
			(if(= flou_bool TRUE)
				(begin
				(gimp-selection-feather image feather)
				(plug-in-sel-gauss 0 image drawable flou delta)
				);end begin
			);end if appliquer un flou

			;flush display
			(gimp-selection-none image)
			(gimp-displays-flush)
			);message d'erreur sur la couleur de PP
			(gimp-message "La couleur de Premier Plan doit être de la couleur des LETTRES\
Utilisez la PIPETTE\
Ou augmentez le seuil"));end if couleur
		);message d'erreur selection utilisateur
		(gimp-message "Aucune sélection !!!\
Veuillez sélectionner la zone à corriger")
	);end if selection utilisateur vide

	;Finish
	(gimp-image-undo-group-end image)
	(gimp-context-pop)
)

(script-fu-register "script-fu-clean-texture"
"2) Clean zone texturée ou transparente..."
"Il faut que la couleur de PP soit la couleur des lettres\
\(Utilisez la PIPETTE -> le noir des lettres n'est jamais du  vrai \(0 0 0\),\
souvent c'est du gris foncé \(30 30 30\)\),
\alors utilisez la pipette sur les lettres..
......................\
Veuillez d'abord sélectionner une zone \(avec l'outil de sélection RECTANGULAIRE par exemple\)"
"Sergeileduc"
"Sergeileduc"
"2018-08"
"RGB*"
SF-IMAGE "Input Image" 0
SF-DRAWABLE "Current Layer" 0
SF-ADJUSTMENT "Seuil de tolérance à la couleur des LETTRES (défault = 30)" '(30 0 70 1 10 0 0)
SF-ADJUSTMENT "Agrandir la sélection autour des lettres de n (pixels)\
1 ou 2 généralement, jouer plutôt sur le seuil si les lettres disparaissent mal" '(1 0 10 1 10 0 0)
SF-ADJUSTMENT "Context sampling width \(pixels\)" '(10 0 100 1 10 0 0)
SF-OPTION "Sample from" '("All around" "Sides" "Above and below")
SF-OPTION "Filling order" '("Random" "Inwards towards center" "Outwards from center")
SF-TOGGLE "FACULTATIF : Flouter avec un flou gaussien sélectif \(qui conserve les lignes contrastées\) après la correction ?\
\(tout ce qui suit concerne un flou facultatif\)" FALSE
SF-ADJUSTMENT "Intensité du flou gaussien sélectif à appliquer en fin de script pour gommer les défauts" '(5 0 10 1 10 0 0)
SF-ADJUSTMENT "Fondu entre zone floue et zone nette\
0 pas de fondu" '(20 0 40 1 10 0 0)
SF-ADJUSTMENT "Seuil de contraste à ne pas flouter\
\(évite que des objets contrastés, comme des lignes noires, etc... ne soient floutées\)\
50 est le seuil par défaut" '(51 0 255 1 10 0 0)
)

( script-fu-menu-register
	"script-fu-clean-texture" "<Image>/DC-trad/")
