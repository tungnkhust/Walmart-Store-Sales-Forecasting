import React from 'react'
import data from './data/data'
import { Form } from 'react-bootstrap'
import 'bootstrap/dist/css/bootstrap.min.css';
class App extends React.Component {
  getStoreOption = () => {
    let options = []
    console.log(data)
    for (let key in data) {
      options.push(
        <option key={key} value={key}>{key}</option>
      )
    }
    return options
  }
  render() {
    return (
      <div className="container">
        <Form.Group controlId="exampleForm.ControlSelect1">
          <Form.Label>Store</Form.Label>
          <Form.Control as="select">
            {this.getStoreOption()}
          </Form.Control>
        </Form.Group>
      </div>
    )
  }
}

export default App;
