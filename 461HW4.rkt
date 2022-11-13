;461 HW4
;Jiahao Lai

;Problem2
(define (A m n)
  (cond 
    ((= m 0) (+ n 1))                                       ;A(m,n)=n+1             if m=0
    ((and (> m 0) (= n 0)) (A (- m 1) 1))                   ;A(m,n)=A(m-1,1)        if m>0 and n=0
    ((and (> m 0) (> n 0)) (A (- m 1) (A m (- n 1))))       ;A(m,n)=A(m-1,A(m,n-1)) if m>0 and n>0
    (else 'Error...)))                                      ;otherwise, not defined in this function, error

;Problem3
(define (Mac n)
  (cond
    ((> n 100) (- n 10))             ;Mac(n)=n-10           if n>100
    (else Mac(Mac(+ n 11)))))        ;Mac(n)=Mac(Mac(n+11)  if n <=100

;Problem4
(define (payback n)
  (cond
    ((< n 0) 'Error...)                                  ;if input is negative, error
    ((<= n 1000) (* n 0.005))                            ;0.5% for the first $1000 charges
    ((<= n 2000) (+ 5 (* (- n 1000) 0.0075)))            ;0.75% for the next $1000 (payback from first $1000 is $5)
    ((<= n 3500) (+ (+ 5 7.5) (* (- n 2000) 0.01)))      ;1.0% for the next $1500 (payback from first $1000 and second $1000 is 5+7.5=$12.5)
    (else (+ (+ (+ 5 7.5) 15) (* (- n 3500) 0.015)))))   ;1.5% for everything above $3500 (payback from the first $1000 and second $1000 and next $1500 is 12.5+15=$27.5)