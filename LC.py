### LAMBDA CALCULUS IN PYTHON ###
#### The Y Combinator
ycomb = lambda f: ((lambda x: f(lambda y: x(x)(y)))(lambda x: f(lambda y: x(x)(y))))
########### BOOLEANS #####################################
true  = lambda x: lambda y: x
false = lambda x: lambda y: y

NOT = lambda p: lambda a: lambda b: p(b)(a)
AND = lambda p: lambda q: p(q)(p)
OR  = lambda p: lambda q: p(p)(q)

displayBool = lambda b: "TRUE" if b(1)(2) == 1 else "FALSE"
########## CHURCH NUMERALS ###############################
zero  = lambda f: lambda x: x
one   = lambda f: lambda x: f(x)
two   = lambda f: lambda x: f(f(x))
three = lambda f: lambda x: f(f(f(x)))
four  = lambda f: lambda x: f(f(f(f(x))))
five  = lambda f: lambda x: f(f(f(f(f(x)))))
six   = lambda f: lambda x: f(f(f(f(f(f(x))))))
seven = lambda f: lambda x: f(f(f(f(f(f(f(x)))))))
eight = lambda f: lambda x: f(f(f(f(f(f(f(f(x))))))))
nine  = lambda f: lambda x: f(f(f(f(f(f(f(f(f(x)))))))))
ten   = lambda f: lambda x: f(f(f(f(f(f(f(f(f(f(x))))))))))

succ = lambda n: lambda f: lambda x: (f(n(f)(x)))
plus = lambda m: lambda n: lambda f: lambda x: m(f)((n(f)(x)))
mult = lambda m: lambda n: lambda f: lambda x: m(n(f))(x)
pred = lambda n: lambda f: lambda x: (n(lambda g: lambda h: h(g(f)))(lambda u: x))(lambda u: u)
sub = lambda m: lambda n: n(pred)(m)
poww  = lambda b: lambda e: e(b)

displayNum = lambda n: n(lambda x: x + 1)(0)

church = lambda n: (lambda f: lambda x: x) if n == 0 else (lambda f: lambda x: f(church(n - 1)(f)(x)))
############ IF-THEN-ELSE PREDICATES ######################
ifthenelse = lambda p: lambda a: lambda b: p(a)(b)
isZero = lambda n: n(lambda x: false)(true)
# comparisons of Church numbers
leq = lambda m: lambda n: isZero(sub(m)(n))
eq = lambda m: lambda n: AND(leq(m)(n))(leq(n)(m))
lt = lambda m: lambda n: AND(leq(m)(n))(NOT(eq(m)(n)))
gt = lambda m: lambda n: NOT(leq(m)(n))
geq = lambda m: lambda n: OR(eq(m)(n))(gt(m)(n))
neq = lambda m: lambda n: NOT(eq(m)(n))

# additional arithmetic operators: div, mod
div_step = lambda f: lambda m: lambda n: lt(m)(n)(lambda _: zero)(lambda _: succ(f(sub(m)(n))(n)))(zero)
div = ycomb(div_step)

mod_step = lambda f: lambda m: lambda n: (lt(m)(n))(lambda _: m)(lambda _: f(sub(m)(n))(n))(zero)
mod = ycomb(mod_step)
########### LISTS #########################################
pair = lambda x: lambda y: lambda z: z(x)(y)
fst = lambda p: p(lambda x: lambda y: x)
snd = lambda p: p(lambda x: lambda y: y)

cons = lambda x: lambda y: lambda z: z(x)(y)
head = lambda p: p(lambda x: lambda y: x)
tail = lambda p: p(lambda x: lambda y: y)
nil = lambda x: lambda x: lambda y: x
isempty = lambda l: l(lambda h: lambda t: lambda x: lambda y: y)
################# Y-COMBINATOR #############################
fact = lambda f: lambda n: ifthenelse(isZero(n))(lambda _: one)(lambda _: mult(n)(f(pred(n))))(one)
#fact = lambda f: lambda n: isZero(n)(lambda _: one)(lambda _: mult(n)(f(pred(n))))(zero)  # this also works
factorial = lambda n: ycomb(fact)(n)

max = lambda x: lambda y: ifthenelse(leq)(x)(y)(y)(x)
min = lambda x: lambda y: ifthenelse(leq)(x)(y)(x)(y)

mylist1 = cons(one)(cons(two)(cons(three)(cons(four)(cons(five)(nil)))))    # mylist1 = [1,2,3,4,5]
mylist2 = cons(four)(cons(ten)(cons(three)(cons(five)(cons(nine)(nil)))))   # mylist2 = [4,10,3,5,9]

slist = lambda f: lambda x: ifthenelse(isempty(x))(lambda _: zero)(lambda _: plus(head(x))(f((tail(x)))))(zero)
dlist = lambda f: lambda x: ifthenelse(isempty(x))(lambda _: nil)(lambda _: cons(head(x))(cons(head(x))(f(tail(x)))))(zero)
zlist = lambda f: lambda x: ifthenelse(isempty(x))(lambda _: zero)(lambda _: plus(one)(f(tail(x))))(zero)
xlist = lambda f: lambda x: ifthenelse(isempty(x))(lambda _: zero)(lambda _: ifthenelse(leq(head(x)))(f(tail(x)))(f(tail(x)))(head(x)))(zero)

sumlist = lambda l: ycomb(slist)(l)  # returns sum of numbers in a list
doublelist = lambda l: ycomb(dlist)(l) # returns a list of duplicated elements of a list
length = lambda l: ycomb(zlist)(l) # returns size of a list
maxlist = lambda l: ycomb(xlist)(l) # returns max element in a list

