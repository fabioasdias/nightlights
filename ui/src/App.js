import React, { Component } from 'react';
import Map from './glmap';
import './App.css';

class App extends Component {
  render() {
    return (
      <div className="App">
        <Map
          URL={'bright2p.geojson'}
          // URL2={'bright.geojson'}
        />
      </div>
    );
  }
}

export default App;
