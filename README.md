# Market Service
The Market Service provides APIs for the following entities, Create API needs to be admin but read APIs are public:

1. Assets:

    Assets that can be trated.

2. Symbols:

    Symbols that can be traded, each symbol is for trading a pair of assets.


# Execution

In the project directory you have the following options:

* Python:
    
    1. Install the requirments.txt file:

        ```
        pip install -r requirements.txt
        ```

    2.  Run the following command:

        ```
        python app/main.py
        ```

* Docker:

    Run the following command:
    ```
    docker-compose up
    ```
    or 
    ```
    docker-compose up -d 
    ```
    to run in detach mode.