var map;

function set_map_to(lon, lat) {
	var lonLat = new OpenLayers.LonLat(lon, lat).transform(new OpenLayers.Projection("EPSG:4326"), map.projection);
	map.setCenter(lonLat, 12);
}

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
	var gsat = new OpenLayers.Layer.Google("Google Satellite",
		{type: G_SATELLITE_MAP, 'sphericalMercator': true, numZoomLevels: 22}
	);
	map.addLayers([layerMapnik, gsat]);

//	Tyumen
	set_map_to(65.54, 57.13);

//	Tobolsk
//	set_map_to(68.28, 58.22);

	loadNDData();
}

OpenLayers.Renderer.symbol.bus = [10,0, 3,21, 10,18, 18,21, 10,0];

function loadNDData() {
	// Add KML layer with placemarks
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
	map.addLayer(kml_trackers);


	// Add the Layer with GPX Track
	var lgpx = new OpenLayers.Layer.Vector("Пути за сутки", {
		strategies : [ new OpenLayers.Strategy.BBOX() ],
		projection : new OpenLayers.Projection("EPSG:4326"),
		protocol : new OpenLayers.Protocol.HTTP( {
			url : "/trackers/gpx/86400/",
			format : new OpenLayers.Format.GPX()
		}),
		styleMap : new OpenLayers.StyleMap( {
			   "default" : {
					strokeColor: "green",
					strokeWidth: 5,
					strokeOpacity: 0.5
				}
		})
	});

	map.addLayer(lgpx);


	var s = new OpenLayers.Strategy.Refresh({interval: 10000, force: true});
	s.setLayer(kml_trackers);
	s.activate();
	s.reset();

	var s2 = new OpenLayers.Strategy.Refresh({interval: 10000, force: true});
	s2.setLayer(lgpx);
	s2.activate();
	s2.reset();

	kml_trackers.redraw(true);
	lgpx.redraw(true);
}

