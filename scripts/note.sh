#!/usr/bin/env bash
# Ajoute une entrée datée à notes.md, en te posant les questions du modèle.

read -p "Étape (ex: 1.1 Lire l'export) : " step
read -p "Ce que j'ai fait : " did
read -p "Pourquoi : " why
read -p "Commande ou code clé : " code
read -p "Ce que j'ai appris : " learned
read -p "Question restante : " question

{
  echo ""
  echo "### $(date +%F) Étape $step"
  echo "- **Ce que j'ai fait :** $did"
  echo "- **Pourquoi :** $why"
  echo "- **Commande ou code clé :** \`$code\`"
  echo "- **Ce que j'ai appris :** $learned"
  echo "- **Question restante :** $question"
} >> notes.md

echo "Entrée ajoutée à notes.md"