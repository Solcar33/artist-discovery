#!/usr/bin/env bash
# Ajoute une entrée datée à notes.md, en te posant les questions du modèle.

read -e -p "Étape (ex: 1.1 Lire l'export) : " step
read -e -p "Ce que j'ai fait : " did
read -e -p "Pourquoi : " why
read -e -p "Commande ou code clé : " code
read -e -p "Ce que j'ai appris : " learned
read -e -p "Question restante : " question

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