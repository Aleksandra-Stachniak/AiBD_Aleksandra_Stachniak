import numpy as np
import pickle

import psycopg2 as pg
import pandas.io.sql as psql
import pandas as pd

from typing import Union, List, Tuple

connection = pg.connect(host='pgsql-196447.vipserv.org', port=5432, dbname='wbauer_adb', user='wbauer_adb', password='adb2020');

def film_in_category(category_id:int)->pd.DataFrame:
    ''' Funkcja zwracająca wynik zapytania do bazy o tytuł filmu, język, oraz kategorię dla zadanego id kategorii.
    Przykład wynikowej tabeli:
    |   |title          |languge    |category|
    |0	|Amadeus Holy	|English	|Action|
    
    Tabela wynikowa ma być posortowana po tylule filmu i języku.
    
    Jeżeli warunki wejściowe nie są spełnione to funkcja powinna zwracać wartość None.
    
    Parameters:
    category_id (int): wartość id kategorii dla którego wykonujemy zapytanie
    
    Returns:
    pd.DataFrame: DataFrame zawierający wyniki zapytania
    '''
    if not isinstance(category_id, int):
        return None

    else:
        df = pd.read_sql("""select film.title, language.name as languge, category.name as category from film 
               inner join language on film.language_id = language.language_id 
               inner join film_category on film.film_id = film_category.film_id
               inner join category on film_category.category_id = category.category_id
               where film_category.category_id = {c}
               order by film.title, languge""".format(c=category_id), con=connection)
        return df
  
def number_films_in_category(category_id:int)->pd.DataFrame:
    ''' Funkcja zwracająca wynik zapytania do bazy o ilość filmów w zadanej kategori przez id kategorii.
    Przykład wynikowej tabeli:
    |   |category   |count|
    |0	|Action 	|64	  | 
    
    Jeżeli warunki wejściowe nie są spełnione to funkcja powinna zwracać wartość None.
        
    Parameters:
    category_id (int): wartość id kategorii dla którego wykonujemy zapytanie
    
    Returns:
    pd.DataFrame: DataFrame zawierający wyniki zapytania
    '''
    if not isinstance(category_id, int):
        return None

    df =  pd.read_sql_query("""select film_list.category, count(film_list.title) from film_list
                    join category on category.name = film_list.category
                    where category.category_id = {cat_id}
                    group by film_list.category""".format(cat_id=category_id), con=connection)
    return df
    
def number_film_by_length(min_length: Union[int,float] = 0, max_length: Union[int,float] = 1e6 ) :
    ''' Funkcja zwracająca wynik zapytania do bazy o ilość filmów o dla poszczegulnych długości pomiędzy wartościami min_length a max_length.
    Przykład wynikowej tabeli:
    |   |length     |count|
    |0	|46 	    |64	  | 
    
    Jeżeli warunki wejściowe nie są spełnione to funkcja powinna zwracać wartość None.
        
    Parameters:
    min_length (int,float): wartość minimalnej długości filmu
    max_length (int,float): wartość maksymalnej długości filmu
    
    Returns:
    pd.DataFrame: DataFrame zawierający wyniki zapytania
    '''
    if (not isinstance(min_length, (int, float))) or (not isinstance(max_length, (int, float))):
        return None
    
    elif min_length > max_length:
        return None
    
    else:
        df = pd.read_sql("""select film.length, count(film.film_id) from film
               where film.length between {min_l} and {max_l}
               group by film.length""".format(min_l=min_length, max_l=max_length), con=connection)
        return df

