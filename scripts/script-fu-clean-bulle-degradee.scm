#!/usr/bin/env gimp-script-fu-interpreter-3.0
;!# Close comment started on first line. Needed by gettext.

;; Purpose: Global flag to control debug output.
(define debug #f)

(define (script-fu-clean-degrade image drawable)

	(gimp-message "Script-Fu Clean Bulle dégradée...")

	;Prep
	(gimp-context-push)
	(gimp-image-undo-group-start image)
	(gimp-context-set-sample-threshold-int 15)

	;test if selection not empty
	(when (= TRUE (car (gimp-selection-is-empty image)))
		(gimp-message ("Aucune sélection !!!\
Veuillez sélectionner la(les) bulle(s) à corriger (baguette magique seuil ~ 100 par exemple"))
		(quit -1))

	(gimp-image-get-selection image)

  ;Selectionne la bulle entière
  (gimp-selection-flood image)
  ;Selectionne les lettres de couleur de PP dans la bulle
  (gimp-image-select-color image CHANNEL-OP-INTERSECT drawable (car (gimp-context-get-foreground)))

  (if (= (car (gimp-selection-is-empty image)) FALSE)
    (begin
    ;agrandis la sélection pour éviter les liserés
    (gimp-selection-grow image 2)

    ;this is where we call resynthesizer
    ;vector is because resynthesizer plugin expects a vector of layers
    (script-fu-heal-selection image (vector drawable) 10 0 0)

    (gimp-selection-none image)
    (gimp-displays-flush)
    );message d'erreur sur la couleur de PP
    (gimp-message "La couleur de Premier Plan doit être de la couleur des LETTRES\
Utilisez la PIPETTE"));end if couleur

	;Finish
	(gimp-image-undo-group-end image)
	(gimp-context-pop)
)

(script-fu-register
  "script-fu-clean-degrade"       ; run func name
  "1b) Clean bulle dégradée..."   ; menu label
  (string-append                  ; description
"Il faut que la couleur de PP soit la couleur des LETTRES\
(Utilisez la PIPETTE -> le noir des lettres n'est jamais du  vrai \(0 0 0\),\
souvent c'est du gris foncé \(30 30 30\)\),\
alors utilisez la pipette sur les lettres..
.......................\
Veuillez d'abord sélectionner une (ou plusieurs bulles) 
\(avec l'outil baguette magique par exemple\)
(seuil ~ 100-120 en général, mais faut tester)"
)
  "Sergeileduc"	                   ; author
  "2018 Sergeileduc"               ; copyright notice
  "2025"                           ;date created
  "RGB* GRAY*"                     ; image types handled by script
  SF-IMAGE "Input Image" 0
  SF-DRAWABLE "Current Layer" 0
)

(script-fu-menu-register "script-fu-clean-degrade"
    "<Image>/DC-trad/")
