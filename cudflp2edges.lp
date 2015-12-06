edge(N1,V1,N2,V2) :- conflict(N1,V1,ID), satisfies(N2,V2,ID).
edge(N1,V1,N2,V2) :- depends(N1,V1,ID), satisfies(N2,V2,ID).
edge(N1,V1,N2,V2) :- recommends(N1,V1,ID), satisfies(N2,V2,ID).
#show edge/4.