import { SpaceObject } from "@/types/spaceObject";
import { useEffect, useState } from "react";
import { SpaceObjectDetail } from "../SpaceObjectDetail";
import { classNames } from "@/utils/classNames";
import { RecentSpaceObjectsProps } from "./types";

export const RecentSpaceObjects = ({
  spaceObjects,
}: RecentSpaceObjectsProps) => {
  const [selectedSpaceObjectId, setSelectedSpaceObjectId] = useState<
    string | null
  >(null);

  const isCurrentSpaceObjectSelected = (spaceObjectId: string): boolean => {
    return selectedSpaceObjectId === spaceObjectId;
  };

  const handleSpaceObjectClick = (spaceObjectId: string) => {
    if (isCurrentSpaceObjectSelected(spaceObjectId)) {
      setSelectedSpaceObjectId(null);
    } else {
      setSelectedSpaceObjectId(spaceObjectId);
    }
  };

  return (
    <ul role="list" className="divide-y divide-gray-100">
      {spaceObjects.map((spaceObject) => (
        <li
          key={spaceObject.sat_id}
          className={classNames(
            "py-5 cursor-pointer",
            "hover:bg-indigo-50",
            isCurrentSpaceObjectSelected(spaceObject.sat_id)
              ? "bg-indigo-100 hover:bg-indigo-100"
              : ""
          )}
          onClick={() => handleSpaceObjectClick(spaceObject.sat_id)}
        >
          <div className="flex justify-between gap-x-6 px-6">
            <div className="flex min-w-0 gap-x-4">
              <div className="min-w-0 flex-auto">
                <p className="text-sm font-semibold leading-6 text-gray-900">
                  Name: {spaceObject.sat_name}
                </p>
                <p className="mt-1 truncate text-xs leading-5 text-gray-500">
                  Type: {spaceObject.object_type}
                </p>
              </div>
            </div>
            <div className="hidden shrink-0 sm:flex sm:flex-col sm:items-end">
              <p className="text-sm leading-6 text-gray-900">
                {spaceObject.launch_country}
              </p>
              {spaceObject.object_type == "UNKNOWN" ? (
                <p className="mt-1 text-xs leading-5 text-gray-500">
                  Unknown Object Type
                </p>
              ) : (
                <div className="mt-1 flex items-center gap-x-1.5">
                  <div className="flex-none rounded-full bg-emerald-500/20 p-1">
                    <div className="h-1.5 w-1.5 rounded-full bg-emerald-500" />
                  </div>
                  <p className="text-xs leading-5 text-gray-500">
                    {spaceObject.launch_date}
                  </p>
                </div>
              )}
            </div>
          </div>
          {selectedSpaceObjectId === spaceObject.sat_id && (
            <SpaceObjectDetail spaceObject={spaceObject} />
          )}
        </li>
      ))}
    </ul>
  );
};
