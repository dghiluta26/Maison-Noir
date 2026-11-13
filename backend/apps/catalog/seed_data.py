"""
Seed data for the MAISON NOIR catalogue (used by `manage.py seed_catalogue`).

Products, categories and collections are copied unchanged from the agreed
catalogue in frontend/src/mocks/catalog.ts (MAISON NOIR Product Catalogue v2):
names, SKUs, slugs, prices (lei), stock and descriptions.

Collection `description` and `launch_year` are not part of that catalogue;
they are DRAFT values and can be edited here or in the Django admin.

Final editorial texts (collection tagline/story; product description, tagline,
size, olfactory pyramid, materials, edition, ritual) replace the catalogue
descriptions as they are written, starting with Midnight in Paris and
Fleur de Minuit. Optional fields that are left out stay empty.
"""

CATEGORIES = [
    {"name": 'Fine Fragrances', "slug": 'fine-fragrances', "sort_order": 1},
    {"name": 'Scented Candles', "slug": 'scented-candles', "sort_order": 2},
    {"name": 'Home Fragrance', "slug": 'home-fragrance', "sort_order": 3},
    {"name": 'Design Objects', "slug": 'design-objects', "sort_order": 4},
    {"name": 'Limited Gift Sets', "slug": 'limited-gift-sets', "sort_order": 5},
]

# description / launch_year: DRAFT values (see module docstring)
COLLECTIONS = [
    {
        "name": 'After Hours',
        "slug": 'after-hours',
        "description": (
            'Bergamot, iris and musk, composed for the late hours of a Parisian evening.'
        ),
        "tagline": 'Quand le salon s’apaise',
        "story": (
            'At half past ten in an apartment on the boulevard Raspail, a guest folds the evening '
            'programme and leaves it beside her gloves. Someone twists a strip of bergamot peel over the '
            'last drink. Its bright scent briefly fills the room before settling into the powdery trace '
            'of iris on a silk scarf. After Hours follows that movement from freshness to intimacy. '
            'Bergamot opens the composition, iris gives it a soft, dry heart, and musk lingers as the '
            'conversation falls quiet.'
        ),
        "launch_year": 2026,
        "sort_order": 1,
    },
    {
        "name": 'Golden Hour',
        "slug": 'golden-hour',
        "description": (
            'Neroli, amber and sandalwood: warm, luminous and golden, like the last light over Paris.'
        ),
        "launch_year": 2026,
        "sort_order": 2,
    },
    {
        "name": 'Midnight in Paris / Nuit Parisienne',
        "slug": 'midnight-in-paris',
        "description": (
            'Black tea, rose and woods, expressed as the Midnight in Paris eau de parfum and the Nuit Parisienne candle.'
        ),
        "tagline": 'Minuit, rue du Bac',
        "story": (
            'Just before midnight on the rue du Bac, a bookbinder closes her ledger and sets a rose '
            'between its pages. Her cup of black tea has gone cold. She opens the tall window, and the '
            'cool air lifts the smell of cedar shavings from her worktable. Across the courtyard, a lamp '
            'goes out beneath the zinc roofs. Midnight in Paris carries the bitterness of that last cup '
            'onto the skin. Nuit Parisienne holds the rose a little longer in the room.'
        ),
        "launch_year": 2026,
        "sort_order": 3,
    },
    {
        "name": 'Fleur de Minuit',
        "slug": 'fleur-de-minuit',
        "description": (
            'White florals, pepper and musk. A personal fragrance only, never translated into a home format.'
        ),
        "launch_year": 2026,
        "sort_order": 4,
    },
    {
        "name": 'Cafe Creme',
        "slug": 'cafe-creme',
        "description": (
            'Coffee, vanilla and tonka bean, inspired by a slow Parisian morning.'
        ),
        "tagline": 'Un matin au comptoir',
        "story": (
            'The first café crème of the morning arrives at the zinc counter of a small café in '
            'Saint-Germain-des-Prés. For a moment, the milk leaves a pale curl on the surface. A spoon '
            'touches porcelain. The coffee is still dark at the edges, and that first roasted note is '
            'where Café Crème begins. Vanilla softens its bitterness, while tonka bean leaves a dry, '
            'almond-like warmth. The collection carries those sensations into warm crème glass, brushed '
            'champagne metal and the deep espresso glaze of Le Plateau Café.'
        ),
        "launch_year": 2026,
        "sort_order": 5,
    },
    {
        "name": 'Paris After Dark',
        "slug": 'paris-after-dark',
        "description": (
            'Incense, dark woods and warm spice: deep, enveloping and made for intimate evenings.'
        ),
        "tagline": 'Le salon se vide',
        "story": (
            'The last guest has gone from an apartment on the Île Saint-Louis. Someone lifts the lid '
            'of a cedar box to return a deck of cards. A little incense still hangs in the folds of the '
            'curtains, mingling with the scent of clove from an empty glass. In the drawing room, a lamp '
            'picks out a single white vein in the black marble mantel. Paris After Dark gathers these '
            'traces of an evening into a fragrance for the home.'
        ),
        "launch_year": 2026,
        "sort_order": 6,
    },
    {
        "name": 'Maison Blanche',
        "slug": 'maison-blanche',
        "description": (
            'Clean woods, white tea and soft musk, presented as a Home Ritual Duo of scented candle and reed diffuser.'
        ),
        "tagline": 'Le calme du matin',
        "story": (
            'On a Sunday morning in a courtyard apartment on the rue de Varenne, the first pot of white '
            'tea steeps by an open window. A pale oak drawer slides shut. Sunlight moves across the '
            'marble mantel, catching a fine grey vein that disappears again by noon. Maison Blanche '
            'takes its scent from this room before the day begins. White tea lends a delicate leafy '
            'note, clean woods give it depth, and soft musk lingers like the warmth of linen against skin.'
        ),
        "launch_year": 2026,
        "sort_order": 7,
    },
    {
        "name": 'Soft Linen',
        "slug": 'soft-linen',
        "description": (
            'Cotton blossom, pear and white musk: clean, soft and airy.'
        ),
        "tagline": 'Le pli du lin',
        "story": (
            'At a linen merchant’s on the rue du Mail, the first customer of the morning runs her thumb '
            'along the selvedge of a bolt of ivory cloth. The merchant unrolls a length across the '
            'counter. It settles in a single loose fold beside his breakfast pear, still cool from the '
            'market. Soft Linen opens with that first bite of pear. Cotton blossom gives the fragrance '
            'its airy heart, and white musk stays close, like the inside of a freshly pressed cuff.'
        ),
        "launch_year": 2026,
        "sort_order": 8,
    },
    {
        "name": 'Ambre Parisien',
        "slug": 'ambre-parisien',
        "description": (
            'Amber, labdanum and sandalwood, with a golden, resinous warmth.'
        ),
        "tagline": 'Le bois des loges',
        "story": (
            'In a dressing room at the Palais Garnier, a violinist sets her cufflinks on the wooden '
            'ledge beneath the mirror. The orchestra is tuning on the other side of the wall. She lifts '
            'a fluted bottle to the light, and a narrow stripe of burnt orange falls across the evening '
            'programme. Ambre Parisien begins with the warmth of amber. Labdanum lends a darker, almost '
            'leathery note, and sandalwood stays at the wrist long after the music has ended.'
        ),
        "launch_year": 2026,
        "sort_order": 9,
    },
    {
        "name": "L'Appartement",
        "slug": 'l-appartement',
        "description": (
            'Fig leaf, cedar and polished wood: the scent of a Parisian apartment.'
        ),
        "tagline": 'Les fenêtres ouvertes',
        "story": (
            'On the rue de Tournon, the windows of a first-floor apartment stand open to the courtyard. '
            'A fig branch brushes the sill. Inside, someone sharpens a cedar pencil at a writing desk, '
            'then sweeps the shavings into one hand. The tabletop smells faintly of polish where the '
            'morning sun has warmed it. L’Appartement brings those three scents together. Its candle and '
            'diffuser are carved in honed travertine, with shallow flutes that catch the light like the '
            'mouldings beside the window.'
        ),
        "launch_year": 2026,
        "sort_order": 10,
    },
    {
        "name": 'Chambre Noire',
        "slug": 'chambre-noire',
        "description": (
            'Leather, incense and cedar: dark, intimate and quiet.'
        ),
        "tagline": 'Derrière le rideau rouge',
        "story": (
            'Behind a velvet curtain in a portrait studio on the rue des Archives, a photographer opens '
            'the leather case that belonged to her father. The clasp gives a small click. Inside, the '
            'camera rests beside a cedar pencil worn flat on one side. A thread of incense drifts in from '
            'the next room as she lifts the camera to her eye. Chambre Noire draws its fragrance from '
            'that instant: the dry scent of cedar, a little smoke and the warmth leather takes from a hand.'
        ),
        "launch_year": 2026,
        "sort_order": 11,
    },
    {
        "name": 'Fleur de Maison',
        "slug": 'fleur-de-maison',
        "description": (
            'Green stems, peony and fresh air, presented as a Home Ritual Duo of scented candle and reed diffuser.'
        ),
        "tagline": 'Les pivoines du dimanche',
        "story": (
            'On a Sunday in May, the peonies come home from the marché d’Aligre wrapped in brown paper. '
            'At the kitchen sink, a pair of scissors cuts through the stems, releasing a sharp green scent '
            'before the flowers have even reached the vase. By afternoon, the petals have loosened in the '
            'air from the courtyard window. Fleur de Maison holds both moments together, with the '
            'freshness of cut stems beneath the softer scent of an open peony.'
        ),
        "launch_year": 2026,
        "sort_order": 12,
    },
    {
        "name": 'Santal Residence',
        "slug": 'santal-residence',
        "description": (
            'Sandalwood, cedar and dry amber, presented as a Home Ritual Duo of scented candle and reed diffuser.'
        ),
        "tagline": 'Dans l’atelier d’ébénisterie',
        "story": (
            'In a cabinetmaker’s atelier on the rue du Faubourg Saint-Antoine, a curl of cedar falls from '
            'a hand plane onto the bench. The cabinetmaker pauses to test the fit of a walnut drawer. It '
            'slides home with a soft click. Santal Residence takes its opening from the scent of those '
            'fresh shavings. Sandalwood follows, smooth and close, with dry amber beneath. A narrow ring '
            'of walnut circles the diffuser, its grain still visible under the brushed metal collar.'
        ),
        "launch_year": 2026,
        "sort_order": 13,
    },
]

