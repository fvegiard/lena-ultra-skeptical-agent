# Lena - Agent Ultra-Sceptique pour Claude Code CLI

> **Agent ultra-sceptique qui ne prend JAMAIS rien pour acquis**

Lena est un agent spécialisé pour Claude Code CLI qui vérifie systématiquement le code réel, recherche automatiquement les erreurs sur internet, et ne fait jamais confiance à la documentation sans vérification.

## 🎯 Caractéristiques Principales

- ✅ **Vérification systématique** - Lit toujours le code source réel avec `Read`
- ✅ **Recherche automatique** - Utilise WebSearch/WebFetch pour chaque erreur rencontrée
- ✅ **Scan préventif** - Exécute flake8, bandit, eslint AVANT toute modification
- ✅ **Preuves obligatoires** - Ne dit jamais "c'est corrigé" sans montrer l'output des tests
- ✅ **Git workflow** - Vérifie git status et propose des commits après validation
- ✅ **Outils complets** - Read, Write, Edit, Grep, Glob, Bash, WebSearch, WebFetch, TodoWrite

## 📦 Installation

### Installation Automatique (Recommandée)

```bash
# Télécharger et exécuter le script d'installation
curl -fsSL https://raw.githubusercontent.com/fvegiard/lena-ultra-skeptical-agent/main/install.sh | bash
```

### Installation Manuelle

1. **Créer le répertoire des agents (si nécessaire)**
   ```bash
   mkdir -p ~/.claude/agents
   ```

2. **Télécharger la définition de l'agent**
   ```bash
   curl -o ~/.claude/agents/lena.md \
     https://raw.githubusercontent.com/fvegiard/lena-ultra-skeptical-agent/main/lena.md
   ```

3. **Ajouter l'alias dans ~/.bashrc**
   ```bash
   echo "# Agent Lena - Ultra-sceptique" >> ~/.bashrc
   echo "alias lena='claude --agent lena'" >> ~/.bashrc
   source ~/.bashrc
   ```

4. **Vérifier l'installation**
   ```bash
   claude --agent lena --print
   ```

## 🚀 Utilisation

### Dans Claude Code CLI

```bash
# Méthode 1: Via l'alias
lena

# Méthode 2: Via claude --agent
claude --agent lena

# Méthode 3: Avec une question directe
claude --agent lena "Vérifie si ce fichier app.py respecte les bonnes pratiques"
```

### Avec l'Agent SDK (Python)

```python
from claude_agent_sdk import ClaudeAgent, ClaudeAgentOptions

async def use_lena():
    agent = ClaudeAgent()
    
    async for message in agent.query(
        prompt="Utilise lena pour vérifier ce code",
        options=ClaudeAgentOptions(
            setting_sources=["user", "project", "local"],  # Charge ~/.claude/
            allowed_tools=["Task"]  # Permet d'appeler des sous-agents
        )
    ):
        print(message.result)
```

Voir [example.py](example.py) pour un exemple complet.

## 🔧 Configuration

### Outils Disponibles

Lena a accès à tous les outils nécessaires pour une vérification complète:

| Outil | Usage |
|-------|-------|
| **Read** | Lire le code source réel |
| **Write** | Créer des fichiers de rapport |
| **Edit** | Corriger le code après validation |
| **Grep** | Chercher des patterns (secrets, injections SQL, etc.) |
| **Glob** | Trouver des fichiers par pattern |
| **Bash** | Exécuter des outils (flake8, bandit, eslint, git) |
| **WebSearch** | Rechercher des erreurs sur Stack Overflow/GitHub |
| **WebFetch** | Lire la documentation en ligne |
| **TodoWrite** | Planifier et suivre les corrections |

### Mode de Permission

```yaml
permissionMode: acceptEdits
```

Lena accepte automatiquement les modifications de fichiers (Edit/Write) pour corriger les problèmes identifiés.

## 📖 Principes de Lena

### 1. LIRE avant croire
- ❌ Faire confiance aux README ou documentation
- ✅ Toujours lire le code source avec `Read`

### 2. SCANNER avant modifier
- ❌ Modifier directement le code
- ✅ Scanner avec flake8, bandit, eslint, hadolint selon le langage

### 3. RECHERCHER chaque erreur
- ❌ Deviner la solution
- ✅ Rechercher l'erreur sur WebSearch → Stack Overflow/GitHub

### 4. PROUVER avant affirmer
- ❌ "Bug corrigé"
- ✅ "Bug corrigé, test passé: [output]"

### 5. DOUTER systématiquement
- Documentation = **suspect** jusqu'à vérification
- README = **non fiable** jusqu'à confirmation
- Seule vérité = **le code qui s'exécute**

## 📋 Workflow de Lena

### Étape 1: INVENTAIRE
```bash
find . -name "*.py" -o -name "*.js"
tree -L 3 -I 'node_modules|.git'
git status
```

### Étape 2: LECTURE RÉELLE
- Lire chaque fichier mentionné avec `Read`
- Analyser si les claims correspondent au code réel
- Signaler toute divergence

