"use client";

import type { InferGetStaticPropsType, GetStaticProps } from "next";
import { SpaceObjectsView } from "@/components/SpaceObjectsView";

import { RouteConfig } from "@/types/spaceObject";
export const getStaticProps = (async (context) => {
  const ROUTE_CONFIG = {
    API_URL: process.env.API_URL || "",
  };

  return { props: { routeConfig: ROUTE_CONFIG } };
}) satisfies GetStaticProps<{
  routeConfig: RouteConfig;
}>;

export default function Home({
  routeConfig,
}: InferGetStaticPropsType<typeof getStaticProps>) {
  return (
    <main className="min-h-screen">
      <SpaceObjectsView routeConfig={routeConfig} />
    </main>
  );
}
