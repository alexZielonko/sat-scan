import { InfoItemProps } from "./types";

export const InfoItem = ({ title, value }: InfoItemProps) => {
  return (
    <div className="p-4 sm:grid sm:grid-cols-4 sm:gap-4">
      <dt className="text-sm font-medium text-gray-900">{title}</dt>
      <dd className="mt-1 text-sm leading-2 text-gray-700 sm:col-span-3 sm:mt-0">
        {value}
      </dd>
    </div>
  );
};
