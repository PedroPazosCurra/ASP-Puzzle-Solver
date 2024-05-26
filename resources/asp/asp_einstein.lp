% Predicados de tipo y de relación que se reciben de forma programática.

%   Predicados de tipo
%       tobaccobrand(B)
%       beverage(B)
%       pet(P)
%       color(C)

%   Predicados de relación
%       smokes(P, B)
%       drinks(P, B)
%       keepspet(P, M)
%       housecolor(P, C)
%       neighbor(P, P')

% Entrenar solo con has
% Probar a meter categoria banda (o a cualquiera)
% Meter predicado image(Cosa , Ruta).
% Preparar modelo de lenguaje puro1


% Representación interna: el LLM tiene que sacarla
%type(X,V) ;- house(V).
type(house,V) :- house(V).
type(color,V) :- color(V).
type(pet,V) :- pet(V).
type(beverage,V) :- beverage(V).
type(tobacco,V) :- tobacco_brand(V).

% Ruta de imagen para representar átomo: LLM lo sabe
%image(brittish, pics/england.png).

% Actualmente, sin uso: LLM sabe 'has(P,X,H)'
:- smokes(P,B), not has(P,tobacco,B).
:- drinks(P,B), not has(P,beverage,B).
:- keeps_pet(P,Q), not has(P,pet,Q).
:- house_color(P,C), not has(P,color,C).
:- house_number(P,N), not has(P, house, N).

% Reglas para determinar cosas de una casa
house_of(X,H) :- has(P,_,X), has(P,house,H).
house_of(P,H) :- has(P,house,H).

%  Manejar predicados cruzados: 
:- same_house(X,Y), house_of(X,H), house_of(Y,H'), H != H'.
:- neighbor(X,Y), house_of(X,H), house_of(Y,H'), |H-H'| != 1.
:- left_to(X,Y), house_of(X,H), house_of(Y,H'), H!=H'-1.
:- right_to(X,Y), house_of(X,H), house_of(Y,H'), H!=H'+1.

1 { has(X,T,V): person(X) } 1 :- type(T,V).
:- has(X,T,V), has(X,T,V'), V!=V'.

#show has/3.