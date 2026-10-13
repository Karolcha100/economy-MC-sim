# Instrukcje dla Agentów 

### 1. Co To jest?

Co to jest, jest wyjaśnione w `README.md`.

Generalnie wszystko poza komunikacją ze mną powinno być poa angielsku.

---

### 2. Co jest do zrobienia [Ogólnie]?

Generalnie, robimy część symulatora wiążącą ze sobą dane statystyczne i opisowe. 

---

#### Opis Danych:
1. Prawdziwe Dane Statystyczne 
    - np. pobrane z internetu z world banku, GDP, corruption index
    - Generalnie **realne** dane mające oparcie w rzeczywistości
2. Sztuczne Dane Opisowe
    - np. Internal Grades, Relations Directed
    - Generalnie dane które zostaną uzupełnione przez model LLM

3. Użytkownik ma mieć możliwość dodawania własnych danych statystycznych oraz opisowych.

---

#### Jak użytkownik może dodawać dane?

1. Może zmieniać same wartości przechowywane przez dane opisowe.
    - Czyli np. zmienić to ile `stability` ma dane country.
2. Może edytować/dodawać wzory danych opisowych.
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

### 3. Dane Opisowe

Tutaj analizujemy dane opisowe (czyli te którychy wartości są generowane poprzez modele LLM)

---

#### Sposób przechowyania Templates -> wzorów -> danych opisowych

1. Template:
    - Są przechowywane w `simulator/common/templates/[nazwa template].csv`
    - Każde pole to oddzielny wiersz

2. Wzorów:
    - Są przechowywane w `simulator/scenarios/[nazwa scenariusza]/formulas/[nazwa template].csv`
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


#### Sposób wprowadzania danych opisowych

1. Internal Grades
    - Należy utworzyć skrypt który pozwoli na dodawanie/edytowanie Internal Grades na podstawie:
        - przedziału dat
        - wartości początkowej i końcowej 
        - jednej z kilku funkcji zmiany (np. liniowa, wykładnicza, logistyczna) od wartości początkowej do końcowej (zawsze pozostaje opcja ustawiania wartości z iteracji na iteracje)

2. Relations Directed
    - Należy utworzyć skrypt który pozwoli na dodawanie/edytowanie Internal Grades na podstawie:
        - przedziału dat
        - wartości początkowej i końcowej 
        - jednej z kilku funkcji zmiany (np. liniowa, wykładnicza, logistyczna) od wartości początkowej do końcowej (zawsze pozostaje opcja ustawiania wartości z iteracji na iteracje)

3. Relations Directed
    - Należy utworzyć skrypt który pozwoli na dodawanie/edytowanie Internal Grades na podstawie:
        - przedziału dat
        - wartości początkowej i końcowej 
        - jednej z kilku funkcji zmiany (np. liniowa, wykładnicza, logistyczna) od wartości początkowej do końcowej (zawsze pozostaje opcja ustawiania wartości z iteracji na iteracje)
        - skrypt powinien uwzględniać to że zmiana relacji z kraju AAA na kraj BBB, zmienia ją także w drugą stronę (krawedź nieskierowana grafu)

**Te skrypty będą używane przez inne modele LLM do wypełniania danych**

---

### 3. Dane Statystyczne (prawdziwe)

Tutaj analizujemy dane statystyczne (prawdziwe) - czyli bazujące na danych np. z world banku. Np. GDP, corruption index. 

---

#### Sposób przechowywania Danych Statystycznych

1. Przechowywane są w `simulator/scenarios/[nazwa scenariusza]/history/[nazwa danych statystycznych].csv`
    - nazwa danych statystycznych musi być bez spacji, zamiast niej powinien być minus.

---

#### Sposób wprowadzania danych statystycznych

1. Należy dostosować je do formatu w którym kolumny to tagi państw a wiersze to kolejne iteracje/daty.

---

### 5. Dodatkowe elementy Scenariuszy.

(Nie mylić ze scenariuszami generowanymi przez model)

1. Tagi
    - plik: `simulator/scenarios/[nazwa scenariusza]/tags.csv`
    - Lista Tagów i odpowiadających nazw Państw.

2. Daty
    - plik: `simulator/scenarios/[nazwa scenariusza]/dates.csv`
    - Lista Dat

---

### 6. Dodatkowe uwagi

1. W pliku `create-descriptive-stats.ipynb` znajdują się:
    1. Templates do:
        - Internal Grades
        - Relations Directed
        - Relations double-sided

    2. Przykładowe Wzory do:
        - Internal Grades
        - Relations Directed
        - Relations double-sided

    3. Format Zapisu:
        - Internal Grades
        - Relations Directed
        - Relations double-sided

---