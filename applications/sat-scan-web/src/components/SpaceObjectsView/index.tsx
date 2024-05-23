import { useEffect, useState } from "react";
import { Popover } from "@headlessui/react";
import { MagnifyingGlassIcon } from "@heroicons/react/20/solid";
import { CONTACT, PROJECT_INFO } from "@/constants/text";
import { RecentSpaceObjects } from "./components/RecentSpaceObjects";
import { SpaceObject } from "@/types/spaceObject";

import { doesSpaceObjectContainText } from "./utils/doesSpaceObjectContainText";
import { SpaceObjectDetail } from "./components/SpaceObjectDetail";
import { hasFilterResults } from "./utils/hasFilterResults";
import { Footer } from "./components/Footer";
import { classNames } from "@/utils/classNames";
import { SpaceObjectsViewProps } from "./types";

export const SpaceObjectsView = ({ spaceObjects }: SpaceObjectsViewProps) => {
  const [filteredSpaceObjects, setFilteredSpaceObjects] = useState<
    SpaceObject[]
  >([]);
  const [selectedSpaceObject, setSelectedSpaceObject] =
    useState<SpaceObject | null>(null);

  useEffect(() => {
    // Set the filtered space object list to an initial value when the space objects are fetched
    setFilteredSpaceObjects(spaceObjects);
  }, [spaceObjects]);

  useEffect(() => {
    // Reset the selected space object when a user filters the results
    const [newSelectedSpaceObject] = filteredSpaceObjects;
    setSelectedSpaceObject(newSelectedSpaceObject);
  }, [filteredSpaceObjects]);

  const [currentFilterTerm, setCurrentFilterTerm] = useState<string | null>(
    null,
  );

  const handleSearch = (event: React.ChangeEvent<HTMLInputElement>) => {
    const input = (event.target as HTMLInputElement)?.value || "";
    const searchTerm = input.trim();

    if (searchTerm && searchTerm.length >= 2) {
      setCurrentFilterTerm(searchTerm);
      const newFilteredSpaceObjects = filteredSpaceObjects.filter(
        (spaceObject) => {
          return doesSpaceObjectContainText(spaceObject, searchTerm);
        },
      );

      setFilteredSpaceObjects(newFilteredSpaceObjects);
    } else if (!searchTerm || searchTerm.length == 0) {
      setCurrentFilterTerm(null);
      setFilteredSpaceObjects(spaceObjects);
    }
  };

  const getResultCountMessage = () => {
    const displayCount = filteredSpaceObjects.length;
    const totalCount = spaceObjects.length;

    return `Displaying ${displayCount} of ${totalCount} results`;
  };

  return (
    <>
      <div className="h-screen">
        <Popover as="header" className="bg-indigo-500 pb-48 pt-12">
          <>
            <div className="mx-auto max-w-3xl px-4 sm:px-6 lg:max-w-7xl lg:px-8">
              <div className="relative flex items-center justify-center py-5 lg:justify-between">
                {/* Logo */}
                <div className="absolute left-0 flex-shrink-0 lg:static">
                  <div className="flex">
                    <span className="text-6xl">🛰️</span>
                    <span className=" text-white my-auto ml-4">
                      <h1 className="text-3xl font-weight-semibold">
                        {PROJECT_INFO.NAME}
                      </h1>
                      <p className="text-gray-100 max-w-[290px] text-sm">
                        {PROJECT_INFO.DESCRIPTION}
                      </p>
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </>
        </Popover>
        <main className="-mt-36 pb-8 h-fit max-h-fit">
          <div className="mx-auto max-w-3xl px-4 sm:px-6 lg:max-w-7xl lg:px-8">
            <div className="grid grid-cols-1 items-start lg:grid-cols-3 lg:gap-8">
              <div className="grid grid-cols-1 lg:col-span-2">
                <h2 className=" text-xl text-white">Recent Space Objects</h2>
                <p className="text-gray-100 text-sm mb-4">
                  {getResultCountMessage()}
                </p>
              </div>

              {/* Search/Filter */}
              <div className="grid grid-cols-1 gap-4 mb-4 lg:mb-0">
                <label htmlFor="mobile-search" className="sr-only">
                  Search
                </label>
                <div className="relative text-white focus-within:text-gray-600">
                  <div className="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3">
                    <MagnifyingGlassIcon
                      className="h-5 w-5"
                      aria-hidden="true"
                    />
                  </div>
                  <input
                    id="mobile-search"
                    className="block w-full rounded-md border-0 bg-white/20 py-1.5 pl-10 pr-3 text-white placeholder:text-white focus:bg-white focus:text-gray-900 focus:ring-0 focus:placeholder:text-gray-500 sm:text-sm sm:leading-6"
                    placeholder="Filter Results"
                    type="search"
                    name="search"
                    onChange={handleSearch}
                  />
                </div>
              </div>
            </div>

            {/* Main 3 column grid */}
            <div className="grid grid-cols-1 items-start gap-4 lg:grid-cols-3 lg:gap-8">
              {/* Left column */}
              <div className="grid grid-cols-1 gap-4 lg:col-span-2">
                <section aria-labelledby="section-1-title">
                  <h2 className="sr-only" id="section-1-title">
                    New Space Objects List
                  </h2>

                  <div className="max-h-[25vh] lg:max-h-[60vh] lg:h-[60vh] overflow-scroll rounded-lg bg-white shadow">
                    {spaceObjects.length == 0 && (
                      <div className="p-24 text-center text-lg text-red-500">
                        ⚠️ Something went wrong: unable to load space objects
                      </div>
                    )}

                    {filteredSpaceObjects.length > 0 && (
                      <RecentSpaceObjects
                        spaceObjects={filteredSpaceObjects}
                        selectedSpaceObject={selectedSpaceObject}
                        onSpaceObjectClick={(spaceObject: SpaceObject) =>
                          setSelectedSpaceObject(spaceObject)
                        }
                      />
                    )}

                    {!!currentFilterTerm &&
                      !hasFilterResults(filteredSpaceObjects) && (
                        <div className="p-24 text-center text-lg">
                          No space objects found for filter text: {'"'}
                          <span className="font-bold">{currentFilterTerm}</span>
                          {'"'}
                        </div>
                      )}
                  </div>
                </section>
              </div>

              {/* Right column */}
              <div className="grid grid-cols-1 gap-4">
                <section aria-labelledby="section-2-title">
                  <h2 className="sr-only" id="section-2-title">
                    Section title
                  </h2>
                  <div
                    className={classNames(
                      "overflow-hidden rounded-lg shadow",
                      selectedSpaceObject == null
                        ? "bg-gray-100 opacity-90"
                        : "bg-white",
                    )}
                  >
                    <div className="p-2 min-h-[300px]">
                      {selectedSpaceObject && (
                        <SpaceObjectDetail spaceObject={selectedSpaceObject} />
                      )}
                    </div>
                  </div>
                </section>
              </div>
            </div>
          </div>
        </main>

        <Footer />
      </div>
    </>
  );
};
