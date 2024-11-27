# Nouveau fichier: data_quality.py
def check_data_quality(df: pd.DataFrame) -> Dict[str, List[str]]:
    issues = {
        'missing_values': [],
        'invalid_formats': [],
        'inconsistencies': []
    }
    # Vérifier les valeurs manquantes
    for col in df.columns:
        missing = df[col].isna().sum()
        if missing > 0:
            issues['missing_values'].append(f"{col}: {missing} valeurs manquantes")
    return issues