PRODUCTS = [
    {
        "sku": 'MN-AH-P',
        "name": 'After Hours - Eau de Parfum',
        "slug": 'after-hours-eau-de-parfum',
        "category": 'fine-fragrances',
        "collection": 'after-hours',
        "price": "590.00",
        "stock_quantity": 8,
        "description": (
            'Bright bergamot settles into powdery iris, with soft musk lingering close to the skin. The '
            'bevelled smoked-espresso flacon rests on a heavy glass base beneath an arch-engraved '
            'champagne cap. Burgundy silk suspends a wax seal above the hand-numbered cotton-paper label, '
            'catching a faint wine-coloured reflection in the glass.'
        ),
        "tagline": 'Bergamot fading into iris and musk.',
        "size": '100 ml',
        "notes_top": 'Bergamot',
        "notes_heart": 'Iris',
        "notes_base": 'Musk',
        "materials": (
            'Smoked glass, brushed champagne-gold cap, burgundy silk, wax seal and ivory cotton-rag paper.'
        ),
        "ritual": 'Mist the inside of each wrist and let the iris emerge as the bergamot softens.',
    },
    {
        "sku": 'MN-AH-C',
        "name": 'After Hours - Scented Candle',
        "slug": 'after-hours-scented-candle',
        "category": 'scented-candles',
        "collection": 'after-hours',
        "price": "290.00",
        "stock_quantity": 7,
        "description": (
            'Bergamot lifts from the warming wax before iris and musk settle through the room. The '
            'straight-sided smoked-glass vessel has a substantial base and a brushed champagne lid '
            'engraved with the house arch. Two turns of burgundy silk carry a wax seal above its '
            'hand-numbered ivory label.'
        ),
        "tagline": 'The last light in the salon.',
        "size": '220 g',
        "burn_time": 'Approximately 50 hours',
        "notes_top": 'Bergamot',
        "notes_heart": 'Iris',
        "notes_base": 'Musk',
        "materials": (
            'Scented wax, cotton wick, smoked glass, champagne-gold lid, burgundy silk and cotton-rag paper.'
        ),
        "ritual": (
            'Lift the lid, unwind the silk and set the seal aside before lighting the wick at dusk.'
        ),
    },
    {
        "sku": 'MN-AH-D',
        "name": 'After Hours - Reed Diffuser',
        "slug": 'after-hours-reed-diffuser',
        "category": 'home-fragrance',
        "collection": 'after-hours',
        "price": "390.00",
        "stock_quantity": 6,
        "description": (
            'Six dark rattan reeds carry bergamot and iris over a quiet base of musk. Their slender '
            'silhouettes remain visible through the rounded smoked-espresso bottle. Burgundy silk holds a '
            'small wax seal beneath the arch-engraved champagne collar, falling over the upper edge of the '
            'hand-numbered cotton-paper label.'
        ),
        "tagline": 'Iris at the drawing-room door.',
        "size": '200 ml',
        "burn_time": 'Approximately three months',
        "notes_top": 'Bergamot',
        "notes_heart": 'Iris',
        "notes_base": 'Musk',
        "materials": (
            'Smoked glass, brushed champagne-gold collar, rattan reeds, burgundy silk and ivory '
            'cotton-rag paper.'
        ),
        "ritual": (
            'Fan the reeds on a hallway console and turn them occasionally to refresh the fragrance.'
        ),
    },
    {
        "sku": 'MN-AH-O',
        "name": 'After Hours - Nocturne Tray',
        "slug": 'after-hours-nocturne-tray',
        "category": 'design-objects',
        "collection": 'after-hours',
        "price": "420.00",
        "stock_quantity": 4,
        "description": (
            'Carved from honed dark smoked stone, Nocturne gathers the After Hours candle and diffuser '
            'within a low rectangular rim. Subtle mineral markings cross its matte surface, while a '
            'discreet champagne Maison Noir signature follows the front edge. Its substantial base gives '
            'the arrangement a grounded presence on a console or bedside table.'
        ),
        "tagline": 'A stone setting for evening rituals.',
        "materials": 'Honed dark smoked stone with champagne lettering.',
        "ritual": (
            'Arrange the candle and diffuser together, leaving a little space around each glass vessel.'
        ),
    },
    {
        "sku": 'MN-GH-P',
        "name": 'Golden Hour - Eau de Parfum',
        "slug": 'golden-hour-eau-de-parfum',
        "category": 'fine-fragrances',
        "collection": 'golden-hour',
        "price": "570.00",
        "stock_quantity": 10,
        "description": (
            'An eau de parfum of neroli, amber and sandalwood — warm, luminous and golden.'
        ),
    },
    {
        "sku": 'MN-GH-C',
        "name": 'Golden Hour - Scented Candle',
        "slug": 'golden-hour-scented-candle',
        "category": 'scented-candles',
        "collection": 'golden-hour',
        "price": "280.00",
        "stock_quantity": 8,
        "description": (
            'Neroli, amber and sandalwood in a scented candle that brings the warmth of the golden hour indoors.'
        ),
    },
    {
        "sku": 'MN-GH-D',
        "name": 'Golden Hour - Reed Diffuser',
        "slug": 'golden-hour-reed-diffuser',
        "category": 'home-fragrance',
        "collection": 'golden-hour',
        "price": "380.00",
        "stock_quantity": 7,
        "description": (
            'A reed diffuser of neroli, amber and sandalwood for a softly radiant interior.'
        ),
    },
    {
        "sku": 'MN-GH-O',
        "name": 'Golden Hour - Soleil Vide-Poche',
        "slug": 'golden-hour-soleil-vide-poche',
        "category": 'design-objects',
        "collection": 'golden-hour',
        "price": "360.00",
        "stock_quantity": 5,
        "description": (
            'A champagne-toned jewellery dish for rings, keys and the small treasures of the day.'
        ),
    },
    {
        "sku": 'MN-MP-P',
        "name": 'Midnight in Paris - Eau de Parfum',
        "slug": 'midnight-in-paris-eau-de-parfum',
        "category": 'fine-fragrances',
        "collection": 'midnight-in-paris',
        "price": "750.00",
        "stock_quantity": 4,
        "description": (
            'Black tea opens with a tannic edge. Rose softens it, and dry cedar lingers at the wrist. '
            'The bevelled flacon fades from near-black lacquer to smoky glass beneath a fine gold '
            'roofline. The arch engraved on the cap appears again on the burgundy wax seal, tied with '
            'black silk above the hand-numbered ivory label.'
        ),
        "tagline": 'The last cup of black tea.',
        "size": '100 ml',
        "notes_top": 'Black tea leaf',
        "notes_heart": 'Rose petals',
        "notes_base": 'Dry cedarwood',
        "materials": (
            'Lacquered glass with a heavy solid base, brushed champagne-gold cap, black silk cord '
            'and deckle-edged cotton-rag paper.'
        ),
        "edition": 'Édition Limitée · N° 047 / 500',
        "ritual": 'Mist the inside of each wrist and give the rose a moment to emerge through the tea.',
    },
    {
        "sku": 'MN-NP-C',
        "name": 'Nuit Parisienne - Scented Candle',
        "slug": 'nuit-parisienne-scented-candle',
        "category": 'scented-candles',
        "collection": 'midnight-in-paris',
        "price": "340.00",
        "stock_quantity": 5,
        "description": (
            'As the wax warms, the dry scent of black tea gives way to rose and cedar. Gold lacquer '
            'catches the flame inside the black glass tumbler. Two turns of black silk hold a burgundy '
            'wax seal above the hand-numbered label. Lift the lid by its brass knob to feel the fine '
            'arch engraved there.'
        ),
        "tagline": 'A rose left by the window.',
        "size": '220 g',
        "burn_time": 'Approximately 50 hours',
        "notes_top": 'Black tea leaf',
        "notes_heart": 'Rose petals',
        "notes_base": 'Dry cedarwood',
        "materials": (
            'Scented wax, straight-sided lacquered glass with a smoky base and champagne-gold rooftop '
            'motif, gold interior, black glass lid, brass knob, black silk cord and ivory cotton-rag paper.'
        ),
        "edition": 'Édition Limitée · N° 047 / 500',
        "ritual": 'Unwind the silk, set the seal aside and light the wick as you settle in to read.',
    },
    {
        "sku": 'MN-FM-P',
        "name": 'Fleur de Minuit - Eau de Parfum',
        "slug": 'fleur-de-minuit-eau-de-parfum',
        "category": 'fine-fragrances',
        "collection": 'fleur-de-minuit',
        "price": "680.00",
        "stock_quantity": 6,
        "description": (
            'Pepper gives the jasmine a cool edge before musk warms on the skin. Light travels through '
            'the bevelled shoulders of the burgundy flacon and pools in its clear glass base. The house '
            'arch is engraved on the brushed champagne cap and pressed into the wax seal. Burgundy silk '
            'holds the seal just above the hand-numbered cotton-paper label.'
        ),
        "tagline": 'White petals against burgundy silk.',
        "size": '100 ml',
        "notes_top": 'Black pepper',
        "notes_heart": 'Jasmine and white florals',
        "notes_base": 'Soft musk',
        "ritual": (
            'Mist the inside of the wrist before dressing, letting the fragrance dry before lowering a sleeve.'
        ),
    },
    {
        "sku": 'MN-CC-P',
        "name": 'Cafe Creme - Eau de Parfum',
        "slug": 'cafe-creme-eau-de-parfum',
        "category": 'fine-fragrances',
        "collection": 'cafe-creme',
        "price": "620.00",
        "stock_quantity": 7,
        "description": (
            'Roasted coffee opens with a gentle bitterness, softened by vanilla and the almond-like warmth '
            'of tonka bean. The crème glass flacon rests on a substantial clear base beneath an '
            'arch-engraved champagne cap. Espresso silk suspends a burgundy wax seal above the '
            'hand-numbered ivory label.'
        ),
        "tagline": 'The warmth of the first cup.',
        "size": '100 ml',
        "notes_top": 'Roasted coffee',
        "notes_heart": 'Vanilla',
        "notes_base": 'Tonka bean',
        "materials": (
            'Crème glass, brushed champagne-gold cap, espresso silk, burgundy wax and cotton-rag paper.'
        ),
        "ritual": (
            'Mist the inside of each wrist and allow the coffee to soften into vanilla as the fragrance warms.'
        ),
    },
    {
        "sku": 'MN-CC-C',
        "name": 'Cafe Creme - Scented Candle',
        "slug": 'cafe-creme-scented-candle',
        "category": 'scented-candles',
        "collection": 'cafe-creme',
        "price": "300.00",
        "stock_quantity": 8,
        "description": (
            'Coffee rises gently from the warming wax, followed by vanilla and a lingering trace of tonka '
            'bean. The straight-sided crème glass tumbler has a heavy clear base and an arch-engraved '
            'champagne lid. Two turns of espresso silk carry a burgundy wax seal above its hand-numbered '
            'cotton-paper label.'
        ),
        "tagline": 'A slow morning, held in wax.',
        "size": '220 g',
        "burn_time": 'Approximately 50 hours',
        "notes_top": 'Roasted coffee',
        "notes_heart": 'Vanilla',
        "notes_base": 'Tonka bean',
        "materials": (
            'Scented wax, cotton wick, crème glass, brushed champagne-gold lid, espresso silk and '
            'cotton-rag paper.'
        ),
        "ritual": (
            'Lift the lid, unwind the silk and set the seal aside before lighting the wick during a quiet '
            'morning at home.'
        ),
    },
    {
        "sku": 'MN-CC-D',
        "name": 'Cafe Creme - Reed Diffuser',
        "slug": 'cafe-creme-reed-diffuser',
        "category": 'home-fragrance',
        "collection": 'cafe-creme',
        "price": "395.00",
        "stock_quantity": 6,
        "description": (
            'Roasted coffee greets you first, with soft vanilla and tonka bean bringing warmth to the room. '
            'Six dark rattan reeds rise from a rounded crème glass bottle. An arch-engraved champagne '
            'collar crowns the vessel, while espresso silk holds a burgundy wax seal just above the '
            'hand-numbered label.'
        ),
        "tagline": 'Coffee drifting through an open doorway.',
        "size": '200 ml',
        "burn_time": 'Approximately three months',
        "notes_top": 'Roasted coffee',
        "notes_heart": 'Vanilla',
        "notes_base": 'Tonka bean',
        "materials": (
            'Crème glass, brushed champagne-gold collar, rattan reeds, espresso silk, burgundy wax and '
            'cotton-rag paper.'
        ),
        "ritual": 'Fan the reeds on an entrance console and turn them occasionally to refresh the fragrance.',
    },
    {
        "sku": 'MN-CC-O',
        "name": 'Cafe Creme - Le Plateau Cafe',
        "slug": 'cafe-creme-le-plateau-cafe',
        "category": 'design-objects',
        "collection": 'cafe-creme',
        "price": "390.00",
        "stock_quantity": 5,
        "description": (
            'A deep espresso glaze pools across the gently irregular surface of this oval ceramic tray. Its '
            'raised rim gathers the Café Crème candle and diffuser into one arrangement, with room for the '
            'small objects of everyday life. A discreet champagne-gold Maison Noir signature follows the '
            'curve of the front edge.'
        ),
        "tagline": 'A place for the morning ritual.',
        "materials": 'Glazed espresso ceramic with champagne-gold lettering.',
        "ritual": (
            'Arrange the candle and diffuser together, letting the dark glaze frame their warm crème glass.'
        ),
    },
    {
        "sku": 'MN-CC-G',
        "name": 'Cafe Creme - Edition Gift Set',
        "slug": 'cafe-creme-edition-gift-set',
        "category": 'limited-gift-sets',
        "collection": 'cafe-creme',
        "price": "1590.00",
        "stock_quantity": 2,
        "description": (
            'An espresso linen case opens to reveal the eau de parfum, candle and capped reed diffuser '
            'alongside Le Plateau Café. Coffee, vanilla and tonka bean connect the three fragrances. '
            'Arch-engraved metalwork, burgundy wax seals and hand-numbered labels finish the crème glass '
            'vessels, with the reeds bundled separately in the fitted ivory insert.'
        ),
        "tagline": 'The complete Café Crème ritual.',
        "includes": (
            '100 ml eau de parfum · 220 g candle with lid · 200 ml reed diffuser with separate reeds · '
            'Le Plateau Café'
        ),
        "notes_top": 'Roasted coffee',
        "notes_heart": 'Vanilla',
        "notes_base": 'Tonka bean',
        "materials": (
            'Crème glass, champagne metalwork, glazed espresso ceramic, silk and an espresso '
            'linen-covered presentation case.'
        ),
        "ritual": (
            'Arrange the home fragrances on the ceramic tray, then finish the morning with a light mist '
            'of the eau de parfum.'
        ),
    },
    {
        "sku": 'MN-PD-C',
        "name": 'Paris After Dark - Scented Candle',
        "slug": 'paris-after-dark-scented-candle',
        "category": 'scented-candles',
        "collection": 'paris-after-dark',
        "price": "320.00",
        "stock_quantity": 6,
        "description": (
            'Three wooden wicks crackle above a low bowl carved from Nero Marquina marble. Clove warms '
            'the incense, and dark woods linger as the room grows quiet. Two turns of black silk hold a '
            'burgundy wax seal above the hand-numbered label. The seal’s fine arch appears again on the '
            'brass knob of the matching stone lid.'
        ),
        "tagline": 'Three flames above black marble.',
        "size": '400 g',
        "burn_time": 'Approximately 80 hours',
        "notes_top": 'Clove',
        "notes_heart": 'Incense',
        "notes_base": 'Dark cedarwood',
        "ritual": (
            'Lift the marble lid, slip off the silk cord and seal, and light all three wicks as evening settles.'
        ),
    },
    {
        "sku": 'MN-PD-D',
        "name": 'Paris After Dark - Reed Diffuser',
        "slug": 'paris-after-dark-reed-diffuser',
        "category": 'home-fragrance',
        "collection": 'paris-after-dark',
        "price": "410.00",
        "stock_quantity": 5,
        "description": (
            'Six dark reeds rise from a rounded vessel of polished Nero Marquina. A brushed '
            'champagne-gold collar carries the engraved house arch. Black silk suspends a burgundy wax '
            'seal above the hand-numbered ivory label. In a hallway, the first impression is warm spice, '
            'followed by incense and the dry grain of cedar.'
        ),
        "tagline": 'Incense at the threshold.',
        "size": '200 ml',
        "burn_time": 'Approximately 3 months',
        "notes_top": 'Clove',
        "notes_heart": 'Incense',
        "notes_base": 'Dark cedarwood',
        "ritual": (
            'Fan the six rattan reeds through the collar and turn them occasionally to refresh the fragrance.'
        ),
    },
    {
        "sku": 'MN-PD-G',
        "name": 'Paris After Dark - Night Edition Gift Set',
        "slug": 'paris-after-dark-night-edition-gift-set',
        "category": 'limited-gift-sets',
        "collection": 'paris-after-dark',
        "price": "890.00",
        "stock_quantity": 2,
        "description": (
            'Burgundy linen opens to reveal two black marble vessels nestled in espresso velvet. The '
            'hand-numbered candle and diffuser share an accord of clove, incense and dark cedar. The '
            'arch engraved in their metalwork appears in champagne foil inside the lid. Beneath the '
            'pair, a burgundy wax seal fastens black silk beside the numbered edition card.'
        ),
        "tagline": 'One fragrance, two evening rituals.',
        "size": '400 g candle and 200 ml diffuser',
        "notes_top": 'Clove',
        "notes_heart": 'Incense',
        "notes_base": 'Dark cedarwood',
        "edition": 'Edition card · N° 012 / 300',
        "ritual": (
            'Set the diffuser in the entrance and light the candle in the salon, carrying the same '
            'fragrance from one room to the next.'
        ),
    },
    {
        "sku": 'MN-MB-H',
        "name": 'Maison Blanche - Home Ritual Duo',
        "slug": 'maison-blanche-home-ritual-duo',
        "category": 'home-fragrance',
        "collection": 'maison-blanche',
        "price": "610.00",
        "stock_quantity": 5,
        "description": (
            'White tea opens into clean woods and soft musk. Carved from white Calacatta marble, the '
            'wooden-wick candle and rounded reed diffuser share a matching stone tray. The house arch is '
            'engraved on the brass lid knob and diffuser collar. Ivory silk holds a burgundy wax seal '
            'above each hand-numbered cotton-paper label.'
        ),
        "tagline": 'White tea on a marble mantel.',
        "size": '400 g candle · 200 ml diffuser',
        "burn_time": 'Approximately 80 hours of candlelight and three months of diffusion',
        "includes": (
            '400 g candle with matching marble lid · 200 ml diffuser with rattan reeds · '
            'Calacatta marble tray'
        ),
        "notes_top": 'White tea',
        "notes_heart": 'Clean woods',
        "notes_base": 'Soft musk',
        "ritual": (
            'Let the diffuser greet you in the hallway, then carry the candle to your reading table, '
            'untie its silk cord and light the wooden wick.'
        ),
    },
    {
        "sku": 'MN-SL-P',
        "name": 'Soft Linen - Eau de Parfum',
        "slug": 'soft-linen-eau-de-parfum',
        "category": 'fine-fragrances',
        "collection": 'soft-linen',
        "price": "550.00",
        "stock_quantity": 9,
        "description": (
            'Cool pear gives way to cotton blossom and a trace of white musk at the wrist. Fine white '
            'veins cross the flacon’s grey stone-effect finish, ending where the heavy glass base turns '
            'clear. Beneath the arch-engraved champagne cap, an ivory linen knot holds a burgundy wax '
            'seal above the hand-numbered label.'
        ),
        "tagline": 'Pear beneath a linen cuff.',
        "size": '100 ml',
        "notes_top": 'Pear',
        "notes_heart": 'Cotton blossom',
        "notes_base": 'White musk',
        "ritual": 'Mist the inside of each wrist and let the fragrance dry before slipping on a shirt.',
    },
    {
        "sku": 'MN-SL-C',
        "name": 'Soft Linen - Scented Candle',
        "slug": 'soft-linen-scented-candle',
        "category": 'scented-candles',
        "collection": 'soft-linen',
        "price": "270.00",
        "stock_quantity": 10,
        "description": (
            'A wooden wick crackles as pear and cotton blossom rise from the warm wax. White musk '
            'lingers in the room. The rounded vessel and its lid are carved from pale grey stone, '
            'threaded with white. Ivory linen circles the hand-numbered vessel twice, and its burgundy '
            'seal echoes the arch engraved on the lid’s brass knob.'
        ),
        "tagline": 'Cotton blossom by candlelight.',
        "size": '400 g',
        "burn_time": 'Approximately 80 hours',
        "notes_top": 'Pear',
        "notes_heart": 'Cotton blossom',
        "notes_base": 'White musk',
        "ritual": (
            'Lift the stone lid, unwind the linen cord and set the seal aside before lighting the wooden wick.'
        ),
    },
    {
        "sku": 'MN-SL-D',
        "name": 'Soft Linen - Reed Diffuser',
        "slug": 'soft-linen-reed-diffuser',
        "category": 'home-fragrance',
        "collection": 'soft-linen',
        "price": "360.00",
        "stock_quantity": 8,
        "description": (
            'Six dark rattan reeds carry pear and cotton blossom through the room over a soft base of '
            'white musk. Their slender lines pick up the pale veining in the rounded stone bottle. An '
            'ivory linen cord carries a burgundy wax seal between the arch-engraved champagne collar and '
            'the hand-numbered cotton-paper label.'
        ),
        "tagline": 'A fresh note at the door.',
        "size": '200 ml',
        "burn_time": 'Approximately three months',
        "notes_top": 'Pear',
        "notes_heart": 'Cotton blossom',
        "notes_base": 'White musk',
        "ritual": (
            'Set the bottle on a hallway console and fan the reeds so the pear greets you at the door.'
        ),
    },
    {
        "sku": 'MN-AP-P',
        "name": 'Ambre Parisien - Eau de Parfum',
        "slug": 'ambre-parisien-eau-de-parfum',
        "category": 'fine-fragrances',
        "collection": 'ambre-parisien',
        "price": "690.00",
        "stock_quantity": 5,
        "description": (
            'Amber opens on the skin, deepening through resinous labdanum to a smooth sandalwood finish. '
            'Fine flutes run down the cognac glass to a heavy, clear base. Beneath the square '
            'champagne-gold cap, burgundy silk holds a wax seal above the hand-numbered ivory label. The '
            'house arch is engraved on the cap’s brushed top face.'
        ),
        "tagline": 'Amber against a silk cuff.',
        "size": '100 ml',
        "notes_top": 'Amber accord',
        "notes_heart": 'Labdanum',
        "notes_base": 'Sandalwood',
        "ritual": 'Mist the inside of the wrist and let the sandalwood emerge as the fragrance warms.',
    },
    {
        "sku": 'MN-AP-C',
        "name": 'Ambre Parisien - Scented Candle',
        "slug": 'ambre-parisien-scented-candle',
        "category": 'scented-candles',
        "collection": 'ambre-parisien',
        "price": "330.00",
        "stock_quantity": 6,
        "description": (
            'A single flame sends narrow bars of amber light through the fluted cognac tumbler. '
            'Labdanum gives the melting wax a resinous depth, softened by sandalwood. Burgundy silk '
            'circles the glass twice above the hand-numbered label. Pressed into the wax seal, the house '
            'arch appears again on the brushed champagne-gold lid.'
        ),
        "tagline": 'Amber lit from within.',
        "size": '220 g',
        "burn_time": 'Approximately 50 hours',
        "notes_top": 'Amber accord',
        "notes_heart": 'Labdanum',
        "notes_base": 'Sandalwood',
        "ritual": (
            'Lift the lid, unwind the silk cord and set the seal aside before lighting the wick at dusk.'
        ),
    },
    {
        "sku": 'MN-AP-D',
        "name": 'Ambre Parisien - Reed Diffuser',
        "slug": 'ambre-parisien-reed-diffuser',
        "category": 'home-fragrance',
        "collection": 'ambre-parisien',
        "price": "430.00",
        "stock_quantity": 5,
        "description": (
            'Six espresso rattan reeds rise from a rounded bottle of fluted cognac glass. Amber greets '
            'you at the door, with labdanum and sandalwood giving the room a quiet, woody warmth. A '
            'burgundy wax seal hangs from silk knotted beneath the arch-engraved champagne collar, just '
            'above the hand-numbered cotton-paper label.'
        ),
        "tagline": 'The scent of the drawing room.',
        "size": '200 ml',
        "burn_time": 'Approximately three months',
        "notes_top": 'Amber accord',
        "notes_heart": 'Labdanum',
        "notes_base": 'Sandalwood',
        "ritual": (
            'Set the diffuser on a console and fan the reeds, leaving room between them for the '
            'fragrance to travel.'
        ),
    },
    {
        "sku": 'MN-LA-C',
        "name": "L'Appartement - Scented Candle",
        "slug": 'l-appartement-scented-candle',
        "category": 'scented-candles',
        "collection": 'l-appartement',
        "price": "310.00",
        "stock_quantity": 7,
        "description": (
            'A wooden wick crackles softly as green fig leaf gives way to cedar and the warmth of '
            'polished wood. The low travertine vessel has a fluted lid with the house arch engraved on '
            'its brass knob. Two turns of espresso silk hold a burgundy wax seal above the hand-numbered '
            'cotton-paper label.'
        ),
        "tagline": 'Fig leaf by an open window.',
        "size": '400 g',
        "burn_time": 'Approximately 80 hours',
        "notes_top": 'Fig leaf',
        "notes_heart": 'Cedar',
        "notes_base": 'Polished wood',
        "ritual": (
            'Lift the stone lid, unwind the silk cord and set the seal aside before lighting the wooden wick.'
        ),
    },
    {
        "sku": 'MN-LA-D',
        "name": "L'Appartement - Reed Diffuser",
        "slug": 'l-appartement-reed-diffuser',
        "category": 'home-fragrance',
        "collection": 'l-appartement',
        "price": "400.00",
        "stock_quantity": 6,
        "description": (
            'Six dark rattan reeds carry the green scent of fig leaf through the room, with dry cedar and '
            'polished wood beneath. Fine pores remain visible along the flutes of the rounded travertine '
            'bottle. An espresso silk knot suspends a burgundy wax seal between the arch-engraved '
            'champagne collar and the hand-numbered ivory label.'
        ),
        "tagline": 'Green fig for the entrance hall.',
        "size": '200 ml',
        "burn_time": 'Approximately three months',
        "notes_top": 'Fig leaf',
        "notes_heart": 'Cedar',
        "notes_base": 'Polished wood',
        "ritual": (
            'Set the vessel on the entrance console and fan the reeds so the scent of fig leaf greets '
            'you at the door.'
        ),
    },
    {
        "sku": 'MN-CN-C',
        "name": 'Chambre Noire - Scented Candle',
        "slug": 'chambre-noire-scented-candle',
        "category": 'scented-candles',
        "collection": 'chambre-noire',
        "price": "325.00",
        "stock_quantity": 5,
        "description": (
            'The wooden wick crackles as dry cedar and incense give way to soft leather. Fine white veins '
            'cross the low Rosso Levanto marble bowl and its matching lid. Two turns of burgundy silk hold '
            'a wax seal above the hand-numbered label. The arch pressed into the seal is engraved on the '
            'lid’s brass knob.'
        ),
        "tagline": 'Leather warmed by candlelight.',
        "size": '400 g',
        "burn_time": 'Approximately 80 hours',
        "notes_top": 'Dry cedar',
        "notes_heart": 'Incense',
        "notes_base": 'Soft leather',
        "ritual": (
            'Lift the stone lid, unwind the silk cord and set the seal aside before lighting the wooden wick.'
        ),
    },
    {
        "sku": 'MN-CN-D',
        "name": 'Chambre Noire - Reed Diffuser',
        "slug": 'chambre-noire-reed-diffuser',
        "category": 'home-fragrance',
        "collection": 'chambre-noire',
        "price": "420.00",
        "stock_quantity": 5,
        "description": (
            'Six dark rattan reeds lift the scent of cedar from a rounded Rosso Levanto marble bottle. '
            'Incense lends a faint smoky edge, with supple leather underneath. A burgundy silk knot '
            'suspends the wax seal beneath the arch-engraved champagne collar. The deckled edge of the '
            'hand-numbered ivory label follows the curve of the stone.'
        ),
        "tagline": 'Cedar at the study door.',
        "size": '200 ml',
        "burn_time": 'Approximately three months',
        "notes_top": 'Dry cedar',
        "notes_heart": 'Incense',
        "notes_base": 'Soft leather',
        "ritual": 'Set the bottle on a shelf near the study door and fan the six reeds above the marble.',
    },
    {
        "sku": 'MN-FM-H',
        "name": 'Fleur de Maison - Home Ritual Duo',
        "slug": 'fleur-de-maison-home-ritual-duo',
        "category": 'home-fragrance',
        "collection": 'fleur-de-maison',
        "price": "590.00",
        "stock_quantity": 6,
        "description": (
            'Green stems give peony a crisp edge, softened by a fresh-air accord. The wooden-wick candle '
            'and six-reed diffuser share a blush-taupe Rosa Portogallo marble tray. Champagne silk holds a '
            'burgundy wax seal above each hand-numbered label. The house arch is engraved on the brass '
            'knob of the candle’s matching marble lid.'
        ),
        "tagline": 'Peonies by an open window.',
        "size": '400 g candle · 200 ml diffuser',
        "burn_time": 'Approximately 80 hours of candlelight and three months of diffusion',
        "includes": (
            '400 g candle with marble lid · 200 ml diffuser with six rattan reeds · Matching marble tray'
        ),
        "notes_top": 'Fresh green stems',
        "notes_heart": 'Peony',
        "notes_base": 'Fresh-air accord',
        "ritual": (
            'Fan the reeds in the entrance hall, then slip the silk and seal from the candle and light its '
            'wooden wick at the dining table.'
        ),
    },
    {
        "sku": 'MN-SR-H',
        "name": 'Santal Residence - Home Ritual Duo',
        "slug": 'santal-residence-home-ritual-duo',
        "category": 'home-fragrance',
        "collection": 'santal-residence',
        "price": "640.00",
        "stock_quantity": 5,
        "description": (
            'Cedar opens into sandalwood and dry amber. The wooden-wick candle and six-reed diffuser share '
            'a tray of dark Emperador marble. A walnut ring sits beneath the diffuser’s champagne-gold '
            'collar. The house arch, engraved on the collar and brass lid knob, appears again on burgundy '
            'wax seals tied with espresso silk above the hand-numbered labels.'
        ),
        "tagline": 'Fresh cedar, worn walnut, warm sandalwood.',
        "size": '400 g candle · 200 ml diffuser',
        "burn_time": 'Approximately 80 hours of candlelight and three months of diffusion',
        "includes": (
            '400 g candle with matching marble lid · 200 ml diffuser with six rattan reeds · '
            'Emperador marble tray'
        ),
        "notes_top": 'Cedar',
        "notes_heart": 'Sandalwood',
        "notes_base": 'Dry amber',
        "ritual": (
            'Fan the reeds in the study, then slip the silk and seal from the candle and light its wooden '
            'wick beside your reading chair.'
        ),
    },
]

