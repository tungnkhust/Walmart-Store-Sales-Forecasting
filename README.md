# BTL_BA

## Setup
- To install all library:
```bash
pip install -r requirements.txt
```
- To install each library:
```bash
pip install pandas
```

## Run
- To train model:
```bash
python train.py
```

- To predict test data to submit on Kaggle:
```bash
python predict_submission.py
```

## Run app as API
- To run serve:
```
FLASK_ENV=development FLASK_APP=app.py flask run
```

- To test api vs request. Change input as json such as:
```json
{
  "Store": 1,
  "Dept": 1,
  "Date": "2012-11-02"
}
```
with:
- Store: num of store
- Dept: num of department
- Date: Week

then run command line:
```bash
python test_api.py
```
