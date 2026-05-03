from __future__ import annotations
from typing import List, Dict, TYPE_CHECKING
from collections import deque

if TYPE_CHECKING:
    from core.graph import Graph

from animation.events import (
    make_step,
    VISIT_NODE, RELAX_EDGE, REJECT_EDGE, FINAL_PATH,
)

def bellman(graph: "Graph", source: int) -> List[Dict]:
    """
    Calcule les plus courts chemins à source unique pour un Graphe Orienté Sans Circuit (DAG).
    
    Cet algorithme correspond à la version simplifiée de Bellman pour les graphes 
    sans circuit. Il utilise un tri topologique pour s'assurer qu'un sommet est 
    traité uniquement lorsque tous ses prédécesseurs l'ont été.

    Complexité
    ----------
    Temps  : O(V + E) - très efficace grâce au tri topologique.
    Espace : O(V) - un simple tableau 1D suffit.
    """
    steps: List[Dict] = []

    if source not in graph.nodes:
        raise KeyError(f"Le nœud source {source} n'existe pas dans le graphe.")
    
    if not graph.directed:
        raise ValueError("L'algorithme pour graphes sans circuit nécessite un graphe orienté (DAG).")

    INF = float("inf")
    node_ids = list(graph.nodes.keys())
    V = len(node_ids)

    # 1. Construction de la liste d'adjacence et calcul des degrés entrants (in-degree)
    adj: Dict[int, List[tuple]] = {n: [] for n in node_ids}
    in_degree: Dict[int, int] = {n: 0 for n in node_ids}

    for src, dest, weight in graph.edges:
        adj[src].append((dest, weight))
        in_degree[dest] += 1

    # 2. Tri Topologique (Algorithme de Kahn)
    # Permet de trouver un ordre où chaque sommet est visité après tous ses prédécesseurs
    queue = deque([n for n in node_ids if in_degree[n] == 0])
    topo_order = []

    while queue:
        u = queue.popleft()
        topo_order.append(u)
        for v, w in adj[u]:
            in_degree[v] -= 1
            if in_degree[v] == 0:
                queue.append(v)

    if len(topo_order) != V:
        raise ValueError("Un circuit a été détecté. Ce graphe n'est pas un DAG.")

    # 3. Initialisation des distances (1D au lieu de 2D)
    dist: Dict[int, float] = {n: INF for n in node_ids}
    prev: Dict[int, int | None] = {n: None for n in node_ids}
    dist[source] = 0.0

    # Émettre VISIT_NODE pour la source
    steps.append(make_step(VISIT_NODE, node=source))

    # 4. Boucle principale : relaxation selon l'ordre topologique
    for u in topo_order:
        # Si le nœud u n'est pas atteignable, il ne peut pas relaxer ses voisins
        if dist[u] == INF:
            for v, w in adj[u]:
                steps.append(make_step(REJECT_EDGE, src=u, dest=v))
            continue

        for v, w in adj[u]:
            new_dist = dist[u] + w

            if new_dist < dist[v]:
                first_visit = (dist[v] == INF)
                dist[v] = new_dist
                prev[v] = u
                
                steps.append(make_step(RELAX_EDGE, src=u, dest=v, weight=w))
                
                if first_visit:
                    steps.append(make_step(VISIT_NODE, node=v))
            else:
                steps.append(make_step(REJECT_EDGE, src=u, dest=v))

    # 5. Reconstruire et émettre FINAL_PATH pour chaque nœud atteignable
    for target in node_ids:
        if target == source:
            steps.append(make_step(FINAL_PATH, path=[source]))
            continue

        if dist[target] == INF:
            continue

        path: List[int] = []
        current: int | None = target
        
        # Le graphe est garanti sans circuit, mais on garde une sécurité par habitude
        visited_check: set = set()

        while current is not None:
            if current in visited_check:
                break
            visited_check.add(current)
            path.append(current)
            current = prev[current]

        path.reverse()

        if path and path[0] == source:
            steps.append(make_step(FINAL_PATH, path=path))

    return steps