def client_from_city(city:str)->pd.DataFrame:
    ''' Funkcja zwracająca wynik zapytania do bazy o listę klientów z zadanego miasta przez wartość city.
    Przykład wynikowej tabeli:
    |   |city	    |first_name	|last_name
    |0	|Athenai	|Linda	    |Williams
    
    Tabela wynikowa ma być posortowana po nazwisku i imieniu klienta.
    
    Jeżeli warunki wejściowe nie są spełnione to funkcja powinna zwracać wartość None.
        
    Parameters:
    city (str): nazwa miaste dla którego mamy sporządzić listę klientów
    
    Returns:
    pd.DataFrame: DataFrame zawierający wyniki zapytania
    '''
    if not isinstance(city, str):
        return None
    
    else:      
        df = pd.read_sql("""select city.city, customer.first_name, customer.last_name from customer
               inner join address on customer.address_id = address.address_id
               inner join city on address.city_id = city.city_id
               where city.city = '{c}' """.format(c=city), con=connection)
        return df

def avg_amount_by_length(length:Union[int,float])->pd.DataFrame:
    ''' Funkcja zwracająca wynik zapytania do bazy o średnią wartość wypożyczenia filmów dla zadanej długości length.
    Przykład wynikowej tabeli:
    |   |length |avg
    |0	|48	    |4.295389
    
    
    Jeżeli warunki wejściowe nie są spełnione to funkcja powinna zwracać wartość None.
        
    Parameters:
    length (int,float): długość filmu dla którego mamy pożyczyć średnią wartość wypożyczonych filmów
    
    Returns:
    pd.DataFrame: DataFrame zawierający wyniki zapytania
    '''
    if not isinstance(length, (int, float)):
        return None
    
    else:       
        df = pd.read_sql("""select film.length, avg(payment.amount) from film
               inner join inventory on film.film_id = inventory.film_id
               inner join rental on inventory.inventory_id = rental.inventory_id
               inner join payment on rental.rental_id = payment.rental_id
               where film.length = {l}
               group by film.length""".format(l=length), con=connection)
        return df

def client_by_sum_length(sum_min:Union[int,float])->pd.DataFrame:
    ''' Funkcja zwracająca wynik zapytania do bazy o sumaryczny czas wypożyczonych filmów przez klientów powyżej zadanej wartości .
    Przykład wynikowej tabeli:
    |   |first_name |last_name  |sum
    |0  |Brian	    |Wyman  	|1265
    
    Tabela wynikowa powinna być posortowane według sumy, imienia i nazwiska klienta.
    Jeżeli warunki wejściowe nie są spełnione to funkcja powinna zwracać wartość None.
        
    Parameters:
    sum_min (int,float): minimalna wartość sumy długości wypożyczonych filmów którą musi spełniać klient
    
    Returns:
    pd.DataFrame: DataFrame zawierający wyniki zapytania
    '''
    if not isinstance(sum_min, (int, float)):
        return None
    
    elif sum_min < 0:
        return None
    
    else:        
        df = pd.read_sql("""select customer.first_name, customer.last_name, sum(film.length) from customer
               inner join rental on customer.customer_id = rental.customer_id
               inner join inventory on rental.inventory_id = inventory.inventory_id
               inner join film on inventory.film_id = film.film_id
               group by customer.first_name, customer.last_name
               having sum(film.length) > {s_min}
               order by sum(film.length), customer.last_name""".format(s_min=sum_min), con=connection)
        return df

def category_statistic_length(name:str)->pd.DataFrame:
    ''' Funkcja zwracająca wynik zapytania do bazy o statystykę długości filmów w kategorii o zadanej nazwie.
    Przykład wynikowej tabeli:
    |   |category   |avg    |sum    |min    |max
    |0	|Action 	|111.60 |7143   |47 	|185
    
    Jeżeli warunki wejściowe nie są spełnione to funkcja powinna zwracać wartość None.
        
    Parameters:
    name (str): Nazwa kategorii dla której ma zostać wypisana statystyka
    
    Returns:
    pd.DataFrame: DataFrame zawierający wyniki zapytania
    '''
    if not isinstance(name, str):
        return None

    else:
        df =  pd.read_sql_query("""select category.name as category, avg(film.length), sum(film.length), min(film.length), max(film.length) from film
                    inner join film_category on film_category.film_id = film.film_id
                    inner join category on category.category_id = film_category.category_id
                    where category.name = '{n}'
                    group by category.name""".format(n=name), con=connection)
        return df
