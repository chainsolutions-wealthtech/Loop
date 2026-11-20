"""Build a repository and dependency catalog from read-only Git observations."""
import ast
from collections import defaultdict
from html import escape
from pathlib import PurePosixPath
import json
import re
from urllib.parse import quote, urlsplit


CLASSIFICATIONS = {
    'mcp_client_code': 'code_client',
    'mcp_provider_code': 'code_fournisseur',
    'wealthtech_workflow_http_candidate': 'workflow_candidat',
    'workflow_wiring_candidate': 'workflow_candidat',
    'configuration_or_reference': 'configuration',
    'reference': 'reference',
}
_WORKFLOW = re.compile(r'^\.github/workflows/[^/]+\.ya?ml$', re.I)
_SCRIPT = re.compile(r'\.(py|js|mjs|cjs|ts|tsx|sh|bash|ps1|rb|pl|php|go|rs|bat|cmd|zsh|ksh|lua|r)$', re.I)
_URL = re.compile(r'https?://[^\s\x22\x27<>`),;]+', re.I)
_MCP_KEY = re.compile(r'\b(?:GOVERNED_MCP_URL|MCP_(?:SERVER_)?(?:URL|ENDPOINT)|mcp_endpoint)\b', re.I)
_RPC = re.compile(r'\btools/(call|list)\b')
_TOOL = re.compile(r"""\b(?:call_tool|callTool|invoke_tool|invokeTool|mcp_call|call_mcp)\s*\(\s*["']([\w.-]+)["']""")
_PROVIDER_TOOL = re.compile(r"""\.(?:tool|registerTool|add_tool)\s*\(\s*["']([\w.-]+)["']""")
_CLIENT_NAME = re.compile(r"""["']?clientInfo["']?\s*:\s*\{\s*["']?name["']?\s*:\s*["']([\w.-]+)["']""")
_USES_LOCAL = re.compile(r'^\s*(?:-\s+)?uses:\s*["\x27]?(\./[A-Za-z0-9_./-]+)', re.I)
_EXTERNAL_USE = re.compile(r'^\s*(?:-\s+)?uses:\s*["\x27]?([A-Za-z0-9_.-]+/[A-Za-z0-9_./-]+@[A-Za-z0-9_./-]+)', re.I)
_LOCAL = re.compile(r'(?<![\w./@-])(?:\./)?(?:[\w.-]+/)*[\w.-]+\.(?:ya?ml|py|m?js|cjs|tsx?|sh|bash|ps1|rb|pl|php|go|rs|bat|cmd|zsh|ksh|lua)(?![\w./-])', re.I)
_TOOL_NAME = re.compile(r"""["']name["']\s*:\s*["']([A-Za-z][\w.-]+)["']""")
_NPM = re.compile(r'\b(?:npm|pnpm|yarn)\s+(?:run\s+)([\w:.-]+)')
_IDENT = re.compile(r'^[A-Za-z0-9_][A-Za-z0-9_.-]{0,79}$')


def artifact_type(path):
    if _WORKFLOW.fullmatch(path):
        return 'workflow'
    if path.rsplit('/', 1)[-1] == 'package.json':
        return 'package_manifest'
    if _SCRIPT.search(path) or re.search(r'(^|/)(?:scripts?|bin)/[^/.]+$', path):
        return 'script'
    if (re.search(r'(^|/)(action\.ya?ml|[^/]*mcp[^/]*\.(json|ya?ml|toml))$', path, re.I)
            or path.startswith('.mcp/')):
        return 'configuration'
    return 'other'


def source(path, revision, line=None):
    return {'path': path, 'sha': revision, 'line': line}


def _safe_endpoint(raw):
    try:
        url = urlsplit(raw)
        if not url.hostname or url.username or url.password:
            return None
        host = url.hostname.lower()
        if not re.fullmatch(r'[a-z0-9.-]+', host):
            return None
        route = url.path.rstrip('/')
        if route in ('/mcp', '/sse', '/'):
            return f'{url.scheme}://{host}' + (f':{url.port}' if url.port else '') + route
        # Do not export opaque paths that could carry credentials.
        return f'{url.scheme}://{host}' + (f':{url.port}' if url.port else '')
    except ValueError:
        return None


def _safe_directory(value):
    if not isinstance(value, str) or not value.startswith('/') or value.startswith('//'):
        return None
    path = PurePosixPath(value)
    return value if '..' not in path.parts and str(path) == value and value != '/' and all(
        re.fullmatch(r'[A-Za-z0-9_.@-]+', part) for part in path.parts[1:]
    ) else None


