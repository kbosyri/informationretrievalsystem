# Project Structure
- __Corpus__
    - Contains All The Preprocessing Programs For dataset __'antique/train'__ those include

        - __MakeCorpus.py__: responsible for storing all the dataset documents into a dictionary and then storing the dictionary in a .json file in the __'Files'__ directory

        - __MakeProcessedCorpus.py__: responsible for sending the corpus from the previous program to be processed by TextServer.py And Then Storing The Results in a .json file in the __'Files'__ directory

        - __MakeInvertedIndex.py__: responsible for creating the inverted index for the corpus and storing it in a dictionary and then storing the dictionary in a .json file in the __'Files'__ directory
    
- __Corpus2__
    - Has the same functionality as __Corpus__ but for __'wikir/en1k/training'__ dataset

- __tfidf__
    - Contains both the query tfidf vector calculation service, and the corpus tfidf vectors generating preprocessing step for dataset __'antique/train'__

        - __MakeTFIDF.py__: responsible for calculating the tfidf vector for every document in the corpus and storing the result in a .json file inside the __'Files'__ directory

        - __tfidfServer.py__: Represents the interface that the other services communicate with to get the tfidf vectors for queries, Calls All The Functions from __calculate_tfidf.py__

        - __calculate_tfidf.py__: The main program for the tfidf vector generating service, contatins the implementation that gets called in __tfidfServer.py__

- __tfidf2__
    - Contains Only the corpus tfidf vectors generating preprocessing step for __'wikir/en1k/training'__

- __text processing__
    - Contains The Text Processing Service Of The System

        - __TextServer.py__: Represents the interface that the other services communicates with for text processing of queries and corpuses, calls the All the functions form __textprocessing.py__

        - __textprocessing.py__: The main program for the text processing service, contains the implementation that gets called in __TextServer.py__

- __Matching__
    - Contains The Matching Service Of THe System

        - __MatchingServer.py__: Represents the interface that the other services communicates with for matching the queries to get results, calls the All the functions form __matching.py__

        - __matching.py__: The main program for the matching service, contains the implementation that gets called in __MatchingServer.py__

- __Ranking__
    - Contains The Ranking Service Of The System

        - __RankingServer.py__: Represents the interface that the other services communicates with for ranking the query results and sorting them by their ranks, calls the All the functions form __ranking.py__

        - __ranking.py__: The main program for the ranking service, contains the implementation that gets called in __RankingServer.py__

- __Evaluation__
    - Contains the evaluation service of the system

        - __EvaluationServer.py__: Represents an interface that __main.py__ communicates with for getting the results evaluation score during the evaluation process, calls the All the functions form __evaluate.py__

        - __evaluate.py__: Contains the main program for the evaluation service, contains the implementation that gets called in __EvaluationServer.py__

- __Files__
    - Contains all the results of the preprocessing of both datasets in form of .json files

- __templates__
    - Contains all the html templates that get rendered by __Flask__ rendering engine

- __static__
    - contains all the static dependencies for the html templates inside the __'templates'__ directory

- __eval.json__
    - Contains the system evaluations results for __'antique/train'__

- __eval2.json__
    - Contains the system evaluations results for __'wikir/en1k/training'__

- __main.py__
    - The Main Gateway To The System, Responsible For sending queries through the different steps to fetch their results, displaying the results by rendering them on the html templates, runninig the evaluation process and calculating evaluation metrics