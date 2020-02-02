male(george).
male(philip).
male(spencer).
male(charles).
male(mark).
male(andrew).
male(edward).
male(william).
male(peter).
male(harry).
male(james).
female(mum).
female(kydd).
female(elizabeth).
female(margaret).
female(diana).
female(anne).
female(sarah).
female(sophie).
female(zara).
female(beatrice).
female(eugenie).
female(louise).
father(george, elizabeth).
father(george, margaret).
father(philip, charles).
father(philip, anne).
father(philip, andrew).
father(philip, edward).
father(spencer, diana).
father(charles, william).
father(charles, harry).
father(mark, peter).
father(mark, zara).
father(andrew, beatrice).
father(andrew, eugenie).
father(edward, louise).
father(edward, james).
mother(mum, elizabeth).
mother(mum, margaret).
mother(elizabeth, charles).
mother(elizabeth, anne).
mother(elizabeth, andrew).
mother(elizabeth, edward).
mother(kydd, diana).
mother(diana, william).
mother(diana, harry).
mother(anne, peter).
mother(anne, zara).
mother(sarah, beatrice).
mother(sarah, eugenie).
mother(sophie, louise).
mother(sophie, james).
child(elizabeth, george).
child(elizabeth, mum).
child(margaret, george).
child(margaret, mum).
child(diana, spencer).
child(diana, kydd).
child(charles, elizabeth).
child(charles, philip).
child(anne, elizabeth).
child(anne, philip).
child(andrew, elizabeth).
child(andrew, philip).
child(edward, elizabeth).
child(edward, philip).
child(william, diana).
child(william, charles).
child(harry, diana).
child(harry, charles).
child(peter, anne).
child(peter, mark).
child(zara, anne).
child(zara, mark).
child(beatrice, andrew).
child(beatrice, sarah).
child(eugenie, andrew).
child(eugenie, sarah).
child(louise, edward).
child(louise, sophie).
child(james, edward).
child(james, sophie).
couple(george, mum).
couple(mum, george).
couple(spencer, kydd).
couple(kydd, spencer).
couple(elizabeth, philip).
couple(philip, elizabeth).
couple(diana, charles).
couple(charles, diana).
couple(anne, mark).
couple(mark, anne).
couple(andrew, sarah).
couple(sarah, andrew).
couple(edward, sophie).
couple(sophie, edward).

sibling(X, Y):-child(X, Z), child(Y, Z), X \== Y.
grandchild(X, Y):-child(X, Z), child(Z, Y).
greatgrandparent(X, Y):-grandchild(Y, Z), child(Z, X).
ancestor(X, Y):-father(X, Y);mother(X, Y).
ancestor(X, Y):-father(Z, Y), ancestor(X, Z).
ancestor(X, Y):-mother(Z, Y), ancestor(X, Z).
brother(X, Y):-sibling(X, Y), male(X).
sister(X, Y):-sibling(X, Y), female(X).
daugther(X, Y):-child(X, Y), female(X).
son(X, Y):-child(X, Y), male(X).

firstcousin(X, Y):-child(Y, Z), child(X, U), sibling(Z, U).

brotherinlaw(X, Y):-sibling(Y, Z), couple(X, Z), male(X).
brotherinlaw(X, Y):-couple(Y, Z), sibling(X, Z), male(X).

sisterinlaw(X, Y):-sibling(Y, Z), couple(X, Z), female(X).
sisterinlaw(X, Y):-couple(Y, Z), sibling(X, Z), female(X).

aunt(X, Y):-child(Y, U), sibling(U, X), female(X).
aunt(X, Y):-child(Y, U), sisterinlaw(X, U).
uncle(X, Y):-child(Y, U), sibling(U, X), male(X).
uncle(X, Y):-child(Y, U), brotherinlaw(X, U).

distance(X, Y, 0):-firstcousin(X, Y);sibling(X, Y).
distance(X, Y, 1):-child(X, Y).
distance(X, Y, N):-N1 is N - 1, child(X, Z), distance(Z, Y, N1), N >= 1.

mthcousin(X, Y, 1):-firstcousin(X, Y).
mthcousin(X, Y, M):-M1 is M - 1, child(X, Z), mthcousin(Z, Y, M1), M >= 2.
mthcousinnremoved(X, Y, N, M):-distance(X, Y, N), mthcousin(X, Y, M).




