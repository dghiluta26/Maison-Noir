/**
 * TEMPORARY mock catalogue — used only until the Django catalogue API
 * (task 2.4) is available. Task 2.5 deletes this file and switches
 * `services/catalogService.ts` to the live API.
 *
 * Source: MAISON NOIR Product Catalogue v2 — the 32 SKUs with their
 * official names, prices (lei) and stock. Descriptions are drafts based on
 * each collection's "scent / design direction".
 * Images are intentionally empty so the UI's image placeholder is exercised.
 */
import type { Category, Collection, ProductDetail } from '../types/catalog'

export const mockCategories: Category[] = [
  { id: 1, name: 'Fine Fragrances', slug: 'fine-fragrances' },
  { id: 2, name: 'Scented Candles', slug: 'scented-candles' },
  // Reed diffusers and the three Home Ritual Duos (candle + diffuser in one SKU)
  { id: 3, name: 'Home Fragrance', slug: 'home-fragrance' },
  { id: 4, name: 'Design Objects', slug: 'design-objects' },
  { id: 5, name: 'Limited Gift Sets', slug: 'limited-gift-sets' },
]

export const mockCollections: Collection[] = [
  { id: 1, name: 'After Hours', slug: 'after-hours' },
  { id: 2, name: 'Golden Hour', slug: 'golden-hour' },
  { id: 3, name: 'Midnight in Paris / Nuit Parisienne', slug: 'midnight-in-paris' },
  { id: 4, name: 'Fleur de Minuit', slug: 'fleur-de-minuit' },
  { id: 5, name: 'Cafe Creme', slug: 'cafe-creme' },
  { id: 6, name: 'Paris After Dark', slug: 'paris-after-dark' },
  { id: 7, name: 'Maison Blanche', slug: 'maison-blanche' },
  { id: 8, name: 'Soft Linen', slug: 'soft-linen' },
  { id: 9, name: 'Ambre Parisien', slug: 'ambre-parisien' },
  { id: 10, name: "L'Appartement", slug: 'l-appartement' },
  { id: 11, name: 'Chambre Noire', slug: 'chambre-noire' },
  { id: 12, name: 'Fleur de Maison', slug: 'fleur-de-maison' },
  { id: 13, name: 'Santal Residence', slug: 'santal-residence' },
]

const [FRAGRANCE, CANDLE, HOME, OBJECT, GIFT] = mockCategories
const [
  afterHours,
  goldenHour,
  midnightInParis,
  fleurDeMinuit,
  cafeCreme,
  parisAfterDark,
  maisonBlanche,
  softLinen,
  ambreParisien,
  lAppartement,
  chambreNoire,
  fleurDeMaison,
  santalResidence,
] = mockCollections

let nextId = 1

function product(
  sku: string,
  name: string,
  slug: string,
  category: Category,
  collection: Collection,
  priceLei: number,
  stock: number,
  description: string,
): ProductDetail {
  return {
    id: nextId++,
    sku,
    name,
    slug,
    price: priceLei.toFixed(2),
    category,
    collection,
    primary_image: null,
    images: [],
    in_stock: stock > 0,
    stock_quantity: stock,
    description,
  }
}

