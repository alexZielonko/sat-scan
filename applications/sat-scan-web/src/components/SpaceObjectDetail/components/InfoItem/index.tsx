import { InfoItemProps } from "./types";

export const InfoItem = ({ title, value }: InfoItemProps) => {
  return (
    <div className="px-4 py-6 sm:grid sm:grid-cols-6 sm:gap-4 sm:px-6">
      <dt className="text-sm font-medium text-gray-900">{title}</dt>
      <dd className="mt-1 text-sm leading-2 text-gray-700 sm:col-span-5 sm:mt-0">
        {value}
      </dd>
    </div>
  );
};
