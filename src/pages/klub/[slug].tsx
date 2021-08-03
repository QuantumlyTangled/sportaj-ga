import { gql } from '@apollo/client';
import type { Club } from '@sportajga/mappings';
import ClubAddress from 'components/Club/ClubAddress';
import ClubCalendar from 'components/Club/ClubCalendar';
import ClubDescription from 'components/Club/ClubDescription';
import ClubLogo from 'components/Club/ClubLogo';
import type { LatLon } from 'components/Club/ClubMap';
import Loading from 'components/Loading';
import Offset from 'components/Offset';
import { client, GraphQLResponse } from 'core/apiClient';
import { allClubSlugs } from 'core/clubs';
import type { GetStaticProps, NextPage } from 'next';
import { NextSeo } from 'next-seo';
import { useRouter } from 'next/dist/client/router';
import dynamic from 'next/dynamic';
import React, { useEffect, useState } from 'react';
import ReactPlaceholder from 'react-placeholder/lib';

export interface KlubProps {
	name: string;
	description: string | null;
	location: string | null;
	locationFriendly: string | null;
	logo: string | null;
}

const ClubMap = dynamic(() => import('components/Club/ClubMap'), {
	ssr: false,
	loading: () => (
		<ReactPlaceholder showLoadingAnimation={true} ready={false} type="rect">
			.
		</ReactPlaceholder>
	)
});

const KlubPage: NextPage<KlubProps> = ({ name, description, location, locationFriendly, logo }) => {
	const router = useRouter();
	const [latLon, setLatLon] = useState<LatLon>();

	useEffect(() => {
		if (location) {
			const [latitude, longitude] = location.split(',').map(Number);
			setLatLon({ latitude, longitude });
		}
		// eslint-disable-next-line react-hooks/exhaustive-deps
	}, []);

	if (router.isFallback) {
		return <Loading />;
	}

	return (
		<>
			<NextSeo //
				title={name}
				description={description ?? undefined}
			/>
			<Offset />
			<div className="container pb-8 px-4 md:px-0">
				<div className="flex flex-wrap">
					<div className="content-center w-7/24 hidden md:block">
						<div className="bg-white rounded-md shadow-lg">
							<figure className="px-10 pt-10">
								<ClubLogo logo={logo} name={name} />
							</figure>
							{locationFriendly && (
								<div className="card">
									<div className="card-body">
										<ClubAddress address={locationFriendly} />
									</div>
								</div>
							)}
							{location && latLon && (
								<div className="h-96 p-4">
									<ClubMap latlon={latLon} title={name} />
								</div>
							)}
						</div>
					</div>
					<div className="md:w-1/24" />
					<div className="w-full bg-white rounded-md shadow-lg md:w-15/24">
						<figure className="px-10 pt-10">
							<img className="w-full h-auto rounded-md" src="https://storage.googleapis.com/sportaj-cdn/headers/5.jpg" />
						</figure>
						<div className="card px-10">
							<div className="card-body">
								<span className="card-title text-center">{name}</span>
								{locationFriendly && <ClubAddress address={locationFriendly} className="md:hidden text-sm" />}
								<div className="flex flex-col py-4">
									<section className="flex justify-between">
										<p>1</p>
										<p>2</p>
									</section>
								</div>
								<ClubDescription description={description} />
								<ClubCalendar className="hidden md:block" />
							</div>
						</div>
					</div>
				</div>
			</div>
		</>
	);
};

const GET_CLUB = gql`
	query Club($slug: citext!) {
		club(where: { slug: { _eq: $slug } }) {
			name
			description
			location
			location_friendly
			logo
		}
	}
`;

export const getStaticProps: GetStaticProps<KlubProps, { slug: string }> = async ({ params }) => {
	const { data } = await client.query<GraphQLResponse<'club'>>({ query: GET_CLUB, variables: { slug: params?.slug } });
	const club = data.club as Pick<Club, 'name' | 'description' | 'location' | 'location_friendly' | 'logo'>;

	return {
		props: {
			name: club.name!,
			description: club.description!,
			location: club.location!,
			locationFriendly: club.location_friendly!,
			logo: club.logo!
		},
		revalidate: 120
	};
};

export async function getStaticPaths() {
	const slugs = await allClubSlugs();

	return {
		paths: slugs.map((slug) => ({ params: { slug }, locale: 'sl' })),
		fallback: true
	};
}

export default KlubPage;
