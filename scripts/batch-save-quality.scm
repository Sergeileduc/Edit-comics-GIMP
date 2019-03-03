;Script pour copier l'image originale dans un nouveau calque, au sommet, en non visible, et en vérouillé.

(define (batch-save-quality pattern quality)

	; process pattern
	(let* ((filelist (cadr (file-glob pattern 1))))
		(while (not (null? filelist))


	;variable
	(let* ((filename (car filelist))
		   (image (car (gimp-file-load RUN-NONINTERACTIVE
									   filename filename)))
		   (drawable (car (gimp-image-get-active-layer image))))
	  (file-jpeg-save RUN-NONINTERACTIVE image drawable filename filename quality 0 0 0 " " 0 1 0 1)
	  (gimp-image-delete image)) ; just delete from RAM !

	(set! filelist (cdr filelist)))))

(script-fu-register "batch-save-quality"
"Batch save in jpeg"
"Sergeileduc"
"Sergeileduc"
"2019-03"
"RGB*"
SF-IMAGE "Input Image" 0
;SF-DRAWABLE "Current Layer" 0
)
