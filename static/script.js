// static/script.js

// Fonctions utilitaires
function formatEuro(number) {
    if (number === null || number === undefined) return 'Non spécifié';
    return new Intl.NumberFormat('fr-FR', { style: 'currency', currency: 'EUR' }).format(number);
}

function formatNumber(number) {
    if (number === null || number === undefined) return 'Non spécifié';
    return new Intl.NumberFormat('fr-FR').format(number);
}

// Fonction pour afficher les erreurs
function displayError(message) {
    document.getElementById('resultContent').innerHTML = `
        <div class="error-message">
            ${message}
        </div>
    `;
}

// Fonction pour afficher les résultats de recherche
// static/script.js

// ... (autres fonctions inchangées)

function displaySearchResults(results) {
    const resultDiv = document.getElementById('resultContent');
    
    if (!results || results.length === 0) {
        resultDiv.innerHTML = '<div class="info-message">Aucun résultat trouvé</div>';
        return;
    }

    let html = `
        <div class="results-summary">
            <h3>Résultats trouvés: ${results.length}</h3>
        </div>
        <div class="results-grid">
    `;

    results.forEach(opp => {
        // Vérifier et nettoyer l'ID avant affichage
        const opportunityId = opp.id || 'Non spécifié';
        
        html += `
            <div class="result-card ${opp.est_exploitable ? 'exploitable' : 'non-exploitable'}">
                <div class="opportunity-header">
                    <h3>Opportunité ${opportunityId}</h3>
                </div>
                
                <div class="status-section ${opp.est_exploitable ? 'success' : 'warning'}">
                    <h4>Statut: ${opp.est_exploitable ? 'Exploitable' : 'Non Exploitable'}</h4>
                    ${!opp.est_exploitable && opp.raisons_non_exploitable ? `
                        <div class="warning-details">
                            <ul>
                                ${opp.raisons_non_exploitable.map(raison => `<li>${raison}</li>`).join('')}
                            </ul>
                        </div>
                    ` : ''}
                </div>

                <div class="main-info-section">
                    <h4>Informations principales</h4>
                    <div class="info-grid">
                        <div class="info-item">
                            <label>Âge :</label>
                            <span>${formatNumber(opp.informations_principales?.age)} ans</span>
                        </div>
                        <div class="info-item">
                            <label>Revenu mensuel :</label>
                            <span>${formatEuro(opp.informations_principales?.revenu_mensuel)}</span>
                        </div>
                        <div class="info-item">
                            <label>Banque :</label>
                            <span>${opp.informations_principales?.banque || 'Non spécifiée'}</span>
                        </div>
                    </div>
                </div>

                ${opp.details_complementaires ? `
                    <div class="details-section">
                        <h4>Détails complémentaires</h4>
                        <div class="info-grid">
                            <div class="info-item">
                                <label>Type de bien :</label>
                                <span>${opp.details_complementaires.type_bien || 'Non spécifié'}</span>
                            </div>
                            <div class="info-item">
                                <label>Usage du bien :</label>
                                <span>${opp.details_complementaires.usage_bien || 'Non spécifié'}</span>
                            </div>
                            <div class="info-item">
                                <label>Type de projet :</label>
                                <span>${opp.details_complementaires.type_projet || 'Non spécifié'}</span>
                            </div>
                        </div>
                    </div>
                ` : ''}
            </div>
        `;
    });

    html += '</div>';
    resultDiv.innerHTML = html;
}

// Fonction pour formatter les nombres
function formatNumber(number) {
    if (number === null || number === undefined) return 'Non spécifié';
    return new Intl.NumberFormat('fr-FR').format(number);
}

// Fonction pour formatter les montants en euros
function formatEuro(number) {
    if (number === null || number === undefined) return 'Non spécifié';
    return new Intl.NumberFormat('fr-FR', { 
        style: 'currency', 
        currency: 'EUR',
        maximumFractionDigits: 0
    }).format(number);
}

// Gestionnaires d'événements
document.getElementById('searchById').addEventListener('submit', async (e) => {
    e.preventDefault();
    const id = document.getElementById('opportunity_id').value;
    const includeProps = document.getElementById('include_propositions').checked;
    
    try {
        const response = await fetch(`/opportunities/${id}?include_propositions=${includeProps}`);
        if (!response.ok) throw new Error('Erreur lors de la recherche');
        const data = await response.json();
        displaySearchResults([data]); // Envoyer les données dans un tableau pour uniformiser l'affichage
    } catch (error) {
        displayError(error.message);
    }
});

// gestionnaire d'événements de recherche avancée
document.getElementById('advancedSearch').addEventListener('submit', async (e) => {
    e.preventDefault();
    const formData = new FormData(e.target);
    const params = new URLSearchParams();
    
    for (let [key, value] of formData.entries()) {
        if (value) params.append(key, value);
    }
    
    try {
        const response = await fetch(`/opportunities/search?${params.toString()}`);
        if (!response.ok) throw new Error('Erreur lors de la recherche');
        const data = await response.json();
        console.log('Données reçues:', data);  // Log pour debug
        displaySearchResults(data);
    } catch (error) {
        displayError(error.message);
    }
});

// Fonction d'export
async function exportOpportunity() {
    const id = document.getElementById('opportunity_id').value;
    if (!id) {
        displayError("Veuillez entrer un ID d'opportunité");
        return;
    }
    
    try {
        window.location.href = `/opportunities/${id}/export`;
    } catch (error) {
        displayError(`Erreur lors de l'export: ${error.message}`);
    }
}