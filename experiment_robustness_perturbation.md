# Expérience : Robustesse face aux perturbations

## Objectif
Tester ce qui se passe lorsque l'environnement change pendant la mission d'un agent de livraison.

## Scénario
Agent livraison :
- Normal : Route A libre
- Puis : Route A bloquée

### Résultat attendu
- Sans Environment Learning : l'agent continue son plan initial et échoue.
- Avec Environment Learning : l'agent met à jour son modèle, choisit un nouveau chemin et réussit.

## Mesure
- Recovery Rate γ : capacité à récupérer après perturbation.
- Plus γ est élevé, plus l'agent est robuste.

## Comparaison attendue
- Baseline sans apprentissage : échec frequent
- Avec apprentissage de l'environnement : récupération élevée

## Fichier associé
- `simulation_robustness_perturbation.py` : script de simulation comparant un agent baseline et un agent qui met à jour son modèle.
