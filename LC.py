### LAMBDA CALCULUS IN PYTHON ###
#### The Y Combinator
ycomb = lambda f: ((lambda x: f(lambda y: x(x)(y)))(lambda x: f(lambda y: x(x)(y))))
########### BOOLEANS #####################################
true  = lambda x: lambda y: x
false = lambda x: lambda y: y

NOT = lambda p: lambda a: lambda b: p(b)(a)
AND = lambda p: lambda q: p(q)(p)
OR  = lambda p: lambda q: p(p)(q)

eqbool = lambda p: lambda q: p(q)(NOT(q))

displayBool = lambda b: "TRUE" if b(1)(2) == 1 else "FALSE"
########### Pair data structure ################
pair = lambda x: lambda y: lambda z: z(x)(y)
fst  = lambda p: p(lambda x: lambda y: x)
snd  = lambda p: p(lambda x: lambda y: y)

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
add = lambda m: lambda n: lambda f: lambda x: m(f)((n(f)(x)))
mult = lambda m: lambda n: lambda f: lambda x: m(n(f))(x)
pred = lambda n: lambda f: lambda x: (n(lambda g: lambda h: h(g(f)))(lambda u: x))(lambda u: u)
sub  = lambda m: lambda n: n(pred)(m)
poww = lambda b: lambda e: e(b)

displayNum = lambda n: n(lambda x: x + 1)(0)

church = lambda n: (lambda f: lambda x: x) if n == 0 else (lambda f: lambda x: f(church(n - 1)(f)(x)))
############ IF-THEN-ELSE PREDICATES ######################
ifthenelse = lambda p: lambda a: lambda b: p(a)(b)
isZero = lambda n: n(lambda x: false)(true)
# comparisons of Church numbers
leq = lambda m: lambda n: isZero(sub(m)(n))
eq  = lambda m: lambda n: AND(leq(m)(n))(leq(n)(m))
lt  = lambda m: lambda n: AND(leq(m)(n))(NOT(eq(m)(n)))
gt  = lambda m: lambda n: NOT(leq(m)(n))
geq = lambda m: lambda n: OR(eq(m)(n))(gt(m)(n))
neq = lambda m: lambda n: NOT(eq(m)(n))

# additional arithmetic operators: div, mod
div_step = lambda f: lambda m: lambda n: \
    lt(m)(n) \
        (lambda _: zero) \
        (lambda _: succ(f(sub(m)(n))(n))) \
    (zero)

div = lambda m: lambda n: ycomb(div_step)(m)(n)

mod_step = lambda f: lambda m: lambda n: \
    lt(m)(n) \
        (lambda _: m) \
        (lambda _: f(sub(m)(n))(n)) \
    (zero)

mod = lambda m: lambda n: ycomb(mod_step)(m)(n)
########### Signed Numbers ################################
# Signed Number Constructors
make_pos = lambda n: pair(n)(zero)
make_neg = lambda n: pair(zero)(n)

# Extract components
pos_part = fst
neg_part = snd

# Normalize pair (p, n) by subtracting min(p, n) from both parts
norm_step = lambda f: lambda p: \
    OR(isZero(pos_part(p)))(isZero(neg_part(p))) \
    (lambda _: p) \
    (lambda _: f(pair(pred(pos_part(p)))(pred(neg_part(p))))) \
    (zero)

normalize = lambda p: ycomb(norm_step)(p)

# Display signed number as a Python integer
displaySignedNum = lambda p: (lambda np: displayNum(pos_part(np)) - displayNum(neg_part(np)))(normalize(p))

# Signed Operations
add_signed = lambda p1: lambda p2: normalize(
    pair(add(pos_part(p1))(pos_part(p2)))(add(neg_part(p1))(neg_part(p2)))
)

sub_signed = lambda p1: lambda p2: normalize(
    pair(add(pos_part(p1))(neg_part(p2)))(add(neg_part(p1))(pos_part(p2)))
)

negate = lambda p: pair(neg_part(p))(pos_part(p))

mult_signed = lambda p1: lambda p2: normalize(
    pair(
        add(mult(pos_part(p1))(pos_part(p2)))(mult(neg_part(p1))(neg_part(p2)))
    )(
        add(mult(pos_part(p1))(neg_part(p2)))(mult(neg_part(p1))(pos_part(p2)))
    )
)

