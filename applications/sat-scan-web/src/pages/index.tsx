"use client";

import type { InferGetServerSidePropsType, GetServerSideProps } from "next";
import { SpaceObjectsView } from "@/components/SpaceObjectsView";

import { SpaceObject } from "@/types/spaceObject";
import { fetchSpaceObjects } from "@/interfaces/spaceObject";
import { normalizeSpaceObjects } from "@/utils/normalizeSpaceObjects";

export const getServerSideProps = (async () => {
  const routeConfig = {
    API_URL: process.env.API_URL || "",
  };

  const spaceObjects = await fetchSpaceObjects(routeConfig);
  const normalizedSpaceObjects = normalizeSpaceObjects(spaceObjects);

  return { props: { spaceObjects: normalizedSpaceObjects } };
}) satisfies GetServerSideProps<{
  spaceObjects: SpaceObject[];
}>;

export default function Home({
  spaceObjects,
}: InferGetServerSidePropsType<typeof getServerSideProps>) {
  return (
    <main className="min-h-screen">
      <SpaceObjectsView spaceObjects={spaceObjects} />
    </main>
  );
}
