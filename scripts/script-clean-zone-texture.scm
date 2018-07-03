(define (script-fu-clean-texture image drawable grow-pixel sampling-width sample-from filling-order flou)

	;Prep
	(gimp-context-push)
	(gimp-image-undo-group-start image)
	
	(let* (
		(select-bounds (gimp-selection-bounds image))
        (select-x1 (cadr select-bounds))
        (select-y1 (caddr select-bounds))
        (select-x2 (cadr (cddr select-bounds)))
        (select-y2 (caddr (cddr select-bounds)))
        (select-width (- select-x2 select-x1))
        (select-height (- select-y2 select-y1))
	)
  
	;script
	(gimp-image-get-selection image)
	(gimp-image-select-color image CHANNEL-OP-INTERSECT (car (gimp-image-get-active-drawable image)) (car (gimp-context-get-foreground)))
	(gimp-selection-grow image grow-pixel)
	(python-fu-heal-selection 1 image drawable sampling-width sample-from filling-order)

	(gimp-image-select-round-rectangle image 2 select-x1 select-y1 select-width select-height 5 5)
	(plug-in-gauss 0 image (car (gimp-image-get-active-drawable image)) flou flou 0)

	;Finish
	(gimp-displays-flush)
	(gimp-selection-none image)
	(gimp-image-undo-group-end image)
	(gimp-context-pop)
	)
)

(script-fu-register "script-fu-clean-texture"
	"<Image>/DCT-trad/2) Clean zone texturée ou transparente..."
	"Il faut que la couleur de PP soit la couleur des lettres 
	\(Utilisez la PIPETTE -> le noir des lettres n'est jamais du  vrai \(0 0 0\),
	souvent c'est du gris foncé \(30 30 30\)\),
	alors utilisez la pipette sur les lettres..
	
	Veuillez d'abord sélectionner une zone \(avec l'outil de sélection RECTANGULAIRE par exemple\)"
	"Sergeileduc"
	"Sergeileduc"
	"2018-06-28"
	"RGB*"
	SF-IMAGE "Input Image" 0
	SF-DRAWABLE "Current Layer" 0
	SF-ADJUSTMENT "Agrandir la sélection autour des lettres de n (pixels) 
	\(1 ou 2, agrandir si nécéssaire, si la bordure des lettres apparaît toujours après correction" '(2 0 10 1 10 0 0)
	SF-ADJUSTMENT "Context sampling width \(pixels\)" '(10 0 100 1 10 0 0)
	SF-OPTION "Sample from" '("All around" "Sides" "Above and below")
	SF-OPTION "Filling order" '("Random" "Inwards towards center" "Outwards from center")
	;SF-TOGGLE "Flouter avec un flou gaussien après la correction ?" FALSE
	SF-ADJUSTMENT "Intensité du flou gaussien à appliquer en fin de script pour gommer les défauts" '(0 0 10 1 10 0 0)
)