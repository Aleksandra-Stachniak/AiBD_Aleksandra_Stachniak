Analizowanym przeze mnie zbiorem danym jest 3_LUBUSKIE.csv.


1. Dane, które otrzymałam w pierwotnej postaci znajdują się w folderze "orginal_data" o nazwie 3_LUBUSKIE.csv.

2. Dane wczytałam w pliku L6_Aleksandra_Stachniak.ipynb z wykorzystaniem biblioteki pandas.

3. Po wstępnej analizie danych zaobserwowałam pewne braki dotyczące kolumn "Wiek kupującego" oraz "Płeć kupującego".
Braki te postanowiłam zastąpić wartością NaN i nie usuwać ich, ponieważ dla kolumny "Wiek kupującego" tych braków jest 67.
Natomiast dla kolumny "Płeć kupującego" tych braków jest 137 (informacje te zaczerpnęłam po poleceniu df.info()).
W związku z tym usunięcie tych danych spowodowałyby znaczną stratę dla pozostałych kategorii.

4. Po wykonaniu czynności czyszczenia danych zapisałam gotowy plik do analizy w folderze "analysis_data" pod nazwą analysis_data.csv.

5. W następnym kroku dla każdej zmiennej wykonałam stosowne wykresy, które dodatkowo zapisałam w formie pliku png.
Znajdują się one w folderze diagrams znajdującym się z kolei w folderze documents.