# Predicates
is_neg = lambda p: (lambda np: AND(isZero(pos_part(np)))(NOT(isZero(neg_part(np)))))(normalize(p))
is_pos = lambda p: (lambda np: AND(NOT(isZero(pos_part(np))))(isZero(neg_part(np))))(normalize(p))
is_zero_signed = lambda p: (lambda np: AND(isZero(pos_part(np)))(isZero(neg_part(np))))(normalize(p))
########### LISTS #########################################
cons    = lambda x: lambda y: lambda z: z(x)(y)
head    = lambda p: p(lambda x: lambda y: x)
tail    = lambda p: p(lambda x: lambda y: y)
nil     = lambda x: lambda x: lambda y: x
isempty = lambda l: l(lambda h: lambda t: lambda x: lambda y: y)

## init of Haskell - all but last element
init_step = lambda f: lambda xs: \
    isempty(tail(xs)) \
        (lambda _: nil) \
        (lambda _: cons(head(xs))(f(tail(xs)))) \
    (zero)

init = lambda xs: ycomb(init_step)(xs)

## last item of a list
last_step = lambda f: lambda xs: \
    isempty(tail(xs)) \
        (lambda _: head(xs)) \
        (lambda _: f(tail(xs))) \
    (zero)
last = lambda xs: ycomb(last_step)(xs)

## append two lists
append_step = lambda f: lambda xs: lambda ys: \
    isempty(xs) \
        (lambda _: ys) \
        (lambda _: cons(head(xs))(f(tail(xs))(ys))) \
    (zero)

append = lambda xs: lambda ys: ycomb(append_step)(xs)(ys)

## reverse a list
reverse_step = lambda f: lambda xs: \
    isempty(xs) \
        (lambda _: xs) \
        (lambda _: append(f(tail(xs)))(cons(head(xs))(nil))) \
    (zero)

reverse = lambda xs: ycomb(reverse_step)(xs)

## is x an element of xs?
elem_step = lambda f: lambda x: lambda xs: \
    isempty(xs) \
        (lambda _: false) \
        (eq(x)(head(xs)) \
            (lambda _: true) \
            (lambda _: f(x)(tail(xs))) \
        ) \
    (zero)

elem = lambda x: lambda xs: ycomb(elem_step)(x)(xs)

# insert into list - no duplicates
insert = lambda x: lambda xs: \
    elem(x)(xs) \
        (lambda _: xs) \
        (lambda _: cons(x)(xs)) \
    (zero)

# subset
subset_step = lambda f: lambda xs: lambda ys: \
    isempty(xs) \
        (lambda _: true) \
        (elem(head(xs))(ys) \
            (lambda _: f(tail(xs))(ys)) \
            (lambda _: false) \
        ) \
    (zero)

subset = lambda xs: lambda ys: ycomb(subset_step)(xs)(ys)
equal  = lambda xs: lambda ys: AND(subset(xs)(ys))(subset(ys)(xs))
################# Y-COMBINATOR #############################
fact_step = lambda f: lambda n: \
    isZero(n) \
        (lambda _: one) \
        (lambda _: mult(n)(f(pred(n)))) \
    (zero)

fact = lambda n: ycomb(fact_step)(n)

fib_step = lambda f: lambda n: \
    isZero(pred(n)) \
        (lambda _: one) \
        (isZero(pred(pred(n))) \
            (lambda _: one) \
            (lambda _: add(f(pred(n)))(f(pred(pred(n))))) \
        ) \
    (zero)

fib = lambda n: ycomb(fib_step)(n)

minn = lambda x: lambda y: leq(x)(y)(x)(y)
maxx = lambda x: lambda y: leq(x)(y)(y)(x)

mylist1 = cons(one)(cons(two)(cons(three)(cons(four)(cons(five)(nil)))))    # mylist1 = [1,2,3,4,5]
mylist2 = cons(four)(cons(ten)(cons(three)(cons(five)(cons(nine)(nil)))))   # mylist2 = [4,10,3,5,9]
mylist3 = cons(eight)(cons(ten)(cons(seven)(cons(six)(cons(nine)(nil)))))   # mylist3 = [8,10,7,6,9]
mylist4 = cons(one)(cons(three)(cons(five)(nil)))   # mylist4 = [1,3,5]

# sum numbers in a list
slist_step = lambda f: lambda xs: \
    isempty(xs) \
        (lambda _: zero) \
        (lambda _: add(head(xs))(f((tail(xs))))) \
    (zero)

