# Treball de recerca
En aquest repositori hi trobareu els documents de dades usats en el treball de recerca.
Es tracta dels programes Python usats per la generació de les malles així com els gràfics de les malles en sí i les taules horàries en format CSV per tal de generar les malles.
Per altra banda, també hi tribareu un document de càlcul ODS on s'hi representen els càlculs realitzats durant el treball, els mateixos que hi ha a l'annex.
## Estructura del repositori
* `README.md`
* `calculs.ods` Full de càlcul les dades usades
* `generator.py` Programa base generador d'escenaris
* _`escenaris`_ Carpeta amb els escenaris
  * `README.md`
  * _`escenari_1`_ Carpeta amb els continguts de l'escenari 1
    * `esc1.py` Programa python generador de l'escenari
    * `horari.csv` Fitxer de dades CSV amb els horaris en format HH:MM:SS comptant des d'un instant zero (repetició horària)
    * `malla.png` Malla horària de l'escenari
  * _`escenari_2`_ Carpeta amb els continguts de l'escenari 1
    * `esc2.py` Programa python generador de l'escenari
    * `horari.csv` Fitxer de dades CSV amb els horaris en segons comptant des d'un instant zero (repetició horària)
    * `horari_llegible.csv` Fitxer de dades CSV amb els horaris en format HH:MM:SS comptant des d'un instant zero (repetició horària)
    * `malla.png` Malla horària de l'escenari
  * _`escenari_3`_ Carpeta amb els continguts de l'escenari 1
    * `esc3.py` Programa python generador de l'escenari
    * `malles.csv` Fitxer de dades CSV amb els horaris en segons comptant des d'un instant zero (repetició horària)
    * `malles_llegibles.csv` Fitxer de dades CSV amb els horaris en format HH:MM:SS comptant des d'un instant zero (repetició horària)
    * `malles.png` Malla horària de l'escenari
  * _`escenari_4`_ Carpeta amb els continguts de l'escenari 1
    * `esc4.py` Programa python generador de l'escenari (versió més nova i completa, no requereix el generator.py)
    * `horaris.csv` Fitxer de dades CSV amb els horaris en format cada hora als MM:SS (repetició horària)
    * `malla.png` Malla horària de l'escenari
## Python generador de malles
Es tracta d'un programa base, `generator.py`, que conté les declaracions de classes i constants generals.
Després, els programes generadors dels escenaris 1, 2 i 3 contenen les especificitats de cada escenari (trens i hores de pas).
Abans de cridar a aquests primer cal executar el generator.py.

L'esceari 4 té una versió més nova i per tant tot ja està inclòs al fitxer `esc4.py`.
Aquest genera les classes, declara les constants i genera els fitxes de dades així com mostra per pantalla les malles.

És important destacar que si s'executa el programa es mostra ua finestra emergent amb les malles, amb opcions que permeten fer-hi zoom per tal de veure els continguts amb més presició.

Per a instruccions de com executar un codi Python estàndard, aneu a [python.org](https://www.python.org).
## Malles i horaris
Cada malla i horari es troba en la respectiva carpeta.
Els fitxers en format PNG de les malles s'han exportat mitjançant l'eina d'exportació pròpia del Matplotlib.
En canvi, pel que fa als fitxers CSV aquests es poden generar de tres maneres en funció del segon paràmetre de la funció `generateCSV`.
Aquest pot ser o bé en segons des d'un instant zero, el que usen les malles; en format hores, minuts i segons des d'un instat zero, és com l'anterior però convertint els segons en hores i minuts per tal que sigui més entendedor; i finalment el format cada hora als minuts, encara més entendor per l'ull humà, però només permet renderitzar un cicle horàri.
## Document de càlcul ODS
Aquest document és la versió exportada del full de càlcul usat per als càlculs de l'`annex B`.
S'hi troben des de les primeres versions d'horaris fins a tots els càlculs detallats a l'annex.
Es recomana consultar l'annex, donat que poden haver-hi problemes de compatibilitat amb aquest fitxer.
