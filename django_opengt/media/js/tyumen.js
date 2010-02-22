		var lat=57.10
		var lon=65.57
		var zoom=13
 		var map;
		var route = null;
		var popup = null;
 		function init(){
			var map = new OpenLayers.Map("map", {
				controls: [	
							new OpenLayers.Control.Navigation(), 
							new OpenLayers.Control.PanZoomBar(), 
							new OpenLayers.Control.LayerSwitcher(),
							new OpenLayers.Control.Attribution()],
				maxExtent: 	new OpenLayers.Bounds(	-20037508.34,
													-20037508.34,
													20037508.34,
													20037508.34),
				maxResolution: 156543.0399,
				numZoomLevels: 15,
				units:"m",
				projection: 		new OpenLayers.Projection("EPSG:900913"),
				displayProjection: 	new OpenLayers.Projection("EPSG:4326")
				
			});
			
			var layerMapnik = new OpenLayers.Layer.OSM.Mapnik("ОСМ");
			map.addLayer(layerMapnik);
			
			var layerMarkers = new OpenLayers.Layer.Markers("Маркеры");
			map.addLayer(layerMarkers);

/*			var newroute = new OpenLayers.Layer.Vector("KML", {
					strategies : [ new OpenLayers.Strategy.BBOX() ],
					projection : new OpenLayers.Projection("EPSG:4326"),
					protocol : new OpenLayers.Protocol.HTTP( {
						url : "http://voronkin.homelinux.org:4545/gps/nddata?ids=1,2,3,4,5,6",
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
			map.addLayer(layerMarkers);
*/			
			var lonLat = new OpenLayers.LonLat(lon, lat).transform(new OpenLayers.Projection("EPSG:4326"), map.getProjectionObject());

			var size = new OpenLayers.Size(21, 25);
			var offset = new OpenLayers.Pixel(-(size.w / 2), -size.h);
			var red_marker = new OpenLayers.Marker(lonLat, new OpenLayers.Icon('http://www.openstreetmap.org/openlayers/img/marker.png', size, offset));
			layerMarkers.addMarker(red_marker);
			
			map.setCenter(lonLat, zoom);
			loadNDData();
		}

function onPopupClose(evt) {
	selectControl.unselect(selectedFeature);
}

function onFeatureSelect(feature) {
	// loadPoi(feature.attributes.bsid);
	selectedFeature = feature;
	feat = feature;
	text = '<h3>' + feat.attributes.description + '</h3>';
    if(popup != null)
    	map.removePopup(popup);
	popup = new OpenLayers.Popup.FramedCloud("chicken", feature.geometry
			.getBounds().getCenterLonLat(), new OpenLayers.Size(100, 100),
			text, null, true, onPopupClose);
	feature.popup = popup;
	popup.setOpacity(0.7);
	map.addPopup(popup);
}

function onFeatureUnselect(feature) {
	map.removePopup(feature.popup);
	feature.popup.destroy();
	feature.popup = null;
}

function loadNDData() {
	newroute = new OpenLayers.Layer.Vector("NDDATA", {
		strategies : [ new OpenLayers.Strategy.BBOX() ],
		projection : new OpenLayers.Projection("EPSG:4326"),
		protocol : new OpenLayers.Protocol.HTTP( {
			url : "http://voronkin.homelinux.org:4545/gps/nddata?ids=1",
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
	selectControl = new OpenLayers.Control.SelectFeature(map.layers[1], {
		onSelect : onFeatureSelect,
		onUnselect : onFeatureUnselect
	});

	selectControl = new OpenLayers.Control.SelectFeature(map.layers[2], {
		onSelect : onFeatureSelect,
		onUnselect : onFeatureUnselect
	});

	selectControl = new OpenLayers.Control.SelectFeature(map.layers[3], {
		onSelect : onFeatureSelect,
		onUnselect : onFeatureUnselect
	});

	selectControl = new OpenLayers.Control.SelectFeature(map.layers[4], {
		onSelect : onFeatureSelect,
		onUnselect : onFeatureUnselect
	});

	selectControl = new OpenLayers.Control.SelectFeature(map.layers[5], {
		onSelect : onFeatureSelect,
		onUnselect : onFeatureUnselect
	});

	map.addControl(selectControl);
	selectControl.activate();
	if (route != null)
		map.removeLayer(route);
	route = newroute;
	route.redraw(true);
// 	setTimeout("loadNDData()",5000);
// 	setTimeout("updateKML()",5000);
}