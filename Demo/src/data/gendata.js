let csv = require('csvtojson')
let fs = require('fs')

let data = {}
const createData = async () => {
    let arr = await csv().fromFile('./stores.csv');
    for (let i = 0; i < arr.length; i++) {
        data[arr[i].Store] = {}
    }
    arr = await csv().fromFile('./test.csv')
    for (let i = 0; i < arr.length; i++) {
        if (data[arr[i].Store][arr[i].Dept]) {
            data[arr[i].Store][arr[i].Dept].push(arr[i].Date)
        } else {
            data[arr[i].Store][arr[i].Dept] = []
        }
    }
    fs.writeFileSync('./data.js', 'let Data =' + JSON.stringify(data) + '; export default Data');

}
createData()
