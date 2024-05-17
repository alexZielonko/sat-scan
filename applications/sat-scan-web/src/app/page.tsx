"use client";

import { SpaceObjectsView } from "@/components/SpaceObjectsView";
import { SpaceObject } from "@/types/spaceObject";
import { useEffect, useState } from "react";

export default function Home() {
  return (
    <main className="min-h-screen">
      <SpaceObjectsView />
    </main>
  );
}
