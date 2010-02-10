		var lat=57.10
		var lon=65.57
		var zoom=13
 		var map;
 		function init(){
			var map = new OpenLayers.Map("map", {
				controls: [new OpenLayers.Control.Navigation(), new OpenLayers.Control.PanZoomBar(), new OpenLayers.Control.LayerSwitcher(), new OpenLayers.Control.Attribution()],
				//				maxExtent: new OpenLayers.Bounds(-20037508.34,-20037508.34,20037508.34,20037508.34),
				//				maxResolution: 156543.0399,
				//				numZoomLevels: 19,
				units: 'm',
			//				projection: new OpenLayers.Projection("EPSG:900913"),
			//				displayProjection: new OpenLayers.Projection("EPSG:4326")
			});
			
			
			// Define the map layer
			// Note that we use a predefined layer that will be
			// kept up to date with URL changes
			// Here we define just one layer, but providing a choice
			// of several layers is also quite simple
			// Other defined layers are OpenLayers.Layer.OSM.Mapnik, OpenLayers.Layer.OSM.Maplint and OpenLayers.Layer.OSM.CycleMap
			var layerMapnik = new OpenLayers.Layer.OSM.Mapnik("ОСМ");
			map.addLayer(layerMapnik);
			var layerMarkers = new OpenLayers.Layer.Markers("Маркеры");
			map.addLayer(layerMarkers);
			var lgpx = new OpenLayers.Layer.GML("Треки", "m/gpx/tyumen.gpx", {
				format: OpenLayers.Format.GPX,
				style: {
					strokeColor: "black",
					strokeWidth: 1,
					strokeOpacity: 1
				},
				projection: new OpenLayers.Projection("EPSG:4326")
			});
			map.addLayer(lgpx);
			
			var lonLat_red = new OpenLayers.LonLat(lon, lat).transform(new OpenLayers.Projection("EPSG:4326"), map.getProjectionObject());
			var lonLat = new OpenLayers.LonLat(lon + 0.1, lat + 0.1).transform(new OpenLayers.Projection("EPSG:4326"), map.getProjectionObject());
			var size = new OpenLayers.Size(21, 25);
			var offset = new OpenLayers.Pixel(-(size.w / 2), -size.h);
			
			var red_marker = new OpenLayers.Marker(lonLat_red, new OpenLayers.Icon('http://www.openstreetmap.org/openlayers/img/marker.png', size, offset));
			
			layerMarkers.addMarker(red_marker);
			map.setCenter(lonLat_red, zoom);
		}