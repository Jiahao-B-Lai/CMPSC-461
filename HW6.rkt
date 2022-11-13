;Jiahao Lai
;jvl6364@psu.edu

;HW6:

;#1:
;define global variable:
(define al '())
;define fib:
(define (fib n)
  (if (= n 0) 0
      (if (<= n 2) 1
          (+ (fib (- n 1)) (fib (- n 2))))))
;define bind:
(define (bind k v al)
  (cons (list k v) al))
;define lookup (here I make some change to the old lookup definition, which directly return the value):
(define (lookup k al)
  (cond ((null? al) #f)
        ((equal? k (caar al)) (cadar al))
        (else (lookup k (cdr al)))))
;define fib_mem:
(define (fib_mem n)
  (if (equal? (lookup n al) #f) (begin
                                  (set! al (bind n (fib n) al))
                                  (fib n))
      (begin
        (display "memoization hit \n")
        (lookup n al))))




;#2:
;define build_mem:
(define (build_mem f)
  (let ((al2 '()))
    (lambda (n) (if (equal? (lookup n al2) #f) (begin
                                                 (set! al2 (bind n (f n) al2))
                                                 (f n))
                    (begin
                      (display "memoization hit \n")
                      (lookup n al2))))))

;as professor said on Campuswire, I bind (build_mem fib) to fib_m; the it should work correctly.
(define fib_m (build_mem fib))