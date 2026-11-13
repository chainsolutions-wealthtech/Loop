# Registres de travail de Loop

- [work.json](work.json) relie exigences, unités, états, dépendances et critères.
- [evidence.json](evidence.json) indexe les preuves et snapshots.
- [public-repositories.json](public-repositories.json) conserve les fiches minimales des seuls dépôts publics du relevé.
- [dispatch-review.json](dispatch-review.json) conserve la qualification des sites de dispatch.
- [La mémoire](../memory/README.md) décrit leur provenance et leurs limites.

Le dépôt est public. Les inventaires privés et chemins serveur restent hors
Git. Les identifiants de snapshots et leurs empreintes relient le registre
Git au détail autorisé, sans y recopier les données.

## Reproduire la base SQLite dans un environnement autorisé

```sh
python3 -m loop.evidence_store registre-prive.sqlite rapport-prive.json --snapshot-id INVENTAIRE-ID --scope 'Périmètre daté' --expected-count 45
```

Le rapport HTML produit par Loop est également accepté. L'identifiant est
réutilisable à l'identique pour la même entrée et le même périmètre, mais une
nouvelle observation ne remplace jamais un instantané existant. Garder
le fichier SQLite hors du dépôt public. Exemple de lecture privée :

```sql
SELECT full_name, section, count(*)
FROM observation JOIN repository USING (snapshot_id, github_id)
WHERE snapshot_id = 'LOOP-INV-20261113-02'
GROUP BY full_name, section;
```

## Navigation par identifiant

[Identité du projet et continuité](identity.json) · [Contrats des modules](modules.json) · [Sous-projets, sujets et tables](subjects.json) · [Mode d'emploi](../docs/LOOP_CANONICAL_REGISTRY.md).
