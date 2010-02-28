        // make map available for easy debugging
        var map;
		
        // increase reload attempts 
        OpenLayers.IMAGE_RELOAD_ATTEMPTS = 3;

        function init(){
            var options = {
                projection: new OpenLayers.Projection("EPSG:900913"),
                displayProjection: new OpenLayers.Projection("EPSG:4326"),
                units: "m",
                numZoomLevels: 18,
                maxResolution: 156543.0339,
                maxExtent: new OpenLayers.Bounds(-20037508, -20037508,
                                                 20037508, 20037508.34)
            };
            map = new OpenLayers.Map('map', options);

            // create Google Mercator layers
            var gmap = new OpenLayers.Layer.Google(
                "Google Streets",
                {'sphericalMercator': true}
            );
            var gsat = new OpenLayers.Layer.Google(
                "Google Satellite",
                {type: G_SATELLITE_MAP, 'sphericalMercator': true, numZoomLevels: 22}
            );
            var ghyb = new OpenLayers.Layer.Google(
                "Google Hybrid",
                {type: G_HYBRID_MAP, 'sphericalMercator': true}
            );

            // create Virtual Earth layers
            var veroad = new OpenLayers.Layer.VirtualEarth(
                "Virtual Earth Roads",
                {'type': VEMapStyle.Road, 'sphericalMercator': true}
            );
            var veaer = new OpenLayers.Layer.VirtualEarth(
                "Virtual Earth Aerial",
                {'type': VEMapStyle.Aerial, 'sphericalMercator': true}
            );
            var vehyb = new OpenLayers.Layer.VirtualEarth(
                "Virtual Earth Hybrid",
                {'type': VEMapStyle.Hybrid, 'sphericalMercator': true}
            );

            // create Yahoo layer
            var yahoo = new OpenLayers.Layer.Yahoo(
                "Yahoo Street",
                {'sphericalMercator': true}
            );
            var yahoosat = new OpenLayers.Layer.Yahoo(
                "Yahoo Satellite",
                {'type': YAHOO_MAP_SAT, 'sphericalMercator': true}
            );
            var yahoohyb = new OpenLayers.Layer.Yahoo(
                "Yahoo Hybrid",
                {'type': YAHOO_MAP_HYB, 'sphericalMercator': true}
            );

            // create OSM layer
            var mapnik = new OpenLayers.Layer.OSM();
            // create OAM layer
            var oam = new OpenLayers.Layer.XYZ(
                "OpenAerialMap",
                "http://tile.openaerialmap.org/tiles/1.0.0/openaerialmap-900913/${z}/${x}/${y}.png",
                {
                    sphericalMercator: true
                }
            );

            // create OSM layer
            var osmarender = new OpenLayers.Layer.OSM(
                "OpenStreetMap (Tiles@Home)",
                "http://tah.openstreetmap.org/Tiles/tile/${z}/${x}/${y}.png"
            );


            // create WMS layer
            var wms = new OpenLayers.Layer.WMS(
                "World Map",
                "http://world.freemap.in/tiles/",
                {'layers': 'factbook-overlay', 'format':'png'},
                {
                    'opacity': 0.4, visibility: false,
                    'isBaseLayer': false,'wrapDateLine': true
                }
            );

            // create a vector layer for drawing
            var vector = new OpenLayers.Layer.Vector("Editable Vectors");

            map.addLayers([gmap, gsat, ghyb, veroad, veaer, vehyb,
                           yahoo, yahoosat, yahoohyb, oam, mapnik, osmarender,
                           wms, vector]);
            map.addControl(new OpenLayers.Control.LayerSwitcher());
            map.addControl(new OpenLayers.Control.EditingToolbar(vector));
            map.addControl(new OpenLayers.Control.Permalink());
            map.addControl(new OpenLayers.Control.MousePosition());
            if (!map.getCenter()) {map.zoomToMaxExtent()}
        }