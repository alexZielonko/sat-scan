import { SpaceObject } from '@/types/spaceObject';
import { faker } from '@faker-js/faker';

export const generateMockSpaceObject = (): SpaceObject => {
  const satelliteId = faker.string.uuid()
  const satelliteName = `${faker.word.adverb()}-${faker.word.noun()}`
  
  return {
    file_id: faker.string.uuid(),
    launch_country: faker.location.countryCode('alpha-3'),
    launch_date: `${faker.date.future()}`.split('T')[0],
    launch_number: `${faker.number.int()}`,
    launch_piece: faker.word.noun(),
    launch_site: faker.location.city(),
    launch_year: `${faker.number.int({ min: 1957, max: 2347 })}`,
    object_id: satelliteId,
    object_name: satelliteName,
    object_number: `${faker.number.int({ min: 10000 })}`,
    object_type: faker.word.noun(),
    sat_catalog_number: faker.string.uuid(),
    sat_id: satelliteId,
    sat_name: satelliteName,
  }
}