export const mockProducts: ProductDetail[] = [
  // After Hours — bergamot, iris, musk
  product('MN-AH-P', 'After Hours - Eau de Parfum', 'after-hours-eau-de-parfum', FRAGRANCE, afterHours, 590, 8,
    'An eau de parfum of bergamot, iris and musk, composed for the late hours of a Parisian evening.'),
  product('MN-AH-C', 'After Hours - Scented Candle', 'after-hours-scented-candle', CANDLE, afterHours, 290, 7,
    'The After Hours accord of bergamot, iris and musk, poured into a scented candle for quiet evenings at home.'),
  product('MN-AH-D', 'After Hours - Reed Diffuser', 'after-hours-reed-diffuser', HOME, afterHours, 390, 6,
    'A reed diffuser carrying bergamot, iris and musk gently through the room.'),
  product('MN-AH-O', 'After Hours - Nocturne Tray', 'after-hours-nocturne-tray', OBJECT, afterHours, 420, 4,
    'A smoked-stone tray designed to hold the After Hours candle and reed diffuser.'),

  // Golden Hour — neroli, amber, sandalwood
  product('MN-GH-P', 'Golden Hour - Eau de Parfum', 'golden-hour-eau-de-parfum', FRAGRANCE, goldenHour, 570, 10,
    'An eau de parfum of neroli, amber and sandalwood — warm, luminous and golden.'),
  product('MN-GH-C', 'Golden Hour - Scented Candle', 'golden-hour-scented-candle', CANDLE, goldenHour, 280, 8,
    'Neroli, amber and sandalwood in a scented candle that brings the warmth of the golden hour indoors.'),
  product('MN-GH-D', 'Golden Hour - Reed Diffuser', 'golden-hour-reed-diffuser', HOME, goldenHour, 380, 7,
    'A reed diffuser of neroli, amber and sandalwood for a softly radiant interior.'),
  product('MN-GH-O', 'Golden Hour - Soleil Vide-Poche', 'golden-hour-soleil-vide-poche', OBJECT, goldenHour, 360, 5,
    'A champagne-toned jewellery dish for rings, keys and the small treasures of the day.'),

  // Midnight in Paris / Nuit Parisienne — black tea, rose, woods
  product('MN-MP-P', 'Midnight in Paris - Eau de Parfum', 'midnight-in-paris-eau-de-parfum', FRAGRANCE, midnightInParis, 750, 4,
    'An eau de parfum of black tea, rose and woods — the personal expression of the Nuit Parisienne scent universe.'),
  product('MN-NP-C', 'Nuit Parisienne - Scented Candle', 'nuit-parisienne-scented-candle', CANDLE, midnightInParis, 340, 5,
    'Black tea, rose and woods in a scented candle that shares its scent universe with Midnight in Paris.'),

  // Fleur de Minuit — white florals, pepper, musk
  product('MN-FM-P', 'Fleur de Minuit - Eau de Parfum', 'fleur-de-minuit-eau-de-parfum', FRAGRANCE, fleurDeMinuit, 680, 6,
    'White florals, pepper and musk. A personal fragrance only, never translated into a home format.'),

  // Cafe Creme — coffee, vanilla, tonka bean
  product('MN-CC-P', 'Cafe Creme - Eau de Parfum', 'cafe-creme-eau-de-parfum', FRAGRANCE, cafeCreme, 620, 7,
    'An eau de parfum of coffee, vanilla and tonka bean, inspired by a slow Parisian morning.'),
  product('MN-CC-C', 'Cafe Creme - Scented Candle', 'cafe-creme-scented-candle', CANDLE, cafeCreme, 300, 8,
    'Coffee, vanilla and tonka bean in a scented candle for unhurried mornings at home.'),
  product('MN-CC-D', 'Cafe Creme - Reed Diffuser', 'cafe-creme-reed-diffuser', HOME, cafeCreme, 395, 6,
    'A reed diffuser of coffee, vanilla and tonka bean for kitchens, studies and living rooms.'),
  product('MN-CC-O', 'Cafe Creme - Le Plateau Cafe', 'cafe-creme-le-plateau-cafe', OBJECT, cafeCreme, 390, 5,
    'An espresso ceramic tray designed to hold the Cafe Creme candle and reed diffuser.'),
  product('MN-CC-G', 'Cafe Creme - Edition Gift Set', 'cafe-creme-edition-gift-set', GIFT, cafeCreme, 1590, 2,
    'The complete Cafe Creme collection — eau de parfum, scented candle, reed diffuser and Le Plateau Cafe tray. One of only two MAISON NOIR gift sets.'),

  // Paris After Dark — incense, dark woods, warm spice
  product('MN-PD-C', 'Paris After Dark - Scented Candle', 'paris-after-dark-scented-candle', CANDLE, parisAfterDark, 320, 6,
    'Incense, dark woods and warm spice in a scented candle for intimate evenings.'),
  product('MN-PD-D', 'Paris After Dark - Reed Diffuser', 'paris-after-dark-reed-diffuser', HOME, parisAfterDark, 410, 5,
    'A reed diffuser of incense, dark woods and warm spice — deep and enveloping.'),
  product('MN-PD-G', 'Paris After Dark - Night Edition Gift Set', 'paris-after-dark-night-edition-gift-set', GIFT, parisAfterDark, 890, 2,
    'The Paris After Dark scented candle and reed diffuser together in a numbered edition. One of only two MAISON NOIR gift sets.'),

  // Maison Blanche — Home Ritual Duo
  product('MN-MB-H', 'Maison Blanche - Home Ritual Duo', 'maison-blanche-home-ritual-duo', HOME, maisonBlanche, 610, 5,
    'A scented candle and reed diffuser of clean woods, white tea and soft musk, presented together as one home ritual.'),

  // Soft Linen — cotton blossom, pear, white musk
  product('MN-SL-P', 'Soft Linen - Eau de Parfum', 'soft-linen-eau-de-parfum', FRAGRANCE, softLinen, 550, 9,
    'An eau de parfum of cotton blossom, pear and white musk — clean, soft and airy.'),
  product('MN-SL-C', 'Soft Linen - Scented Candle', 'soft-linen-scented-candle', CANDLE, softLinen, 270, 10,
    'Cotton blossom, pear and white musk in a calm, fresh scented candle.'),
  product('MN-SL-D', 'Soft Linen - Reed Diffuser', 'soft-linen-reed-diffuser', HOME, softLinen, 360, 8,
    'A reed diffuser of cotton blossom, pear and white musk for bedrooms and dressing rooms.'),

  // Ambre Parisien — amber, labdanum, sandalwood
  product('MN-AP-P', 'Ambre Parisien - Eau de Parfum', 'ambre-parisien-eau-de-parfum', FRAGRANCE, ambreParisien, 690, 5,
    'An eau de parfum of amber, labdanum and sandalwood — warm and enveloping.'),
  product('MN-AP-C', 'Ambre Parisien - Scented Candle', 'ambre-parisien-scented-candle', CANDLE, ambreParisien, 330, 6,
    'Amber, labdanum and sandalwood in a scented candle with a golden, resinous warmth.'),
  product('MN-AP-D', 'Ambre Parisien - Reed Diffuser', 'ambre-parisien-reed-diffuser', HOME, ambreParisien, 430, 5,
    'A reed diffuser of amber, labdanum and sandalwood for living rooms and entrance halls.'),

  // L'Appartement — fig leaf, cedar, polished wood
  product('MN-LA-C', "L'Appartement - Scented Candle", 'l-appartement-scented-candle', CANDLE, lAppartement, 310, 7,
    'Fig leaf, cedar and polished wood — the scent of a Parisian apartment, as a scented candle.'),
  product('MN-LA-D', "L'Appartement - Reed Diffuser", 'l-appartement-reed-diffuser', HOME, lAppartement, 400, 6,
    'A reed diffuser of fig leaf, cedar and polished wood.'),

  // Chambre Noire — leather, incense, cedar
  product('MN-CN-C', 'Chambre Noire - Scented Candle', 'chambre-noire-scented-candle', CANDLE, chambreNoire, 325, 5,
    'Leather, incense and cedar in a dark, intimate scented candle.'),
  product('MN-CN-D', 'Chambre Noire - Reed Diffuser', 'chambre-noire-reed-diffuser', HOME, chambreNoire, 420, 5,
    'A reed diffuser of leather, incense and cedar for quiet, shaded rooms.'),

  // Fleur de Maison — Home Ritual Duo
  product('MN-FM-H', 'Fleur de Maison - Home Ritual Duo', 'fleur-de-maison-home-ritual-duo', HOME, fleurDeMaison, 590, 6,
    'A scented candle and reed diffuser of green stems, peony and fresh air, presented together as one home ritual.'),

  // Santal Residence — Home Ritual Duo
  product('MN-SR-H', 'Santal Residence - Home Ritual Duo', 'santal-residence-home-ritual-duo', HOME, santalResidence, 640, 5,
    'A scented candle and reed diffuser of sandalwood, cedar and dry amber, presented together as one home ritual.'),
]
