# Warlock

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
    make self-tests
```
