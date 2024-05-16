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


% Representación interna: el LLM no tiene por qué saberla
type(house,V) :- house(V).
type(color,V) :- color(V).
type(pet,V) :- pet(V).
type(beverage,V) :- beverage(V).
type(tobacco,V) :- tobaccobrand(V).

:- smokes(P,B), not has(P,tobacco,B).
:- drinks(P,B), not has(P,beverage,B).
:- keeps_pet(P,Q), not has(P,pet,Q).
:- house_color(P,C), not has(P,color,C).

:- neighbor(P,P'), has(P,house,H), has(P',house,H'), H'!=H-1, H'!=H+1.

1 { has(X,T,V): person(X) } 1 :- type(T,V).
:- has(X,T,V), has(X,T,V'), V!=V'.

#show has/3.