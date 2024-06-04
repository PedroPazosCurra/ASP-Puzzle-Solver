
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
:- speaks(A,L), person(A), not language(L).
:- speaks(A,L), not person(A), language(L).
:- speaks(A,L), not person(A) , not language(L).
:- speaks(A,L), speaks(A,L'), L!=L'.
:- next_to(P,P'), P == P'.

%% seats_number(N) -> seat(1..N)
seat(1..N) :- seats_number(N).

%% Reglas next_to(X,Y)
:- next_to(X, Y), person(X), person(Y), seated(X,N), seated(Y,M), seats_number(S), |(N\S)- (M\S)| != 1.
:- next_to(X, L), person(X), language(L), seated(X,N), seated(Y,M), speaks(Y,L), seats_number(S), |(N\S)- (M\S)| != 1.
:- next_to(L, X), person(X), language(L), seated(X,N), seated(Y,M), speaks(Y,L), seats_number(S), |(N\S)- (M\S)| != 1.
:- next_to(L, L'), language(L), language(L'), seated(X,N), seated(Y,M), speaks(X,L), speaks(Y,L'), seats_number(S), |(M\S)- (N\S)| != 1.

%% Reglas not_next_to(X,Y)
:- not_next_to(X, Y), person(X), person(Y), seated(X,N), seated(Y,M), seats_number(S), |(N\S)- (M\S)| = 1.
:- not_next_to(X, L), person(X), language(L), seated(X,N), seated(Y,M), speaks(Y,L), seats_number(S), |(N\S)- (M\S)| = 1.
:- not_next_to(L, X), person(X), language(L), seated(X,N), seated(Y,M), speaks(Y,L), seats_number(S), |(N\S)- (M\S)| = 1.
:- not_next_to(L, L'), language(L), language(L'), seated(X,N), seated(Y,M), speaks(X,L), speaks(Y,L'), seats_number(S), |(M\S)- (N\S)| = 1.

%% Reglas opposite(X,Y)
:- opposite(X,Y), person(X), person(Y), seated(X,N), seats_number(SIZE), not seated(Y, (N+(SIZE/2))).

%% Genera átomo final seated(X,n).
1 {seated(P,N) : person(P)} 1 :- seat(N).
:- seated(P,N), seated(P,M), N!=M.
:- seated(P,N), seated(P',N), P!=P'.

#show seated/2.