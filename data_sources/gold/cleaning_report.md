# Rapport de nettoyage des données - 2024-11-24 01:14:43

## Statistiques de nettoyage

### Opportunities
- Nombre initial : 183496
- Nombre après nettoyage : 169334
- Taux de conservation : 92.28%

### Propositions
- Nombre initial : 53458
- Nombre après nettoyage : 1478
- Taux de conservation : 2.76%

### Banques
- Nombre initial : 2881
- Nombre après nettoyage : 1927
- Taux de conservation : 66.89%

## Critères de nettoyage appliqués

### Opportunities
- Age : 18-100 ans
- Revenus : 0-20,000€

### Propositions
- Taux d'intérêt : 0.1-15%
- Durée de prêt : 12-360 mois
- Taux d'assurance : 0-1%
- Suppression des propositions sans banque

### Banques
- Suppression des doublons sur le nom

## Statistiques après nettoyage

### Opportunities
       Age_emprunteur__c      TotRev__c
count      169334.000000  169334.000000
mean           37.152970    4554.283370
std            10.693494    2839.895516
min            18.000000       1.000000
25%            29.000000    2600.000000
50%            35.000000    3833.330000
75%            44.000000    5508.330000
max           100.000000   20000.000000

### Propositions
           TXHA__c  DureePret_Mois__c   TauxAss__c
count  1478.000000        1478.000000  1478.000000
mean      4.536800         261.354533     0.290940
std       0.904248          59.172494     0.266073
min       0.790000          12.000000     0.000000
25%       4.000000         240.000000     0.000000
50%       4.450000         300.000000     0.340000
75%       5.470000         300.000000     0.517500
max       6.000000         360.000000     1.000000
