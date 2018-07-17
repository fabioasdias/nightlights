import React, { Component } from 'react';
import Map from './glmap';
import './App.css';

class App extends Component {
  render() {
    return (
      <div className="App">
        <Map
          URL={'bright.geojson'}
        />
      </div>
    );
  }
}

export default App;