class Catalog:
    def __init__(self, paths, revision):
        self.paths = set(paths)
        self.revision = revision
        self.artifacts = {p: {'path': p, 'type': artifact_type(p), 'read_status': 'not_read'}
                          for p in sorted(self.paths) if artifact_type(p) != 'other'}
        self.relations = []
        self.seen = set()
        self.configs = []
        self.npm = []
        self.packages = defaultdict(list)

    def add(self, kind, path, target, line=None, status='static_candidate'):
        key = (kind, path, target, line, status)
        if key not in self.seen:
            self.seen.add(key)
            self.relations.append({'kind': kind, 'target': target, 'status': status,
                                   'source': source(path, self.revision, line)})

    def mark(self, path, state):
        if path in self.artifacts:
            self.artifacts[path]['read_status'] = state

    def read(self, path, data, signal=None):
        self.mark(path, 'read')
        if signal:
            signal['classification'] = CLASSIFICATIONS[signal['kind']]
            signal['source'] = source(path, self.revision)
        kind = artifact_type(path)
        json_data = None
        if path.endswith('.json'):
            try:
                json_data = json.loads(data)
            except (ValueError, RecursionError):
                pass
        if isinstance(json_data, dict):
            self._json(path, kind, json_data)
        if path.endswith('.py') and 'tools/call' in data:
            self._python_dispatch(path, data)
        if kind == 'script':
            for m in _CLIENT_NAME.finditer(data):
                self.add('mcp_client_identity', path, m[1], data.count('\n', 0, m.start()) + 1, 'declared')
        for i, line in enumerate(data.splitlines(), 1):
            if line.lstrip().startswith(('#', '//', '*')):
                continue
            if kind in ('script', 'workflow', 'configuration'):
                for m in _LOCAL.finditer(line):
                    dest = m.group().removeprefix('./')
                    parent = PurePosixPath(path).parent
                    relative = (parent / dest).as_posix()
                    if dest in self.paths and dest != path:
                        self.add('file_reference', path, dest, i)
                    elif relative in self.paths and relative != path:
                        self.add('file_reference', path, relative, i)
                for m in _NPM.finditer(line):
                    self.npm.append((path, m[1], i))
            if kind in ('workflow', 'configuration'):
                if m := _USES_LOCAL.search(line):
                    dest = m[1][2:].rstrip('/')
                    candidates = [p for p in (dest, f'{dest}/action.yml', f'{dest}/action.yaml') if p in self.paths]
                    for candidate in candidates or [dest]:
                        self.add('local_action_or_workflow', path, candidate, i,
                                 'declared' if candidates else 'unresolved')
                if m := _EXTERNAL_USE.search(line):
                    self.add('external_action_or_workflow', path, m[1], i, 'declared')
            if kind in ('script', 'workflow'):
                for m in _RPC.finditer(line):
                    self.add('mcp_rpc', path, m[0], i)
                for m in _TOOL.finditer(line):
                    self.add('mcp_tool_call', path, m[1], i)
                if 'tools/call' in line and (m := _TOOL_NAME.search(line)):
                    self.add('mcp_tool_call', path, m[1], i)
                if ((signal and signal['kind'] == 'mcp_provider_code')
                        or re.search(r'\b(?:server|mcp)\.(?:tool|registerTool|add_tool)\s*\(', line)):
                    for m in _PROVIDER_TOOL.finditer(line):
                        self.add('mcp_tool_exposed', path, m[1], i)
            for m in _URL.finditer(line):
                raw = m.group().rstrip('.]}>')
                if 'mcp.wealthtechinnovations.com' in raw.lower() or _MCP_KEY.search(line):
                    if endpoint := _safe_endpoint(raw):
                        self.add('mcp_endpoint', path, endpoint, i,
                                 'reference' if kind == 'other' else 'declared')
            if _MCP_KEY.search(line) and ('${{' in line or 'getenv' in line or 'environ' in line):
                self.add('mcp_endpoint_variable', path, _MCP_KEY.search(line)[0], i, 'unresolved')
        if signal and signal['kind'] == 'mcp_client_code':
            self.add('mcp_client_implementation', path, path, status='static_candidate')

    def _python_dispatch(self, path, data):
        # Recognize a bounded static case: a named collection iterated into a
        # tool call. Do not guess a value for arbitrary dynamic tool arguments.
        try:
            tree = ast.parse(data)
        except (SyntaxError, ValueError, RecursionError):
            return
        constants = {}
        for node in tree.body:
            if not isinstance(node, ast.Assign) or len(node.targets) != 1:
                continue
            target = node.targets[0]
            if not isinstance(target, ast.Name):
                continue
            if isinstance(node.value, ast.Dict):
                values = node.value.keys
            elif isinstance(node.value, (ast.Tuple, ast.List, ast.Set)):
                values = node.value.elts
            else:
                continue
            constants[target.id] = [
                x.value for x in values if isinstance(x, ast.Constant)
                and isinstance(x.value, str) and _IDENT.fullmatch(x.value)
            ]
        for node in ast.walk(tree):
            if not isinstance(node, ast.For):
                continue
            iterator = node.iter
            if (isinstance(iterator, ast.Call) and isinstance(iterator.func, ast.Name)
                    and iterator.func.id == 'enumerate' and iterator.args):
                iterator = iterator.args[0]
            if not isinstance(iterator, ast.Name) or iterator.id not in constants:
                continue
            targets = {x.id for x in ast.walk(node.target) if isinstance(x, ast.Name)}
            for call in ast.walk(node):
                if not isinstance(call, ast.Call):
                    continue
                func = call.func.id if isinstance(call.func, ast.Name) else getattr(call.func, 'attr', '')
                if func not in ('call_tool', 'callTool', 'invoke_tool', 'invokeTool', 'mcp_call', 'call_mcp'):
                    continue
                if any(isinstance(a, ast.Name) and a.id in targets for a in call.args):
                    for name in constants[iterator.id]:
                        self.add('mcp_tool_call', path, name, call.lineno, 'static_dispatch_candidate')

    def _json(self, path, kind, doc):
        if kind == 'package_manifest' and isinstance(doc.get('scripts'), dict):
            for name, command in doc['scripts'].items():
                if not isinstance(command, str) or not re.fullmatch(r'[\w:.-]+', name):
                    continue
                ident = f'{path}#scripts.{name}'
                self.packages[name].append(ident)
                self.artifacts[ident] = {'path': ident, 'type': 'package_script', 'read_status': 'read'}
                for m in _LOCAL.finditer(command):
                    target = m[0].removeprefix('./')
                    relative = (PurePosixPath(path).parent / target).as_posix()
                    if relative in self.paths or target in self.paths:
                        self.add('file_reference', ident, relative if relative in self.paths else target)
                for m in _NPM.finditer(command):
                    self.npm.append((ident, m[1], None))
        if isinstance(doc.get('mcpServers'), dict):
            for name, spec in doc['mcpServers'].items():
                if not _IDENT.fullmatch(name) or not isinstance(spec, dict):
                    continue
                self.add('mcp_server_alias', path, name, status='declared')
                if isinstance(spec.get('url'), str) and (url := _safe_endpoint(spec['url'])):
                    self.add('mcp_endpoint', path, url, status='declared')
        dest = doc.get('destination')
        orch = doc.get('orchestrator')
        if path.endswith('mcp-target.json') and isinstance(dest, dict):
            server = dest.get('server')
            server = server if isinstance(server, str) and _IDENT.fullmatch(server) else None
            directory = _safe_directory(dest.get('applicationDirectory'))
            self.configs.append({'server': server, 'directory': directory, 'status': 'declared',
                                 'source': source(path, self.revision)})
            if isinstance(orch, dict) and isinstance(orch.get('endpoint'), str):
                if url := _safe_endpoint(orch['endpoint']):
                    self.add('mcp_endpoint', path, url, status='declared')

    def project(self, row):
        for path, name, line in self.npm:
            targets = self.packages.get(name, [])
            same = f"{PurePosixPath(path.split('#', 1)[0]).parent / 'package.json'}#scripts.{name}"
            if same in targets:
                targets = [same]
            for target in targets:
                self.add('package_script_reference', path, target, line,
                         'static_candidate' if len(targets) == 1 else 'ambiguous')
            if not targets:
                self.add('package_script_reference', path, name, line, 'unresolved')
        row['artifacts'] = sorted(self.artifacts.values(), key=lambda a: (a['type'], a['path']))
        row['relations'] = self.relations
        row['mcp_tools_used'] = sorted({e['target'] for e in self.relations if e['kind'] == 'mcp_tool_call'})
        row['mcp_tools_exposed'] = sorted({e['target'] for e in self.relations if e['kind'] == 'mcp_tool_exposed'})
        row['mcp_server_links'] = sorted({e['target'] for e in self.relations if e['kind'] == 'mcp_endpoint'})
        row['server_bindings'] = self.configs
        row['mcp_clients'] = sorted({e['target'] for e in self.relations if e['kind'] == 'mcp_client_implementation'})
        row['declared_mcp_client_names'] = sorted({e['target'] for e in self.relations if e['kind'] == 'mcp_client_identity'})
        row['declared_mcp_client_links'] = [
            {'client': e['target'], 'source': e['source'], 'status': 'declared_in_code'}
            for e in self.relations if e['kind'] == 'mcp_client_identity'
        ]
        row['linked_mcp_clients'] = []
        row['linked_mcp_clients_status'] = 'not_verified_at_runtime'
        named_sites = {(e['source']['path'], e['source']['line']) for e in self.relations
                       if e['kind'] == 'mcp_tool_call'}
        row['unresolved_mcp_tool_dispatches'] = [
            e['source'] for e in self.relations if e['kind'] == 'mcp_rpc'
            and e['target'] == 'tools/call'
            and (e['source']['path'], e['source']['line']) not in named_sites
        ]
        return row


