# Nombre moyen de mots par phrase et profilage morphosyntaxique

# Utilisation

Le fichier `TP2.py` génère les fichiers XML de chaque méthode des exercices 1 à 3. L'execution de ce dernier prenant assez de temps, les résultats sont joints dans l'archive.

La fonction ```output``` prend en argument un résultat de découpage, et formatte ce dernier au sein d'un fichier XML. Chaque "token" est associé à un id.

## 1. Découpage en phrases

### Comparaison en temps (ordre croissant)

Regex: 0.0004706382751464844 secondes

spaCy: 0.04717254638671875 secondes

spaCy_senter: 0.7426304817199707 secondes


### 1.1 La méthode "à base de règles"

Cette méthode a découpé le texte en 61 (regex 1) et 69 (regex 2) tokens.

L'expression régulière `[^\.\n]+[\.\n]` permet, entre autres, d'isoler les phrases qui finissent par un point. Plus précisement, tous les caractères qui ne sont pas un point ou un caractère d'échappement seront récupérés.

Les résultats sont plutôt corrects mais pas parfaits : une phrase exclamative ou interrogative en plein milieu d'un paragraphe ne sera pas récupérée, et les seules fois où elle peut l'être, c'est lorsque son signe de ponctuation est suivi d'un point (de suspension). Ces points de suspension sont abondants dans ce texte, mais ils ne sont pas non plus la norme.

On perd également de l'information : les points de suspension ne sont par exemple pas entièrement comptabilisés, ce qui rend incomplète la reconstitution du texte ou corpus depuis le découpage -- atout que spaCy a et met en avant.

Si l'on décide plutôt d'opter pour l'expression régulière qui gère ces signes de ponctuation (`[^\.|\!|\?\n]+[\.|\!|\?\n]`) on fait face à un autre problème de bruit (déjà présent mais plus marqué cette fois-ci) : les guillemets. Celles fermantes plus précisément sont découpées seules et comptabilisées comme un token. Les guillemets n'entourent pas toujours une phrase mais parfois un ou plusieurs mot(s) dans une phrase, ainsi les inclure dans l'expression régulière n'est pas pertinent.

### 1.2 Utilisation de librairies dédiées (python)

La méthode spaCy avec `add_pipe` a découpé le texte en 41 tokens, tandis que le Senter spaCy l'a découpé en 60 tokens.

Le Senter gère un peu mieux les points de suspension que l'autre méthode et les considère la plupart du temps comme la délimitation d'une phrase. Cependant, le découpage laisse parfois à désirer et des groupes de mots qui ne sont pas des phrases sont considérés comme telle (```<token id="35">Eh bien,
</token>```).

Même si les résultats ne sont pas sans faute, l'intégrité du texte est conservée. Si l'on considère la méthode d'expression régulière comme notre "témoin", alors Senter spaCy est la méthode qui se rapproche le plus du nombre de tokens escompté. L'autre méthode spaCy quant à elle voit le nombre total de tokens greffé au vu du découpage qui a l'air de faire abstraction des points de suspension, et ce texte en est abondant.

## 2. Découpage en mots

### Comparaison en temps (ordre croissant)

Regex: 0.0003883838653564453 secondes

nltk: 0.008331060409545898 secondes

spaCy: 0.8303797245025635 secondes


### 2.1 Tokéniseur "à base de règles"

L'expression régulière `[A-Za-zÀ-ÖØ-öø-ž]` permet de découper les mots, y compris accentués comme il est le cas en français, de notre corpus. Les mots composés ne sont cependant pas pris en charge : 'c'est-à-dire' consitue 4 mots.
Hormis cela, les résultats sont très concluants : 1031 mots reconnus dans `conte.txt`, et ce sans aucun bruit.

### 2.2 Librairie NLTK (Natural Language ToolKit)

Le découpage produit des résultats plus ou moins corrects. Les apostrophes sont inclues comme des tokens à part entière, ce qui démontre une segmentation un peu hasardeuse, mais les mots sont bien séparés. Les types des mots ne sont pas indiqués, et si ils le sont, ces types sont 'incorrects'. Si un token est rencontré plus d'une fois, un type du même nom semble être créé ('j' pour le pronom personnel 'j'' par exemple). On peut imaginer qu'avec un corpus un peu plus conséquent, cette méthode peut être plus efficace.

Aussi, le seul mot composé de la phrase à tester est bien comptabilisé comme un seul et même token.

### 2.3 Tokéniseur spaCy

Pour la phrase :

```
"Depuis huit jours, j'avais déchiré mes bottines Aux cailloux des chemins. J'entrais à Charleroi. - Au Cabaret-Vert : je demandai des tartines De beurre et du jambon qui fût à moitié froid."
```

La méthode à expression régulière décompose les mots et fait abstraction des mots composés, donc il y a nombre total de 33 tokens. Cependant, le nombre de mots réel est de 32 (car 1 mot est composé). spaCy (40 tokens) a comptabilisé de la ponctuation comme des tokens. Pareil pour nltk (33 tokens), mais à échelle moindre.

### 2.4 Tokéniseur custom

Deux tokéniseurs custom ont été testés : un entièrement à base de règles, et un second à l'aide de spaCy et la pipeline NLP.

Une fois de plus, la méthode spaCy génère beaucoup de bruit, avec des tokens qui ne sont pas des mots mais de la ponctuation. Pour le corpus `conte.txt`, on trouve une différence d'environ 100 tokens mots entre la méthode à base de règles et celle-ci. Pour les phrases, on est à 69 tokens vs. 41.

#### Temps d'exécution regex: 0.0006701946258544922 secondes
#### Temps d'exécution spaCy: 0.8299093246459961 secondes

## 3. Annotation morphosyntaxique

Pour les annotations morphosyntaxique, j'ai décidé de les inclure dans le fichier XML en tant qu'attributs. Ces dernières semblent correctes au premier abord, mais il y a une certaine marge d'erreur non négligeable qui rend l'outil loin d'être totalement fiable. Les +90% de performance annoncés sont évidemment trompeurs.


#### Temps d'exécution spacy: 23.6674063205719 secondes