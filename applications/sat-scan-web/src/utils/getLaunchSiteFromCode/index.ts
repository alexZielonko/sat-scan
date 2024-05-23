import { LAUNCH_SITES } from "./constants";

export const getLaunchSiteFromCode = (
  launchSiteCode: string,
): string | null => {
  return LAUNCH_SITES[launchSiteCode] || null;
};
