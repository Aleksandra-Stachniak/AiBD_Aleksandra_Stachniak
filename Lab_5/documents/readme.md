Zbiór danych, którym się zajmowałam to weather.txt, który uzyskałam podstawiając liczbę liter imienia zamiast nazwiska.
Zrobiłam to przez pomyłkę, o czym zorientowałam się podczas końcowego etapu mojej pracy, dlatego nie rozpoczynałam już pracy nad nowym zbiorem.

Plik weather.txt znajduje się w folderze o nazwie ../original_data/. Zawiera on zbiór pomiarów ze stacji pogodowej MX17004 w Meksyku. 
Dane zawarte w pliku obejmują pomiary od 1955 do 2011 roku.
Naszym zadaniem było wyodrębnienie danych z pierwszych 5 miesięcy roku 2010.

W pierwszej kolejności zajęłam się odfiltrowaniem interesujących nas danych, czyli te dotyczące pierwszych 5 miesięcy 2010 roku. 
Następnie podzieliłam dane:
1) Pierwsza kolumna - nazwa stacji - "id"
2) Druga kolumna - rok - "year"
3) Trzecia kolumna - miesiąc - "month"
4) Czwarta kolumna - rodzaj pomiaru - "element"
5) Kolejne kolumny - pomiary z poszczególnych dni miesiąca - "day1",...,"day31"
W kolejnym kroku moim celem było usunięcie błędnych pomiarów, dlatego niepoprawne dane zastąpiłam wartością "inf".
Następnie wyodrębniłam te wartości, które nie zawierały "inf".
Po czym połączyłam kolumny zawierające informacje o roku, miesiącu i dniu w jedną kolumną zawierającą datę.
Na końcu mojej pracy zapisałam przefiltrowany DataFrame do pliku o nazwie data.txt.