###################################################################################################
## DISPLAY LIST OF NUMBERS
display_list_fn = lambda f: lambda x: ifthenelse(isempty(x))(lambda _: [])(lambda _: [displayNum(head(x))] + f(tail(x)))(zero)

# Recursive display function
displayList = lambda l: ycomb(display_list_fn)(l)

###################################################################################################
# data to test merge two sorted lists
xs = cons(one)(cons(three)(cons(five)(cons(seven)(cons(nine)(nil)))))    # xs = [1,3,5,7,9]
ys = cons(two)(cons(four)(cons(six)(cons(eight)(cons(ten)(nil)))))   # ys = [2,4,6,8,10]

###################################################################################################
#part_step = lambda f: lambda p: lambda l: \
#    ifthenelse(isempty(l))(
#        lambda _: pair(nil)(nil)
#    )(
#        lambda _: (
#            lambda rec: (
#                lambda h: ifthenelse(leq(h)(p))(
#                    lambda _: pair(cons(h)(fst(rec)))(snd(rec))
#                )(
#                    lambda _: pair(fst(rec))(cons(h)(snd(rec)))
#                )(zero)
#            )(head(l))
#        )(f(p)(tail(l)))
#    )(zero)
#partition = ycomb(part_step)

xs2 = cons(five)(cons(three)(cons(one)(cons(nine)(cons(seven)(nil))))) 

xs3 = cons(church(22))(cons(church(32))(cons(church(12))(cons(church(96))(cons(church(112))(cons(church(2))(cons(church(86))(cons(church(91))(cons(church(19))(cons(church(120))(cons(church(812))(cons(church(15))(cons(church(11))(cons(church(66))(cons(church(55))(nil)))))))))))))))
################ QUICKSORT #################################################################
qsplit_step = lambda f: lambda x: lambda xs: \
    isempty(xs) \
        (lambda _: pair(nil)(nil)) \
        (leq(head(xs))(x) \
                (lambda _: pair(cons(head(xs))(fst(f(x)(tail(xs)))))(snd(f(x)(tail(xs))))) \
                (lambda _: pair(fst(f(x)(tail(xs))))(cons(head(xs))(snd(f(x)(tail(xs)))))) \
        ) \
    (zero)

qsplit = lambda xs: ycomb(qsplit_step)(head(xs))(tail(xs))

concat_step = lambda f: lambda l1: lambda l2: \
    isempty(l1)( \
        lambda _: l2 \
    )( \
        lambda _: cons(head(l1))(f(tail(l1))(l2)) \
    )(zero)

concat = lambda l1: lambda l2: ycomb(concat_step)(l1)(l2)

qsort_step = lambda f: lambda xs: \
        isempty(xs) \
        (lambda _: nil) \
        (lambda _: \
            concat(f(fst(ycomb(qsplit_step)(head(xs))(tail(xs))))) \
            (concat(cons(head(xs))(nil))(f(snd(ycomb(qsplit_step)(head(xs))(tail(xs)))))) \
        ) \
        (zero)

qsort = lambda xs: ycomb(qsort_step)(xs)
################ MERGESORT #################################################################
merge_step = lambda f: lambda xs: lambda ys: \
    isempty(xs) \
         (lambda _: ys) \
         (isempty(ys) \
             (lambda _:xs) \
             (leq(head(xs))(head(ys)) \
                 (lambda _: cons(head(xs))(f(tail(xs))(ys))) \
                 (lambda _: cons(head(ys))(f(xs)(tail(ys)))) \
             ) \
         ) \
     (zero)

merge = lambda xs: lambda ys: ycomb(merge_step)(xs)(ys)

msplit_step = lambda f: lambda xs: \
    isempty(xs) \
        (lambda _: pair(nil)(nil)) \
        (isempty(tail(xs)) \
            (lambda _: pair(cons(head(xs))(nil))(nil)) \
            (lambda _: pair(cons(head(xs))(fst(f(tail(tail(xs)))))) \
                           (cons(head(tail(xs)))(snd(f(tail(tail(xs))))))) \
        ) \
    (zero)

msplit = lambda xs: ycomb(msplit_step)(xs)

msort_step = lambda f: lambda xs: \
        isempty(xs) \
        (lambda _: nil) \
        (isempty(tail(xs)) \
            (lambda _: xs)
            (lambda _: merge(f(fst(msplit(xs))))(f(snd(msplit(xs)))))
        ) (zero)

msort = lambda xs: ycomb(msort_step)(xs)
###########################################################################################
# Filter list of numbers using predicate
filter_step = lambda f: lambda g: lambda xs: \
    isempty(xs) \
            (lambda _: nil) \
            (g(head(xs)) \
                (lambda _: cons(head(xs))(f(g)(tail(xs)))) \
                (lambda _: f(g)(tail(xs))) \
            ) (zero)

filterr = lambda g: lambda xs: ycomb(filter_step)(g)(xs)
# displayList(filterr(lambda x: eq(mod(x)(two))(zero))(mylist1))
# displayList(filterr(lambda x: neq(mod(x)(two))(zero))(mylist1))
##########################################################################################
# map list of numbers using function
map_step = lambda f: lambda g: lambda xs: \
    isempty(xs) \
            (lambda _: nil) \
            (lambda _: cons(g(head(xs)))(f(g)(tail(xs)))) (zero)

mapp = lambda g: lambda xs: ycomb(map_step)(g)(xs)
# displayList(mapp(lambda x: poww(x)(church(2)))(mylist1))
# displayList(mapp(lambda x: mult(church(2))(x))(mylist1))
##########################################################################################

