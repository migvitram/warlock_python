```bash
        @@@@%        @@@@%:                                                                   
         %@%=    %   @@::                                                                     
         %@%%   @%   @%::   @@%      @@@%%     @@*       @@%%     @@%%    @%  =%              
          @@%: %@%= @@%:  %@@%%:   %%%::%%%= %%@%:     @@%:-%%%  @@::%%:%%%%  @@%             
          %@%% @@%% @@%-  @@:%%%     @% *@@%%  @%:   . @%*   @%  @%:     @@% @@%:             
           @%%:@%*%%@@::  @%: @%.@= -@%@@::    @%:   = @%%  +@%  @%: : . %@%@@:               
           %@@@%:%@@@%*   @%%@%%:   -@:=%%%%   @%: :   @%#  =@%  @%:     %@:%%%%%             
            @@%:: @@%::  @@::  @%:  .@%  @%:  .@%:  #@ @%%  #@%  @%:  %  %@% @@%:             
          : @@%%: @%%%:  @%: : @%%  @@%: %%% +%%%%@@@%: %%%@@::  %%%@@%  @@% @@%%             
         : .                ..                         .  %#: ==   %+:            .           
       .   .-===--====---=+=-:-==+--=+=-=+++-::+++++*=-.-:  :=..:-.  .-::-=:-:-=: .           
     .. .. :  .. .::::...:..::::::.=::-.:=:-::=::-=.-----.:-.:...-..-.:...  .. . .. .    .    
  . . ..  ..:::.::. ...::.-.--=---:--::-:-:=----=----.::-.-:--:--:-:::-...:.....  .. . .      
                                         .                                                    
```

# Warlock (paper warlock)

### Simple script for routine info tasks

Warlock (Paper Warlock) is the old-school shell-based assistent for some routine tasks with user info. It will track the product presence and price in some internet shops, store the data about price changes and to print results. In the further versions it will track the currencies courses (depends on banks API), search the text in the Telegram chat and something else.

To run the warlock open the terminal and execute:

```bash
    cd path/to/your/warlock_directory
    python3 warlock
```
or, to make it easy, you can update your `~/.bashrc` with 

```bash
    alias warlock='/usr/bin/python3 warlock'
```
(upd 2.03.2026) or we can use the Makefile to run our app in the Docker container:
```bash
    make build
    make up
```

If you want to check some available functions, you can type in `warlock` dialog
```bash
    print demo
```
or
```bash
    print demo table
```

Available (in the future) commands list:

```bash
    add the product for tracking
    remove the product for tracking
    run the product tracking
    print the product price history
    print the summary product table
    print demo
    print demo-multi
    print demo table
    
    * search the keyword ' ' in the text {file}
    * search the keyword ' ' among news {url}
    * search the user among messages
    * search the message among messages
    * show the diagram of currencies course
    * show the diagram from the file
    * show the diagram of product price
    * schedule the news tracking
    * schedule the message tracking
    make tests

    * - will be available later
```

### Chapter 1
Okey, boys and girls, let's take a look at the Python scripts. I'm new in Python, so I will learn it with this project development. If this repo will be usefull for you, please like, subscribe and share. And let's learn Python together.

First I've wrote the single script to get info about the products I like. Then, the functions number rise and scripts became many. Classes, of course, was very useful. But, of course, it was just a first version, scratch. So let's do it beter.

After we add the products for tracking (`add product for tracking`) and run the tracking for first time (`run the product tracking`), we'll get the main info about product presence, price and date of tracking.

Warlock can print this info in the command line by request (`print the product summary table`):

```text
---------------------------------------------------------------------------------------------------------
| productName                 | url                                    | price | presence | date        |
|-----------------------------+----------------------------------------+-------+----------+-------------|
| Кіберіада                   | https://knigoland.com.ua/kiberiada-... | 399   | No       | 27/02/2026  | 
| Повернення із зірок         | https://knigoland.com.ua/povernenny... | 289   | Yes      | 27/02/2026  | 
| Розповіді про пілота Піркса | https://knigoland.com.ua/rozpovidi-... | 299   | No       | 27/02/2026  | 
| Test prod 2                 | some.fake@url.dod?adfas;dfjoai j   ... | False | False    | 27/02/2026  | 
---------------------------------------------------------------------------------------------------------

```

One of the most important, I think, is a Test Oriented Development, so I've add some `pytest` tests. They require the `pytest` installed on your OS and can be executed by `warlock` itself:

```bash
    warlock
    'Greeting...'
    'What do you want me to do?'
    make tests
```
or with the shell commands:

```bash
    cd /your_warlock_directory/tests
    pytest
```

### Chapter 2
At some point we have the web pages of the products we like, that encoded (compressed)  with some compress method (gzip, zstd etc.). That means we need most up-to-date modules and OS components. So I've decide to wrap the project in some simple docker container.

I've also use `Makefile`, quite useful tool. We can `up`, `down` the containers, and acces to Warlock by `shell`:

```bash
    make build
    make up
    make up-log
    make shell
    make down
```

### Chapter 3
To implement the different web shop scraping (which have different pages structure), I've added the Abstract scraping provider class to implement inheritance of some common functions for children classes.

### Chapter 4
So we have the simple and tiny data web page scraping. Now let's update the Printing library to get beautifull Charts (the multi line charts also). We can watch demo version with `print demo` or `print demo-multi` in the dialog with Warlock.
```bash
    ----------------------------------------------------------------------------------------
              DEMO History diagram (for single data set)
    ----------------------------------------------------------------------------------------
    _____ | ________________________________________________________________________________
    164.0 | __________________________________________________________________________●_____
    _____ | ________________________________________________________________________________
    _____ | ________________________________________________________________________________
    161.0 | __________________________________________________________●_____________________
    _____ | ________________________________________________________________________________
    _____ | ________________________________________________________________________________
    _____ | ________________________________________________________________________________
    157.0 | __________________________________________________________________●_____________
    _____ | ________________________________________________________________________________
    155.0 | __________________________________________________●_____________________________
    _____ | ________________________________________________________________________________
    153.0 | __●_____________________________________________________________________________
    152.0 | __________●_____________________________________________________________________
    151.0 | __________________________________________●_____________________________________
    150.0 | __________________●_____________________________________________________________
    149.0 | __________________________________●_____________________________________________
    148.0 | __________________________●_____________________________________________________
    _____ | ________________________________________________________________________________
          | 22/05 | 12/06 | 14/07 | 25/08 | 14/09 | 05/10 | 18/11 | 02/12 | 23/01 | 23/02

```

For the development, debugging and just in case we going to add the Logger class, and also the PersonalSettings class to store some info between sessions.

