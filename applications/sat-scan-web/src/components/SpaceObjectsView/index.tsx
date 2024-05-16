import { Popover } from "@headlessui/react";
import { MagnifyingGlassIcon } from "@heroicons/react/20/solid";
import { CONTACT, PROJECT_INFO } from "@/constants/text";
import { classNames } from "@/utils/classNames";
import { RecentSpaceObjects } from "../RecentSpaceObjects";

const navigation: { name: string; href: string; current: boolean }[] = [
  // { name: "Home", href: "#", current: true },
  // { name: "About", href: "#", current: false },
];

export const SpaceObjectsView = () => {
  return (
    <>
      <div className="h-screen">
        <Popover as="header" className="bg-indigo-500 pb-48 pt-12">
          <>
            <div className="mx-auto max-w-3xl px-4 sm:px-6 lg:max-w-7xl lg:px-8">
              <div className="relative flex items-center justify-center py-5 lg:justify-between">
                {/* Logo */}
                <div className="absolute left-0 flex-shrink-0 lg:static">
                  <a href="/" className="flex">
                    <span className="text-6xl">🛰️</span>
                    <span className="text-2xl text-white font-weight-semibold my-auto ml-4">
                      {PROJECT_INFO.NAME}
                    </span>
                  </a>
                </div>

                {/* Search */}
                <div className="min-w-0 flex-1 px-12 lg:hidden">
                  <div className="mx-auto w-full max-w-xs hidden">
                    <label htmlFor="desktop-search" className="sr-only">
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
                        id="desktop-search"
                        className="block w-full rounded-md border-0 bg-white/20 py-1.5 pl-10 pr-3 text-white placeholder:text-white focus:bg-white focus:text-gray-900 focus:ring-0 focus:placeholder:text-gray-500 sm:text-sm sm:leading-6"
                        placeholder="Search"
                        type="search"
                        name="search"
                      />
                    </div>
                  </div>
                </div>
              </div>
              <div className="hidden border-t border-white border-opacity-20 py-5 lg:block">
                <div className="grid grid-cols-3 items-center gap-8">
                  <div className="col-span-2">
                    <nav className="flex space-x-4">
                      {navigation.map((item) => (
                        <a
                          key={item.name}
                          href={item.href}
                          className={classNames(
                            item.current ? "text-white" : "text-indigo-100",
                            "rounded-md bg-white bg-opacity-0 px-3 py-2 text-sm font-medium hover:bg-opacity-10"
                          )}
                          aria-current={item.current ? "page" : undefined}
                        >
                          {item.name}
                        </a>
                      ))}
                    </nav>
                  </div>
                  <div>
                    <div className="mx-auto w-full max-w-md">
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
                          placeholder="Search"
                          type="search"
                          name="search"
                        />
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </>
        </Popover>
        <main className="-mt-44 pb-8 h-fit max-h-fit">
          <div className="mx-auto max-w-3xl px-4 sm:px-6 lg:max-w-7xl lg:px-8">
            <h1 className="mb-8 text-2xl text-white">Space Objects</h1>
            <div className="">
              <section aria-labelledby="section-1-title">
                <h2 className="sr-only" id="section-1-title">
                  New Space Objects List
                </h2>
                <div className="max-h-[60vh] overflow-scroll rounded-lg bg-white shadow">
                  <div className="mb-8">
                    <RecentSpaceObjects />
                  </div>
                </div>
              </section>
            </div>
          </div>
        </main>
        <footer>
          <div className="mx-auto max-w-3xl px-4 sm:px-6 lg:max-w-7xl lg:px-8">
            <div className="border-t border-gray-200 py-8 text-center text-sm text-gray-500 sm:text-left">
              <span className="block sm:inline">
                &copy; {new Date().getFullYear()} {CONTACT.NAME}
              </span>{" "}
              <span className="block sm:inline">All rights reserved.</span>
            </div>
          </div>
        </footer>
      </div>
    </>
  );
};
