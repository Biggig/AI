so([Empty|Tiles], [Tile|Tiles1], 1):-
	swap(Emptym Tile, Tiles Tiles1).
swap(Empty, Tile, [Tile|Ts], [Empty|Ts]):-
	mandist(Empty, Tile, 1).
swap(Empty, Tile, [T1|Ts], [T1|Ts1]):-
	swap(Empty, Tile, Ts, Ts1).
mandist(X/Y, X1/Y1, D):-
	dif(X, X1, Dx),
	dif(Y, Y1, Dy),
	D is Dx + Dy.
dif(A, B, D):-
	D is A - B, D >= 0, !
	;
	D is B - A.
h([Empty|Tiles], H):-
	goal([Empty1|GoalSquares]),
	totdist(Tiles, GoalSquares, D),
	seq(Tiles, S)
	H is D + 3*S.
totdist([], [], 0).
totdist([Tile|Tiles], [Square|Squares], D):-
	mandist(Tile, Square, D1),
	totdist(Tile, Squares, D2),
	D is D1 + D2.
seq([Frist|OtherTiles], S):-
	seq([Frist|OtherTiles], First, S).
seq([Tile1, Tile2|Tiles], First, S):-
	score(Tile1, Tile2, S1),
	seq([Tile2|Tiles], First, S2),
	S is S1 + S2.