var o = [48.3,10.0] //Draw the origin - Add a marker and popup for the place
var B = [-180,-144,-108,-72,-36,0,36,72,108,144,180]
var sw = L.latLng(36.0, 0.0);
var ne = L.latLng(72.0, 36.0);
var grid = L.latLngBounds(sw, ne);
var map = L.map('map', {zoomControl: false, maxBounds: grid, maxBoundsViscosity: 1.0 }).setView(o, 4);
L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png',).addTo(map) 
var y = [[90, o[1]], [-90, o[1]]];   //Dashed line between two points: [latitude, longitude]
var x = [[o[0], -180], [o[0], 180]]; // A horizontal line needs two points: [latitude, longitude]
var lonLine = L.polyline(y, {color: 'red',weight: 2,opacity: 0.7,dashArray: '5, 5' }).addTo(map); 
var latLine = L.polyline(x, {color: 'blue',weight: 2,opacity: 0.7,dashArray: '5, 5'}).addTo(map);
var unicodeIcon = L.divIcon({ className: 'my-unicode-icon', 
    html: '<div style="font-size: 10px; color: blue;">&#9733;</div>',iconSize: [15, 15], iconAnchor: [5,5] });
var loc = [["&#9733;", "Ulrich", o],["&#128218;", "Pavia", [45.200, 9.1050]],["&#127891;","Zurich", [47.8566, 8.3522]],[ "&#129668;", "Prague", [50.4168, 14.7038]]];
loc.forEach(function(x){ L.marker(x[2], { icon: unicodeIcon }).addTo(map).bindPopup("<b>" + x[0]+x[1] + "</b>");});
//locationsInEurope.forEach(function(location) {L.circleMarker([location[1], location[2]]).addTo(map).bindPopup("<b>" + location[0] + "</b>");});
//map.setMaximumBounds(([36,0],[72,36]),{padding: [50, 50]}); // Centered near Germany
//var lonLabel = L.marker([70, 0], {interactive: false }).addTo(map);
//lonLabel.bindTooltip("", {permanent: true, direction: 'right'}).openTooltip();
//var latLabel = L.marker(o, { interactive: false}).addTo(map);
//latLabel.bindTooltip("()", {permanent: true, direction: 'bottom'}).openTooltip();
