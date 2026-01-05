#!/usr/bin/env python3
"""
Exemple d'utilisation de l'agent Lena avec le Claude Agent SDK.

Ce script montre comment intégrer Lena dans une application Python
en utilisant le SDK et en chargeant la configuration depuis ~/.claude/

Prérequis:
  pip install claude-agent-sdk

Authentification:
  Le SDK utilise automatiquement les credentials OAuth de Claude Code CLI
  stockés dans ~/.claude/.credentials.json
  
  AUCUNE configuration manuelle d'API key n'est nécessaire !
"""

import asyncio
from claude_agent_sdk import ClaudeAgent, ClaudeAgentOptions


async def verify_code_with_lena(code_file: str):
    """
    Utilise l'agent Lena pour vérifier un fichier de code.
    
    Args:
        code_file: Chemin vers le fichier à vérifier
    """
    print(f"🔍 Vérification de {code_file} avec Lena...")
    
    agent = ClaudeAgent()
    
    # Options pour charger la config depuis ~/.claude/
    # settingSources permet de charger les agents définis dans ~/.claude/agents/
    options = ClaudeAgentOptions(
        setting_sources=["user", "project", "local"],
        allowed_tools=["Task"]  # Permet d'appeler des sous-agents
    )
    
    # Demander à Lena de vérifier le fichier
    prompt = f"Utilise lena pour auditer le fichier {code_file} et vérifier s'il respecte les bonnes pratiques de sécurité et de qualité."
    
    print("\n📋 Résultats de Lena:\n")
    
    async for message in agent.query(prompt=prompt, options=options):
        if hasattr(message, 'result'):
            print(message.result)
        elif hasattr(message, 'content'):
            print(message.content)


async def compare_implementations(file1: str, file2: str):
    """
    Utilise Lena pour comparer deux implémentations.
    
    Args:
        file1: Premier fichier
        file2: Deuxième fichier
    """
    print(f"⚖️  Comparaison de {file1} vs {file2} avec Lena...")
    
    agent = ClaudeAgent()
    
    options = ClaudeAgentOptions(
        setting_sources=["user", "project", "local"],
        allowed_tools=["Task", "Read", "Grep"]
    )
    
    prompt = f"""Utilise lena pour:
1. Lire RÉELLEMENT les fichiers {file1} et {file2}
2. Comparer les deux implémentations
3. Identifier les différences concrètes (avec numéros de ligne)
4. Recommander quelle version est meilleure (avec preuves)
"""
    
    print("\n📊 Rapport de comparaison:\n")
    
    async for message in agent.query(prompt=prompt, options=options):
        if hasattr(message, 'result'):
            print(message.result)


async def search_and_fix_error(error_message: str, file_path: str):
    """
    Utilise Lena pour rechercher une solution à une erreur et l'appliquer.
    
    Args:
        error_message: Message d'erreur complet
        file_path: Fichier où l'erreur se produit
    """
    print(f"🚨 Recherche de solution pour l'erreur dans {file_path}...")
    
    agent = ClaudeAgent()
    
    options = ClaudeAgentOptions(
        setting_sources=["user", "project", "local"],
        allowed_tools=["Task", "WebSearch", "WebFetch", "Read", "Edit"]
    )
    
    prompt = f"""Utilise lena pour:
1. Analyser cette erreur: {error_message}
2. Rechercher automatiquement sur Stack Overflow/GitHub
3. Lire le fichier {file_path} pour comprendre le contexte
4. Proposer une solution basée sur les résultats de recherche
5. Appliquer la correction si approuvée
6. TESTER que la correction fonctionne
"""
    
    print("\n🔧 Solution proposée:\n")
    
    async for message in agent.query(prompt=prompt, options=options):
        if hasattr(message, 'result'):
            print(message.result)


async def audit_security():
    """
    Utilise Lena pour faire un audit de sécurité complet du projet.
    """
    print("🔐 Audit de sécurité avec Lena...")
    
    agent = ClaudeAgent()
    
    options = ClaudeAgentOptions(
        setting_sources=["user", "project", "local"],
        allowed_tools=["Task", "Bash", "Grep", "Read"]
    )
    
    prompt = """Utilise lena pour faire un audit de sécurité complet:
1. Scanner tous les fichiers Python/JS
2. Chercher les secrets hardcodés
3. Détecter les injections SQL potentielles
4. Vérifier les eval/exec dangereux
5. Exécuter bandit (Python) et npm audit (JS)
6. Fournir un rapport avec sévérités (🔴🟠🟡🟢)
"""
    
    print("\n🛡️ Rapport de sécurité:\n")
    
    async for message in agent.query(prompt=prompt, options=options):
        if hasattr(message, 'result'):
            print(message.result)


# Exemples d'utilisation
if __name__ == "__main__":
    print("""
╔════════════════════════════════════════════════════════════════╗
║  Lena - Agent Ultra-Sceptique - Exemples Python SDK          ║
╚════════════════════════════════════════════════════════════════╝

Choisissez un exemple:
1. Vérifier un fichier de code
2. Comparer deux implémentations
3. Rechercher et corriger une erreur
4. Audit de sécurité complet
""")
    
    choice = input("Votre choix (1-4): ").strip()
    
    if choice == "1":
        file_path = input("Fichier à vérifier: ").strip()
        asyncio.run(verify_code_with_lena(file_path))
    
    elif choice == "2":
        file1 = input("Premier fichier: ").strip()
        file2 = input("Deuxième fichier: ").strip()
        asyncio.run(compare_implementations(file1, file2))
    
    elif choice == "3":
        error = input("Message d'erreur: ").strip()
        file_path = input("Fichier concerné: ").strip()
        asyncio.run(search_and_fix_error(error, file_path))
    
    elif choice == "4":
        asyncio.run(audit_security())
    
    else:
        print("❌ Choix invalide")