### Étape 3: SCAN SÉCURITÉ
```bash
# Secrets hardcodés
grep -rn "password\|secret\|api.key" . --exclude-dir={node_modules,.git}

# Injections SQL
grep -n 'f".*SELECT\|f".*INSERT' *.py

# eval/exec dangereux
grep -rn "eval(\|exec(\|os.system(" . --exclude-dir={node_modules,.git}
```

### Étape 4: SCAN PAR LANGAGE

**Python:**
```bash
python3 -m py_compile fichier.py  # Syntaxe
flake8 fichier.py                  # Style
bandit -r fichier.py               # Sécurité
```

**JavaScript:**
```bash
npx eslint fichier.js              # Lint
npm audit                          # Sécurité dépendances
```

**Docker:**
```bash
hadolint Dockerfile                # Best practices
```

### Étape 5: RECHERCHE AUTOMATIQUE
Si erreur rencontrée:
1. Capturer l'erreur exacte: `commande 2>&1 | tee error.log`
2. WebSearch: `"[message erreur] python"`
3. Analyser Stack Overflow, GitHub Issues
4. Appliquer et tester la solution

### Étape 6: VALIDATION
```bash
python3 fichier.py    # Ou npm test, etc.
git diff              # Vérifier les changements
git status            # État final
```

## 💡 Exemples d'Utilisation

### Exemple 1: Vérification de Claims
```bash
$ lena
User: "L'agent supporte température 0"

Lena:
1. Je lis le code de l'agent...
   [utilise Read pour lire le fichier]

2. Je cherche le paramètre temperature...
   [utilise Grep pour chercher "temperature"]

3. RÉSULTAT:
   ❌ CLAIM DOUTEUX
   - Claim: "supporte température 0"
   - Réalité: Aucune mention de "temperature" dans le code
   - Fichiers vérifiés: [liste]

4. Je recherche sur le web...
   [WebSearch "Claude Code CLI temperature parameter"]

5. CONCLUSION BASÉE SUR FAITS:
   La température n'est PAS configurable au niveau agent.
   Preuve: [citations exactes]
```

### Exemple 2: Audit de Sécurité
```bash
$ lena "Audite ce fichier app.py pour la sécurité"

Lena:
1. Lecture du fichier app.py... ✅
   [Read app.py]

2. Scan sécurité...
   🔴 CRITIQUE: Secret hardcodé ligne 8
   🔴 CRITIQUE: SQL injection ligne 13
   🟡 MOYENNE: print() au lieu de logging ligne 14

3. Recherche solutions...
   [WebSearch pour chaque problème]

4. Table de corrections:
   | # | Sévérité | Problème | Solution |
   |---|----------|----------|----------|
   | 1 | 🔴 | Secret | Env var |
   | 2 | 🔴 | SQL inj | Paramétré |
   | 3 | 🟡 | print | logging |

5. Application des corrections... ✅
6. Tests de validation... ✅
7. Proposition de commit Git... ✅
```

## ⚙️ Intégration avec Autres Agents

Lena peut être utilisé comme sous-agent dans des workflows complexes:

```python
# Dans un autre agent ou workflow
Task("Vérifie la sécurité avec un audit sceptique", subagent_type="lena")
```

## 🔍 Anti-Patterns

| ❌ Ne jamais faire | ✅ Faire à la place |
|-------------------|---------------------|
| "Selon le README..." | "J'ai lu le fichier avec Read..." |
| "La doc dit qu'il y a X" | "J'ai compté avec find, il y a X" |
| "Je suppose que..." | "J'ai analysé ligne X-Y, il fait..." |
| "L'erreur vient probablement de..." | "J'ai recherché sur Stack Overflow..." |
| "C'est corrigé" | "Test passé, output: [...]" |

## 🛠️ Dépannage

### Lena ne répond pas
```bash
# Vérifier que le fichier existe
ls -la ~/.claude/agents/lena.md

# Vérifier la syntaxe YAML
head -20 ~/.claude/agents/lena.md

# Tester directement
claude --agent lena --print
```

### Erreur "agent not found"
```bash
# Réinstaller
curl -o ~/.claude/agents/lena.md \
  https://raw.githubusercontent.com/fvegiard/lena-ultra-skeptical-agent/main/lena.md
```

### L'alias ne fonctionne pas
```bash
# Recharger .bashrc
source ~/.bashrc

# Ou utiliser directement
claude --agent lena
```

## 📚 Ressources

- [Documentation Claude Code CLI](https://code.claude.com/docs)
- [Agent SDK Documentation](https://platform.claude.com/docs/en/agent-sdk/overview)
- [Repository GitHub](https://github.com/fvegiard/lena-ultra-skeptical-agent)

## 🤝 Contribution

Les contributions sont les bienvenues! Pour dupliquer et personnaliser Lena:

1. Fork ce repository
2. Modifier `lena.md` selon vos besoins
3. Tester avec `claude --agent lena`
4. Soumettre une Pull Request

## 📄 Licence

MIT License - Utilisez et modifiez librement

---

**Rappel**: Lena ne croit que ce qu'elle peut LIRE dans le code et PROUVER par l'exécution. 🔍