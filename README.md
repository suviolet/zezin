# Zezin

-  App para GET e POST de PDV's, usando:
    - python 3.7.3
    - Flask
    - Postgres
    - Flask-SQLAlchemy
    - GeoAlchemy2

Antes de começar, é necessário a criação e ativação de uma VirtualEnv com Python 3.7.3, para isso recomendo pyenv.
Após isso, vá para a pasta raiz desse projeto (zezin) e siga as instruções abaixo.

1) Instale os requisitos do projeto

    ```shell
    $ make requirements-pip
    ```

2) Suba o docker

    ```shell
    $ make docker-compose-up
    ```

3) Faça a migração e suba a aplicação

    ```shell
    $ make runserver-dev
    ```

***

## Usando a aplicação com curl:

- Cria um novo parceiro no banco:

    ```shell
    $ curl -X POST 'http://127.0.0.1:5000/partners/' -d '{"owner_name": "Ze do churros", "document": "209/30000", "trading_name": "Churreria do ze",  "coverage_area": {"type": "MultiPolygon", "coordinates": [[[[-43.36556, -22.99669], [-43.36539, -23.01928 ], [ -43.26583, -23.01802 ], [ -43.25724, -23.00649 ], [ -43.23355, -23.00127 ], [ -43.2381, -22.99716 ], [ -43.23866, -22.99649 ], [ -43.24063, -22.99756 ], [ -43.24634, -22.99736 ], [ -43.24677, -22.99606 ], [ -43.24067, -22.99381 ], [ -43.24886, -22.99121 ], [ -43.25617, -22.99456 ], [ -43.25625, -22.99203 ], [ -43.25346, -22.99065 ], [ -43.29599, -22.98283 ], [ -43.3262, -22.96481 ], [-43.33427, -22.96402], [-43.33616, -22.96829], [-43.342, -22.98157], [-43.34817, -22.97967], [-43.35142, -22.98062], [-43.3573, -22.98084], [-43.36522, -22.98032], [-43.36696, -22.98422], [-43.36717, -22.98855], [-43.36636, -22.99351], [-43.36556, -22.99669]]]]}, "address": {"type": "Point", "coordinates": [-43.297337, -23.013538]}}' -H 'Content-type: application/json'
    ```

    ```
    {"address":{"coordinates":[-43.297337,-23.013538],"type":"Point"},"coverage_area":{"coordinates":[[[[-43.36556,-22.99669],[-43.36539,-23.01928],[-43.26583,-23.01802],[-43.25724,-23.00649],[-43.23355,-23.00127],[-43.2381,-22.99716],[-43.23866,-22.99649],[-43.24063,-22.99756],[-43.24634,-22.99736],[-43.24677,-22.99606],[-43.24067,-22.99381],[-43.24886,-22.99121],[-43.25617,-22.99456],[-43.25625,-22.99203],[-43.25346,-22.99065],[-43.29599,-22.98283],[-43.3262,-22.96481],[-43.33427,-22.96402],[-43.33616,-22.96829],[-43.342,-22.98157],[-43.34817,-22.97967],[-43.35142,-22.98062],[-43.3573,-22.98084],[-43.36522,-22.98032],[-43.36696,-22.98422],[-43.36717,-22.98855],[-43.36636,-22.99351],[-43.36556,-22.99669]]]],"type":"MultiPolygon"},"document":"209/30000","owner_name":"Ze do churros","trading_name":"Churreria do Ze"}
    ```

- Retorna um parceiro por id:

    ```shell
    $ curl -X GET 'http://127.0.0.1:5000/partners/1/' -H 'Content-type: application/json'
    $ curl -X GET 'http://127.0.0.1:5000/partners/1/' -H 'Content-type: application/json' | python -m json.tool # pretty view
    ```

    ```
    {
        "address": {
            "coordinates": [
                -43.297337,
                -23.013538
            ],
            "type": "Point"
        },
        "coverage_area": {
            "coordinates": [
                [
                    [
                        [
                            -43.36556,
                            -22.99669
                        ],
                        ...
                        [
                            -43.36556,
                            -22.99669
                        ]
                    ]
                ]
            ],
            "type": "MultiPolygon"
        },
        "document": "209/30000",
        "owner_name": "Ze do churros",
        "trading_name": "Churreria do Ze"
    }
    ```

- Procura por parceiro mais próximo dentro da area de cobertura:

    ```shell
    $ curl -X GET 'http://127.0.0.1:5000/partners/?lat=-23.0104&lng=-43.3562'
    $ curl -X GET 'http://127.0.0.1:5000/partners/?lat=-23.0104&lng=-43.3562' | python -m json.tool # pretty view
    ```

    ```
    {
        "address": {
            "coordinates": [
                -43.297337,
                -23.013538
            ],
            "type": "Point"
        },
        "coverage_area": {
            "coordinates": [
                [
                    [
                        [
                            -43.36556,
                            -22.99669
                        ],
                        ...
                        [
                            -43.36556,
                            -22.99669
                        ]
                    ]
                ]
            ],
            "type": "MultiPolygon"
        },
        "document": "209/30000",
        "owner_name": "Ze do churros",
        "trading_name": "Churreria do ze"
    }
    ```

***
- Caso queira testar com os dados do arquivo `pdvs.json` rodar os seguintes comandos:

    ```
    $ make populate
    $ make runserver
    ```

- Procura por parceiro mais próximo dentro da area de cobertura utilizando os dados da base populada:

    ```shell
    $ curl -X GET 'http://127.0.0.1:5000/partners/?lat=-23.61440&lng=-46.62135'
    $ curl -X GET 'http://127.0.0.1:5000/partners/?lat=-23.61440&lng=-46.62135' | python -m json.tool # pretty view
    ```

    ```
    {
        "address": {
            "coordinates": [
                -46.624012,
                -23.611038
            ],
            "type": "Point"
        },
        "coverage_area": {
            "coordinates": [
                [
                    [
                        [
                            -46.64198,
                            -23.575
                        ],
                        ...
                        [
                            -46.64198,
                            -23.575
                        ]
                    ]
                ]
            ],
            "type": "MultiPolygon"
        },
        "document": "26.091.851/0001-80",
        "owner_name": "Rai da Silva",
        "trading_name": "Adega Sao Paulo"
    }
    ```

***

## Para testar a aplicação:
- Rodar testes unitários:

    ```shell
    $ make test
    ```

- Rodar cobertura dos testes:

    ```shell
    $ make coverage
    ```