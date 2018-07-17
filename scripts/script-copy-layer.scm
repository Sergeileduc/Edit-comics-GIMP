(define (script-fu-copy-layer image drawable)

	;variable
	(let*	(
		(drawable (car (gimp-image-active-drawable image)))
		(layer (car (gimp-image-get-active-layer image)))
			)


	;Prep
	(gimp-context-push)
	(gimp-image-undo-group-start image)

	;SCRIPT
	(gimp-item-set-name layer "Edit")
	(define new-layer (car (gimp-layer-copy drawable 1)))
	(gimp-image-insert-layer image new-layer 0 0)
	(gimp-item-set-name new-layer "Original")
	(gimp-image-set-active-layer image layer)
	(gimp-item-set-lock-position layer TRUE)
	(gimp-item-set-lock-position new-layer TRUE)
	(gimp-item-set-lock-content new-layer TRUE)
	(gimp-item-set-visible new-layer FALSE)
	;Finish
	(gimp-displays-flush)
	(gimp-image-undo-group-end image)
	(gimp-context-pop)
	);end let
)

(script-fu-register "script-fu-copy-layer"
"0) Dupliquer le calque image pour garder l'original..."
"Duplique le calque image, pour avoir un calque de travail \"Edit\" et une calque de reference \#Original\"\
Le script verouille les calques en deplacement, et verouille le calque original pour le rendre non modifiable"
"Sergeileduc"
"Sergeileduc"
"2008-06-28"
"RGB*"
SF-IMAGE "Input Image" 0
SF-DRAWABLE "Current Layer" 0
)

( script-fu-menu-register
	"script-fu-copy-layer" "<Image>/DC-trad/")
