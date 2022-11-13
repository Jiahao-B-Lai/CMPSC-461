;Name Jiahao Lai
;psu email: jvl6364
;CMPSC461 proj-2


;problem 1
(define (dncall f n x)
  (if (= n 0) x
      (f (f (dncall f (- n 1) x)))))


;problem 2
(define (keep-if f l)
  (if (null? l) '()
      (if (equal? (f (car l)) #t) (cons (car l) (keep-if f (cdr l)))
          (keep-if f (cdr l)))))


;problem 3
;(a):
;least-helper:
(define (least-helper k x)
  (if (null? x) k
      (if (< k (car x)) (least-helper k (cdr x))
          (least-helper (car x) (cdr x)))))
;(b):
;least:
(define (least l)
  (if (null? l) '()
      (least-helper (car l) (cdr l))))


;problem 4
(define (to-words x)
  (cond ((= x 0) (cons 'zero '()))
        ((< x 0) (cons 'negative (to-words (* -1 x))))
        ((= x 1) (cons 'one '()))
        ((= x 2) (cons 'two '()))
        ((= x 3) (cons 'three '()))
        ((= x 4) (cons 'four '()))
        ((= x 5) (cons 'five '()))
        ((= x 6) (cons 'six '()))
        ((= x 7) (cons 'seven '()))
        ((= x 8) (cons 'eight '()))
        ((= x 9) (cons 'nine '()))
        ((= x 10) (cons 'ten '()))
        ((= x 11) (cons 'eleven '()))
        ((= x 12) (cons 'twelve '()))
        ((= x 13) (cons 'thirteen '()))
        ((= x 14) (cons 'fourteen '()))
        ((= x 15) (cons 'fifteen '()))
        ((= x 16) (cons 'sixteen '()))
        ((= x 17) (cons 'seventeen '()))
        ((= x 18) (cons 'eighteen '()))
        ((= x 19) (cons 'nineteen '()))
        ((= x 20) (cons 'twenty '()))
        ((= x 30) (cons 'thirty '()))
        ((= x 40) (cons 'fourty '()))
        ((= x 50) (cons 'fifty '()))
        ((= x 60) (cons 'sixty '()))
        ((= x 70) (cons 'seventy '()))
        ((= x 80) (cons 'eighty '()))
        ((= x 90) (cons 'ninety '()))
        (else (cond ((= (quotient x 10) 2) (cons 'twenty (to-words (remainder x 10))))
                    ((= (quotient x 10) 3) (cons 'thirty (to-words (remainder x 10))))
                    ((= (quotient x 10) 4) (cons 'fourty (to-words (remainder x 10))))
                    ((= (quotient x 10) 5) (cons 'fifty (to-words (remainder x 10))))
                    ((= (quotient x 10) 6) (cons 'sixty (to-words (remainder x 10))))
                    ((= (quotient x 10) 7) (cons 'seventy (to-words (remainder x 10))))
                    ((= (quotient x 10) 8) (cons 'eighty (to-words (remainder x 10))))
                    ((= (quotient x 10) 9) (cons 'ninety (to-words (remainder x 10))))
                    (else 'error)))))

;problem5
;(a)
;helper function member?:
(define (member? a lst)
  (cond ((null? lst) #f)
        ((equal? a (car lst)) #t)
        (else (member? a (cdr lst)))))
;helperfunction filterWords: (first-time-delete the irrelevant words )
(define (filterWords1 l1 l2)
  (if (null? l2) l1
      (if (equal? (member? (car l2) l1) #t) (if (null? l1) '()
                                                (if (equal? (car l2) (car l1)) (append '() (filterWords1 (cdr l1) (cdr l2)))
                                                    (cons (car l1) (filterWords1 (cdr l1) l2))))
          (filterWords1 l1 (cdr l2)))))
;filterWords: (all-occurrence-delete the irrelevant words)
(define (filterWords l1 l2)
  (if (equal? (filterWords1 l1 l2) l1) l1
      (filterWords (filterWords1 l1 l2) l2)))


;(b)
(define (iniWordCountList x)
  (if (null? x) '()
      (map (lambda (n) (if (null? n) '()
                           (append (list n 1) '())))
           x)))

;(c)
(define (mergeWordCounts l1 l2)
  (if (null? l1) l2
      (if (null? l2) (cons l1 '())
          (if (equal? (car l1) (caar l2)) (cons (list (caar l2) (+ (cadr l1) (cadar l2))) (cdr l2))
              (cons (car l2) (mergeWordCounts l1 (cdr l2)))))))

;(d)
;helper function reduce:
(define (reduce f l v)
  (if (null? l) v
      (f (car l) (reduce f (cdr l) v))))

;mergeByWord:
(define (mergeByWord l)
   (reduce mergeWordCounts l '()))


;(e)
(define (relevantWordCount l1 l2)
  (mergeByWord (iniWordCountList (filterWords l1 l2))))
      
             
          