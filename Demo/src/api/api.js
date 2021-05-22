import axios from 'axios'

const headers = {
    'Content-Type': 'application/json',
}

const api = {
    getPredict: async (store, dept) => {
        return axios.post(
            'http://localhost:5000/predict',
            {
                Store: store,
                Dept: dept
            },
            {
                headers: headers
            }
        )
    }
}

export default api