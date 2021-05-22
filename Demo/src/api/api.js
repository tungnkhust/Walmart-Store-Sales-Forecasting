import axios from 'axios'

const api = {
    getPredic: async (store, dept) => {
        return axios.post('localhost:5000/predic', {
            Store: store,
            Dept: dept
        })
    }
}

export default api