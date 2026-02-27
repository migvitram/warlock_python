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

Available commands list:

```bash
    run the product tracking
    add the product for tracking
    remove the product for tracking
    print the product price history
    print the summary product table
    search the keyword ' ' in the text {file}
    search the keyword ' ' among news {url}
    search the user among messages
    search the message among messages
    show the diagram of currencies course
    show the diagram from the file
    show the diagram of product price
    schedule the news tracking
    schedule the message tracking
    make tests
```

Okey, boys and girls, let's take a look at the python scripts. I'm new in python, so I will learn it with this project development. If this repo will be usefull for you, please like, subscribe and share. And let's learn Python together.

First I've wrote the single script to get info about the products I like. Then, the functions number rise and scripts became many. Classes, of course, was very useful. But, of course, it was just a first version, scratch. So let's do it beter.

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
