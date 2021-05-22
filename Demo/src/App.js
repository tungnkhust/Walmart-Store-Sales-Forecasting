import React from 'react'
import data from './data/data'

class App extends React.Component {
  render() {
    return (
      <div>
        {JSON.stringify(data)}
      </div>
    )
  }
}

export default App;
