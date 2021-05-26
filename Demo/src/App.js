import React from 'react'
import data from './data/data'
import { Form, Col, Row, Button } from 'react-bootstrap'
import api from './api/api'
import 'bootstrap/dist/css/bootstrap.min.css';
import ApexChart from './Chart';
class App extends React.Component {
  constructor(props) {
    super(props)
    this.state = {
      store: 1,
      dept: 1,
      data: []
    }
  }

  getStoreOption = () => {
    let options = []
    for (let key in data) {
      options.push(
        <option key={key} value={key}>{key}</option>
      )
    }
    return options
  }

  getDeptOption = (store) => {
    let options = []
    for (let key in data[store]) {
      options.push(
        <option key={key} value={key}>{key}</option>
      )
    }
    return options
  }

  changeStore = (e) => {
    this.setState({ store: e.target.value })
  }
  changeDept = (e) => {
    this.setState({ dept: e.target.value })
  }

  submit = async (e) => {
    e.preventDefault()
    try {
      let res = await api.getPredict(this.state.store, this.state.dept)
      let date = res.data.Date;
      let weekly_sales = res.data.Weekly_Sales;
      let len = date.length;
      let data = [];
      for (let i = 0; i < len; i++) {
        let datum = {
          x: new Date(date[i]).getTime(),
          y: weekly_sales[i]
        }
        data.push(datum);
      }
      this.setState({ data });
    } catch (err) {
      console.log(err)
    }
  }

  render() {
    return (
      <div className="container">
        <Form>
          <Form.Group controlId="exampleForm.ControlSelect1">
            <Row>
              <div className="h1">Demo</div>
            </Row>
            <Row>
              <Col>
                <Form.Label>Store</Form.Label>
                <Form.Control as="select" onChange={this.changeStore}>
                  {this.getStoreOption()}
                </Form.Control>
              </Col>
              <Col>
                <Form.Label>Department</Form.Label>
                <Form.Control as="select" onChange={this.changeDept}>
                  {this.getDeptOption(this.state.store)}
                </Form.Control>
              </Col>
            </Row>
          </Form.Group>
          <Form.Group>
            <Row>
              <Col>
                <Button variant="primary" type="submit" className="w-100" onClick={this.submit}>Submit</Button>
              </Col>
            </Row>
          </Form.Group>
        </Form>
        <div>
          <ApexChart data={this.state.data} />
        </div>
      </div>
    )
  }
}

export default App;
