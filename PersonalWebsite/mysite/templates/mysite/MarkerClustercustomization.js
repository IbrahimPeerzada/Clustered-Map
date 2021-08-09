var tiles = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
				maxZoom: 18,
				attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
			}),
			latlng = new L.LatLng(50.5, 30.51);

		var map = new L.Map('map', {center: latlng, zoom: 15, layers: [tiles]});

		var markers = new L.MarkerClusterGroup();
		var markersList = [];

		function populate() {
			for (var i = 0; i < 100; i++) {
				var m = new L.Marker(getRandomLatLng(map));
				markersList.push(m);
				markers.addLayer(m);
			}
			return false;
		}
		function populateRandomVector() {
			for (var i = 0, latlngs = [], len = 20; i < len; i++) {
				latlngs.push(getRandomLatLng(map));
			}
			var path = new L.Polyline(latlngs);
			map.addLayer(path);
		}
		function getRandomLatLng(map) {
			var bounds = map.getBounds(),
				southWest = bounds.getSouthWest(),
				northEast = bounds.getNorthEast(),
				lngSpan = northEast.lng - southWest.lng,
				latSpan = northEast.lat - southWest.lat;

			return new L.LatLng(
					southWest.lat + latSpan * Math.random(),
					southWest.lng + lngSpan * Math.random());
		}

		markers.on('clusterclick', function (a) {
			alert('cluster ' + a.layer.getAllChildMarkers().length);
		});
		markers.on('click', function (a) {
			alert('marker ' + a.layer);
		});

		populate();
		map.addLayer(markers);

		L.DomUtil.get('populate').onclick = function () {
			var bounds = map.getBounds(),
			southWest = bounds.getSouthWest(),
			northEast = bounds.getNorthEast(),
			lngSpan = northEast.lng - southWest.lng,
			latSpan = northEast.lat - southWest.lat;
			var m = new L.Marker(new L.LatLng(
					southWest.lat + latSpan * 0.5,
					southWest.lng + lngSpan * 0.5));
			markersList.push(m);
			markers.addLayer(m);
		};
		L.DomUtil.get('remove').onclick = function () {
			markers.removeLayer(markersList.pop());
		};