# Expérience : Influence de la précision du modèle d'environnement sur la fiabilité de l'agent

## Objectif
Montrer que lorsque la précision du modèle d'environnement augmente, la fiabilité de l'agent augmente également.

## Contexte
La fiabilité d'un agent dépend souvent de la qualité du modèle qu'il utilise pour prédire les effets de ses actions. Dans cette expérience, nous considérons un agent simple qui agit dans un environnement stochastique.

## Méthodologie
1. Définir un environnement de référence avec des transitions et des récompenses.
2. Construire plusieurs versions d'un modèle d'environnement de précision croissante.
3. Simuler un agent qui choisit des actions en se basant sur le modèle.
4. Mesurer la fiabilité de l'agent en fonction de la précision du modèle.

## Mesures
- Précision du modèle : rapport entre les prédictions du modèle et la réalité de l'environnement.
- Fiabilité de l'agent : taux de réussite, score moyen ou erreur moyenne sur une série de trajets.

## Interprétation attendue
- Une précision faible du modèle conduit à des décisions sous-optimales et une fiabilité réduite.
- Une précision élevée du modèle conduit à des décisions plus robustes et une fiabilité accrue.

## Fichiers associés
- `simulation_environment_agent_reliability.py` : script de simulation pour tester différentes précisions du modèle.
