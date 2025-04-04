;Script pour copier l'image originale dans un nouveau calque, au sommet, en non visible, et en vérouillé.

(define (script-fu-copy-layer image drawable)

	;Prep
	(gimp-context-push)
	(gimp-image-undo-group-start image)
	(define layer car(gimp-layer-copy drawable 1))

	;Resolution
	(gimp-image-set-resolution image 72 72)
	;SCRIPT
	(gimp-item-set-name drawable "Edit")
	(define new-layer (car (gimp-layer-copy drawable 1)))
	(gimp-image-insert-layer image new-layer 0 0)
	(gimp-item-set-name new-layer "Original") 
	; (gimp-image-set-active-layer image layer)  ; problem here !
	; (gimp-image-set-selected-layers image (make-vector 1 layer))
	(gimp-image-set-selected-layers image (make-vector 1 drawable))
	(gimp-item-set-lock-position drawable TRUE)
	(gimp-item-set-lock-position new-layer TRUE)
	(gimp-item-set-lock-content new-layer TRUE)
	(gimp-item-set-visible new-layer FALSE)
	;Finish
	(gimp-displays-flush)
	(gimp-image-undo-group-end image)
	(gimp-context-pop)
)

(script-fu-register "script-fu-copy-layer"
"0) Dupliquer le calque image pour garder l'original..."
"Duplique le calque image, pour avoir un calque de travail \"Edit\" et une calque de reference \#Original\"\
Le script verouille les calques en deplacement, et verouille le calque original pour le rendre non modifiable"
"Sergeileduc"
"Sergeileduc"
"2018-08"
"RGB*"
SF-IMAGE "Input Image" 0
SF-DRAWABLE "Current Layer" 0
)

( script-fu-menu-register
	"script-fu-copy-layer" "<Image>/DC-trad/")
