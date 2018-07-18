import React from 'react'
import mapboxgl from 'mapbox-gl'
import 'mapbox-gl/dist/mapbox-gl.css'
import './glmap.css'


mapboxgl.accessToken = 'pk.eyJ1IjoiZGlhc2YiLCJhIjoiY2plNHpweTRrMDA3MzJ3bmVuMGE5MTM1aCJ9.euL_A73QyruCda9iXc3ESA';



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
      style: 'mapbox://styles/diasf/cjjqdvh110bfy2rpczjs0hplj',
      center: [-80.138,26.109],
      zoom:4
    });
    // diasf.3trjgf18
    navigator.geolocation.getCurrentPosition((d)=>{
      this.moving=true;
      this.map.setZoom(4);
      this.map.flyTo({
        center: [
            d.coords.longitude,
            d.coords.latitude,
            ]});
        });
      this.moving=false;

    let BoundsChange=(d)=>{
      if (d.originalEvent!==undefined){//&&(this.moving===false))  
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
        fetch(this.props.URL)
        .then((response) => {
          if (response.status >= 400) {throw new Error("Bad response from server");}
          return response.json();
        })
        .then((ret)=>{
          console.log(ret)
          this.map.addSource('gj', {
            type: 'geojson',
            data: ret,
          });

          this.map.addLayer({
            id: 'gjlayer',
            type: 'line',
            source: 'gj', 
            paint: {'line-color':'red',
                    },
            // filter: ["!=", "tID", -1]
          }, 'country-label-lg'); 
          this.setFill();            
        });
      }
      this.setState({'map':this.map});
    });
  }

  setFill() {
    if (this.props.paintProp!==undefined){
      this.map.setPaintProperty('gjlayer', 'fill-color', ['get', this.props.paintProp]);    
    }
    // this.map.setFilter('faded',['!', ["has", ["to-string", ['get', "tID"]], ['literal', tids]]]);
    // this.map.setFilter('gjlayer',["has", ["to-string", ['get', "tID"]], ['literal', tids]]);
}

  render() {
    return (
      <div ref={el => this.mapContainer = el} 
      className={(this.props.className!==undefined)?this.props.className:"absolute top right left bottom"}
      />
    );
  }
}


export default Map;
