# Instrukcje dla Agentów 

### Co To jest?

Co to jest, jest wyjaśnione w `README.md`.

---

### Co jest do zrobienia [Ogólnie]?

Generalnie, robimy część symulatora wiążącą ze sobą dane statystyczne i opisowe. 

---

#### Opis Danych:
1. Realne Dane Statystyczne 
    - np. pobrane z internetu z world banku, GDP, corruption index
    - Generalnie **realne** dane mające oparcie w rzeczywistości
2. Sztuczne Dane Opisowe
    - np. Internal Grades, Relations Directed
    - Generalnie dane które zostaną uzupełnione przez model LLM

3. Użytkownik ma mieć możliwość dodawania własnych danych statystycznych oraz opisowych.

---

#### Jak użytkownik może dodawać dane?

1. Może zmieniać same wartości przechowywane przez statystytki opisowe.
    - Czyli np. zmienić to ile `stability` ma dane country.
2. Może edytować/dodawać wzory statystyk opisowych.
    - Na podstawie podanych templates.
    - Może zmieniać ich zakres, nazwy, typy etc.

3. Czym są templates?
    - Użytkownik nie może ich edytować, tylko programista.
    - Obecnie są 4 Templates:
        - Internal Grades
        - Relations Directed
        - Relations double-sided
    - Templates zawierają pola np: `name | type | valmin | valmax`, Gdzie:
        - name - nazwa
        - type - np. "float"/"int"/"TAG", 
        - valmin, valmax - przedziały na zmienną liczbową.

---

#### Sposób przechowyania Templates -> wzorów -> statystyk (opisowych)

1. Template:
    - Są przechowywane w `simulator/common/templates/[nazwa template].csv`
    - Każde pole to oddzielny wiersz

2. Wzorów:
    - Są przechowywane w `simulator/common/formulas/[nazwa template].csv`
    - Każdy wzór to oddzielny wiersz
    - Kolumny są takie same jak pola w `simulator/common/templates/[nazwa template].csv`

3. Statystyk (opisowych):
    - Internal Grades:
        - Są przechowywane w `simulator/scenarios/[nazwa scenariusza]/narrated/[rok]/Countries/[nazwa country]/internal-grades.csv`
    - Relations Directed:
        - Są przechowywane w `simulator/scenarios/[nazwa scenariusza]/narrated/[rok]/relations-directed/[nazwa relacji].csv` 
        - minus ("-") zamiast spacji (" ") w nazwie pliku `relations-directed/[nazwa relacji].csv`
    - Relations double-sided:
        - Są przechowywane w `simulator/scenarios/[nazwa scenariusza]/narrated/[rok]/relations-doublesided/[nazwa relacji].csv` 
        - minus ("-") zamiast spacji (" ") w nazwie pliku `relations-doublesided/[nazwa relacji].csv`

---

### Co jest do uzupełnienia?

Należy dokończyć implementacje poniższych rzeczy.

1. W pliku `create-descriptive-stats.ipynb` znajdują się wzorce (Templates) do:
    1. Internal Grades
    2. Relations Directed
    3. Relations double-sided

---