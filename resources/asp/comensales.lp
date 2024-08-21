
%% Filtrado de entradas incorrectas
:- next_to(X,Y), not person(X), not language(X).
:- next_to(X,Y), not person(Y), not language(Y).
:- next_to(P,P'), P == P'.
:- not_next_to(X,Y), not person(X), not language(X).
:- not_next_to(X,Y), not person(Y), not language(Y).
:- not_next_to(P,P'), P == P'.
:- speaks(A,L), person(A), not language(L).
:- speaks(A,L), not person(A), language(L).
:- speaks(A,L), not person(A) , not language(L).
:- speaks(A,L), speaks(A,L'), L!=L'.
:- opposite(P,P'), not person(P).
:- opposite(P,P'), not person(P').
:- opposite(P,P'), P == P'.

%% seats_number(N) -> seat(1..N)
seat(1..N) :- seats_number(N).

neighbor(X,Y) :- person(X), person(Y), seated(X,S), seated(Y,M), seats_number(S), X !=Y, S <= 3.
neighbor(X,Y) :- person(X), person(Y), seated(X,S), seated(Y,M), seats_number(S), X !=Y, M != S,  M\(S-2) == 1.
neighbor(X,Y) :- person(X), person(Y), seated(X,N), seated(Y,S), seats_number(S), X !=Y, N != S,  N\(S-2) == 1.
neighbor(X,Y) :- person(X), person(Y), seated(X,N), seated(Y,M), seats_number(S), X !=Y, N != S, M != S,  |N- M| == 1.
neighbor(Y,X) :- neighbor(X,Y), X != Y.

%% next_to(X,Y)
:- next_to(X, Y), person(X), person(Y), not neighbor(X, Y).
:- next_to(X, L), seats_number(S), S > 3, person(X), language(L), person(Y), speaks(Y,L), not neighbor(X,Y).
:- next_to(L, X), seats_number(S), S > 3, person(X), language(L), person(Y), speaks(Y,L), not neighbor(X,Y).

%% not_next_to(X,Y)
:- not_next_to(X, Y), person(X), person(Y), neighbor(X, Y).
:- not_next_to(X, L), person(X), language(L), speaks(Y,L), neighbor(X,Y).
:- not_next_to(L, X), person(X), language(L), speaks(Y,L), neighbor(X,Y).

%% opposite(X,Y)
:- opposite(X,Y), person(X), person(Y), seated(X,N), seats_number(SIZE), N == SIZE/2,  not seated(Y, 1). 
:- opposite(X,Y), person(X), person(Y), seated(X,N), seats_number(SIZE), N != SIZE/2, not seated(Y, ((N+(SIZE/2))\SIZE)).

%% Átomo final seated(X,n).
1 {seated(P,N) : person(P)} 1 :- seat(N).
:- seated(P,N), seated(P,M), N!=M.
:- seated(P,N), seated(P',N), P!=P'.

#show seated/2.