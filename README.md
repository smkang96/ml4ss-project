# ml4ss-project

## Preparation
- Activate virtual environment
```
$ python3 -m venv venv
$ source venv/bin/activate
```
- Install requirements
```
$ pip install -r requirements.txt
```
- Create directory to save models
```
$ mkdir models
```

## Execution
- Create models
```
$ python main.py -c
    [-c] Create models (necessary on first run)
```
- Get results (results are already in `results/`)
```
$ python main.py -t -l
    [-t] Evaluate tf-idf
    [-l] Evaluate LDA
```
