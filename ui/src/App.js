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
        <footer className="footer">
          Original satellite data from <a target="_blank" rel="noopener noreferrer" href="https://ngdc.noaa.gov/eog/viirs/download_dnb_composites.html"> the Earth Observation Group, NOAA National Geophysical Data Center</a>.
          &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
          <a target="_blank" rel="noopener noreferrer" href="https://github.com/fabioasdias/nightlights/">Project page</a>
        </footer>
      </div>
    );
  }
}

export default App;
