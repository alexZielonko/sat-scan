import { classNames } from "@/utils/classNames";
import { RecentSpaceObjectsProps } from "./types";

export const RecentSpaceObjects = ({
  spaceObjects,
  selectedSpaceObject,
  onSpaceObjectClick,
}: RecentSpaceObjectsProps) => {
  const isCurrentSpaceObjectSelected = (spaceObjectId: string): boolean => {
    return selectedSpaceObject?.satellite.id === spaceObjectId;
  };

  return (
    <ul role="list" className="divide-y divide-gray-100">
      {spaceObjects.map((spaceObject) => (
        <li
          key={spaceObject.satellite.id}
          className={classNames(
            "py-5 cursor-pointer",
            "hover:bg-indigo-50",
            isCurrentSpaceObjectSelected(spaceObject.satellite.id)
              ? "bg-indigo-100 hover:bg-indigo-100"
              : ""
          )}
          onClick={() => onSpaceObjectClick(spaceObject)}
        >
          <div className="flex justify-between gap-x-6 px-6">
            <div className="flex min-w-0 gap-x-4">
              <div className="min-w-0 flex-auto">
                <p className="text-sm font-semibold leading-6 text-gray-900">
                  Name: {spaceObject.satellite.name}
                </p>
                <p className="mt-1 truncate text-xs leading-5 text-gray-500">
                  {spaceObject.launch.date}
                </p>
              </div>
            </div>
          </div>
        </li>
      ))}
    </ul>
  );
};
