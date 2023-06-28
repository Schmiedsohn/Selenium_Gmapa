# Selenium_Gmapa
Test za proveru rezultata koje Google mape izbacuju prilikom trazenje najkraceg ili najduzeg puta izmedju dve tacke u fajlu Gmape.py

Da bi aplikacija radila neophodno je imati instaliran Python.

Ako ga nemate instaliranog pratite sledece uputstvo:
1. Go to the miniconda install page - https://docs.conda.io/en/latest/miniconda.html.
2. Download a 64-bit version of Miniconda.
3. Run the installer, paying attention to the following options:
    a. If you’re asked where to install the software, you want to install it “For me only,” not “Install for all users of this computer.” Note that as of July 2021, you may find the “For me only” option has a warning saying you can’t install there, but if you click a different option then click on the “For me only” option again, the warning goes away.
    b. On Windows, you’ll be asked if you want to add Miniconda to your PATH variable. Although it recommends that you do not do this, DO add it to your PATH. This will be important when we change how our command line works.
4. Miniconda is installed!
5. Changing the Default Repository
6. Open the default command line on your computer (on a Mac, it’s Terminal in Applications > Utilities; on Windows, you can use PowerShell, which you can get by just putting PowerShell in the search bar), and run the following three commands:
        conda config --add channels conda-forge (you may be told you already have it listed)
        conda config --set channel_priority strict
        conda install python=3.10

U fajlu postavke se nalaze osnovne postavke. Tu se mogu naci i izabrane tacke, trenutno Budimpesta i Beograd

Test prvo tazi od korisnika da unese da li ce se proveravati najkraci ili najduzi put,
zatim ocita u levoma panou koje vrednosti trajanja i duzine izbaci google , 
a onda proveri da li iste rezultate daje i kad se klikne na dugme Detalji

Ako je sve OK ne dobija se nikakva poruka, 
ako nije dobije se poruka da neki od testova (ista vremena i iste duzine) nisu prosli.