sumlist = lambda xs: ycomb(slist_step)(xs)

# double each element in a list
dlist_step = lambda f: lambda xs: \
    isempty(xs) \
        (lambda _: nil) \
        (lambda _: cons(head(xs))(cons(head(xs))(f(tail(xs))))) \
    (zero)

doublelist = lambda xs: ycomb(dlist_step)(xs)

# length of a list
zlist_step = lambda f: lambda xs: \
    isempty(xs) \
        (lambda _: zero) \
        (lambda _: add(one)(f(tail(xs)))) \
    (zero)

length = lambda xs: ycomb(zlist_step)(xs)

# max number in list
xlist_step = lambda f: lambda xs: \
    isempty(xs) \
        (lambda _: zero) \
        (lambda _: leq(head(xs))(f(tail(xs)))(f(tail(xs)))(head(xs))) \
    (zero)

maxlist = lambda xs: ycomb(xlist_step)(xs)

###################################################################################################
## DISPLAY LIST OF NUMBERS
display_list_step = lambda f: lambda xs: \
    isempty(xs) \
        (lambda _: []) \
        (lambda _: [displayNum(head(xs))] + f(tail(xs))) \
    (zero)

# Recursive display function
displayList = lambda xs: ycomb(display_list_step)(xs)

## DISPLAY List of Lists of numbers
displayListOfLists = lambda ll: ifthenelse(isempty(ll))\
    (lambda _: [])\
    (lambda _: [head(mapp(displayList)(ll))] + displayListOfLists(tail(ll)))\
(zero)
###################################################################################################
# data to test merge two sorted lists
xs = cons(one)(cons(three)(cons(five)(cons(seven)(cons(nine)(nil)))))    # xs = [1,3,5,7,9]
ys = cons(two)(cons(four)(cons(six)(cons(eight)(cons(ten)(nil)))))   # ys = [2,4,6,8,10]

###################################################################################################
xs2 = cons(five)(cons(three)(cons(one)(cons(nine)(cons(seven)(nil))))) 

xs3 = cons(church(22))(  \
      cons(church(32))(  \
      cons(church(12))(  \
      cons(church(96))(  \
      cons(church(112))( \
      cons(church(2))(   \
      cons(church(86))(  \
      cons(church(91))(  \
      cons(church(19))(  \
      cons(church(120))( \
      cons(church(812))( \
      cons(church(15))(  \
      cons(church(11))(  \
      cons(church(66))(  \
      cons(church(55))(  \
      nil)))))))))))))))
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
# foldr :: (a -> b -> b) -> b -> [a] -> b
# foldr f z []     = z
# foldr f z (x:xs) = f x (foldr f z xs)
foldr_step = lambda f: lambda g: lambda acc: lambda xs: \
    isempty(xs)\
      (lambda _: acc)\
      (lambda _: g(head(xs))(f(g)(acc)(tail(xs)))) (zero)
            
foldr = lambda g: lambda acc: lambda xs: ycomb(foldr_step)(g)(acc)(xs)
# displayList(mylist# displayNum(foldr(add)(zero)(mylist1))
##########################################################################################
# foldl :: (b -> a -> b) -> b -> [a] -> b
# foldl f z []     = z
# foldl f z (x:xs) = foldl f (f z x) xs
foldl_step = lambda f: lambda g: lambda acc: lambda xs: \
    isempty(xs)\
      (lambda _: acc)\
      (lambda _: f(g)(g(acc)(head(xs)))(tail(xs))) (zero)
            
foldl = lambda g: lambda acc: lambda xs: ycomb(foldl_step)(g)(acc)(xs)
##########################################################################################
disjoint_step = lambda f: lambda xs: lambda ys: \
    isempty(xs)\
        (lambda _: true) \
        (isempty(ys) \
            (lambda _: true) \
            (eq(head(xs))(head(ys)) \
                (lambda _: false) \
                (lt(head(xs))(head(ys)) \
                 (lambda _: f(tail(xs))(ys)) \
                 (lambda _: f(xs)(tail(ys))) \
                ) \
            ) \
        ) (zero)

