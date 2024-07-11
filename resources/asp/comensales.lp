
%% Generado por LLM

%seats_number(4).
%person(a; b; c; d).
%language(german; french; spanish; russian).
%speaks(a, german).
%speaks(b, spanish).
%speaks(c, french).
%speaks(d, russian).

%next_to(a,b).
%next_to(a, russian).
%not_next_to(b, french).
%opposite(a,c).

%% Prohibiciones para la entrada (filtrar entradas incorrectas ya)
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

neighbor(X,Y) :- person(X), person(Y), seated(X,S), seated(Y,M), seats_number(S), X !=Y, S <= 2.
neighbor(X,Y) :- person(X), person(Y), seated(X,S), seated(Y,M), seats_number(S), X !=Y, M != S,  M\(S-2) == 1.
neighbor(X,Y) :- person(X), person(Y), seated(X,N), seated(Y,S), seats_number(S), X !=Y, N != S,  N\(S-2) == 1.
neighbor(X,Y) :- person(X), person(Y), seated(X,N), seated(Y,M), seats_number(S), X !=Y, N != S, M != S,  |N- M| == 1.
neighbor(Y,X) :- neighbor(X,Y), X != Y.

%% Reglas next_to(X,Y)
:- next_to(X, Y), not neighbor(X, Y).
:- next_to(X, L), person(X), language(L), speaks(Y,L), not neighbor(X,Y).
:- next_to(L, X), person(X), language(L), speaks(Y,L), not neighbor(X,Y).
:- next_to(L, L'), language(L), language(L'), speaks(X,L), speaks(Y,L'), not neighbor(X, Y).

%% Reglas not_next_to(X,Y)
:- not_next_to(X, Y), neighbor(X, Y).
:- not_next_to(X, L), person(X), language(L), speaks(Y,L), neighbor(X,Y).
:- not_next_to(L, X), person(X), language(L), speaks(Y,L), neighbor(X,Y).
:- not_next_to(L, L'), language(L), language(L'), speaks(X,L), speaks(Y,L'), neighbor(X,Y).

%% Reglas opposite(X,Y)
:- opposite(X,Y), person(X), person(Y), seated(X,N), seats_number(SIZE), N == SIZE/2,  not seated(Y, 1). 
:- opposite(X,Y), person(X), person(Y), seated(X,N), seats_number(SIZE), N != SIZE/2, not seated(Y, ((N+(SIZE/2))\SIZE)).

%% Genera átomo final seated(X,n).
1 {seated(P,N) : person(P)} 1 :- seat(N).
:- seated(P,N), seated(P,M), N!=M.
:- seated(P,N), seated(P',N), P!=P'.

#show seated/2.