import { SpaceObjectDetailProps } from "./types";
import { InfoItem } from "./components/InfoItem";

export const SpaceObjectDetail = ({ spaceObject }: SpaceObjectDetailProps) => {
  return (
    <div className="overflow-scroll bg-white">
      <div className="px-2 py-2">
        <h3 className="text-base font-semibold leading-7 text-gray-900">
          Space Object Detail
        </h3>
      </div>
      <div className="border-t border-gray-100">
        <dl className="divide-y divide-gray-100">
          <InfoItem title="Satellite Name" value={spaceObject.satellite.name} />
          <InfoItem title="Launch Date" value={spaceObject.launch.date} />
          <InfoItem
            title="Launch Country"
            value={spaceObject.launch.location.country}
          />
          <InfoItem
            title="Launch Site"
            value={spaceObject.launch.location.site}
          />
          <InfoItem title="Space Object Type" value={spaceObject.objectType} />
        </dl>
      </div>
    </div>
  );
};