disjoint = lambda xs: lambda ys: ycomb(disjoint_step)(xs)(ys)
# displayBool(disjoint(mylist1)(mylist2))
# displayBool(disjoint(mylist1)(mylist3))
##########################################################################################
## union
union_step = lambda f: lambda xs: lambda ys: \
    isempty(xs) \
        (lambda _: ys) \
        (elem(head(xs))(ys) \
            (lambda _: f(tail(xs))(ys)) \
            (lambda _: cons(head(xs))(f(tail(xs))(ys))) \
        ) \
    (zero)
union = lambda xs: lambda ys: ycomb(union_step)(xs)(ys)
##########################################################################################
## intersect
intersect_step = lambda f: lambda xs: lambda ys: \
    isempty(xs) \
        (lambda _: nil) \
        (elem(head(xs))(ys) \
            (lambda _: cons(head(xs))(f(tail(xs))(ys))) \
            (lambda _: f(tail(xs))(ys)) \
        ) \
    (zero)
intersect = lambda xs: lambda ys: ycomb(intersect_step)(xs)(ys)
##########################################################################################
## intersect
difference_step = lambda f: lambda xs: lambda ys: \
    isempty(xs) \
        (lambda _: nil) \
        (elem(head(xs))(ys) \
            (lambda _: f(tail(xs))(ys)) \
            (lambda _: cons(head(xs))(f(tail(xs))(ys))) \
        ) \
    (zero)
difference = lambda xs: lambda ys: ycomb(difference_step)(xs)(ys)
##########################################################################################
bs = cons(one)(cons(two)(cons(three)(nil)))
subsets_step = lambda f: lambda xs: \
    isempty(xs)\
        (lambda _: cons(nil)(nil))\
        (lambda _: (lambda recursive_subsets: \
                      append(recursive_subsets) \
                            (mapp(lambda x: cons(head(xs))(x))(recursive_subsets))
                   ) \
                   (f(tail(xs))) \
        ) \
        (zero)
subsets = lambda xs: ycomb(subsets_step)(xs)
# displayListOfLists(subsets(bs))
##########################################################################################
ordered_step = lambda f: lambda xs: \
    isempty(xs)\
        (lambda _: true) \
        (isempty(tail(xs)) \
            (lambda _: true) \
            (gt(head(xs))(head(tail(xs))) \
                (lambda _: false) \
                (lambda _: f(tail(xs))) \
            ) \
        ) (zero)

ordered = lambda xs: ycomb(ordered_step)(xs)
# displayBool(ordered(mylist1))
# displayBool(ordered(mylist2))
# displayBool(ordered(mylist3))
##########################################################################################
# Char data

between = lambda low: lambda high: lambda x: AND(geq(x)(low))(leq(x)(high)) # low <= x <= high

# Character Constructors (ASCII Encodings)
# Numbers: '0' (48) to '9' (57)
# Upper:   'A' (65) to 'Z' (90)
# Lower:   'a' (97) to 'z' (122)
encode_char = lambda c: church(ord(c))
decode_char = lambda n: chr(displayNum(n))

# Predicates using ASCII bounds
isDigit = between(encode_char('0'))(encode_char('9'))
isUpper = between(encode_char('A'))(encode_char('Z'))
isLower = between(encode_char('a'))(encode_char('z'))

# Convert uppercase character to lowercase
toLower = lambda c: \
    isUpper(c) \
        (lambda _: add(c)(church(32))) \
        (lambda _: c) \
    (zero)

# Convert lowercase character to uppercase
toUpper = lambda c: \
    isLower(c) \
        (lambda _: sub(c)(church(32))) \
        (lambda _: c) \
    (zero)

# Example characters
char_A = encode_char('A')
char_g = encode_char('g')
char_5 = encode_char('5')

#displayBool(isUpper(char_A)))
#displayBool(isLower(char_A)))
#displayBool(isDigit(char_5)))
#displayNum(toLower(char_A)))
#######################################################################
# String data as a list of char data
encode_str_step = lambda f: lambda s: nil if s=="" else cons(encode_char(s[0]))(f(s[1:]))
encode_str = lambda s: ycomb(encode_str_step)(s)

decode_str_step = lambda f: lambda s: \
    isempty(s) \
        (lambda _: "") \
        (lambda _: decode_char(head(s))+f(tail(s))) \
    (zero)
decode_str = lambda s: ycomb(decode_str_step)(s)

displaySList = lambda xs: \
    isempty(xs) \
        (lambda _: []) \
        (lambda _: [decode_str(head(xs))] + displaySList(tail(xs))) \
    (zero)

