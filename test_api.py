import requests


def test_predict(inputs):
    res = requests.post('http://localhost:5000/predict', json=inputs)
    print(res.json())


if __name__ == '__main__':
    inputs = {
        "Store": 2,
        "Dept": 1,
        "Date": "2012-11-02"
    }
    test_predict(inputs)
