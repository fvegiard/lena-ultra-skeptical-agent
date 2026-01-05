#!/usr/bin/env bash
set -e

# Couleurs pour l'affichage
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# URLs des fichiers
REPO_URL="https://raw.githubusercontent.com/fvegiard/lena-ultra-skeptical-agent/main"
LENA_MD_URL="$REPO_URL/lena.md"

# Répertoires
CLAUDE_DIR="$HOME/.claude"
AGENTS_DIR="$CLAUDE_DIR/agents"
LENA_FILE="$AGENTS_DIR/lena.md"
BASHRC="$HOME/.bashrc"

echo -e "${BLUE}"
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║     Installation de Lena - Agent Ultra-Sceptique              ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Vérifier que Claude Code CLI est installé
echo -e "${YELLOW}[1/5]${NC} Vérification de Claude Code CLI..."
if ! command -v claude &> /dev/null; then
    echo -e "${RED}❌ ERREUR: Claude Code CLI n'est pas installé${NC}"
    echo ""
    echo "Installez-le d'abord avec:"
    echo "  npm install -g @anthropic-ai/claude-code"
    echo ""
    echo "Ou avec Bun (recommandé):"
    echo "  bun install -g @anthropic-ai/claude-code"
    echo ""
    exit 1
fi
echo -e "${GREEN}✅ Claude Code CLI détecté$(NC)"

# Créer le répertoire ~/.claude/agents si nécessaire
echo -e "${YELLOW}[2/5]${NC} Création du répertoire des agents..."
if [ ! -d "$AGENTS_DIR" ]; then
    mkdir -p "$AGENTS_DIR"
    echo -e "${GREEN}✅ Répertoire créé: $AGENTS_DIR${NC}"
else
    echo -e "${GREEN}✅ Répertoire existant: $AGENTS_DIR${NC}"
fi

# Télécharger lena.md
echo -e "${YELLOW}[3/5]${NC} Téléchargement de la définition de Lena..."
if command -v curl &> /dev/null; then
    curl -fsSL "$LENA_MD_URL" -o "$LENA_FILE"
elif command -v wget &> /dev/null; then
    wget -q "$LENA_MD_URL" -O "$LENA_FILE"
else
    echo -e "${RED}❌ ERREUR: curl ou wget requis${NC}"
    exit 1
fi

if [ -f "$LENA_FILE" ]; then
    echo -e "${GREEN}✅ Lena téléchargée: $LENA_FILE${NC}"
else
    echo -e "${RED}❌ ERREUR: Échec du téléchargement${NC}"
    exit 1
fi

# Ajouter l'alias dans ~/.bashrc
echo -e "${YELLOW}[4/5]${NC} Configuration de l'alias..."
ALIAS_LINE="alias lena='claude --agent lena'"

if grep -q "alias lena=" "$BASHRC" 2>/dev/null; then
    echo -e "${YELLOW}⚠️  Alias 'lena' déjà présent dans $BASHRC${NC}"
else
    echo "" >> "$BASHRC"
    echo "# Agent Lena - Ultra-sceptique" >> "$BASHRC"
    echo "$ALIAS_LINE" >> "$BASHRC"
    echo -e "${GREEN}✅ Alias ajouté à $BASHRC${NC}"
fi

# Vérifier l'installation
echo -e "${YELLOW}[5/5]${NC} Vérification de l'installation..."
if claude --agent lena --print &> /dev/null; then
    echo -e "${GREEN}✅ Installation réussie !${NC}"
else
    echo -e "${RED}❌ L'agent Lena ne semble pas fonctionner${NC}"
    echo "Vérifiez manuellement avec: claude --agent lena --print"
fi

# Instructions finales
echo ""
echo -e "${GREEN}"
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║                  ✅ Installation terminée !                    ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo -e "${NC}"
echo ""
echo "📝 Prochaines étapes:"
echo ""
echo "1. Recharger votre .bashrc:"
echo -e "   ${BLUE}source ~/.bashrc${NC}"
echo ""
echo "2. Tester Lena:"
echo -e "   ${BLUE}lena${NC}"
echo "   ou"
echo -e "   ${BLUE}claude --agent lena${NC}"
echo ""
echo "3. Exemples d'utilisation:"
echo -e "   ${BLUE}lena \"Vérifie ce fichier app.py\"${NC}"
echo -e "   ${BLUE}lena \"Audite la sécurité du projet\"${NC}"
echo ""
echo "📚 Documentation:"
echo "   https://github.com/fvegiard/lena-ultra-skeptical-agent"
echo ""
echo -e "${YELLOW}💡 Rappel:${NC} Lena ne croit que ce qu'elle peut LIRE et PROUVER !"
echo ""
