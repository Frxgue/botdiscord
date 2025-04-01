from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return """
    <html>
        <head>
            <title>Bot Discord de Modération</title>
            <link rel="stylesheet" href="https://cdn.replit.com/agent/bootstrap-agent-dark-theme.min.css">
            <style>
                body {
                    padding: 20px;
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    background-color: var(--bs-dark);
                    color: var(--bs-light);
                }
                .container {
                    max-width: 800px;
                    margin: 0 auto;
                }
                .feature-list {
                    margin-top: 20px;
                }
                .feature-item {
                    margin-bottom: 10px;
                    padding-left: 20px;
                    position: relative;
                }
                .feature-item:before {
                    content: '→';
                    position: absolute;
                    left: 0;
                    color: var(--bs-info);
                }
            </style>
        </head>
        <body>
            <div class="container mt-4">
                <h1 class="mb-4">Bot Discord de Modération</h1>
                <div class="alert alert-primary" role="alert">
                    Le bot Discord est en cours d'exécution dans le workflow "run_discord_bot".
                </div>
                
                <h2 class="mt-4">Fonctionnalités</h2>
                <div class="feature-list">
                    <div class="feature-item">Modération: kick, ban, mute, warn</div>
                    <div class="feature-item">Anti-invitation: bloquez les invitations Discord non autorisées</div>
                    <div class="feature-item">Filtre de mots: supprimez automatiquement les messages contenant des mots interdits</div>
                    <div class="feature-item">Système d'avertissements: suivez les avertissements des utilisateurs</div>
                    <div class="feature-item">Commandes propriétaire: fonctionnalités spéciales pour les propriétaires de serveur</div>
                </div>
                
                <h2 class="mt-4">Commandes</h2>
                <div class="feature-list">
                    <div class="feature-item">!ban [user_id] [raison] - Bannir un utilisateur</div>
                    <div class="feature-item">!mute [@user] [durée] [raison] - Mettre un utilisateur en sourdine</div>
                    <div class="feature-item">!warn [@user] [raison] - Donner un avertissement</div>
                    <div class="feature-item">!warnings [@user] - Voir les avertissements d'un utilisateur</div>
                    <div class="feature-item">!anti-invite [on|off] - Activer/désactiver le système anti-invitation</div>
                    <div class="feature-item">!blocword [mot] - Ajouter un mot à la liste noire</div>
                    <div class="feature-item">!clear [nombre] - Supprimer des messages</div>
                </div>
            </div>
        </body>
    </html>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)