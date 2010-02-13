OpenLayers.Renderer.symbol.bus = [10,0, 3,21, 10,18, 18,21, 10,0];

var map;
var route = null;
var popup = null;

function init() {
	map = new OpenLayers.Map('map', {
		controls: [	
			new OpenLayers.Control.Navigation(), 
			new OpenLayers.Control.PanZoomBar(), 
			new OpenLayers.Control.LayerSwitcher()],
		maxExtent : new OpenLayers.Bounds(-20037508.34, -20037508.34,
				20037508.34, 20037508.34),
		numZoomLevels : 15,
		maxResolution : 156543.0399,
		units : 'm',
		projection : new OpenLayers.Projection("EPSG:900913"),
		displayProjection : new OpenLayers.Projection("EPSG:4326")
	});

	var layerMapnik = new OpenLayers.Layer.OSM.Mapnik("Mapnik");

	map.addLayers([layerMapnik]);
	
	var lonLat = new OpenLayers.LonLat(38.8269, 58.0492).transform(new OpenLayers.Projection("EPSG:4326"), map.projection);
	map.setCenter(lonLat, 12);
	loadNDData();
}

function loadNDData() {
	newroute = new OpenLayers.Layer.Vector("Маркеры", {
		strategies : [ new OpenLayers.Strategy.BBOX() ],
		projection : new OpenLayers.Projection("EPSG:4326"),
		protocol : new OpenLayers.Protocol.HTTP( {
			url : "/m/gpx/bus.kml",
			format : new OpenLayers.Format.KML( {
				extractStyles : true,
				extractAttributes : true,
				kmlns : 2.2
			})
				}),
		styleMap : new OpenLayers.StyleMap( {
			"default" : {
				label : "${name}",
				fillColor : "#00ff00",
				strokeColor : "#ffffff",
				strokeOpacity : 1,
				strokeWidth : 1,
				strokeLinecap : "butt",
				fillOpacity : 0.7,
				pointRadius : 16,
				rotation : "${angle}",
				//externalGraphic : "${image}",
				//graphicHeight : 32,
				//graphicYOffset : -16,
				graphicName: "${graphic}",
				fontSize : "18px",
				cursor : "pointer"
			},
			"select" : {
				fillColor : "#8aeeef",
				strokeColor : "#32a8a9"
			}
		})
	});

	newroute.events.register('loadend', this, function() {
	    if(popup != null)
	    	map.removePopup(popup);
		setTimeout("updateKML()",5000);
	});
	newroute.events.register('loadcancel', this, function() {
	    if(popup != null)
	    	map.removePopup(popup);
	    setTimeout("updateKML()",10000);
    });

	map.addLayer(newroute);

	route = newroute;
	route.redraw(true);
}

function updateKML() {
	route.refresh({force: true});
}