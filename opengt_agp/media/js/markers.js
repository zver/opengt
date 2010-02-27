var map;

function init() {
	map = new OpenLayers.Map('map', {
		controls: [	
			new OpenLayers.Control.Navigation(), 
			new OpenLayers.Control.PanZoomBar(), 
			new OpenLayers.Control.LayerSwitcher(),
			new OpenLayers.Control.MousePosition()],
		maxExtent : new OpenLayers.Bounds(	-20037508.34, 
											-20037508.34,
											20037508.34, 
											20037508.34),
		numZoomLevels : 15,
		maxResolution : 156543.0399,
		units : 'm',
		projection : new OpenLayers.Projection("EPSG:900913"),
		displayProjection : new OpenLayers.Projection("EPSG:4326")
	});
	var layerMapnik = new OpenLayers.Layer.OSM.Mapnik("ОСМ");

	map.addLayers([layerMapnik]);

//	Tyumen
//	var lonLat = new OpenLayers.LonLat(65.54, 57.13).transform(new OpenLayers.Projection("EPSG:4326"), map.projection);

//	Tobolsk
	var lonLat = new OpenLayers.LonLat(68.28, 58.22).transform(new OpenLayers.Projection("EPSG:4326"), map.projection);

	map.setCenter(lonLat, 12);
	loadNDData();
}

OpenLayers.Renderer.symbol.bus = [10,0, 3,21, 10,18, 18,21, 10,0];

function loadNDData() {
	kml_trackers = new OpenLayers.Layer.Vector("Маркеры", {
		strategies : [ new OpenLayers.Strategy.BBOX() ],
		projection : new OpenLayers.Projection("EPSG:4326"),
		protocol : new OpenLayers.Protocol.HTTP( {
			url : "/trackers/kml/",
			format : new OpenLayers.Format.KML( {
				extractStyles : true,
				extractAttributes : true,
				kmlns : 2.2
			})
				}),
		styleMap : new OpenLayers.StyleMap( {
			"default" : {
				label : "${name}",
				fillColor : "${marker_color}",
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
				fontSize : "16px",
				cursor : "pointer"
			},
			"select" : {
				fillColor : "#8aeeef",
				strokeColor : "#32a8a9"
			}
		})
	});
	kml_trackers.events.register('loadend', this, function() {
		setTimeout("updateKML()", 10000);
	});
	map.addLayer(kml_trackers);

	// Add the Layer with GPX Track
	var lgpx = new OpenLayers.Layer.GML("Пути за сутки", "/trackers/gpx/86400/", {
						format:		OpenLayers.Format.GPX,
						style:		{strokeColor: "green", strokeWidth: 5, strokeOpacity: 0.5},
						projection: new OpenLayers.Projection("EPSG:4326")
	});
	map.addLayer(lgpx);

	kml_trackers.redraw(true);
}

function updateKML() {
	kml_trackers.refresh({force: true});
}

