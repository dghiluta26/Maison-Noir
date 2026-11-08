/**
 * Prices are stored in Romanian lei (RON) and displayed as in the
 * MAISON NOIR Product Catalogue: "590 lei", "1,590 lei".
 */
const wholeNumber = new Intl.NumberFormat('en-US', { maximumFractionDigits: 0 })
const withDecimals = new Intl.NumberFormat('en-US', {
  minimumFractionDigits: 2,
  maximumFractionDigits: 2,
})

/** Formats an API decimal string such as "1590.00" as "1,590 lei". */
export function formatPrice(price: string): string {
  const amount = Number(price)
  const formatter = Number.isInteger(amount) ? wholeNumber : withDecimals
  return `${formatter.format(amount)} lei`
}
