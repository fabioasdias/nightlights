import React from 'react'
import mapboxgl from 'mapbox-gl'
import 'mapbox-gl/dist/mapbox-gl.css'
import './glmap.css'
import {sendData} from './urls'
import { connect } from 'react-redux';


mapboxgl.accessToken = 'pk.eyJ1IjoiZGlhc2YiLCJhIjoiY2plNHpweTRrMDA3MzJ3bmVuMGE5MTM1aCJ9.euL_A73QyruCda9iXc3ESA';


const mapStateToProps = (state) => ({
  hiers: state.hiers,
  detailLevel: state.detailLevel,
});


let Map = class Map extends React.Component {
  map;
    

  componentDidUpdate() {
    this.setFill();
  }

  componentWillUpdate(nextProps, nextState) {
    if ((this.moving!==undefined)&&(this.moving)){
      return;
    }
    if (nextProps.boundsCallback!==undefined){
      nextProps.boundsCallback(undefined);
    }
  }


  componentDidMount() {
    this.map = new mapboxgl.Map({
      container: this.mapContainer,
      style: 'mapbox://styles/mapbox/light-v9',
      center: [-80.138,26.109],
      zoom:14
    });

    // navigator.geolocation.getCurrentPosition((d)=>{
    //   this.moving=true;
    //   this.map.setZoom(8);
    //   this.map.flyTo({
    //     center: [
    //         d.coords.longitude,
    //         d.coords.latitude,
    //         ]});
    //     });
    //   this.moving=false;

    let BoundsChange=(d)=>{
      if (d.originalEvent!==undefined){//&&(this.moving===false))
        sendData(this.props.URL,{hiers:this.props.hiers,detailLevel:this.props.detailLevel,viewbox:this.map.getBounds()},(ret)=>{
          console.log('newmap',ret);
          this.map.getSource('gj').setData(ret);
        });
      
        if (this.props.boundsCallback!==undefined){
          this.props.boundsCallback(this.map.getBounds());
        }
      }
    }

    this.map.on('dragend', BoundsChange);
    this.map.on('zoomend', BoundsChange);    
    this.map.on('movestart',()=>{this.moving=true;});
    this.map.on('moveend',()=>{this.moving=false;});

    this.map.on('load', () => {
      if (this.props.URL!==undefined){
        sendData(this.props.URL,{hiers:this.props.hiers,detailLevel:this.props.detailLevel,viewbox:this.map.getBounds()},(ret)=>{
          console.log(ret)
          this.map.addSource('gj', {
            type: 'geojson',
            data: ret,
          });

          this.map.addLayer({
            id: 'gjlayer',
            type: 'fill',
            source: 'gj',
            paint: {'fill-opacity':0.75},
            // filter: ["!=", "tID", -1]
          }, 'country-label-lg'); 
          this.setFill();            
        });
      }
      this.setState({'map':this.map});
    });
  }

  setFill() {
    this.map.setPaintProperty('gjlayer', 'fill-color', ['get', this.props.paintProp]);    
    // this.map.setFilter('faded',['!', ["has", ["to-string", ['get', "tID"]], ['literal', tids]]]);
    // this.map.setFilter('gjlayer',["has", ["to-string", ['get', "tID"]], ['literal', tids]]);
}

  render() {
    return (
      <div ref={el => this.mapContainer = el} 
      className={(this.props.className!==undefined)?this.props.className:"absolute top right left bottom"}/>
    );
  }
}


export default connect(mapStateToProps)(Map);
