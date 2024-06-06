%person(a;b;c).
%type(house, V) :- house(V).
%house(1..3).
%living_place(house, V) :- house(V).
%type(pet, V) :- pet(V).
%pet(dog;cat;mouse;).
%type(color, V) :- color(V).
%color(red;blue;yellow).
%has(a,pet,cat).
%has(b,pet,dog).
%same_place(dog,red).
%same_place(cat,yellow).
%neighbor(dog,red).
%neighbor(a,b).

% Filtrado previo de entradas erróneas en cuanto a lógica de puzzle
:- same_place(X,Y), person(X), not type(_,Y).
:- same_place(X,Y), not type(_,X), person(Y).
:- same_place(X,Y), not type(_,X), not type(_,Y).
:- same_place(X,Y), not person(X), not type(_,X).
:- same_place(X,Y), not person(Y), not type(_,Y).
:- same_place(X,Y), person(X), person(Y).
:- not living_place(_,_).

% Reglas para determinar cosas de un elem. central (oculto a llm)
place_of(X,N) :- has(P,_,X), has(P,Y,N), X!=N, living_place(Y,N).
place_of(P,N) :- has(P,Y,N), living_place(Y,N).
type(P, V) :- living_place(P,V).

% Generar soluciones
1 { has(X,T,V): person(X) } 1 :- type(T,V).
:- has(X,T,V), has(X,T,V'), V!=V'.

%%%%%%%%%%%%%%%%%%%%%%%%%%   Interfaz de LLM   %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% place_number( X, nº) para predicados numéricos
%:- place_number(X,N), not person(X), living_place(_,N), has(P,_,N), not has(P,_,X).
%:- place_number(P,N), person(P), living_place(L,N), not has(P,L,N).

%%% Predicados numéricos: 
%same_place (X, nº) 
:- same_place(X,N), not person(X), living_place(_,N), has(P,_,N), not has(P,_,X).
:- same_place(N,X), not person(X), living_place(_,N), has(P,_,N), not has(P,_,X).
:- same_place(P,N), person(P), living_place(L,N), not has(P,L,N).

%%% Predicados de vecindario / cruzados
% same_place(X,Y).
:- same_place(X,Y), place_of(X,H), place_of(Y,H'), H!=H'.
1 {has(P,T,X): person(P)} 1 :- same_place(X,Y), type(T,X).
1 {has(P,T,Y): person(P)} 1 :- same_place(X,Y), type(T,Y).

% next_to(X, Y)
:- next_to(X,Y), place_of(X,H), place_of(Y,H'), |H-H'| != 1.
:- next_to(X,Y), X==Y.
:- next_to(X,Y), same_place(X,Y).
next_to(Y,X) :- next_to(X,Y).

% left(X,Y), right(X,Y)
:- left(X,Y), place_of(X,H), place_of(Y,H'), X!=Y, H!=(H'-1).
:- right(X,Y), place_of(X,H), place_of(Y,H'), X!=Y, H!=(H'+1).
next_to(X,Y), right(Y,X) :- left(X,Y).
next_to(X,Y), left(Y,X) :- right(X,Y).

#show has/3.