strlen = lambda s: length(s)
isempty_str = lambda s: eq(strlen(s))(zero)
strcat = lambda s1: lambda s2: append(s1)(s2)

### let's implement Python's s.join(lst)!
join_step = lambda f: lambda sep: lambda xss: \
    isempty_str(xss) \
        (lambda _: nil) \
            (isempty_str(tail(xss)) \
                (lambda _: head(xss)) \
            ) \
            (lambda _: strcat(head(xss))(strcat(sep)(f(sep)(tail(xss))))) \
    (zero)
join = lambda sep: lambda xss: ycomb(join_step)(sep)(xss)

# sss = cons(encode_str("Donald"))(cons(encode_str("22-Sep-2000"))(cons(encode_str("10 Main Street"))(nil)))
# decode_str(join(encode_str(":"))(sss))
#
# Let's implement find substring 
#find = lambda xs: lambda ys: ycomb(find_step)(xs)(ys)
# Helper: Checks if list/string xs is a prefix of ys
is_prefix_step = lambda f: lambda xs: lambda ys: \
    isempty(xs) \
    (lambda _: true) \
    (isempty(ys) \
        (lambda _: false) \
        (eq(head(xs))(head(ys)) \
            (lambda _: f(tail(xs))(tail(ys))) \
            (lambda _: false) \
        ) \
    ) \
    (zero)

is_prefix = lambda xs: lambda ys: ycomb(is_prefix_step)(xs)(ys)

# is_suffix

# Main recursive search function tracking current index `idx`
#find_step = lambda f: lambda xs: lambda ys: lambda idx: \
#    is_prefix(xs)(ys) \
#        (lambda _: idx) \
#        (isempty(ys) \
#            (lambda _:  false) \
#            (lambda _: f(xs)(tail(ys))(succ(idx))) \
#        ) \
#    (zero)

# Public interface initializing index to zero
#find = lambda xs: lambda ys: ycomb(find_step)(xs)(ys)(zero)

# contains

minus_one = make_neg(one)

find_step = lambda f: lambda xs: lambda ys: lambda idx: \
    is_prefix(xs)(ys) \
    (lambda _: make_pos(idx)) \
    (isempty(ys) \
        (lambda _: minus_one) \
        (lambda _: f(xs)(tail(ys))(succ(idx))) \
    ) \
    (zero)

find = lambda xs: lambda ys: ycomb(find_step)(xs)(ys)(zero)
#######################################################################
# get prefix of string s until index i
prefix_step = lambda f: lambda s: lambda i: \
    isZero(i) \
        (lambda _: cons(head(s))(nil)) \
        (lambda _: cons(head(s))(f(tail(s))(pred(i)))) \
    (zero)

prefix = lambda s: lambda i: ycomb(prefix_step)(s)(i)
# get suffix of string s starting at index i
suffix_step = lambda f: lambda s: lambda i: \
    isZero(i) \
        (lambda _: s) \
        (lambda _: f(tail(s))(pred(i))) \
    (zero)

suffix = lambda s: lambda i: ycomb(suffix_step)(s)(i)
# Extract substring ala Python slice operator!
substr = lambda s: lambda i: lambda j: \
    OR(geq(i)(strlen(s)))(OR(geq(j)(strlen(s)))(lt(j)(i))) \
        (lambda _: nil) \
        (lambda _: prefix(suffix(s)(i))(sub(j)(i))) \
    (zero)
#######################################################################
# Binary Tree of Numbers
#leaf = lambda n: lambda l: l
#node = lambda v: lambda left: lambda right: \
#    lambda n: lambda l: n(v)(left(n)(l))(right(n)(l))
#
## Construct subtrees
#t_left  = node(two)(leaf)(leaf)
#t_right = node(three)(leaf)(leaf)
#
## Root node holding 'one'
#my_tree1 = node(one)(t_left)(t_right)
#
#tree1 = node(one)(leaf)(leaf)
#tree2 = node(two)(tree1)(leaf)
#tree5 = node(five)(leaf)(leaf)
#my_tree2 = node(four)(tree2)(tree5)
#
#sum_tree = lambda t: t(lambda v: lambda l_sum: lambda r_sum: add(v)(add(l_sum)(r_sum)))(zero)
#size_tree = lambda t: t(lambda v: lambda l_size: lambda r_size: add(one)(add(l_size)(r_size)))(zero)
#
###########################################################################################
