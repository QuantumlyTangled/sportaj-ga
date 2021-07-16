import axios from 'axios';
import type * as GeoJSON from 'geojson';
import React from 'react';
import ReactMapGL, { FullscreenControl, GeolocateControl, Layer, Source } from 'react-map-gl';
import { useDispatch, useSelector } from 'react-redux';
import { selectViewport, setViewport } from 'state/reducers/map';
import useSWR from 'swr';

export interface MapMapProps {}

const fetcher = (url: string) => axios.get(url).then((res) => res.data);

const MapMap: React.FC<MapMapProps> = () => {
	const viewport = useSelector(selectViewport);
	const dispatch = useDispatch();

	const { data } = useSWR<GeoJSON.FeatureCollection<GeoJSON.Geometry>>('/api/data/clubs', fetcher, {
		refreshWhenHidden: false,
		refreshInterval: 10000
	});

	return (
		<>
			<ReactMapGL
				{...viewport}
				// TODO: fetch from API endpoint
				mapboxApiAccessToken="pk.eyJ1IjoicXVhbnR1bWx5IiwiYSI6ImNrcjNyODM0MjJscmcybnFoMnNidzJ5cnUifQ.KDqGaslaoCFpU3X6e96MUA"
				mapStyle="mapbox://styles/quantumly/ckr4hgwcl0gtk18o6x7k739a2"
				width="100%"
				height="100%"
				onViewportChange={(viewport: unknown) => dispatch(setViewport(viewport as any))}
			>
				<FullscreenControl className="right-16 top-4" />
				<GeolocateControl className="right-4 top-4" positionOptions={{ enableHighAccuracy: true }} trackUserLocation={true} auto={true} />
				<Source id="clubs" type="geojson" data={data}>
					<Layer
						id="point"
						type="circle"
						paint={{
							'circle-radius': 10,
							'circle-color': '#007cbf'
						}}
					/>
				</Source>
			</ReactMapGL>
		</>
	);
};

export default MapMap;