# --- Images ------------------------------------------------------------------
# Files live in apps/catalog/seed_images/ (committed, unlike media/). The seed
# command copies each one to MEDIA_ROOT under the same relative path.
# Product and collection images were generated with ChatGPT (see README, "AI Tools Used").

# collection slug -> picture shown in the collection page hero
COLLECTION_IMAGES = {
    'after-hours': 'collections/after-hours.jpg',
    'midnight-in-paris': 'collections/midnight-in-paris.jpg',
    'paris-after-dark': 'collections/paris-after-dark.jpg',
    'soft-linen': 'collections/soft-linen.jpg',
    'ambre-parisien': 'collections/ambre-parisien.jpg',
    'l-appartement': 'collections/l-appartement.jpg',
    'chambre-noire': 'collections/chambre-noire.jpg',
    'cafe-creme': 'collections/cafe-creme.jpg',
}

# product SKU -> images, the first one is the primary image
PRODUCT_IMAGES = {
    'MN-AH-P': [
        {
            "file": 'products/after-hours-eau-de-parfum.jpg',
            "alt_text": (
                'After Hours eau de parfum: bevelled smoked-espresso glass flacon with a champagne-gold '
                'cap and a burgundy wax seal'
            ),
        },
    ],
    'MN-AH-C': [
        {
            "file": 'products/after-hours-scented-candle.jpg',
            "alt_text": (
                'After Hours scented candle: straight-sided smoked glass vessel tied with burgundy silk, '
                'its champagne lid leaning beside it'
            ),
        },
    ],
    'MN-AH-D': [
        {
            "file": 'products/after-hours-reed-diffuser.jpg',
            "alt_text": (
                'After Hours reed diffuser: rounded smoked-espresso glass bottle with six dark reeds '
                'and a champagne-gold collar'
            ),
        },
    ],
    'MN-AH-O': [
        {
            "file": 'products/after-hours-nocturne-tray.jpg',
            "alt_text": (
                'Nocturne Tray: low rectangular tray in honed dark smoked stone with a champagne '
                'Maison Noir signature on its front edge'
            ),
        },
    ],
    'MN-MP-P': [
        {
            "file": 'products/midnight-in-paris-eau-de-parfum.jpg',
            "alt_text": 'Midnight in Paris eau de parfum: black lacquered flacon with a gold cap and a burgundy wax seal',
        },
    ],
    'MN-NP-C': [
        {
            "file": 'products/nuit-parisienne-scented-candle.jpg',
            "alt_text": 'Nuit Parisienne scented candle: black glass tumbler with a gold interior, beside its lid',
        },
    ],
    'MN-FM-P': [
        {
            "file": 'products/fleur-de-minuit-eau-de-parfum.jpg',
            "alt_text": 'Fleur de Minuit eau de parfum: burgundy glass flacon with a champagne-gold cap and a wax seal',
        },
    ],
    'MN-PD-C': [
        {
            "file": 'products/paris-after-dark-scented-candle.jpg',
            "alt_text": (
                'Paris After Dark scented candle: low black marble bowl with three wooden wicks, '
                'its marble lid with a brass knob leaning beside it'
            ),
        },
    ],
    'MN-PD-D': [
        {
            "file": 'products/paris-after-dark-reed-diffuser.jpg',
            "alt_text": (
                'Paris After Dark reed diffuser: rounded black marble vessel with six dark reeds '
                'and a champagne-gold collar'
            ),
        },
    ],
    'MN-PD-G': [
        {
            "file": 'products/paris-after-dark-night-edition-gift-set.jpg',
            "alt_text": (
                'Paris After Dark Night Edition gift set: open burgundy box holding a black marble '
                'candle, a reed diffuser, spare reeds and a brass candle snuffer on velvet'
            ),
        },
    ],
    'MN-MB-H': [
        {
            "file": 'products/maison-blanche-home-ritual-duo.jpg',
            "alt_text": (
                'Maison Blanche Home Ritual Duo: white Calacatta marble candle and reed diffuser '
                'on a matching marble tray'
            ),
        },
    ],
    'MN-SL-P': [
        {
            "file": 'products/soft-linen-eau-de-parfum.jpg',
            "alt_text": (
                'Soft Linen eau de parfum: grey stone-effect flacon with a champagne cap, '
                'an ivory linen knot and a burgundy wax seal'
            ),
        },
    ],
    'MN-SL-C': [
        {
            "file": 'products/soft-linen-scented-candle.jpg',
            "alt_text": (
                'Soft Linen scented candle: pale grey stone vessel with a wooden wick, '
                'its stone lid with a brass knob leaning beside it'
            ),
        },
    ],
    'MN-SL-D': [
        {
            "file": 'products/soft-linen-reed-diffuser.jpg',
            "alt_text": (
                'Soft Linen reed diffuser: rounded pale grey stone bottle with six dark rattan reeds '
                'and a champagne collar'
            ),
        },
    ],
    'MN-AP-P': [
        {
            "file": 'products/ambre-parisien-eau-de-parfum.jpg',
            "alt_text": (
                'Ambre Parisien eau de parfum: fluted cognac glass flacon with a square champagne-gold cap '
                'and a burgundy wax seal'
            ),
        },
    ],
    'MN-AP-C': [
        {
            "file": 'products/ambre-parisien-scented-candle.jpg',
            "alt_text": (
                'Ambre Parisien scented candle: fluted cognac glass tumbler tied with burgundy silk, '
                'its champagne-gold lid leaning beside it'
            ),
        },
    ],
    'MN-AP-D': [
        {
            "file": 'products/ambre-parisien-reed-diffuser.jpg',
            "alt_text": (
                'Ambre Parisien reed diffuser: rounded fluted cognac glass bottle with six espresso reeds '
                'and a champagne-gold collar'
            ),
        },
    ],
    'MN-LA-C': [
        {
            "file": 'products/l-appartement-scented-candle.jpg',
            "alt_text": (
                'L’Appartement scented candle: low fluted travertine vessel with a wooden wick, '
                'its fluted lid with a brass knob leaning beside it'
            ),
        },
    ],
    'MN-LA-D': [
        {
            "file": 'products/l-appartement-reed-diffuser.jpg',
            "alt_text": (
                'L’Appartement reed diffuser: rounded fluted travertine bottle with dark rattan reeds '
                'and a champagne collar'
            ),
        },
    ],
    'MN-CN-C': [
        {
            "file": 'products/chambre-noire-scented-candle.jpg',
            "alt_text": (
                'Chambre Noire scented candle: low red Rosso Levanto marble bowl with a wooden wick, '
                'its marble lid with a brass knob leaning beside it'
            ),
        },
    ],
    'MN-CN-D': [
        {
            "file": 'products/chambre-noire-reed-diffuser.jpg',
            "alt_text": (
                'Chambre Noire reed diffuser: rounded red Rosso Levanto marble bottle with six dark reeds '
                'and a champagne collar'
            ),
        },
    ],
    'MN-FM-H': [
        {
            "file": 'products/fleur-de-maison-home-ritual-duo.jpg',
            "alt_text": (
                'Fleur de Maison Home Ritual Duo: blush pink Rosa Portogallo marble candle and reed '
                'diffuser on a matching marble tray'
            ),
        },
    ],
    'MN-SR-H': [
        {
            "file": 'products/santal-residence-home-ritual-duo.jpg',
            "alt_text": (
                'Santal Residence Home Ritual Duo: dark brown Emperador marble candle and reed diffuser '
                'with a walnut ring, on a matching marble tray'
            ),
        },
    ],
    'MN-CC-P': [
        {
            "file": 'products/cafe-creme-eau-de-parfum.jpg',
            "alt_text": (
                'Café Crème eau de parfum: crème glass flacon with a clear base, a champagne-gold cap '
                'and a burgundy wax seal'
            ),
        },
    ],
    'MN-CC-C': [
        {
            "file": 'products/cafe-creme-scented-candle.jpg',
            "alt_text": (
                'Café Crème scented candle: straight-sided crème glass tumbler tied with espresso silk, '
                'its champagne-gold lid leaning beside it'
            ),
        },
    ],
    'MN-CC-D': [
        {
            "file": 'products/cafe-creme-reed-diffuser.jpg',
            "alt_text": (
                'Café Crème reed diffuser: rounded crème glass bottle with six dark reeds '
                'and a champagne-gold collar'
            ),
        },
    ],
    'MN-CC-O': [
        {
            "file": 'products/cafe-creme-le-plateau-cafe.jpg',
            "alt_text": (
                'Le Plateau Café: oval ceramic tray in a deep espresso glaze with a champagne-gold '
                'Maison Noir signature on its front edge'
            ),
        },
    ],
    'MN-CC-G': [
        {
            "file": 'products/cafe-creme-edition-gift-set.jpg',
            "alt_text": (
                'Café Crème Edition gift set: espresso linen case holding the eau de parfum, candle, '
                'reed diffuser, bundled reeds and the espresso ceramic tray'
            ),
        },
    ],
}