def repository_row(name, repo_id, branch, private, account):
    return dict(name=name, url='https://github.com/' + quote(name, safe='/'), repo_id=repo_id,
                account=name.split('/', 1)[0], discovered_via=[account], branch=branch,
                private=private, status='not_examined', evidence=[], file_errors=0, artifacts=[], relations=[],
                mcp_tools_used=[], mcp_tools_exposed=[], mcp_server_links=[], server_bindings=[],
                mcp_clients=[], declared_mcp_client_names=[], declared_mcp_client_links=[], linked_mcp_clients=[],
                linked_mcp_clients_status='not_verified_at_runtime', unresolved_mcp_tool_dispatches=[])


def supplement(report, *, registry_candidates=(), runtime_catalogue=None):
    """Attach separate observations without treating them as active bindings."""
    by_name = {r['name'].casefold(): r for r in report['repositories']}
    for binding in registry_candidates:
        key = binding.get('repo', '').removeprefix('github:').casefold()
        if row := by_name.get(key):
            directory = _safe_directory(binding.get('directory'))
            row['server_bindings'].append({
                'server': binding.get('server'), 'directory': directory,
                'status': 'registry_candidate', 'registry_status': binding.get('binding_status'),
                'project_id': binding.get('project_id'), 'source': binding.get('source', 'Registry projection'),
            })
    if runtime_catalogue and (row := by_name.get(runtime_catalogue['repository'].casefold())):
        row['runtime_tool_catalogue'] = runtime_catalogue
    return report


def render_html(report):
    def e(value):
        return escape(str(value))
    def table(head, rows):
        return ('<table><thead><tr>' + ''.join('<th>'+e(h)+'</th>' for h in head) +
                '</tr></thead><tbody>' + ''.join('<tr>'+''.join('<td>'+cell(v)+'</td>' for v in r)+'</tr>'
                for r in rows) + '</tbody></table>')
    def cell(v):
        if isinstance(v, tuple):
            label, url = v
            if url.startswith('https://github.com/'):
                return f'<a href="{e(url)}">{e(label)}</a>'
            return e(label)
        return e(v)
    def values(row, key):
        return ', '.join(row[key]) or 'Non établi'
    repo_rows = report['repositories']
    doc = ['<!doctype html><html lang="fr"><meta charset="utf-8"><title>Loop – Inventaire MCP</title>',
           '<style>body{font:16px system-ui;max-width:1400px;margin:2rem auto;padding:0 1rem;color:#172033}'
           'table{border-collapse:collapse;width:100%;font-size:.9rem;overflow-wrap:anywhere}'
           'th,td{border:1px solid #cfd7e3;text-align:left;padding:.38rem}th{background:#eef2f8}'
           'details{margin:1rem 0}summary{font-weight:700;cursor:pointer}h3{margin-top:1.5rem}</style>',
           '<h1>Loop · Inventaire GitHub et MCP</h1>',
           '<p>Lecture statique au SHA indiqué. Une déclaration, un candidat de registre ou un appel dans le code '
           'ne prouve pas une exécution, un accès ni un rattachement actif. Non établi ne signifie pas absent.</p>',
           '<p>'+e(report.get('scope', 'Rapport généré par Loop. Les limites et erreurs sont signalées par dépôt.'))+'</p>',
           '<p>'+e(f'{len(repo_rows)} dépôts • {len(report.get("account_errors", []))} comptes avec erreur • données privées possibles')+'</p>',
           '<label for="filter">Filtrer par dépôt ou compte</label> '
           '<input id="filter" type="search" placeholder="Ex. Regulatory" autocomplete="off">',
           '<ol id="repo-list">' + ''.join(f'<li><a href="#r{i}">{e(r["name"])}</a></li>' for i,r in enumerate(repo_rows))+'</ol>']
    if report.get('account_errors'):
        doc.append(table(['Compte', 'Erreur'], [(x['account'], x['error']) for x in report['account_errors']]))
    for i, row in enumerate(repo_rows):
        sha = row.get('revision', 'Non établi')
        counts = defaultdict(int)
        for item in row['artifacts']:
            counts[item['type']] += 1
        fields = [
            ('Nom', row['name']), ('URL', (row['url'], row['url'])), ('Compte associé', row['account']),
            ('Identifiant GitHub', row['repo_id']), ('Branche / SHA', f'{row["branch"]} / {sha}'),
            ('Outils MCP appelés dans le code (candidats)', values(row,'mcp_tools_used')),
            ('Outils MCP exposés dans le code', values(row,'mcp_tools_exposed')),
            ('Liens déclarés avec le serveur MCP', values(row,'mcp_server_links')),
            ('Répertoire serveur associé', '; '.join(
                f'{x.get("server") or "Serveur non établi"} — {x.get("directory") or "Chemin non établi"} ({x["status"]})'
                for x in row['server_bindings']) or 'Non établi'),
            ('Client MCP (code local repéré)', values(row,'mcp_clients')),
            ('Identités client déclarées dans le code', values(row,'declared_mcp_client_names')),
            ('Liste des clients MCP reliés en exécution', values(row,'linked_mcp_clients')),
            ('Couverture', f'{row["status"]} • {row.get("examined",0)} fichiers lus • '
             f'{row["file_errors"]} erreurs • arbre tronqué : {row.get("tree_truncated","non vérifié")} • '
             f'{row.get("omitted_by_limit",0)} hors limite de lecture • {row.get("omitted_by_size",0)} trop volumineux'),
            ('Artefacts exclus de la lecture', row.get('excluded_artifacts', 0)),
        ]
        def provenance(x):
            if isinstance(x, str):
                return x
            text = f'{x["path"]}:{x["line"] or "–"} @ {x["sha"]}'
            if not isinstance(x['sha'], str) or not re.fullmatch(r'[0-9a-f]{40}|[0-9a-f]{64}', x['sha']):
                return text
            href = row['url'] + '/blob/' + x['sha'] + '/' + quote(x['path'].split('#', 1)[0], safe='/')
            if x['line']:
                href += '#L' + str(x['line'])
            return text, href
        runtime = row.get('runtime_tool_catalogue')
        doc += [f'<details id="r{i}"><summary>{e(row["name"])} — {counts["workflow"]} workflows, '
                f'{counts["script"]+counts["package_script"]} scripts, {len(row["relations"])} relations</summary>',
                table(['Champ','Valeur'], fields),
                '<h3>Rattachements serveur</h3>',
                table(['Serveur','Chemin','Statut','Projet du registre','Source'], [
                    (x.get('server') or 'Non établi',x.get('directory') or 'Non établi',
                     ' / '.join(filter(None, (x['status'], x.get('registry_status')))),
                     x.get('project_id') or 'Non établi',provenance(x['source']))
                    for x in row['server_bindings']]),
                ('<h3>Catalogue des outils du fournisseur observé</h3><p>' +
                 e(f'{len(runtime["tools"])} outils • {runtime["observed_at"]} • révision {runtime["revision"]}') +
                 '</p><p>' + e(', '.join(runtime['tools'])) + '</p>') if runtime else '',
                '<h3>Indices classés</h3>',
                table(['Type','Fichier','Signaux'], [(x.get('classification', x['kind']),provenance(x['source']),', '.join(x['signals'])) for x in row['evidence']]),
                '<h3>Workflows, scripts et configurations</h3>',
                table(['Type','Chemin','Lecture'], [(x['type'],x['path'],x['read_status']) for x in row['artifacts']]),
                '<h3>Raccordements et appels</h3>',
                table(['Nature','Cible','Statut','Source'], [(x['kind'],x['target'],x['status'],provenance(x['source'])) for x in row['relations']]),
                '<h3>Appels génériques ou cibles dynamiques à résoudre</h3>',
                table(['Source'], [(provenance(x),) for x in row['unresolved_mcp_tool_dispatches']]),
                '</details>']
    doc += ['<script>document.querySelectorAll("a[href^=\'#r\']").forEach(a=>a.addEventListener("click",()=>{'
            'const d=document.getElementById(a.hash.slice(1)); if(d)d.open=true;}));'
            'document.getElementById("filter").addEventListener("input",e=>{const q=e.target.value.trim().toLowerCase();'
            'document.querySelectorAll("#repo-list li").forEach(li=>{const hide=!li.textContent.toLowerCase().includes(q);'
            'li.hidden=hide;const d=document.getElementById(li.firstChild.hash.slice(1));if(d)d.hidden=hide;});});</script>', '</html>']
    return '\n'.join(doc)
